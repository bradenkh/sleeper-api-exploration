# League Reference — "The Boys" (2026)

Static facts. These only change if league settings change or ownership changes.
Everything here was derived from the Sleeper API on 2026-09-08 (pre-Week 1).

---

## League settings

| Setting | Value |
|---|---|
| League ID | `1401765585515237376` |
| Teams | 6 |
| Scoring | PPR (point per reception) |
| Roster size | 15 (10 starters + 5 bench) |
| **IR / reserve slots** | **0** — injured players occupy real roster spots |
| Taxi slots | 0 |
| Waiver type | **Rolling priority (`waiver_type: 0`) — NOT FAAB.** `waiver_budget: 100` appears in settings but is inert; no bids are used. Winning a claim drops you to last. |
| Waiver processing | `waiver_day_of_week: 2`, 2-day clear. Check the claim screen for the exact run time. |
| Waiver order | Rolling. Snapshot 09-08: ajolson77 1, brdnhnsn 2, sworthy92 3, HntrRundas 4, stalbot8 5, TuR7L3z 6. After brdnhnsn won the Cam Little claim on 09-09 he fell to 6th. |
| **Trade deadline** | **Week 11** |
| Trade review | 2 days |
| **Playoffs start** | **Week 15** |
| Playoff teams | **6 of 6 — everyone qualifies; standings set seeding only** |
| Keepers | 1 max, costs 3 draft rounds next season |
| Draft | 15-round snake, completed 2026-09-06 |

### Starting lineup — 10 slots

`QB · RB · RB · WR · WR · TE · FLEX · FLEX · K · DEF` + 5 bench

**FLEX** = any RB, WR, or TE. So 5 of the 10 starters come from the RB/WR/TE pool.

---

## Managers

| Roster ID | Manager | User ID | Team name |
|---|---|---|---|
| 1 | HntrRundas | `1267967842662227969` | Toad-ally Awesome |
| 2 | TuR7L3z | `1256697432272551936` | — |
| **3** | **brdnhnsn (me)** | `1401782633133780992` | — |
| 4 | ajolson77 | `1402101928837554176` | — |
| 5 | sworthy92 | `1402335919792467968` | — |
| 6 | stalbot8 | `1402414632823500800` | — |

**HntrRundas is the commissioner** (`is_owner: true`) and created the league.

---

## My regular-season schedule

14 weeks, round-robin. I play each opponent 3 times except sworthy92 (twice).

| Week | Opponent |
|---|---|
| 1 | TuR7L3z |
| 2 | HntrRundas |
| 3 | stalbot8 |
| 4 | ajolson77 |
| 5 | sworthy92 |
| 6 | TuR7L3z |
| 7 | HntrRundas |
| 8 | stalbot8 |
| 9 | ajolson77 |
| 10 | sworthy92 |
| 11 | TuR7L3z |
| 12 | HntrRundas |
| 13 | stalbot8 |
| 14 | ajolson77 |

Favorable draw: only **two** meetings with sworthy92, the strongest roster.

---

## 2026 NFL bye weeks

Derived from `/schedule/nfl/regular/2026` — a team's bye is the week it has no
game. Every team plays exactly 17 games across the 18-week season.

| Week | Teams on bye | Count |
|---|---|---|
| 5 | CAR, KC | 2 |
| 6 | CIN, DET, MIA, MIN | 4 |
| 7 | BUF, JAX, LAC, WAS | 4 |
| 8 | HOU, NO, NYG, SF | 4 |
| 9 | PIT, TEN | 2 |
| 10 | CHI, DEN, PHI, TB | 4 |
| 11 | ATL, CLE, GB, LAR, NE, SEA | 6 |
| 13 | BAL, IND, LV, NYJ | 4 |
| 14 | ARI, DAL | 2 |

**No byes in Weeks 1–4, Week 12, or Weeks 15–18.** The playoffs are bye-free.

### Bye exposure by manager

| Manager | Worst week | Players out |
|---|---|---|
| TuR7L3z | 7 | 5 |
| **brdnhnsn (me)** | **11 and 13** | **4 each** |
| HntrRundas | 10 | 4 |
| ajolson77 | 10 | 4 |
| sworthy92 | 6 | 3 |
| stalbot8 | 6 | 3 |

---

## Draft summary

- **Autodrafted.** 90 picks in **2m51s** (~1.9 sec/pick), 10-second pick timer,
  `cpu_autopick` enabled. Nobody made real decisions.
- Held 2026-09-06, ~19:33 ET. Full picks in `data/draft_picks.json`.
- Evidence of bot behavior: TuR7L3z was given **4 QBs, 3 Ks, and 3 DEFs** but
  only **2 RBs**.

### Draft order (snake)

| Slot | Manager |
|---|---|
| 1 | TuR7L3z |
| 2 | stalbot8 |
| 3 | HntrRundas |
| 4 | sworthy92 |
| **5** | **brdnhnsn (me)** |
| 6 | ajolson77 |

---

## Opening rosters (post-autodraft, pre-Week 1)

Ranks are Sleeper `search_rank` (lower = better). Directional, not gospel.

### Roster 3 — brdnhnsn (me)

| Pos | Player | Team | Rank | Bye |
|---|---|---|---|---|
| RB | Jonathan Taylor | IND | 4 | 13 |
| WR | Jaxon Smith-Njigba | SEA | 6 | 11 |
| RB | Derrick Henry | BAL | 7 | 13 |
| RB | Jeremiyah Love | ARI | 15 | 14 |
| WR | Drake London | ATL | 19 | 11 |
| QB | Jayden Daniels | WAS | 20 | 7 |
| RB | Josh Jacobs | GB | 20 | 11 |
| RB | Breece Hall | NYJ | 27 | 13 |
| RB | Travis Etienne | NO | 34 | 8 |
| TE | Tyler Warren | IND | 48 | 13 |
| WR | Mike Evans | SF | 60 | 8 |
| WR | Rome Odunze | CHI | 64 | 10 |
| WR | Marvin Harrison Jr | ARI | 74 | 14 |
| K | Harrison Mevis | LAR | 154 | 11 |
| DEF | Houston | HOU | — | 8 |

### Other managers — headline strengths

| Manager | RB | WR | Notes |
|---|---|---|---|
| **sworthy92** | 6 | 5 | **Strongest roster.** Bijan Robinson, Achane, Kyren Williams, Kenneth Walker; Justin Jefferson, Nabers. **Worst QB in league (Stafford, 66).** |
| **stalbot8** | 5 | 6 | Elite WR room: Ja'Marr Chase, Nico Collins, Adams, McLaurin, Higgins. Jeanty at RB, McBride at TE. |
| **ajolson77** | 5 | 6 | Great proven WRs (A.J. Brown, ARSB, DeVonta Smith, Garrett Wilson). RBs beyond McCaffrey are unproven rookies. |
| **HntrRundas** | 5 | 6 | Balanced. Puka Nacua, CeeDee Lamb, Brock Bowers, Jalen Hurts. |
| **TuR7L3z** | **2** | 4 | Gibbs + Barkley then nothing. Still carries 3 QBs and 2 Ks. Only active manager so far. |

### QB landscape (trade-relevant)

| Manager | QB(s) | Rank |
|---|---|---|
| TuR7L3z | Josh Allen / Lamar Jackson / Joe Burrow | 3 / 10 / 15 |
| stalbot8 | Caleb Williams | 21 |
| **me** | Jayden Daniels | 20 |
| HntrRundas | Jalen Hurts | 26 |
| ajolson77 | Dak Prescott | 39 |
| **sworthy92** | **Matthew Stafford** | **66** |

---

## Transaction history

| Week | Date | Manager | Move | Type |
|---|---|---|---|---|
| 1 | 2026-09-07 | TuR7L3z | +Khalil Shakir (WR-BUF) / −Cam Little (K-JAX) | free agent |
| 1 | 2026-09-07 | TuR7L3z | +Jayden Reed (WR-GB) / −BUF DEF | free agent |
| 1 | 2026-09-07 | TuR7L3z | +Devaughn Vele (WR-NO) / −Drake Maye (QB-NE) | free agent |

**Trades to date: 0.** **Traded draft picks: 0.**

Five of six managers have made zero moves since the autodraft.
