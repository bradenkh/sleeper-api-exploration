# 2026 Season Strategy — "The Boys"

**Manager:** brdnhnsn (roster 3) · **Last updated:** 2026-09-08 (pre-Week 1)

This is the living game plan. It gets revised when the situation actually
changes, not every week. Week-by-week observations live in `weekly/`.

---

## 1. The situation in one paragraph

This is a 6-team keeper league that **autodrafted** — all 90 picks went in
2 minutes 51 seconds on a 10-second timer, so nobody actually chose their team.
The bot happened to hand me a coherent, running-back-heavy roster while handing
other managers genuinely broken ones. Four of the six managers have not logged
in since. Every team makes the playoffs, so the regular season only sets
seeding. My edge here is **attention**, not draft skill: I did not earn this
roster and I don't need to be clever to win — I need to set my lineup every
week and work the waiver wire while most of the league sleeps.

---

## 2. What I actually have

**Strength: running back.** Six startable backs — Jonathan Taylor, Derrick
Henry, Jeremiyah Love, Breece Hall, Travis Etienne, and (injured) Josh Jacobs.
That is more than I can start. Surplus at a scarce position is trade capital.

**Weakness: wide receiver depth.** Jaxon Smith-Njigba and Drake London are
genuinely good. Behind them, Mike Evans / Rome Odunze / Marvin Harrison Jr are
all roughly interchangeable mid-tier guys. If either starter misses time, the
drop-off is steep.

**Fragility: tight end.** Tyler Warren is my *only* tight end, TE is a required
starting slot, and he is out in Week 13 — one of my two worst weeks.

**Adequate: QB, K, DEF.** Jayden Daniels is a fine starter. Kicker and defense
are streamable and shouldn't consume attention.

---

## 3. The three levers, ranked by actual value

| Lever | Window | Why it matters |
|---|---|---|
| **Set the lineup weekly** | All season | Highest-value, lowest-effort. Already caught a starter producing zero. |
| **Waivers / free agents** | All season, $100 FAAB | Where in-season value actually comes from |
| **Trades** | Now → Week 11 only | The only tool that can fix WR; expires |

The order matters. Lineup discipline beats clever roster construction over a
full season, especially against dormant opponents.

---

## 4. Core strategy

### 4.1 Never start a broken player

The Week 1 audit found **Josh Jacobs in the starting lineup while listed `NA`
(not active) with a groin injury and sitting 4th on Green Bay's depth chart.**
That is a starting slot producing zero points. This check — cross-referencing
every starter against injury status *and* depth-chart position — is the single
most valuable thing to run each week and it takes two minutes.

### 4.2 Convert RB surplus into WR quality, before Week 11

The waiver wire **cannot** fix wide receiver. The best available WRs rank 61–75;
my WR3–5 rank 60–74. That's a lateral move. Only a trade fixes this.

**The identified opening:** sworthy92 has the strongest roster in the league but
by far its **worst quarterback** (Matthew Stafford, rank 66) — and four quality
receivers. Meanwhile **Drake Maye (rank 8)** is sitting unowned on waivers,
dropped by TuR7L3z after the autodraft gave him four quarterbacks.

The play: claim Maye for free, then offer a quarterback to sworthy92 for a
receiver. It uses an asset that cost nothing to fix the one hole I have.

Caveat honestly stated: this depends on sworthy92 logging in and accepting. If
they stay dormant, Maye is a bench-spot cost with no payoff. Roster is at 15/15
with **no IR slot**, so bench space is genuinely scarce.

### 4.3 Spend FAAB deliberately, not early

$100 for the whole season, no refill. Most league-winning pickups come from
Weeks 2–6 as injuries reshuffle roles. Guideline: don't exceed ~$25 on any
single player before Week 8 unless they're a clear every-week starter, and keep
$25+ in reserve for the Week 10–11 bye-week stocking.

### 4.4 Pre-load for Weeks 11 and 13

These are the two weeks the schedule breaks against me. Detail in §5. The fix is
boring and works: acquire the fill-ins in Week 9–10, *before* the crunch, when
they're cheap and available.

### 4.5 Exploit dormancy

Only TuR7L3z has made a roster move. Four managers are untouched since the
autodraft. Practically: good players are sitting unowned, and injured or
bye-week players are sitting in opponents' starting lineups every week. This
advantage decays if they wake up — so front-load the value capture.

---

## 5. The schedule problems

Byes derived from the NFL schedule (`data/byes_2026.json`). Full table in
`docs/league-reference.md`.

### Week 11 — 4 players out

Jaxon Smith-Njigba, Drake London (**both** starting WRs), Josh Jacobs, Harrison
Mevis. Losing both starting receivers in one week, at my thinnest position.

Note this is also the **trade deadline week**. A bad Week 11 score is a schedule
artifact — do not let it panic a lopsided deadline trade.

### Week 13 — 4 players out, and the hardest matchup

Jonathan Taylor, Derrick Henry, Breece Hall (three top RBs) **and** Tyler Warren
(my only TE). Both required RB slots and the required TE slot, in the same week —
against stalbot8, one of the league's two best rosters, who lose only two.

This is the likeliest loss on the schedule. Plan for it in Week 10.

### Where the schedule helps

I face **sworthy92 — the best team — only twice** (everyone else three times),
and both times they lose more players to byes than I do. Weeks 5, 6, and 10 all
tilt my way on bye math.

---

## 6. Keeper consideration (end of season)

One keeper allowed, costing draft capital next year (`draft_rounds: 3`). Not
urgent, but worth tracking: if a late-round pick or waiver claim breaks out,
that's the keeper — high production at a cheap draft cost. Note candidates in
the weekly logs as they emerge rather than trying to decide in December.

---

## 7. Open questions to revisit

- Does Josh Jacobs recover and reclaim the Green Bay job? If not, he's droppable
  given RB depth.
- Does sworthy92 ever log in? The entire trade plan depends on it. If they're
  dormant by ~Week 6, pivot to ajolson77 (WR-rich, RB-poor — a natural fit for
  a straight RB-for-WR swap).
- Is Tyler Warren real at TE, or does he need replacing outright?
- Do dormant managers wake up once they start losing? Track login proxies
  (transactions) weekly.

---

## 8. Action log

Recommendations and whether they were acted on. Outcomes get filled in later so
the advice can be graded honestly.

| Date | Action | Status | Outcome |
|---|---|---|---|
| 2026-09-08 | Bench Josh Jacobs (NA, groin, GB depth 4) for Week 1 | Recommended | — |
| 2026-09-08 | Drop Harrison Mevis → add Cam Little (K-JAX): better rank *and* Week 7 bye instead of Week 11 | Recommended | — |
| 2026-09-08 | Claim Drake Maye (rank 8, free) — conditional on pursuing the sworthy92 trade | Recommended, roster full | Blocked: 15/15, needs a drop |
| 2026-09-08 | Offer QB to sworthy92 for a WR | Not yet sent | — |
| By Week 10 | Add a backup TE with a non-Week-13 bye (Gadsden W7 / Kelce W5) | Scheduled | — |
