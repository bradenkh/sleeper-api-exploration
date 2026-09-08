# sleeper-api-exploration

Season tracker for my 2026 Sleeper fantasy football league, **"The Boys"**.

This repo is where the season lives: the strategy, the weekly log of what
everyone is doing, and raw data snapshots from the Sleeper API. I open it in
Claude Code each week to pull fresh data, diff it against what's recorded, and
figure out what to do next.

## Layout

```
CLAUDE.md                  Context for Claude Code sessions — read first
STRATEGY.md                The living season plan
docs/
  league-reference.md      Static facts: settings, rosters, byes, schedule
  api-notes.md             Sleeper API endpoints and gotchas
weekly/
  TEMPLATE.md              Template for each week's entry
  week-01.md               Week-by-week log
data/                      Raw JSON snapshots from the API
  matchups/                Per-week matchup data
```

## The weekly routine

1. Open a Claude Code session here.
2. Pull fresh data from the Sleeper API (endpoints in `docs/api-notes.md`).
3. **Audit the lineup** — cross-check every starter against injury status *and*
   depth-chart position. This is the highest-value check and has already caught
   a starter who couldn't score.
4. Check what the other managers did — adds, drops, trades, and who's still
   dormant.
5. Write `weekly/week-NN.md` from the template.
6. Update `STRATEGY.md` only if the plan actually changed.

## League at a glance

| | |
|---|---|
| Format | 6-team PPR keeper league |
| Roster | 15 (10 starters, 5 bench, **no IR slot**) |
| Waivers | FAAB, $100/season, processes Tuesdays |
| Trade deadline | **Week 11** |
| Playoffs | Week 15 — **all 6 teams qualify**, standings set seeding only |
| Draft | 15-round snake, **autodrafted** (90 picks in 2m51s) |

## Where things stand

Pre-Week 1. The autodraft handed me a running-back-heavy roster that's strong at
RB and thin at WR, and handed some opponents genuinely broken ones. Four of five
opponents haven't logged in since the draft. The plan is in `STRATEGY.md`; the
short version is that lineup discipline and the waiver wire beat cleverness in a
league this passive, and the one real hole — wide receiver — has to be fixed by
trade before the Week 11 deadline.

## Note

The Sleeper API is **read-only**. Nothing here can execute a roster move — all
adds, drops, and trades happen by hand in the Sleeper app.
