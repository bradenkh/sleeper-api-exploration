# CLAUDE.md — Context for Claude Code sessions

This repo tracks Braden's 2026 Sleeper fantasy football season. It is a
**data + strategy journal**, not an application. The point is that each week I can
open a Claude Code session, have you pull fresh data, compare it against what's
recorded here, and tell me what changed and what to do about it.

## Owner context — read this first

**Braden is new to football.** He does not know the sport's terminology or
conventions. When explaining anything:

- Define football terms on first use (FLEX, waiver, bye week, snap share, target
  share, handcuff, etc.).
- Lead with the recommendation, then the reasoning.
- Say plainly when something is a hard fact from the API vs. a judgment call.
  He has explicitly asked for that distinction before.
- Don't assume he'll spot an implication — spell it out.

## League identifiers

| Thing | Value |
|---|---|
| Sleeper username | `brdnhnsn` |
| User ID | `1401782633133780992` |
| League name | The Boys |
| League ID | `1401765585515237376` |
| Draft ID | `1401765586874150912` |
| Braden's roster ID | `3` |
| Season | 2026 (NFL) |

Roster ID → manager mapping lives in `docs/league-reference.md`. Always
re-derive it from `data/users.json` + `data/rosters.json` rather than trusting a
memorized mapping — ownership can change.

## Sleeper API — how to pull fresh data

Public, no auth, no rate limit worth worrying about. Base: `https://api.sleeper.app`

```
/v1/state/nfl                             # current week + season — CHECK THIS FIRST
/v1/league/{league_id}                    # settings, scoring, roster_positions
/v1/league/{league_id}/users              # managers
/v1/league/{league_id}/rosters            # rosters, records, points
/v1/league/{league_id}/matchups/{week}    # weekly matchups + scores
/v1/league/{league_id}/transactions/{week}# adds, drops, trades
/v1/league/{league_id}/traded_picks       # traded draft picks
/v1/draft/{draft_id}/picks                # draft results
/v1/players/nfl                           # ~14MB player dictionary
/schedule/nfl/regular/{season}            # NFL schedule (undocumented but works)
```

Gotchas learned the hard way — see `docs/api-notes.md` for the full list:

- `/v1/players/nfl` is **14MB**. It is deliberately **not committed**. Fetch it to
  the scratchpad and cache it for the session.
- There is **no bye-week field** on players. Byes must be derived from
  `/schedule/nfl/regular/2026` — a team's bye is the week it has no game.
  Already derived and committed as `data/byes_2026.json`.
- `search_rank` is Sleeper's own ranking (lower = better). It's a decent value
  proxy but **lags real-world news** — always flag it as directional, not fact.
- Autopicked draft picks still populate `picked_by`, so that field can't detect
  autodrafting. Use draft duration instead (`start_time` → `last_picked`).
- Defenses have `player_id` = team abbreviation (e.g. `"HOU"`) and usually no
  `search_rank`.

## Weekly workflow

This is the routine to run each week. Full checklist in `weekly/TEMPLATE.md`.

1. `GET /v1/state/nfl` to confirm the current week.
2. Pull rosters, matchups, and transactions for the completed week.
3. Diff against last week's entry in `weekly/`:
   - What did each manager add/drop? Who is active vs. dormant?
   - Any trades? (There have been none so far.)
   - Injury/depth-chart changes on Braden's roster.
4. Check Braden's lineup for **injured or bye-week starters** — this is the
   single highest-value check and has already caught one real problem.
5. Write `weekly/week-NN.md` from the template.
6. Update `STRATEGY.md` if the plan actually changed. Don't churn it otherwise.

## Repo conventions

- One markdown file per week in `weekly/`, named `week-NN.md` (zero-padded).
- Raw JSON snapshots go in `data/`. Keep them small; never commit `players.json`.
- `STRATEGY.md` is the living plan. `docs/league-reference.md` is static facts
  that only change if league settings change.
- Record **what actually happened** alongside what was recommended, so the
  advice can be checked against reality later. Wrong calls stay in the log.

## Standing facts worth not re-deriving

- Lineup is **10 starters**: QB, RB, RB, WR, WR, TE, FLEX, FLEX, K, DEF + 5 bench = 15 total.
- **No IR slot** (`reserve_slots: 0`), so injured players occupy real roster spots.
- Trade deadline: **Week 11**. Playoffs start **Week 15**. All 6 teams make playoffs.
- **No byes in Weeks 1–4, 12, or 15–18** — the playoffs are bye-free.
- The draft was a **full autodraft** (90 picks in 2m51s, 10-second pick timer).
