#!/usr/bin/env python3
"""
Weekly reporting tool for the "The Boys" Sleeper league.

REPORT ONLY. This script states facts and flags anomalies. It deliberately does
not recommend lineup changes, rank players against each other, or tell you who
to start. Ranking heuristics go stale (see docs/api-notes.md on search_rank);
judgment stays in conversation, where it can be argued with.

It reports on ALL SIX managers, not just mine. In a league where most managers
are dormant, knowing that an opponent is starting an injured player is worth as
much as fixing my own lineup.

Usage:
    python3 scripts/fantasy_report.py                  # current week
    python3 scripts/fantasy_report.py --week 3
    python3 scripts/fantasy_report.py --out weekly/week-03.md
    python3 scripts/fantasy_report.py --refresh-players # force player re-fetch
"""

import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
from collections import defaultdict

BASE = "https://api.sleeper.app"
LEAGUE_ID = "1401765585515237376"
ME_ROSTER_ID = 3
SEASON = "2026"

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
CACHE = os.path.join(REPO, ".cache")

# Players dictionary is ~14MB. Cache it; refetch only when stale.
PLAYERS_CACHE = os.path.join(CACHE, "players.json")
PLAYERS_MAX_AGE_HOURS = 12

# injury_status values that mean the player is unlikely or unable to play.
# "NA" means not active and is more severe than "Questionable".
HARD_OUT = {"Out", "IR", "PUP", "Sus", "NA", "DNR", "COV"}
SOFT_FLAG = {"Questionable", "Doubtful"}


# ---------------------------------------------------------------- fetching

def get(path):
    url = BASE + path
    req = urllib.request.Request(url, headers={"User-Agent": "sleeper-season-tracker"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def load_players(refresh=False):
    """Fetch the player dictionary, caching to disk (it is ~14MB)."""
    os.makedirs(CACHE, exist_ok=True)
    if not refresh and os.path.exists(PLAYERS_CACHE):
        age_h = (dt.datetime.now().timestamp() - os.path.getmtime(PLAYERS_CACHE)) / 3600
        if age_h < PLAYERS_MAX_AGE_HOURS:
            with open(PLAYERS_CACHE) as f:
                return json.load(f), f"cached, {age_h:.1f}h old"
    sys.stderr.write("fetching players.json (~14MB)...\n")
    players = get("/v1/players/nfl")
    with open(PLAYERS_CACHE, "w") as f:
        json.dump(players, f)
    return players, "freshly fetched"


def load_byes():
    """Team -> bye week. Derived from the NFL schedule; see docs/api-notes.md."""
    path = os.path.join(DATA, "byes_2026.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    sched = get(f"/schedule/nfl/regular/{SEASON}")
    played = defaultdict(set)
    for g in sched:
        played[g["home"]].add(g["week"])
        played[g["away"]].add(g["week"])
    weeks = set(range(1, 19))
    return {t: (sorted(weeks - w)[0] if weeks - w else None) for t, w in played.items()}


# ---------------------------------------------------------------- helpers

def pname(players, pid):
    p = players.get(pid)
    if not p:
        return pid
    if p.get("position") == "DEF":
        return f"{pid} DEF"
    return p.get("full_name") or f"{p.get('first_name','')} {p.get('last_name','')}".strip() or pid


def describe(players, pid):
    p = players.get(pid, {})
    return {
        "name": pname(players, pid),
        "pos": p.get("position", "?"),
        "team": p.get("team"),
        "injury": p.get("injury_status"),
        "body": p.get("injury_body_part"),
        "depth": p.get("depth_chart_order"),
    }


def audit_starter(players, byes, pid, week):
    """
    Return a list of factual flags for one starter. No recommendations --
    each flag is an observable fact with its source field named.
    """
    d = describe(players, pid)
    flags = []
    if d["team"] and byes.get(d["team"]) == week:
        flags.append(("BYE", f"{d['team']} on bye week {week}"))
    inj = d["injury"]
    if inj in HARD_OUT:
        detail = f"injury_status={inj}"
        if d["body"]:
            detail += f" ({d['body']})"
        flags.append(("OUT", detail))
    elif inj in SOFT_FLAG:
        detail = f"injury_status={inj}"
        if d["body"]:
            detail += f" ({d['body']})"
        flags.append(("QUES", detail))
    # depth_chart_order > 1 means someone is ahead of them on their NFL team.
    # Only meaningful for the positions where a depth chart implies snap share.
    if d["pos"] in ("RB", "WR", "TE", "QB") and isinstance(d["depth"], int) and d["depth"] > 1:
        flags.append(("DEPTH", f"depth_chart_order={d['depth']}"))
    return d, flags


# A starter who is on bye, ruled out, or missing entirely cannot score. That is
# categorically different from a "Questionable" tag, most of which play. Keep the
# two counts separate so a manager with four questionables doesn't read as more
# exposed than one starting a player who is definitively unavailable.
HARD_KINDS = {"BYE", "OUT", "EMPTY"}


def split_severity(flags):
    kinds = {k for k, _ in flags}
    return bool(kinds & HARD_KINDS), bool(kinds - HARD_KINDS)


# ---------------------------------------------------------------- report

def main():
    ap = argparse.ArgumentParser(description="Report-only weekly league scan.")
    ap.add_argument("--week", type=int, help="Week to report on (default: current)")
    ap.add_argument("--out", help="Write markdown here (default: stdout)")
    ap.add_argument("--refresh-players", action="store_true", help="Bypass player cache")
    args = ap.parse_args()

    state = get("/v1/state/nfl")
    week = args.week or state.get("week") or 1
    players, players_src = load_players(refresh=args.refresh_players)
    byes = load_byes()

    league = get(f"/v1/league/{LEAGUE_ID}")
    lsettings = league.get("settings", {})
    users = get(f"/v1/league/{LEAGUE_ID}/users")
    rosters = get(f"/v1/league/{LEAGUE_ID}/rosters")
    uname = {u["user_id"]: u.get("display_name") or u["user_id"] for u in users}
    r2name = {r["roster_id"]: uname.get(r["owner_id"], "?") for r in rosters}
    r2roster = {r["roster_id"]: r for r in rosters}

    def label(rid):
        return f"{r2name.get(rid, '?')}{' (me)' if rid == ME_ROSTER_ID else ''}"

    matchups = get(f"/v1/league/{LEAGUE_ID}/matchups/{week}")
    by_mid = defaultdict(list)
    for m in matchups:
        by_mid[m["matchup_id"]].append(m)
    starters_by_rid = {m["roster_id"]: (m.get("starters") or []) for m in matchups}

    out = []
    w = out.append

    w(f"# Week {week} report — auto-generated")
    w("")
    w(f"Generated {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} · "
      f"NFL state: season {state.get('season')}, week {state.get('week')}, "
      f"{state.get('season_type')} · players.json {players_src}")
    w("")
    w("> Report only. Flags are observable facts from the API, not advice. "
      "`OUT`/`BYE` mean the player cannot or likely will not play; `QUES` and "
      "`DEPTH` are context, not verdicts. Judgment stays out of this file.")
    w("")

    # ---- 1. standings -----------------------------------------------------
    w("## 1. Standings")
    w("")
    w("| Manager | W-L-T | PF | PA |")
    w("|---|---|---|---|")
    ranked = sorted(
        rosters,
        key=lambda r: (
            -(r.get("settings", {}).get("wins", 0)),
            -(r.get("settings", {}).get("fpts", 0)),
        ),
    )
    for r in ranked:
        s = r.get("settings", {})
        pf = s.get("fpts", 0) + s.get("fpts_decimal", 0) / 100
        pa = s.get("fpts_against", 0) + s.get("fpts_against_decimal", 0) / 100
        w(f"| {label(r['roster_id'])} | {s.get('wins',0)}-{s.get('losses',0)}-{s.get('ties',0)} "
          f"| {pf:.2f} | {pa:.2f} |")
    w("")

    # ---- 2. league-wide lineup audit -------------------------------------
    w(f"## 2. Lineup audit — all managers, week {week}")
    w("")
    w("Every manager's starting lineup, cross-referenced against injury status, "
      "bye weeks, and NFL depth chart. Opponents' holes are listed for the same "
      "reason mine are: in a league this passive, an opponent starting a player "
      "who cannot score is information worth having.")
    w("")
    current = state.get("week") or 1
    if week > current:
        w(f"> **Projection, not a set lineup.** Week {week} is ahead of the current "
          f"week ({current}). Sleeper reports each roster's *present* lineup for "
          "future weeks, so this shows what would happen if nobody changed "
          "anything. Managers will normally fix obvious bye conflicts before "
          "kickoff — treat opponent numbers here as a planning aid, not a "
          "prediction.")
        w("")

    hard_counts, soft_counts, hard_detail = {}, {}, defaultdict(list)
    for rid in sorted(starters_by_rid):
        starters = starters_by_rid[rid]
        rows, nhard, nsoft = [], 0, 0
        for pid in starters:
            if not pid or pid == "0":
                rows.append(("— empty slot —", "", "", [("EMPTY", "no player set")]))
                nhard += 1
                hard_detail[rid].append("empty slot")
                continue
            d, flags = audit_starter(players, byes, pid, week)
            is_hard, is_soft = split_severity(flags)
            nhard += is_hard
            nsoft += is_soft
            if is_hard:
                why = ", ".join(v for k, v in flags if k in HARD_KINDS)
                hard_detail[rid].append(f"{d['name']} ({why})")
            rows.append((d["name"], d["pos"], d["team"] or "", flags))
        hard_counts[rid], soft_counts[rid] = nhard, nsoft

        w(f"### {label(rid)} — {nhard} cannot play, {nsoft} questionable "
          f"(of {len(starters)} starters)")
        w("")
        w("| Starter | Pos | Team | Flags |")
        w("|---|---|---|---|")
        for name, pos, team, flags in rows:
            fs = "; ".join(f"**{k}** {v}" for k, v in flags) if flags else "ok"
            w(f"| {name} | {pos} | {team} | {fs} |")
        w("")

    w("**Exposure summary.** `Cannot play` counts starters on bye, ruled out, or "
      "empty slots — those are certain zeros. `Questionable` is softer; most such "
      "players suit up.")
    w("")
    w("| Manager | Cannot play | Questionable | Who cannot play |")
    w("|---|---|---|---|")
    for rid in sorted(hard_counts, key=lambda r: (-hard_counts[r], -soft_counts[r])):
        detail = "; ".join(hard_detail[rid]) if hard_detail[rid] else "—"
        w(f"| {label(rid)} | {hard_counts[rid]} | {soft_counts[rid]} | {detail} |")
    w("")

    # ---- 3. this week's matchups ------------------------------------------
    w(f"## 3. Matchups — week {week}")
    w("")
    w("| Matchup | Cannot play | Questionable | Points |")
    w("|---|---|---|---|")
    for mid, entries in sorted(by_mid.items()):
        if len(entries) != 2:
            continue
        a, b = entries
        ra, rb = a["roster_id"], b["roster_id"]
        w(f"| {label(ra)} vs {label(rb)} "
          f"| {hard_counts.get(ra,0)} — {hard_counts.get(rb,0)} "
          f"| {soft_counts.get(ra,0)} — {soft_counts.get(rb,0)} "
          f"| {a.get('points',0):.2f} — {b.get('points',0):.2f} |")
    w("")

    # ---- 4. activity / dormancy -------------------------------------------
    w("## 4. Manager activity")
    w("")
    w("Who is actually managing their team. This is the core edge in this "
      "league — it decays if dormant managers wake up.")
    w("")

    moves = defaultdict(list)
    trades = []
    for wk in range(0, week + 1):
        try:
            txs = get(f"/v1/league/{LEAGUE_ID}/transactions/{wk}")
        except Exception:
            continue
        for t in txs:
            if t.get("status") != "complete":
                continue
            if t["type"] == "trade":
                trades.append((wk, t))
                for rid in t.get("roster_ids", []):
                    moves[rid].append((wk, "trade"))
            else:
                for rid in t.get("roster_ids", []):
                    moves[rid].append((wk, t["type"]))

    w("| Manager | Total moves | Last active (week) | Status |")
    w("|---|---|---|---|")
    for rid in sorted(r2name):
        ms = moves.get(rid, [])
        last = max((m[0] for m in ms), default=None)
        status = "DORMANT — no moves all season" if not ms else (
            "active" if last is not None and last >= week - 1 else f"quiet since week {last}"
        )
        w(f"| {label(rid)} | {len(ms)} | {last if last is not None else '—'} | {status} |")
    w("")

    dormant = [rid for rid in r2name if not moves.get(rid) and rid != ME_ROSTER_ID]
    w(f"**Dormant opponents: {len(dormant)} of {len(r2name)-1}** "
      f"({', '.join(r2name[r] for r in dormant) if dormant else 'none'})")
    w("")

    w(f"**Trades league-wide: {len(trades)}**")
    if trades:
        w("")
        for wk, t in trades:
            who = " / ".join(label(r) for r in t.get("roster_ids", []))
            w(f"- Week {wk}: {who}")
            for pid, rid in (t.get("adds") or {}).items():
                w(f"  - {pname(players, pid)} → {label(rid)}")
            for pick in (t.get("draft_picks") or []):
                w(f"  - pick: {pick.get('season')} round {pick.get('round')}")
    w("")

    # ---- 5. recent transactions -------------------------------------------
    w("## 5. Recent transactions")
    w("")
    recent_start = max(0, week - 1)
    any_tx = False
    for wk in range(recent_start, week + 1):
        try:
            txs = get(f"/v1/league/{LEAGUE_ID}/transactions/{wk}")
        except Exception:
            continue
        for t in txs:
            if t.get("status") != "complete":
                continue
            any_tx = True
            who = " / ".join(label(r) for r in t.get("roster_ids", []))
            when = dt.datetime.utcfromtimestamp(
                t.get("status_updated", 0) / 1000
            ).strftime("%Y-%m-%d")
            bid = (t.get("settings") or {}).get("waiver_bid")
            bid_s = f" (bid ${bid})" if bid else ""  # only set in FAAB leagues
            w(f"- **wk{wk}** {when} · {who} · `{t['type']}`{bid_s}")
            for pid in (t.get("adds") or {}):
                w(f"  - **+** {pname(players, pid)}")
            for pid in (t.get("drops") or {}):
                w(f"  - **−** {pname(players, pid)}")
    if not any_tx:
        w("_No completed transactions in this window._")
    w("")

    # ---- 6. bye lookahead --------------------------------------------------
    w("## 6. Bye-week lookahead")
    w("")
    w("Players on each roster whose NFL team is on bye, by upcoming week. "
      "Shows when each manager will be short-handed.")
    w("")
    horizon = [x for x in range(week, min(week + 5, 19))]
    w("| Manager | " + " | ".join(f"wk{x}" for x in horizon) + " |")
    w("|---" * (len(horizon) + 1) + "|")
    for rid in sorted(r2name):
        cells = []
        for x in horizon:
            n = sum(
                1
                for pid in (r2roster[rid].get("players") or [])
                if byes.get(players.get(pid, {}).get("team")) == x
            )
            cells.append(str(n) if n else "·")
        w(f"| {label(rid)} | " + " | ".join(cells) + " |")
    w("")

    # ---- 7. notable free agents -------------------------------------------
    w("## 7. Unowned players")
    w("")
    w("Everything not on a roster, by Sleeper `search_rank` (lower = better). "
      "Rank lags real-world news and is listed as raw data, not a ranking "
      "endorsement — see docs/api-notes.md.")
    w("")
    w("**How to get them** differs and the API does not say which is which: a "
      "player nobody has rostered is an instant add, but one another manager "
      "recently *dropped* sits in the waiver period and needs a waiver claim "
      "(which costs waiver position, not money, in this league). The "
      "`WAIVER` tag below marks players dropped within the last "
      f"`waiver_clear_days` ({lsettings.get('waiver_clear_days', '?')}) — "
      "those cannot be grabbed on the spot.")
    w("")

    rostered = set()
    for r in rosters:
        rostered.update(r.get("players") or [])

    # Recently-dropped players are on waivers, not instantly addable. There is no
    # field for this, so reconstruct it from the transaction log.
    clear_days = lsettings.get("waiver_clear_days", 2)
    cutoff_ms = dt.datetime.now().timestamp() * 1000 - clear_days * 86400 * 1000
    on_waivers = {}
    for wk in range(0, week + 1):
        try:
            txs = get(f"/v1/league/{LEAGUE_ID}/transactions/{wk}")
        except Exception:
            continue
        for t in txs:
            if t.get("status") != "complete":
                continue
            when = t.get("status_updated", 0)
            if when < cutoff_ms:
                continue
            for pid in (t.get("drops") or {}):
                if pid not in rostered:
                    on_waivers[pid] = when

    avail = defaultdict(list)
    for pid, p in players.items():
        if pid in rostered or not p.get("team"):
            continue
        pos = p.get("position")
        if pos not in ("QB", "RB", "WR", "TE", "K"):
            continue
        if p.get("status") != "Active":
            continue
        rank = p.get("search_rank")
        if rank is None or rank >= 9999999:
            continue
        avail[pos].append((rank, pid, p))

    for pos in ("QB", "RB", "WR", "TE", "K"):
        # Kickers are near-interchangeable; a short list is enough to spot a
        # better bye week without burying the positions that matter.
        top = sorted(avail[pos])[: 5 if pos == "K" else 8]
        if not top:
            continue
        w(f"**{pos}**")
        w("")
        w("| Rank | Player | Team | Bye | Injury | How to get |")
        w("|---|---|---|---|---|---|")
        for rank, pid, p in top:
            t = p.get("team")
            how = "**WAIVER** (claim + bid)" if pid in on_waivers else "free agent"
            w(f"| {rank} | {pname(players, pid)} | {t} | {byes.get(t) or '—'} "
              f"| {p.get('injury_status') or '—'} | {how} |")
        w("")

    ndef = sum(
        1
        for pid, p in players.items()
        if p.get("position") == "DEF" and pid not in rostered
    )
    w(f"Unowned defenses: **{ndef}**")
    w("")

    # ---- 8. waiver order ---------------------------------------------------
    # This league runs rolling waiver PRIORITY, not FAAB -- waiver_budget in the
    # league settings is inert. Winning a claim sends you to the back of the
    # order, so position is the currency. See docs/api-notes.md.
    w("## 8. Waiver order")
    w("")
    faab = lsettings.get("waiver_type") not in (0, None)
    if faab:
        w("| Manager | FAAB spent | Remaining |")
        w("|---|---|---|")
        for rid in sorted(r2name):
            used = (r2roster[rid].get("settings") or {}).get("waiver_budget_used", 0)
            w(f"| {label(rid)} | ${used} | ${lsettings.get('waiver_budget', 100) - used} |")
    else:
        w("Rolling priority (`waiver_type: 0`) — **no money involved**. Lowest "
          "number wins a contested claim; winning drops you to last.")
        w("")
        w("| Priority | Manager |")
        w("|---|---|")
        order = sorted(
            r2name,
            key=lambda r: (r2roster[r].get("settings") or {}).get("waiver_position", 99),
        )
        for rid in order:
            pos = (r2roster[rid].get("settings") or {}).get("waiver_position", "?")
            w(f"| {pos} | {label(rid)} |")
    w("")

    text = "\n".join(out)
    if args.out:
        path = args.out if os.path.isabs(args.out) else os.path.join(REPO, args.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(text + "\n")
        sys.stderr.write(f"wrote {path}\n")
    else:
        print(text)


if __name__ == "__main__":
    main()
