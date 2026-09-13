"""Minimal read-only client for the public Sleeper API.

The Sleeper API requires no authentication or API key. See https://docs.sleeper.com
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import urllib.request
import urllib.error

BASE = "https://api.sleeper.app/v1"


def _get(path: str):
    """GET {BASE}/{path} and return parsed JSON (or None for a null/404 body)."""
    url = f"{BASE}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "sleeper-api-exploration"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    if not body or body == "null":
        return None
    return json.loads(body)


def get_user(username_or_id: str):
    """Look up a user by username or user_id. Returns the user object or None."""
    return _get(f"user/{username_or_id}")


def get_leagues(user_id: str, season: str, sport: str = "nfl"):
    """All leagues a user belongs to for a given sport/season."""
    return _get(f"user/{user_id}/leagues/{sport}/{season}") or []


def get_league_users(league_id: str):
    """Every member of a league (user_id, username, display_name, ...)."""
    return _get(f"league/{league_id}/users") or []


def get_league(league_id: str):
    """Full league object (settings, roster_positions, scoring, status, ...)."""
    return _get(f"league/{league_id}")


def get_rosters(league_id: str):
    """Every roster in a league (owner_id, players, starters, wins/losses/fpts)."""
    return _get(f"league/{league_id}/rosters") or []


def get_matchups(league_id: str, week: int):
    """All matchup entries for a given week (one per roster, grouped by matchup_id)."""
    return _get(f"league/{league_id}/matchups/{week}") or []


def get_transactions(league_id: str, week: int):
    """All transactions (adds/drops, waivers, trades) reported under a given week."""
    return _get(f"league/{league_id}/transactions/{week}") or []


def get_traded_picks(league_id: str):
    """Draft picks that have been traded away from their original owner."""
    return _get(f"league/{league_id}/traded_picks") or []


def get_nfl_state(sport: str = "nfl"):
    """Current season/week state for a sport (season, week, season_type, ...)."""
    return _get(f"state/{sport}")


def get_players(sport: str = "nfl", cache_hours: float = 24.0):
    """The full player map {player_id: {...}} for a sport.

    This payload is large (~15 MB for the NFL), so it is cached on disk and
    reused for ``cache_hours`` to keep repeated reports fast and gentle on the
    API. Pass ``cache_hours=0`` to always refetch.
    """
    cache_path = os.path.join(tempfile.gettempdir(), f"sleeper_players_{sport}.json")
    if cache_hours > 0 and os.path.exists(cache_path):
        age_hours = (time.time() - os.path.getmtime(cache_path)) / 3600.0
        if age_hours < cache_hours:
            try:
                with open(cache_path, "r", encoding="utf-8") as fh:
                    return json.load(fh)
            except (OSError, ValueError):
                pass  # fall through and refetch on a corrupt/unreadable cache

    players = _get(f"players/{sport}") or {}
    try:
        with open(cache_path, "w", encoding="utf-8") as fh:
            json.dump(players, fh)
    except OSError:
        pass  # caching is best-effort; a read-only tmp is not fatal
    return players


def main(argv):
    if len(argv) < 2:
        print("usage: python sleeper_client.py <username> [season]")
        return 1

    username = argv[1]
    season = argv[2] if len(argv) > 2 else "2025"

    user = get_user(username)
    if not user:
        print(f"No Sleeper user found for '{username}'.")
        print("Sleeper usernames have no spaces — try the exact @handle from the app.")
        return 1

    uid = user["user_id"]
    print(f"user:        {user.get('display_name')} (@{user.get('username')})")
    print(f"user_id:     {uid}")

    leagues = get_leagues(uid, season)
    print(f"\n{season} leagues ({len(leagues)}):")
    for lg in leagues:
        print(f"  - {lg['name']}  [league_id={lg['league_id']}, teams={lg.get('total_rosters')}]")
    if not leagues:
        print("  (none — try a different season, e.g. 2024)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
