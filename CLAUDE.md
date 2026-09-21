# CLAUDE.md — repo memory & operating assumptions

This repo explores the public Sleeper API and includes tooling for a specific
fantasy league check-in / lineup optimization.

## League context
- **League:** "The Boys" — `league_id 1401765585515237376`, 6 teams, **2026** season.
- **Scoring:** full **PPR** (1.0 per reception); standard yardage/TD weights.
- **Primary user:** `brdnhnsn` (`user_id 1401782633133780992`).

## Operating assumptions (assume these from here on)
1. **Waivers are PRIORITY (rolling order), NOT FAAB.** There is no bidding /
   FAAB budget in this league (the `waiver_budget: 100` in the settings is an
   unused default; `waiver_type: 0` and each roster carries a `waiver_position`).
   Contested claims are decided by waiver *order*, and winning a claim drops that
   team to the back of the order. Never advise "outbidding" or spending FAAB.
2. **Treat every unrostered player, defense, and team as a WAIVER CLAIM — assume
   there are NO instantly-addable free agents.** When recommending a pickup or a
   stream (DEF/K/QB/etc.), frame it as a waiver claim, and factor in the user's
   current waiver priority (they lose contested claims when low in the order).
   Do not tell the user something can be added instantly as a free agent.

## Tooling in this repo
- `sleeper_client.py` — read-only Sleeper API client (users, leagues, rosters,
  matchups, transactions, NFL state, projections, cached player map).
- `league_report.py` — standings + since-last-week manager activity.
- `optimize_lineup.py` — points-optimal lineup by the league's own scoring, plus
  a per-position waiver board (best available vs. your starters).
- `season_report.py` — rest-of-season points optimization and bye-week planning.
