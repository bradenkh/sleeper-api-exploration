# Week 3 — 2026-09-26 (catch-up entry, covers Week 2 too)

**Record:** 2-0 · **Standing:** 1st of 6 (most points: 320.90) · **This week's opponent:** stalbot8 (dormant, 1-1)

No Week 2 entry was written. This one fills the gap and opens Week 3 from the
Saturday before the Sunday slate. Mechanical data: `week-03-report.md`.

---

## 1. Result

### Week 1 (final) — Win

| | Score |
|---|---|
| Me | **158.76** |
| TuR7L3z | 153.46 |

Won by 5.3. Henry 35.3, JSN 26.2, Taylor 25.1. HOU DEF scored −1.0 and Mike
Evans scored 16.9 on the bench — a close win with points left over.

### Week 2 (final) — Win

| | Score |
|---|---|
| Me | **162.14** |
| HntrRundas | 121.66 |

**What decided it:** Jaxon Smith-Njigba scored 42.5 on his own. Taylor 29.2 on
top. No lineup mistake mattered; Brock Bowers scored 0.0 on the bench (he was
out), which is the right place for him.

### Week 3 (in progress)

28.40 — 0.00. Drake London scored all 28.4 in Thursday's ATL @ GB game.
Every other game is Sunday 09-27 (PHI @ CHI is Monday).

---

## 2. Lineup audit — the important one

| Starter | Pos | Status | Depth | Flag? |
|---|---|---|---|---|
| **Jayden Daniels** | **QB-WAS** | **Out (elbow)** | **2** | **🚨 swap for Mahomes** |
| Jonathan Taylor | RB-IND | — | 1 | ok |
| Derrick Henry | RB-BAL | — | 1 | ok |
| Jaxon Smith-Njigba | WR-SEA | — | 1 | ok |
| Drake London | WR-ATL | — | 1 | played, 28.4 |
| Tyler Warren | TE-IND | — | 1 | ok |
| Jeremiyah Love | RB-ARI | — | 1 | ok |
| Breece Hall | RB-NYJ | — | 1 | ok |
| Cam Little | K-JAX | — | — | ok |
| **— empty —** | **DEF** | — | — | **🚨 put DET DEF in** |

### Problems found — two certain zeros

**1. Jayden Daniels is starting and ruled `Out`.** Elbow injury; Washington's
depth chart already has him 2nd. **Patrick Mahomes** (added via waiver 09-23) is
on the bench, healthy, and plays Sunday (KC @ MIA). Swap them.

**2. The DEF slot is empty.** The Week 2 waiver claim `+DET DEF / −HOU DEF`
processed on 09-23, which removed HOU from the starting slot — but DET was
placed on the bench, not in the slot. Same failure mode as the Week 1 Warren
drop: a move that empties a starting slot. DET hosts NYJ Sunday; move it in.

Both fixes are still possible — both games are `pre_game`. Total exposure if
missed: a QB (~15–18/wk so far) and a DEF, i.e. roughly a quarter of a weekly
score.

Side note (judgment): DET DEF faces the Jets, and Breece Hall is a Jet. A good
day for the defense is a slightly worse day for Hall. Small effect; not worth
changing either.

The other flags are bench-only and not actionable this week: Brock Bowers
(Questionable, knee — meniscus) and Mike Evans (Questionable, hip).

### Bye-week conflicts

None this week or next — no byes until Week 5 (1 player), Week 6 (1), Week 7 (2).

---

## 3. What the other managers did

| Manager | Moves since Week 1 | Active? |
|---|---|---|
| **TuR7L3z** | 4 — +Watson/−**McConkey**, +Kelce, +Parker Washington, +McLaughlin (K) | **active** |
| **HntrRundas** | 2 — +Ferguson/−Goedert (TE), +MIN DEF/−SEA DEF | **active** |
| ajolson77 | none | dormant |
| sworthy92 | none | dormant |
| stalbot8 | none | dormant |

**Dormant count unchanged: 3 of 5.** Nobody new woke up.

**Opponents leaking points (fact):** HntrRundas has an empty DEF slot this week
(same mistake as mine — MIN DEF is not in the lineup). ajolson77 is still
starting A.J. Brown, who is on IR, for the third straight week. My opponent
stalbot8 is starting Caleb Williams at QB — Doubtful (hamstring), 3rd on the
depth chart.

**Trades league-wide: 0.**

### The big one: TuR7L3z dropped Ladd McConkey

McConkey (WR-LAC, rank 35) was the centerpiece of the planned
Hall-for-McConkey trade in `STRATEGY.md` §4.2. TuR7L3z just dropped him for
Christian Watson. He is now **on waivers** and clears at the next waiver run.
That means the trade is moot — he can be had without giving up anything.

---

## 4. Waiver wire

**Waiver order (fact):** I am **6th — last** — after winning the Mahomes and DET
claims. Order: ajolson77, sworthy92, stalbot8, TuR7L3z, HntrRundas, me.

### Recommendation: claim Ladd McConkey, drop Mike Evans

- **Why McConkey:** rank 35 vs my WR3 options Evans (60) and Odunze (63). This is
  the WR upgrade the whole trade plan was chasing, now for free.
- **Why the claim can still win despite last priority (judgment):** the three
  managers ahead of me at 1–3 have made zero moves all season. The real
  competitors are TuR7L3z (who just dropped him — unlikely to re-claim) and
  HntrRundas (priority 5, ahead of me, active). So it hinges on whether
  HntrRundas wants him.
- **Why drop Evans:** roster is 15/15, so a claim needs a drop. Evans is the
  lowest-value non-QB/TE piece (rank 60, Questionable hip, age). Odunze (63) is
  the alternative; keep whichever has played better if you prefer.
- **Timing:** McConkey clears on the next waiver run, after this week's games.
  He cannot help Week 3 regardless.
- **Bye:** LAC is on bye Week 7 — already my heaviest bye week (2 players). Worth
  knowing, not a reason to pass.

### Also noted

- **Drake Maye (QB-NE, rank 11) is still a free agent.** Less relevant now that
  Mahomes is the backup — two healthy QBs is enough while Daniels is out.
- **Roster crowding (judgment):** 2 QBs, 2 TEs, 5 RBs, 3 WRs, 1 K, 1 DEF. Once
  Daniels's timeline is known, one QB is likely surplus. Same for TE once Bowers
  is healthy — Bowers (23) outranks Warren (47) and should start when active.

---

## 5. My roster changes (since Week 1 entry)

| In | Out | Reason |
|---|---|---|
| Tyler Warren (TE-IND) | Marvin Harrison Jr (WR-ARI) | Waiver claim — reversed the Week 1 Warren drop mistake. |
| Brock Bowers (TE-LV) | — | Waiver claim, no drop. HntrRundas dropped him in Week 1 while he was Out. |
| Patrick Mahomes (QB-KC) | Oronde Gadsden (TE-LAC) | Waiver 09-23 — QB cover for Daniels. |
| DET DEF | HOU DEF | Waiver 09-23 — stream. **Left DEF slot empty.** |

The Week 1 transaction log also shows one failed claim for Drake Maye and four
duplicate failed claims for Warren. Harmless; the API does not say why they
failed.

---

## 6. Strategy check

The plan changed in one place: **the WR fix no longer needs a trade.** If the
McConkey claim hits, Breece Hall stays — and he has been useful (19.8, 14.2) in
the FLEX. If it misses to HntrRundas, reopen the trade conversation with
TuR7L3z or ajolson77 per `docs/trade-targets.md`.

**Update `STRATEGY.md` only after the claim resolves** — no churn yet.

**Process lesson, reinforced:** waiver claims that drop a starter do not
auto-fill the slot. After every waiver run (and every drop), re-run
`scripts/fantasy_report.py` and check "Cannot play". This has now caught an
empty slot twice.

---

## 7. Next week

**Week 4 opponent:** check after Week 3 · **My byes:** 0

### Actions — before Sunday 09-27 kickoff

- [ ] **Start Patrick Mahomes at QB, bench Jayden Daniels** (Out, elbow)
- [ ] **Move DET DEF into the empty DEF slot**
- [ ] Re-run `scripts/fantasy_report.py` — "Cannot play" should read 0

### Actions — this week

- [ ] Waiver claim: **+Ladd McConkey / −Mike Evans**
- [ ] Watch Daniels's elbow news; decide QB surplus once his timeline is known
- [ ] When Bowers is cleared, start him over Warren
