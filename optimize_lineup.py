"""Points-optimal lineup for a Sleeper roster, scored by the league's own rules.

The guiding idea: don't start the biggest *names*, start the players with the
most projected *points* -- and points are defined entirely by the league's
``scoring_settings``. In a full-PPR league a high-volume back who catches passes
can out-score a more talented back stuck in a committee, and this tool makes
that trade-off explicit.

For a target week it:
  1. pulls the league's exact scoring weights,
  2. pulls Sleeper's per-player stat projections for that week,
  3. scores every player as (projected stats . scoring weights) -- the same
     arithmetic Sleeper uses, but with THIS league's numbers, and
  4. fills the lineup slots greedily by projected points (dedicated slots first,
     then FLEX from the best eligible leftovers), and contrasts that optimal
     lineup with whatever is currently set.

Usage:
    python optimize_lineup.py <username|league_id> [week] [--all]

    <week>  target week (defaults to the current NFL week)
    --all   also print the projected points for every bench player
"""
from __future__ import annotations

import sys

import sleeper_client as api

# Positions a FLEX slot will accept in this league type.
FLEX_ELIGIBLE = {"FLEX": {"RB", "WR", "TE"},
                 "WRRB_FLEX": {"RB", "WR"},
                 "REC_FLEX": {"WR", "TE"},
                 "SUPER_FLEX": {"QB", "RB", "WR", "TE"}}


def expected_points(stats: dict, scoring: dict) -> float:
    """Projected fantasy points = projected stats dotted with scoring weights."""
    return round(sum(weight * stats.get(stat, 0) for stat, weight in scoring.items()), 2)


def project_roster(roster, scoring, proj_by_pid, players):
    """[(player_id, name, pos, points)] for every player on a roster, best first."""
    out = []
    for pid in roster.get("players") or []:
        meta = players.get(str(pid), {})
        pos = meta.get("position") or (meta.get("pos"))
        stats = proj_by_pid.get(str(pid))
        pts = expected_points(stats, scoring) if stats else None
        out.append((str(pid), meta.get("full_name") or meta.get("n") or str(pid), pos, pts))
    out.sort(key=lambda r: (r[3] is None, -(r[3] or 0)))
    return out


def optimize(projected, roster_positions):
    """Greedily fill the lineup by projected points.

    Dedicated slots (QB/RB/WR/TE/K/DEF) take their best eligible player; FLEX
    slots then take the best remaining FLEX-eligible player. Filling dedicated
    slots before FLEX is optimal here because every FLEX-eligible position also
    has its own dedicated slot, so no dedicated slot is ever starved by FLEX.
    """
    remaining = [p for p in projected]  # (pid, name, pos, pts)
    slots = [s for s in roster_positions if s != "BN"]
    # Dedicated position slots first, then any flex slots.
    dedicated = [s for s in slots if s not in FLEX_ELIGIBLE]
    flexes = [s for s in slots if s in FLEX_ELIGIBLE]

    lineup = []  # (slot, pid, name, pos, pts)

    def take(eligible_positions):
        for i, (pid, name, pos, pts) in enumerate(remaining):
            if pos in eligible_positions:
                return remaining.pop(i)
        return None

    for slot in dedicated:
        pick = take({slot})
        if pick:
            lineup.append((slot, *pick))
        else:
            lineup.append((slot, None, "(empty)", slot, 0))
    for slot in flexes:
        pick = take(FLEX_ELIGIBLE[slot])
        if pick:
            lineup.append((slot, *pick))
        else:
            lineup.append((slot, None, "(empty)", slot, 0))
    return lineup, remaining


def resolve_league(arg, season):
    if arg.isdigit() and len(arg) >= 12:
        return arg
    user = api.get_user(arg)
    if not user:
        print(f"No Sleeper user found for '{arg}'.")
        return None
    leagues = api.get_leagues(user["user_id"], season)
    if len(leagues) == 1:
        return leagues[0]["league_id"]
    if not leagues:
        print(f"{arg} has no {season} leagues.")
        return None
    print(f"{arg} is in several {season} leagues -- pass a league_id:")
    for lg in leagues:
        print(f"  {lg['league_id']}  {lg['name']}")
    return None


def main(argv) -> int:
    show_all = "--all" in argv
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: python optimize_lineup.py <username|league_id> [week] [--all]")
        return 1
    who = args[0]

    state = api.get_nfl_state() or {}
    season = state.get("season", "2025")
    week = int(args[1]) if len(args) > 1 else (state.get("week") or 1)

    league_id = resolve_league(who, season)
    if not league_id:
        return 1
    league = api.get_league(league_id)
    scoring = league.get("scoring_settings", {})
    roster_positions = league.get("roster_positions", [])
    players = api.get_players()

    # Find the roster: by username if given, else this prints for every team.
    user = None if who.isdigit() else api.get_user(who)
    rosters = api.get_rosters(league_id)
    if user:
        rosters = [r for r in rosters if r.get("owner_id") == user["user_id"]] or rosters

    proj = api.get_projections(season, week)
    proj_by_pid = {str(p.get("player_id")): (p.get("stats") or {}) for p in proj}

    for r in rosters:
        projected = project_roster(r, scoring, proj_by_pid, players)
        starters_now = set(str(x) for x in (r.get("starters") or []) if str(x) != "0")
        lineup, bench = optimize(projected, roster_positions)
        opt_total = round(sum(p[4] for p in lineup), 2)
        cur_total = round(sum(pts for pid, _, _, pts in
                              [(p[0], p[1], p[2], p[3] or 0) for p in projected]
                              if pid in starters_now), 2)

        print(f"\n=== Week {week} optimal lineup (full-PPR expected pts) ===")
        for slot, pid, name, pos, pts in lineup:
            star = "" if (pid in starters_now or pid is None) else "  << not currently started"
            print(f"  {slot:6} {pts:6.2f}  {name} ({pos}){star}")
        print(f"  {'TOTAL':6} {opt_total:6.2f}")
        print(f"\n  Currently-started projected total: {cur_total:.2f}"
              f"   (optimal: {opt_total:.2f}, +{opt_total - cur_total:.2f})")

        # Swaps: who should come in for whom.
        opt_ids = {p[1] for p in lineup}
        sit = [p for p in projected if p[0] in starters_now and p[0] not in opt_ids]
        start = [(slot, pid, name, pos, pts) for slot, pid, name, pos, pts in lineup
                 if pid is not None and pid not in starters_now]
        if start:
            print("\n  Recommended changes:")
            for slot, pid, name, pos, pts in start:
                print(f"    START {name} ({pos}) at {slot} -- proj {pts:.2f}")
            for pid, name, pos, pts in sit:
                print(f"    SIT   {name} ({pos}) -- proj {pts if pts is not None else 0:.2f}")
        else:
            print("\n  Your current lineup is already points-optimal by projection.")

        if show_all:
            print("\n  Bench (projected pts):")
            for pid, name, pos, pts in bench:
                print(f"    {pts if pts is not None else 0:6.2f}  {name} ({pos})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
