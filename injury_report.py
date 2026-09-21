"""Injury-status check for your roster (and, optionally, the whole league).

Pulls Sleeper's ``injury_status`` / ``injury_body_part`` for players so a
game-time decision or a fresh IR stint surfaces before it burns you -- e.g. so
you don't trade a healthy player for someone who just landed on IR.

Two scopes:
  * default -- just your roster (are any of MY guys dinged up?).
  * ``--all`` -- every rostered player in the league, grouped by owner, so you
    can vet trade targets (an opponent's injured star may be a buy-low, or a
    trap) and see who your opponents might be without.

Freshness matters for injuries: the player map is cached (~24h). Pass
``--fresh`` to force a re-download. Even then, for a true game-time decision the
Sleeper app / beat reporters are the source of truth -- this flags who to check,
it is not a substitute for the inactives report on game day.

Usage:
    python injury_report.py <username|league_id> [--all] [--fresh]
"""
from __future__ import annotations

import sys
import time

import sleeper_client as api

# Lower rank = more severe / more urgent to act on.
SEVERITY = {"IR": 0, "PUP": 1, "Sus": 2, "DNR": 3, "COV": 4,
            "Out": 5, "Doubtful": 6, "Questionable": 7}
# Statuses that are not an actual game-availability injury.
IGNORE = {None, "", "NA", "Active", "Healthy"}


def _age_days(ms):
    if not ms:
        return None
    return (time.time() - ms / 1000) / 86400.0


def main(argv) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: python injury_report.py <username|league_id> [--all] [--fresh]")
        return 1
    who = args[0]
    scope_all = "--all" in argv
    fresh = "--fresh" in argv

    state = api.get_nfl_state() or {}
    season = state.get("season", "2025")
    week = state.get("week")

    if who.isdigit() and len(who) >= 12:
        league_id, user = who, None
    else:
        user = api.get_user(who)
        leagues = api.get_leagues(user["user_id"], season) if user else []
        if len(leagues) != 1:
            print("Pass a league_id.")
            return 1
        league_id = leagues[0]["league_id"]

    # injuries are only as fresh as the player map -> allow a forced refresh.
    players = api.get_players(cache_hours=0 if fresh else 24)
    users = {u["user_id"]: u for u in api.get_league_users(league_id)}
    rosters = api.get_rosters(league_id)

    def owner_label(uid):
        u = users.get(uid, {})
        return (u.get("metadata") or {}).get("team_name") or u.get("display_name", "?")

    def injured_on(roster):
        out = []
        for pid in (roster.get("players") or []):
            p = players.get(str(pid), {})
            status = p.get("injury_status")
            if status in IGNORE:
                continue
            out.append({
                "name": p.get("full_name") or str(pid),
                "pos": p.get("position"), "team": p.get("team"),
                "status": status, "part": p.get("injury_body_part") or "?",
                "age": _age_days(p.get("news_updated")),
                "starter": str(pid) in {str(x) for x in (roster.get("starters") or [])},
            })
        out.sort(key=lambda r: (SEVERITY.get(r["status"], 9), not r["starter"]))
        return out

    def render(rows, show_starter=True):
        for r in rows:
            age = f"{r['age']:.0f}d ago" if r["age"] is not None else "?"
            star = " *STARTER*" if (show_starter and r["starter"]) else ""
            print(f"    {r['status']:12} {r['name']} ({r['pos']}-{r['team']}) "
                  f"-- {r['part']}, updated {age}{star}")

    print(f"Injury report -- {season}, week {week}"
          f"{' [fresh pull]' if fresh else ' (cached player data; --fresh to refresh)'}")
    print("=" * 68)

    mine = next((r for r in rosters if user and r.get("owner_id") == user["user_id"]), None)
    if mine:
        rows = injured_on(mine)
        print(f"\nYOUR ROSTER ({owner_label(mine.get('owner_id'))}):")
        if rows:
            render(rows)
        else:
            print("    clean -- no injury designations.")

    if scope_all:
        print("\nLEAGUE-WIDE (trade targets / opponent watch):")
        for r in rosters:
            if mine and r is mine:
                continue
            rows = injured_on(r)
            if rows:
                print(f"  {owner_label(r.get('owner_id'))}:")
                render(rows, show_starter=False)
    elif not mine:
        print("(No matching roster; pass --all to scan the whole league.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
