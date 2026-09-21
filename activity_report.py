"""Manager engagement / activity history for a Sleeper league.

Inactive managers are an edge: they don't work the waiver wire and they tend to
leave broken lineups (empty slots, players on bye) during byes and after
injuries. This profiles how engaged each manager is, from two independent
signals in the public data:

  * Roster churn -- how many adds/drops/waivers/trades they make, when, and how
    recently (do they touch the wire at all?).
  * Lineup discipline -- across completed weeks, how often they leave an empty
    starting slot or start a player who scored 0 (a bye/inactive body), i.e. did
    they bother to set a valid lineup.

With only a few weeks played the read is tentative, but the active/passive split
shows up fast and is what you project forward.

Usage:
    python activity_report.py <username|league_id>
"""
from __future__ import annotations

import datetime
import sys
from collections import defaultdict, Counter

import sleeper_client as api


def manager_labels(league_id):
    users = {u["user_id"]: u for u in api.get_league_users(league_id)}
    labels = {}
    for r in api.get_rosters(league_id):
        u = users.get(r.get("owner_id"), {})
        team = (u.get("metadata") or {}).get("team_name")
        disp = u.get("display_name", f"roster {r['roster_id']}")
        labels[r["roster_id"]] = f"{team} / {disp}" if team else disp
    return labels


def tier(moves_per_week, lineup_misses):
    if moves_per_week >= 1.5:
        base = "ACTIVE"
    elif moves_per_week > 0:
        base = "MODERATE"
    else:
        base = "PASSIVE (no roster moves)"
    if lineup_misses:
        base += " + leaves broken lineups"
    return base


def main(argv) -> int:
    if len(argv) < 2:
        print("usage: python activity_report.py <username|league_id>")
        return 1
    who = argv[1]

    state = api.get_nfl_state() or {}
    season = state.get("season", "2025")
    current = state.get("week") or 1

    if who.isdigit() and len(who) >= 12:
        league_id = who
    else:
        user = api.get_user(who)
        leagues = api.get_leagues(user["user_id"], season) if user else []
        if len(leagues) != 1:
            print("Pass a league_id.")
            return 1
        league_id = leagues[0]["league_id"]

    labels = manager_labels(league_id)
    weeks_played = max(1, current - 1)  # completed weeks (current week in progress)

    # --- roster churn from transactions (attributed to the week we queried) ---
    prof = {rid: {"moves": 0, "types": Counter(), "weeks": set(),
                  "last": 0, "dow": Counter()} for rid in labels}
    for wk in range(0, current + 2):
        for t in api.get_transactions(league_id, wk) or []:
            if t.get("status") != "complete":
                continue
            ts = t.get("status_updated") or t.get("created") or 0
            dow = datetime.datetime.utcfromtimestamp(ts / 1000).strftime("%a")
            for rid in (t.get("roster_ids") or []):
                if rid not in prof:
                    continue
                p = prof[rid]
                p["moves"] += 1
                p["types"][t["type"]] += 1
                p["weeks"].add(wk)
                p["last"] = max(p["last"], ts)
                p["dow"][dow] += 1

    # --- lineup discipline across completed weeks ---
    misses = defaultdict(list)  # rid -> ["wkN: empty=..,zeros=.."]
    for wk in range(1, current):
        for e in api.get_matchups(league_id, wk) or []:
            rid = e["roster_id"]
            sts = e.get("starters") or []
            sp = e.get("starters_points") or []
            empty = sum(1 for x in sts if str(x) == "0")
            zeros = sum(1 for x in sp if x == 0)
            if empty or zeros >= 2:
                misses[rid].append(f"wk{wk}(empty {empty}, 0-pt {zeros})")

    print(f"Manager engagement -- {season}, through week {current} "
          f"({weeks_played} completed)")
    print("=" * 68)
    order = sorted(labels, key=lambda r: -prof[r]["moves"])
    for rid in order:
        p = prof[rid]
        mpw = p["moves"] / weeks_played
        last = (datetime.datetime.utcfromtimestamp(p["last"] / 1000).strftime("%m/%d")
                if p["last"] else "never")
        dow = ", ".join(f"{d}:{n}" for d, n in p["dow"].most_common(3)) or "-"
        print(f"\n{labels[rid]}")
        print(f"  churn: {p['moves']} moves ({mpw:.1f}/wk), types={dict(p['types']) or '{}'}, "
              f"last move {last}")
        print(f"  when:  {dow}")
        print(f"  lineup misses: {', '.join(misses[rid]) if misses[rid] else 'none'}")
        print(f"  --> profile: {tier(mpw, bool(misses[rid]))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
