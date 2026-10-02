# Week 4 — 2026-10-02 (Friday; one game already played)

**Record:** 3-0 · **Standing:** 1st of 6 (tied with sworthy92 at 3-0; I lead on points, 483.80 vs 441.38) · **This week's opponent:** ajolson77 (dormant, 1-2)

Mechanical data: `week-04-report.md`.

---

## 1. Result — Week 3 (final): Win

| | Score |
|---|---|
| Me | **162.90** |
| stalbot8 | 152.38 |

Projected margin was ~26; actual was 10.5.

**What decided it:** Jaxon Smith-Njigba (35.4) and Drake London (28.4). Taylor
(9.2), Cam Little (4.0) and SEA DEF (2.0) were weak. On stalbot8's side, the
three-Bengals stack I flagged hit for 54.7, and Purdy scored 31.3. That's why it
got close.

**Wrong call on my side, logged:** I advised keeping Warren at TE unless Bowers
was confirmed active. Bowers played and scored **27.6 on the bench**, against
Warren's 14.7, which cost 12.9 points. It didn't change the result. In hindsight,
"confirmed active" was the right test; the miss was not re-checking his status
before kickoff.

Other bench points: McConkey 10.6, Etienne 9.0, Odunze 7.4.

---

## 2. Lineup audit — Week 4

| Starter | Pos | Status | Proj | Flag? |
|---|---|---|---|---|
| Patrick Mahomes | QB-KC | — | 21.2 @ LV | ok |
| Jonathan Taylor | RB-IND | — | 21.5 @ WAS | ok |
| Derrick Henry | RB-BAL | — | 19.5 vs TEN | ok |
| Jaxon Smith-Njigba | WR-SEA | — | 22.4 vs LAC | ok |
| Drake London | WR-ATL | — | 16.1 @ NO (Mon) | ok |
| Tyler Warren | TE-IND | — | 12.1 @ WAS | ok |
| Jeremiyah Love | RB-ARI | — | 15.9 @ NYG | ok |
| **Breece Hall** | **RB-NYJ** | **Out (quad)** | **0** | **🚨 replace with Bowers** |
| Cam Little | K-JAX | — | 6.2 @ CIN | ok |
| SEA DEF | DEF | — | 8.8 vs LAC | ok |

Projections are Sleeper's, in league scoring (`optimize_lineup.expected_points`).

### Problem found: Breece Hall is ruled Out

The Jets ruled him out Friday. Reports say week-to-week, the MRI was "good news",
and he's likely questionable at best for Week 5. He sits in a FLEX slot.

**Fix: move Brock Bowers (TE-LV) into that FLEX slot.** FLEX accepts a TE. Bowers
is healthy (no injury tag) and projects 15.3 @ KC. Best unowned RB for this week
is Chuba Hubbard at 16.2, but he's on bye in Week 5 and the edge is under a
point, so it's not worth a roster move. McConkey (12.1, Questionable foot) ranks
below Bowers.

**Projected after the fix: ~159 vs ajolson77 ~108.** ajolson77 is starting two
players who can't play (A.J. Brown on IR, DeVonta Smith Out).

### Bench health

| Player | Status | Back |
|---|---|---|
| Jayden Daniels | Out (elbow), **limited in practice** Wed/Thu | Reported "3 weeks or sooner" → **Week 5 target** |
| Breece Hall | Out (quad) | Week 5 questionable at best |
| Travis Etienne | **IR (hamstring)** as of 10-01 | earliest Nov 8 (Week 9) |
| Ladd McConkey | Questionable (foot) | — |

With Etienne on IR and Hall Out, **2 of 15 roster spots are producing nothing**,
and there is no IR slot.

### Streaming check (K / DEF)

SEA DEF (8.8) is already the best unowned option that doesn't play against one
of my players; the top-4 projected defenses are all owned. Kicker: Little 6.2
vs the best free agent at ~8. Kicker gaps are noise per the backtest. **No
change.**

---

## 3. What the other managers did

| Manager | Since last entry | Status |
|---|---|---|
| TuR7L3z | +PIT DEF / −SF DEF (09-30) | active, but 0-3 |
| stalbot8 | none since the Purdy add | active |
| HntrRundas | none since Week 2 | quiet |
| ajolson77, sworthy92 | none, all season | dormant |

**Fact worth knowing:** sworthy92 (3-0, my rival for the top seed) is starting
two players who can't play this week: Achane (IR, ACL) and Jefferson (Out). A
dormant manager can't fix that, which helps my seeding odds.

**Trades league-wide: 0.**

---

## 4. Waiver wire / roster spots

No add is needed for Week 4. The Etienne spot question (judgment):

- **Keep Etienne for now.** Under the season-only objective (STRATEGY §0) he's
  back by Week 9, which is in time for the Week 13 crunch (Taylor, Henry, Hall,
  Warren and Bowers are all on bye) and for the playoffs. Rank 34 when healthy
  beats anything on the wire.
- **If a spot is needed, Rome Odunze goes first.** He projects 8.2. His job was
  Week 11 WR depth, and a fill-in can be added in Week 10.
- **Week 5 is when a spot may be needed:** Mahomes is on bye (KC, Week 5). If
  Daniels isn't cleared by Wednesday, add a QB as a free agent Wednesday morning
  (Drake Maye, rank 10, still unowned) and drop Odunze.

---

## 5. My roster changes

None since Week 3 (SEA DEF and McConkey were logged there).

---

## 6. Strategy check

No change to `STRATEGY.md`. The 3-0 start, plus sworthy92 leaking points, puts the
**top-2 seed** goal on track.

---

## 7. Next week

**Week 5 byes (mine):** Mahomes (KC). **Watch:** Daniels' practice status and
Hall's.

### Actions — before Sunday 10-04

- [ ] **Move Brock Bowers into the FLEX slot, bench Breece Hall** (Out)
- [ ] Re-run `scripts/fantasy_report.py` — "Cannot play" should read 0
- [ ] Sunday morning: if McConkey is ruled out, nothing changes (he's on the bench)

### Actions — Wednesday 10-07 (after the waiver run)

- [ ] Daniels cleared? → start him in Week 5. Not cleared? → add Drake Maye (free agent), drop Odunze
- [ ] Hall status for Week 5; Bowers stays in FLEX if Hall is out
