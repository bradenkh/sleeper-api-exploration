"""Standings + "since last week" manager-history report for a Sleeper league.

Given a Sleeper username (or a raw league_id), this prints:

  1. the current standings (record, points for / against), and
  2. a per-manager log of every roster move (adds, drops, waivers, trades)
     over the most recent week(s) of the season -- i.e. "what has everyone
     done since last week".

Everything is read-only and uses only the public Sleeper API via
``sleeper_client``. No API key is required.

Usage:
    python league_report.py <username|league_id> [season] [--weeks N]

Examples:
    python league_report.py brdnhnsn 2026
    python league_report.py 1401765585515237376 --weeks 2
"""
from __future__ import annotations

import datetime
import sys

import sleeper_client as api


# --- small formatting helpers ------------------------------------------------

def _fmt_ts(ms) -> str:
    """Epoch-milliseconds -> a short, readable UTC timestamp."""
    if not ms:
        return "?"
    return datetime.datetime.utcfromtimestamp(ms / 1000).strftime("%a %b %d %H:%M UTC")


def _fpts(settings: dict) -> float:
    """Reassemble a roster's points-for from Sleeper's whole/decimal split."""
    whole = settings.get("fpts") or 0
    dec = settings.get("fpts_decimal") or 0
    return float(f"{whole}.{dec}")


def _fpts_against(settings: dict) -> float:
    whole = settings.get("fpts_against") or 0
    dec = settings.get("fpts_against_decimal") or 0
    return float(f"{whole}.{dec}")


# --- lookups -----------------------------------------------------------------

def resolve_league(arg: str, season: str):
    """Turn a CLI argument into (league_id, league_name).

    A long all-digit argument is treated as a league_id directly; otherwise it
    is looked up as a username. If the user is in exactly one league for the
    season we use it; if they are in several, we list them and stop so the
    caller can re-run with a specific league_id.
    """
    if arg.isdigit() and len(arg) >= 12:
        league = api.get_league(arg)
        if not league:
            print(f"No league found for league_id '{arg}'.")
            return None, None
        return arg, league.get("name", arg)

    user = api.get_user(arg)
    if not user:
        print(f"No Sleeper user found for '{arg}'.")
        return None, None
    leagues = api.get_leagues(user["user_id"], season)
    if not leagues:
        print(f"{arg} has no {season} leagues (try a different season).")
        return None, None
    if len(leagues) > 1:
        print(f"{arg} is in {len(leagues)} {season} leagues -- pass a league_id:")
        for lg in leagues:
            print(f"  {lg['league_id']}  {lg['name']}")
        return None, None
    return leagues[0]["league_id"], leagues[0]["name"]


def manager_names(league_id: str):
    """Map roster_id -> a friendly manager label ("Team Name (display_name)")."""
    users = {u["user_id"]: u for u in api.get_league_users(league_id)}
    labels = {}
    for r in api.get_rosters(league_id):
        owner = r.get("owner_id")
        u = users.get(owner, {})
        display = u.get("display_name", f"roster {r['roster_id']}")
        team = (u.get("metadata") or {}).get("team_name")
        labels[r["roster_id"]] = f"{team} ({display})" if team else display
    return labels


def player_label(players: dict, pid) -> str:
    """Readable "Name (POS-TEAM)" for a player_id; DEF ids are team codes."""
    p = players.get(str(pid))
    if not p:
        return f"#{pid}"
    name = p.get("full_name") or " ".join(
        x for x in (p.get("first_name"), p.get("last_name")) if x
    ) or str(pid)
    return f"{name} ({p.get('position') or '?'}-{p.get('team') or 'FA'})"


# --- report sections ---------------------------------------------------------

def print_standings(league_id: str, labels: dict) -> None:
    rosters = api.get_rosters(league_id)

    def sort_key(r):
        s = r.get("settings", {})
        return (-(s.get("wins") or 0), -(s.get("ties") or 0), -_fpts(s))

    rosters.sort(key=sort_key)
    played = any(
        (r.get("settings", {}).get("wins")
         or r.get("settings", {}).get("losses")
         or r.get("settings", {}).get("ties"))
        for r in rosters
    )

    print("STANDINGS")
    print("-" * 60)
    print(f"{'#':>2}  {'Manager':<32} {'W-L-T':>7} {'PF':>7} {'PA':>7}")
    for i, r in enumerate(rosters, 1):
        s = r.get("settings", {})
        rec = f"{s.get('wins',0)}-{s.get('losses',0)}-{s.get('ties',0)}"
        print(f"{i:>2}  {labels.get(r['roster_id'], '?')[:32]:<32} "
              f"{rec:>7} {_fpts(s):>7.2f} {_fpts_against(s):>7.2f}")
    if not played:
        print("\n(No games scored yet -- everyone is 0-0-0 to open the season.)")


def gather_transactions(league_id: str, weeks):
    """All transactions across the given weeks, newest first."""
    txns = []
    for wk in weeks:
        txns.extend(api.get_transactions(league_id, wk))
    txns.sort(key=lambda t: t.get("status_updated") or 0, reverse=True)
    return txns


def describe_transaction(t: dict, labels: dict, players: dict) -> str:
    """One-line-per-move description of a single transaction."""
    rids = t.get("roster_ids") or []
    who = ", ".join(labels.get(r, f"roster {r}") for r in rids)
    kind = t.get("type", "?")
    head = f"[{_fmt_ts(t.get('status_updated'))}] {kind} ({t.get('status')}) - {who}"

    lines = [head]
    faab = {b["roster_id"]: b["amount"] for b in (t.get("waiver_budget") or [])}
    for pid, rid in (t.get("adds") or {}).items():
        bid = f"  (${faab[rid]} FAAB)" if kind == "waiver" and rid in faab else ""
        lines.append(f"    + {player_label(players, pid)} -> {labels.get(rid, rid)}{bid}")
    for pid, rid in (t.get("drops") or {}).items():
        lines.append(f"    - {player_label(players, pid)}  (dropped by {labels.get(rid, rid)})")
    for pick in (t.get("draft_picks") or []):
        lines.append(f"    pick {pick.get('season')} rd {pick.get('round')} "
                     f"-> {labels.get(pick.get('owner_id'), pick.get('owner_id'))}")
    return "\n".join(lines)


def print_activity(league_id: str, labels: dict, players: dict, weeks) -> None:
    txns = gather_transactions(league_id, weeks)
    span = f"week {weeks[0]}" if len(weeks) == 1 else f"weeks {weeks[0]}-{weeks[-1]}"
    print(f"\nMANAGER ACTIVITY ({span})")
    print("-" * 60)
    if not txns:
        print("No roster moves reported in this window.")
        return

    active = {rid for t in txns for rid in (t.get("roster_ids") or [])}
    for t in txns:
        print(describe_transaction(t, labels, players))
    quiet = [labels[rid] for rid in labels if rid not in active]
    if quiet:
        print("\nStood pat (no moves): " + ", ".join(sorted(quiet)))


def print_lineup_alerts(league_id: str, labels: dict, players: dict,
                        owner_display: str | None) -> None:
    """Flag empty starting slots for a specific manager (a common oversight)."""
    if not owner_display:
        return
    positions = (api.get_league(league_id) or {}).get("roster_positions") or []
    slot_names = [p for p in positions if p != "BN"]
    for r in api.get_rosters(league_id):
        if labels.get(r["roster_id"], "").find(owner_display) == -1:
            continue
        starters = r.get("starters") or []
        empty = [slot_names[i] if i < len(slot_names) else "?"
                 for i, pid in enumerate(starters) if pid in ("0", 0, None, "")]
        if empty:
            print(f"\nLINEUP ALERT for {labels[r['roster_id']]}: "
                  f"empty starting slot(s): {', '.join(empty)}")
        return


# --- entry point -------------------------------------------------------------

def main(argv) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    weeks_override = None
    for a in argv[1:]:
        if a.startswith("--weeks"):
            try:
                weeks_override = int(a.split("=", 1)[1]) if "=" in a else int(argv[argv.index(a) + 1])
            except (ValueError, IndexError):
                print("--weeks needs an integer, e.g. --weeks 2")
                return 1

    if not args:
        print("usage: python league_report.py <username|league_id> [season] [--weeks N]")
        return 1

    who = args[0]
    season = args[1] if len(args) > 1 and args[1].isdigit() and len(args[1]) == 4 else None

    state = api.get_nfl_state() or {}
    if season is None:
        season = state.get("season", "2025")
    current_week = state.get("week") or 1

    league_id, league_name = resolve_league(who, season)
    if not league_id:
        return 1

    # "Since last week" = the current week plus the prior one when it exists,
    # unless the caller asked for a specific number of trailing weeks.
    n = weeks_override if weeks_override else (2 if current_week > 1 else 1)
    weeks = [w for w in range(max(1, current_week - n + 1), current_week + 1)]

    labels = manager_names(league_id)
    players = api.get_players()

    print(f"{league_name}  --  {season} season, through week {current_week}")
    print("=" * 60)
    print_standings(league_id, labels)
    # If a username was given, flag empty starting slots for that manager.
    print_lineup_alerts(league_id, labels, players,
                        None if who.isdigit() else who)
    print_activity(league_id, labels, players, weeks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
