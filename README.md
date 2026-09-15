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
scripts/
  fantasy_report.py        Weekly league scan (report-only)
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

```bash
python3 scripts/fantasy_report.py                    # current week
python3 scripts/fantasy_report.py --out weekly/week-03-report.md
python3 scripts/fantasy_report.py --week 13          # look ahead
```

No dependencies — Python 3 standard library only.

1. Run the report. It scans **all six managers**, not just mine.
2. Read §2 (lineup audit) and §4 (manager activity) — who has starters that
   can't play, and who's still dormant.
3. Write `weekly/week-NN.md` from the template, adding interpretation.
4. Update `STRATEGY.md` only if the plan actually changed.

### What the report covers

| § | Section | Why |
|---|---|---|
| 1 | Standings | Records and points |
| 2 | **Lineup audit, all 6 managers** | Starters who can't play — mine *and* opponents' |
| 3 | Matchups | Exposure on both sides of each game |
| 4 | **Manager activity** | Who's managing vs. dormant — the core edge |
| 5 | Recent transactions | Every add/drop/trade |
| 6 | Bye lookahead | 5-week horizon, per manager |
| 7 | Unowned players | What's on the wire |
| 8 | Waiver order | Everyone's priority position |

### Report-only, on purpose

The script states facts and flags anomalies. It does **not** recommend lineups,
rank players against each other, or tell you who to start. Ranking heuristics go
stale — Sleeper had Josh Jacobs at rank 20 while he was listed `NA` and sitting
4th on his depth chart. Judgment stays in conversation where it can be argued
with; the script just makes sure nothing gets missed.

## League at a glance

| | |
|---|---|
| Format | 6-team PPR keeper league |
| Roster | 15 (10 starters, 5 bench, **no IR slot**) |
| Waivers | **Rolling priority, no money.** Winning a claim drops you to last. |
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
