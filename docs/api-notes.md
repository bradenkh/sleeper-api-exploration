# Sleeper API notes

Practical notes from actually working with the API, including things that
weren't obvious and cost time. Base URL: `https://api.sleeper.app`

No authentication, no API key, no meaningful rate limit. All read-only —
**there is no public write API**, so roster moves, waiver claims, and trades all
have to be done by hand in the Sleeper app. This repo can only advise, not act.

---

## Endpoints that work

| Endpoint | Returns |
|---|---|
| `/v1/user/{username}` | User profile → `user_id` |
| `/v1/user/{user_id}/leagues/nfl/{season}` | That user's leagues for a season |
| `/v1/state/nfl` | **Current week + season.** Check this first, every session. |
| `/v1/league/{league_id}` | Settings, scoring, `roster_positions` |
| `/v1/league/{league_id}/users` | Managers (incl. `is_owner` = commissioner) |
| `/v1/league/{league_id}/rosters` | Rosters, starters, records, points |
| `/v1/league/{league_id}/matchups/{week}` | Matchups + per-player scoring |
| `/v1/league/{league_id}/transactions/{week}` | Adds, drops, trades, waiver claims |
| `/v1/league/{league_id}/traded_picks` | Traded draft picks |
| `/v1/league/{league_id}/drafts` | Drafts for the league |
| `/v1/draft/{draft_id}` | Draft settings, order, slot→roster map |
| `/v1/draft/{draft_id}/picks` | Every pick |
| `/v1/players/nfl` | Full player dictionary (**~14MB**) |
| `/schedule/nfl/regular/{season}` | NFL game schedule (undocumented; works) |

---

## Gotchas

### `/v1/players/nfl` is 14MB

Do not commit it. Fetch once per session into the scratchpad and reuse:

```bash
curl -sS "https://api.sleeper.app/v1/players/nfl" -o "$SCRATCH/players.json"
```

### There is no bye-week field

Nothing on the player or team object gives a bye week. Derive it: pull
`/schedule/nfl/regular/2026`, collect the weeks each team appears in, and the
missing week is the bye. Every team plays 17 games across 18 weeks.

Already derived → `data/byes_2026.json` (team abbreviation → bye week).

```python
played = defaultdict(set)
for g in schedule:
    played[g['home']].add(g['week'])
    played[g['away']].add(g['week'])
bye = (set(range(1, 19)) - played[team]).pop()
```

### Autopicks can't be detected from `picked_by`

Intuitively an autopicked pick would have an empty `picked_by`. It doesn't —
autopicks are still attributed to the roster owner. All 90 picks in this
league's draft had a populated `picked_by` despite being a full autodraft.

**Detect it from timing instead:** `draft.start_time` → `draft.last_picked`.
This league: 90 picks in 2m51s ≈ 1.9 sec/pick, with `settings.pick_timer: 10`
and `cpu_autopick: 1`. Roster construction corroborates (one manager was given
4 QBs, 3 Ks, 3 DEFs, and only 2 RBs).

### `search_rank` is a proxy, not truth

Lower = better. It's Sleeper's own ranking, useful for rough tiering, but it
**lags real-world news** — an injured or benched player can hold a stale high
rank. Josh Jacobs sat at rank 20 while listed `NA` and 4th on the depth chart.

Always cross-reference `injury_status` and `depth_chart_order`, and flag
rank-based claims as directional when reporting them.

Players with `search_rank >= 9999999` (or null) are irrelevant — filter them out.

### Injury and depth-chart fields

Useful fields on a player object:

- `injury_status` — `Questionable`, `Doubtful`, `Out`, `NA`, or null.
  **`NA` means not active** — worse than Questionable, effectively unavailable.
- `injury_body_part`, `injury_notes`
- `depth_chart_order` — **1 = starter.** A high rank with `depth_chart_order` 3+
  is the classic "drafted as a stud, lost the job" trap.
- `news_updated` — epoch ms; how fresh the record is.

The highest-value weekly check is: for every starter, look at `injury_status`
**and** `depth_chart_order` together. Neither alone catches the Jacobs case.

### Defenses are odd

`player_id` is the team abbreviation (`"HOU"`), `position` is `DEF`, and
`search_rank` is usually absent. Filter them separately when ranking.

### When a player is an instant add vs. a waiver claim

**Revised 2026-09-26.** The earlier model here ("a drop stays on waivers until
the next weekly run", plus an unexplained "waiver window") was wrong in one
case and incomplete in the other. The API still does not label waiver status,
but two documented Sleeper rules explain every transaction in the log.

**Rule 1 — drop timer.** A dropped player is on waivers for
`waiver_clear_days` (this league: 2 → Sleeper holds him **47 hours**). Pending
claims process when the timer expires, not at the weekly run.

**Rule 2 — game lock.** When a player's NFL game kicks off, every unrostered
player on that team locks onto waivers **until the weekly run**, even if
nobody ever rostered him. The weekly run is Wednesday ~07:11 UTC (≈ 12:10 a.m.
PT / 3:10 a.m. ET). After it, everyone unclaimed becomes a free agent.

A player is a **free agent (instant add)** only if neither rule applies: not
dropped in the last 47 h, **and** his team has not kicked off since the last
Wednesday run.

| Evidence | What happened | Rule |
|---|---|---|
| Cam Little | dropped Mon 09-07 01:01 UTC, claimed Wed 09-09 **00:11** — 47h10m later, 7 h *before* any weekly-run slot | 1 |
| Oronde Gadsden | never rostered, instant add Tue 09-08 (no games played yet) | neither |
| Tyler Warren | dropped Sun 09-13 04:13; IND played that day → held until Wed 09-16 07:12 run | 1 then 2 |
| Everything, Tue 09-15 | every unowned player showed as a claim — all 32 teams had played | 2 |
| Kelce, McLaughlin, P. Washington | instant adds Wed 09-23 ~10:10 UTC, 3 h after the run | cleared by run |
| Ladd McConkey | dropped at the 09-23 07:11 run; instant add Sat 09-26 (79 h later, LAC not yet played) | 1 expired |

The last row disproves the old model, which predicted McConkey would stay on
waivers until 09-30.

Sources: Sleeper support — [Waivers for Regular Season & Playoffs](https://support.sleeper.com/en/articles/3978868-waivers-for-regular-season-playoffs)
("once their game starts, they lock and move to waivers"; "2 Days … 47 hours")
and [After Game Waivers](https://support.sleeper.com/en/articles/3242468-after-game-waivers-custom-daily-waivers).

**Weekly rhythm this produces:**

| When | Instant adds available |
|---|---|
| Wed ~3 a.m. ET run → Thursday kickoff | **everyone** (except 47-h drops) |
| Thu night → Sunday | only players whose team has **not** played yet |
| Sunday games → Mon night | only Monday-night teams, until they kick off |
| Tue → Wed run | **nobody** — every unowned player is a claim |

Practical consequences:

- The best time to add anyone is **Wednesday morning** after the run.
- A Sunday-morning injury fix works for any player on a Sunday/Monday team who
  was not dropped in the last 47 hours.
- Dropping a player whose game has not started puts him on a 47-hour timer;
  if his game kicks off inside it, he is locked until Wednesday.
- Sleeper's 24-hour rule: a free-agent add cannot be dropped for 24 hours.

`fantasy_report.py` §7 implements both rules in `waiver_status()`. Kickoff
*times* are not in the schedule endpoint, only dates and `status`, so "started"
means `status != pre_game` — correct once a game is under way, but a label on
game day morning should be read as "free agent until kickoff".

### Pending waiver claims are not exposed by the API

`/transactions/{week}` returns only completed (and failed) transactions. A claim
sitting in the queue is invisible — which is correct, since claims are blind and
nobody should be able to read anyone else's. There is no way to confirm from the
API that a claim was submitted; check the app, and verify after the run.

### `waiver_budget` in settings does not mean the league uses FAAB

This league's `/v1/league/{id}` returns `waiver_budget: 100`, which looks like
FAAB. It is not — the league runs **rolling waiver priority**. Three checks
settle it, and the third is decisive:

1. `settings.waiver_type` — `0` is rolling priority. FAAB is a different value.
2. Every roster carries `settings.waiver_position` (1..N) and
   `waiver_budget_used: 0`. A budget nobody has spent is a budget nobody has.
3. **Look at a completed `waiver` transaction.** A real FAAB claim carries a bid;
   this league's came back with `"waiver_budget": []` and `settings: {"seq": 0}`.

Winning a claim moves that roster to the back of the order — comparable
`waiver_position` across two snapshots proves it (brdnhnsn: 2nd on 09-08, 6th
after winning a claim on 09-09). Compare snapshots rather than assuming.

### Transactions are per-week and sparse

`/transactions/{week}` returns `[]` for weeks with no activity. Loop weeks 0–18
to get a full season history. Week 0 covers pre-season/post-draft activity in
some leagues; in this one the post-draft moves landed in week 1.

Transaction `type` values seen: `free_agent`, `waiver`, `trade`. A `trade` has
multiple entries in `roster_ids` and may include `draft_picks` and
`waiver_budget` transfers.

### Timestamps

All epoch milliseconds. `datetime.utcfromtimestamp(ts / 1000)`.

---

## Rebuilding the committed data

Everything in `data/` came from these calls (league ID `1401765585515237376`,
draft ID `1401765586874150912`):

```bash
BASE=https://api.sleeper.app
L=1401765585515237376
D=1401765586874150912

curl -sS "$BASE/v1/league/$L"                  -o data/league.json
curl -sS "$BASE/v1/league/$L/users"            -o data/users.json
curl -sS "$BASE/v1/league/$L/rosters"          -o data/rosters.json
curl -sS "$BASE/v1/draft/$D"                   -o data/draft.json
curl -sS "$BASE/v1/draft/$D/picks"             -o data/draft_picks.json
curl -sS "$BASE/schedule/nfl/regular/2026"     -o data/nfl_schedule_2026.json
for w in $(seq 1 14); do
  curl -sS "$BASE/v1/league/$L/matchups/$w" -o "data/matchups/week_$(printf %02d $w).json"
done
```

`data/byes_2026.json` is derived from the schedule, not fetched directly.
