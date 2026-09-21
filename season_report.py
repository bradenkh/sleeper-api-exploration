"""Rest-of-season points optimization for a Sleeper roster.

Weekly optimization (optimize_lineup.py) answers "who do I start this Sunday".
This answers the season-long questions behind a winning strategy:

  * Rest-of-season (ROS) value: sum each rostered player's weekly projection to
    see who your real point-getters are and where you're thin.
  * Weekly optimal totals: project your best-possible score every remaining week
    so the bye-week dips (and playoff weeks) are visible at a glance.
  * Bye/gap alerts: weeks where you can't field a full-strength group at a
    position, which is where waivers/trades have to fill in.

Sleeper's weekly projections are week-specific (they already zero out byes), so
summing them is a fair ROS estimate -- treat it as a planning baseline, not a
guarantee.

Usage:
    python season_report.py <username|league_id> [--through WEEK] [--playoffs]
"""
from __future__ import annotations

import sys
from collections import defaultdict

import sleeper_client as api
from optimize_lineup import expected_points, project_roster, optimize, FLEX_ELIGIBLE


def _name(meta):
    return meta.get("full_name") or meta.get("n") or meta.get("last_name") or "?"


def _pos(meta):
    return meta.get("position") or meta.get("pos")


def main(argv) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: python season_report.py <username|league_id> [--through W] [--playoffs]")
        return 1
    who = args[0]
    through = None
    for a in argv:
        if a.startswith("--through"):
            through = int(a.split("=", 1)[1]) if "=" in a else int(argv[argv.index(a) + 1])
    include_playoffs = "--playoffs" in argv

    state = api.get_nfl_state() or {}
    season = state.get("season", "2025")
    start_week = state.get("week") or 1

    # Resolve league + roster.
    if who.isdigit() and len(who) >= 12:
        league_id = who
        user = None
    else:
        user = api.get_user(who)
        leagues = api.get_leagues(user["user_id"], season) if user else []
        if len(leagues) != 1:
            print("Pass a league_id (user is in %d leagues)." % len(leagues))
            return 1
        league_id = leagues[0]["league_id"]

    league = api.get_league(league_id)
    scoring = league["scoring_settings"]
    roster_positions = league["roster_positions"]
    players = api.get_players()
    playoff_start = league.get("settings", {}).get("playoff_week_start", 15)

    end_week = through or ((17 if include_playoffs else playoff_start - 1))
    weeks = list(range(start_week, end_week + 1))

    rosters = api.get_rosters(league_id)
    me = ([r for r in rosters if user and r.get("owner_id") == user["user_id"]] or rosters)[0]
    my_ids = [str(x) for x in (me.get("players") or [])]

    flex_positions = set()
    for slot in roster_positions:
        flex_positions |= FLEX_ELIGIBLE.get(slot, set())
    starts_needed = defaultdict(int)
    for slot in roster_positions:
        if slot != "BN":
            starts_needed[slot] += 1

    ros_points = defaultdict(float)   # player_id -> summed projection
    ros_games = defaultdict(int)      # weeks not on bye
    weekly = []                       # (week, optimal_total, bye_players, gaps)

    for wk in weeks:
        proj = api.get_projections(season, wk)
        by_pid = {str(p.get("player_id")): (p.get("stats") or {}) for p in proj}
        projected = project_roster(me, scoring, by_pid, players)
        for pid, name, pos, pts in projected:
            if pts:
                ros_points[pid] += pts
                ros_games[pid] += 1
        lineup, _ = optimize(projected, roster_positions)
        opt_total = round(sum(p[4] or 0 for p in lineup), 2)

        # A player projecting 0 is on bye (or inactive); count by position.
        on_bye = [(name, pos) for pid, name, pos, pts in projected if not pts]
        avail_by_pos = defaultdict(int)
        for pid, name, pos, pts in projected:
            if pts:
                avail_by_pos[pos] += 1
        # Gaps: not enough non-bye bodies to fill dedicated + flex demand.
        gaps = []
        flex_demand = sum(starts_needed[s] for s in starts_needed if s in FLEX_ELIGIBLE)
        for pos in ("QB", "RB", "WR", "TE", "K", "DEF"):
            need = starts_needed.get(pos, 0)
            if avail_by_pos[pos] < need:
                gaps.append(f"{pos} (have {avail_by_pos[pos]}/{need})")
        flex_bodies = sum(avail_by_pos[p] for p in flex_positions)
        flex_need = sum(starts_needed.get(p, 0) for p in flex_positions) + flex_demand
        if flex_bodies < flex_need:
            gaps.append(f"FLEX-eligible (have {flex_bodies}/{flex_need})")
        weekly.append((wk, opt_total, on_bye, gaps))

    # --- report ---
    print(f"{league['name']} -- rest-of-season ({season}), weeks {weeks[0]}-{weeks[-1]}"
          f"{' incl. playoffs' if include_playoffs else ''}")
    print("=" * 66)

    print("\nREST-OF-SEASON VALUE (summed weekly projections, best first)")
    print(f"  {'Player':26} {'Pos':>3} {'ROS pts':>8} {'Gms':>4} {'Pts/Gm':>7}")
    ranked = sorted(my_ids, key=lambda p: -ros_points[p])
    for pid in ranked:
        meta = players.get(pid, {})
        g = ros_games[pid]
        ppg = ros_points[pid] / g if g else 0
        print(f"  {_name(meta)[:26]:26} {str(_pos(meta)):>3} "
              f"{ros_points[pid]:8.1f} {g:4} {ppg:7.1f}")

    print("\nWEEKLY OPTIMAL PROJECTED TOTAL (dips = bye trouble)")
    avg = sum(w[1] for w in weekly) / len(weekly)
    for wk, tot, on_bye, gaps in weekly:
        bar = "#" * int(round(tot / 6))
        flag = ""
        if gaps:
            flag = "  << GAP: " + ", ".join(gaps)
        elif tot < avg - 12:
            flag = "  << low (byes: " + ", ".join(n for n, _ in on_bye) + ")"
        print(f"  wk{wk:2} {tot:6.1f} {bar}{flag}")
    print(f"  avg optimal total: {avg:.1f}")

    print("\nPOSITIONAL DEPTH (rostered, by ROS value)")
    by_pos = defaultdict(list)
    for pid in my_ids:
        meta = players.get(pid, {})
        by_pos[_pos(meta)].append((ros_points[pid], _name(meta)))
    for pos in ("QB", "RB", "WR", "TE", "K", "DEF"):
        lst = sorted(by_pos.get(pos, []), reverse=True)
        print(f"  {pos:4} ({len(lst)}): " + ", ".join(f"{n} {p:.0f}" for p, n in lst))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
