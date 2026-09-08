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
| `/v1/league/{league_id}/transactions/{week}` | Adds, drops, trades, FAAB |
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

### "Unowned" splits into two very different states

An unrostered player is either an **instant-add free agent** or a **waiver
claim**, and the API does not label which. The difference is whether anyone has
recently dropped them.

| State | How it arises | How to get them |
|---|---|---|
| Free agent | never rostered this season | instant add, no bid |
| On waivers | **dropped** by a manager within `waiver_clear_days` (2) | FAAB claim, processes on the waiver run |

Confirmed empirically on 2026-09-08:

- **Oronde Gadsden** — never rostered — posted as `free_agent` / `complete`
  immediately, no waiver period, no bid.
- **Cam Little** and **Drake Maye** — both dropped by TuR7L3z on 2026-09-07 —
  are waiver claims, not instant adds, despite showing up as "unowned".

**How to tell them apart:** scan `/transactions/{week}` for the player in
`drops`. A recent drop means they're in the waiver period. There is no field on
the player object for this.

`fantasy_report.py` §7 now labels each unowned player `free agent` or
**`WAIVER`**, reconstructing the waiver state from recent `drops` in the
transaction log. Kickers are included there too, since a bye-week swap at K is a
common cheap upgrade.

Practical consequence: a Sunday-morning fix works only for never-rostered
players. Insurance behind a Questionable starter is still worth a bench spot,
because the obvious replacement may well be someone another manager just cut.

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
