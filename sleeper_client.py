"""Minimal read-only client for the public Sleeper API.

The Sleeper API requires no authentication or API key. See https://docs.sleeper.com
"""
from __future__ import annotations

import json
import sys
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
