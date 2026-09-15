# 2026 Season Strategy — "The Boys"

**Manager:** brdnhnsn (roster 3) · **Last updated:** 2026-09-15 (Week 1 final — won 158.76–153.46; waiver system
corrected to priority, see §4.3 and §9)

This is the living game plan. It gets revised when the situation actually
changes, not every week. Week-by-week observations live in `weekly/`.

---

## 1. The situation in one paragraph

This is a 6-team keeper league that **autodrafted** — all 90 picks went in
2 minutes 51 seconds on a 10-second timer, so nobody actually chose their team.
The bot happened to hand me a coherent, running-back-heavy roster while handing
other managers genuinely broken ones. Three of my five opponents still have not
logged in. Every team makes the playoffs, so the regular season only sets
seeding. My edge here is **attention**, not draft skill: I did not earn this
roster and I don't need to be clever to win — I need to set my lineup every
week and work the waiver wire while most of the league sleeps.

---

## 2. What I actually have

**Strength: running back — but the "surplus" is one player, not two.** Five
backs: Taylor (4), Henry (7), Love (15), Hall (27), Etienne (34). **Four of them
start** — Taylor and Henry at RB, Love and Etienne in the two FLEX slots. Only
**Hall** is genuine surplus.

Corrected 2026-09-13: this section previously claimed Hall *and* Etienne were
tradeable. Trading Etienne would force a WR ranked 60+ into a FLEX slot — a
downgrade, not consolidation. One tradeable back, not two.

**Weakness: wide receiver depth.** Jaxon Smith-Njigba and Drake London are
genuinely good. Behind them, Mike Evans / Rome Odunze / Marvin Harrison Jr are
all roughly interchangeable mid-tier guys. If either starter misses time, the
drop-off is steep.

**Fragile again: tight end.** Oronde Gadsden (83) is now my **only** TE — Warren
was dropped on 09-13 (a mistake, see §8). TE is a required slot, so this is a
single point of failure once more, and Gadsden's **Week 7 bye is now uncovered**.
Either reclaim Warren off waivers or add a second TE whose bye is not Week 7.

**Adequate QB; K and DEF are an active scoring opportunity, not an afterthought.**
Jayden Daniels is a fine starter. Kicker and defense should be **streamed on
matchup every week** — defenses in the week's five best matchups average ~10.4
points, more than a point per game above even a top-five season-long defense, and
streamed kickers grade out around K4. Two minutes a week for real points.

Corrected 2026-09-13: previously said these "shouldn't consume attention." That
was wrong and left points on the table.

---

## 3. The three levers, ranked by actual value

| Lever | Window | Why it matters |
|---|---|---|
| **Set the lineup weekly** | All season | Highest-value, lowest-effort. Won Week 1 on its own — see §8. |
| **Waivers / free agents** | All season, **priority order (no money)** | Where in-season value actually comes from |
| **Trades** | Now → Week 11 only | The only tool that can fix WR; expires |

The order matters. Lineup discipline beats clever roster construction over a
full season, especially against dormant opponents.

---

## 4. Core strategy

### 4.0 Run the report *after* roster moves, not just before

Week 1 lesson: dropping Tyler Warren left the **TE slot empty**, which scores
zero just as surely as starting an injured player. The report's "Cannot play"
column catches empty slots, but only if it is run after the change. Make the
last step of any roster move a re-run of `scripts/fantasy_report.py`.

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
with **no IR slot**, so bench space is genuinely scarce — which is why the spot
went to TE insurance instead in Week 1.

**Better first target: TuR7L3z.** One of two managers actually active, and he
rosters just **two** RBs (Gibbs, Barkley) against my five. Ask: **Hall (27)** for
**Ladd McConkey (35)**, upgrading my WR3 over Mike Evans (60). No dormant
counterparty required. Full per-manager playbook in `docs/trade-targets.md`.

**Pitch it as an upgrade, not a rescue.** Corrected 2026-09-13: I had him as
*desperate* for RBs. He is not — **Rhamondre Stevenson (58) is on the wire** and
he can patch for $1. Claiming he is stuck is both false and transparently so,
which costs credibility with an active manager.

The leverage that *is* real: the best free RB is rank 58, and **Hall is 27**. The
wire cannot replace a back that good. Sell the gap between 27 and 58, not a hole
he does not have.

**One tradeable back, not two** (see §2). And per the consolidation research,
don't trade depth away when the bench is already thin — right now the bench is
Hall plus three middling WRs, so Hall is the only piece that can leave.

### 4.3 Waivers are PRIORITY, not money — spend position deliberately

**Corrected 2026-09-15. This league does not use FAAB.** The league config carries
`waiver_budget: 100`, but it is inert: `waiver_type: 0` means rolling priority,
every roster has a `waiver_position` (1-6), `waiver_budget_used` is 0 for
everyone, and the completed Cam Little claim came back with `waiver_budget: []`
and no bid. There is no bid box in the app because there is nothing to bid.

Everything previously written here about bid tiers and budget percentages was
wrong for this league and has been removed.

**How it actually works.** Claims are ranked by `waiver_position`. Highest
position wins a contested player. **Winning a claim sends you to the back of the
line.** That is the entire cost — and it is a real one.

| Date | My waiver_position |
|---|---|
| 2026-09-08 (before the Cam Little claim) | **2nd** |
| after winning it | **6th — last** |

So the cost of that claim was not "$1". It was my second-best priority in the
league, spent on a kicker. It returned +11 points in Week 1 and fixed the Week 11
bye, so it was not a loss — but it was never free, and it was recommended as
though it were.

**The rules that follow from priority, not budget:**

1. **A claim costs position, so spend it on difference-makers.** A player I would
   actually start, not a streamer. Kickers and defenses are exactly what *not* to
   burn a high position on.
2. **While at the bottom, claim freely.** At position 6 there is nowhere to fall,
   so the marginal cost of a claim is zero. Bottom of the order is the time to be
   aggressive; near the top is the time to be picky.
3. **Free agents cost nothing.** A never-rostered player is an instant add that
   does not touch waiver position at all (confirmed: Gadsden). Only
   recently-dropped players go through the waiver period. Always check whether a
   target is actually on waivers before spending position — the report's §7
   labels this.
4. **There is no budget to hoard or exhaust**, so the FAAB-era worries about
   saving for byes or spending before Week 10 simply do not apply here.

### 4.3b Churn the bench — this league is shallow

Short-bench leagues reward activity over stockpiling: the wire holds startable
fill-ins that deeper leagues would have absorbed, so **middling depth on my bench
is worth less than the next add off the wire.** The test is simple — if I cannot
picture starting a player, he goes back.

Applied now: Evans (60), Odunze (64), and Harrison Jr (73) are exactly that
middling tier. Hall (27) is not — he is better than anything on the wire and is
the trade chip.

### 4.4 Pre-load for Weeks 11 and 13

These are the two weeks the schedule breaks against me. Detail in §5. The fix is
boring and works: acquire the fill-ins in Week 9–10, *before* the crunch, when
they're cheap and available.

### 4.4b Stream the defense off collision weeks

My defense scores by stopping opposing offenses, so starting it against **my own**
players is the one roster conflict with no offsetting upside. Houston collides
seven times:

| Week | Game | My player on the other side |
|---|---|---|
| 3 | HOU @ IND | Jonathan Taylor |
| 6 | HOU @ JAX | Cam Little |
| 9 | HOU @ LAC | Oronde Gadsden |
| 11 | IND @ HOU | Jonathan Taylor |
| 12 | BAL @ HOU | Derrick Henry |
| 14 | HOU @ WAS | Jayden Daniels |
| 15 | JAX @ HOU | Cam Little |

Fix is nearly free — 25 of 32 defenses are unowned, and §2 now says to stream on
matchup anyway. Weeks 3, 11 and 12 matter most (Taylor, Henry). Never bench a
starter to protect a defense; move the defense.

Two players of mine simply *sharing* a game (Taylor vs Henry in Week 1) is a much
weaker effect and happens **40 times this season** — unavoidable, and not worth
managing around.

### 4.4c Match variance to the opponent

Rostering players in the same game changes my score's **variance, not its
expected value**. Whether that is good depends on whether I am favored:

| Situation | Want | Opponents |
|---|---|---|
| Favored | **Low** variance — protect the edge | TuR7L3z |
| Even | neutral | HntrRundas, ajolson77 |
| Underdog | **High** variance — need an outlier | **sworthy92 (W5, W10), stalbot8 (W3, W8, W13)** |

In those five underdog weeks, prefer the boom/bust option (e.g. Harrison Jr) over
the safer floor. This is a tiebreaker between close options, never a reason to
bench a clearly better player.

### 4.5 Exploit dormancy — and note that it is already decaying

**Updated 2026-09-13: three of five opponents are dormant, down from four.**
HntrRundas logged in on 09-12 and correctly replaced an injured Brock Bowers
with Mark Andrews — real management, not autodraft cleanup. TuR7L3z was already
active.

Published shallow-league advice backs this up directly: *being one of the most
active managers is paramount* when benches are short and the wire is rich. The
core thesis is sound; the window is what's closing.

The advantage is still real (ajolson77 started an IR player in Week 1), but it
is shrinking. Two consequences:

1. **Front-load the trade approach.** The original plan waited for Weeks 5–8.
   The two active managers are also the two best trade targets, and an active
   manager is one who will actually see an offer. Do not wait for Week 8.
2. **Good free agents will start disappearing.** Drake Maye (8) has sat unowned
   for a week; that will not hold once more managers are looking.

---

## 5. The schedule problems

Byes derived from the NFL schedule (`data/byes_2026.json`). Full table in
`docs/league-reference.md`.

Recomputed 2026-09-13 against the current 14-man roster.

| Week | Out | Who |
|---|---|---|
| 7 | **3** | Jayden Daniels (QB), Cam Little (K), **Oronde Gadsden (TE)** |
| 8 | 3 | Mike Evans (WR), Travis Etienne (RB), HOU (DEF) |
| 10 | 1 | Rome Odunze (WR) |
| 11 | 2 | Jaxon Smith-Njigba, Drake London (**both** starting WRs) |
| 13 | 3 | Jonathan Taylor, Derrick Henry, Breece Hall (three top RBs) |
| 14 | 2 | Marvin Harrison Jr (WR), Jeremiyah Love (RB) |

### Week 7 — new problem, created by my own moves

Gadsden is my only TE and he is **on bye in Week 7**, alongside my QB and kicker.
Three required slots, one of them with no replacement on the roster.

The Warren drop traded a Week 13 TE hole for a Week 7 one. Fixing it is the same
job either way: get a second TE whose bye is not Week 7.

### Week 11 — 2 players out

Both starting WRs, at my thinnest position. Improved from 3 by the Cam Little
swap (his bye is Week 7, Mevis's was Week 11).

Also the **trade deadline week**. A bad Week 11 score is a schedule artifact —
do not let it panic a lopsided deadline trade.

### Week 13 — 3 RBs out, and the hardest matchup

Taylor, Henry, and Hall all out, against stalbot8 — one of the league's two best
rosters. Both required RB slots hit at once; Etienne and Love are the survivors,
so a third startable RB is worth having by Week 12. Gadsden does cover TE that
week. Still the likeliest loss on the schedule.

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

- **Do the dormant four ever wake up?** Everything rests on this. Track it via
  §4 of the weekly report (transactions are the only login proxy available).
- **Does sworthy92 log in?** The Maye/QB trade needs them. Re-evaluate ~Week 6.
  Note the fallback is **TuR7L3z**, not ajolson77 — see §4.2.
- **Is Tyler Warren real at TE?** Gadsden is behind him now, so this is a
  competition rather than a crisis.
- **Third startable RB for Week 13?** Taylor, Henry, and Hall are all out that
  week. Worth solving by Week 12.
- **Second TE, bye not Week 7?** Gadsden is the only TE and is out Week 7.
  Reclaiming Warren off waivers solves it (IND bye is Week 13, which Gadsden
  covers) — the two would cover each other cleanly.
- **Correction to carry forward:** ajolson77's RB room is *not* weak — Omarion
  Hampton is rank 12. Pitch him on WR redundancy (six receivers, starts three),
  never on RB need.

---

## 8. Action log

Recommendations and whether they were acted on. Outcomes get filled in later so
the advice can be graded honestly.

| Date | Action | Status | Outcome |
|---|---|---|---|
| 2026-09-08 | Bench Josh Jacobs (NA, groin, GB depth 4) for Week 1 | **DONE** — dropped him outright, Etienne into FLEX | Roster 14/15, one bench spot open |
| 2026-09-08 | Use open bench spot on **Oronde Gadsden (TE-LAC, bye 7)** — Warren is my only TE, Questionable now, and out Week 13 | **DONE** | Roster back to 15/15 |
| 2026-09-08 | Drop Harrison Mevis → add Cam Little (K-JAX): better rank *and* Week 7 bye instead of Week 11 | **DONE** — waiver claim won 09-09 | Week 11 bye exposure now 2, not 3 |
| 2026-09-13 | Dropped Tyler Warren, leaving the TE slot empty | **MISTAKE** | Warren had recovered (healthy, rank 48 vs Gadsden 83) and played that day. Fixed by starting Gadsden. Warren now on waivers. |
| 2026-09-08 | Claim Drake Maye (8) — deferred behind the TE fix | Deferred | Still unowned 09-08. Trading him *for a TE* was checked and rejected — see below. |
| Weeks 5–8 | Trade an RB (Hall 27 / Etienne 34) for a WR. Playbook in `docs/trade-targets.md` | Not yet sent | — |

**Note on the Jacobs drop:** dropping rather than benching was the right call
given no IR slot and five other RBs, but it means **MarShawn Lloyd (RB-GB, 102)**
— the back who took his job — is unowned. Not a priority while TE is fragile.

**Rejected: trading Drake Maye for a TE.** Checked against the rosters and it is
structurally blocked. Only TuR7L3z holds a spare TE, and he already rosters three
elite QBs, so Maye is worth nothing to him. Every other manager carries exactly
one TE and cannot trade it without emptying a required slot. Maye's real trade
path is a **WR from sworthy92**. Separately, TE scarcity is not a live risk:
156 TEs are unowned and ~14 are startable.

**"Unowned" is two states, and the API doesn't distinguish them.** Never-rostered
players (Gadsden) add instantly. Recently-dropped players (Cam Little, Drake Maye
— both cut by TuR7L3z on 09-07) sit in a 2-day waiver period and need a waiver
claim, which costs waiver position (see §4.3), not money. Check `/transactions` for a recent drop before assuming a player can be
grabbed on the spot. This also means a Sunday-morning injury fix only works for
never-rostered players, so bench insurance still earns its spot.

---

## 9. Revision log — strategy reviewed against published advice (2026-09-13)

Audited this plan against current fantasy strategy writing. Four things changed,
one was validated, one caveat was added. Sources at the bottom.

| § | Verdict | What changed |
|---|---|---|
| 4.3 FAAB | **THROWN OUT 09-15** | The whole section was moot: **this league uses waiver priority, not FAAB.** `waiver_budget: 100` is inert. Replaced with priority-cost rules. The bid-tier research below does not apply here. |
| 2 K/DEF | **Reworked** | "Shouldn't consume attention" was wrong. Streaming on matchup is worth ~1+ pt/game at DEF. |
| 2 RB surplus | **Corrected** | Claimed two tradeable backs; it is one. Four of five RBs start. |
| 4.2 trade pitch | **Corrected** | TuR7L3z is not desperate for RBs — Stevenson (58) is free on the wire. Sell the 27-vs-58 gap instead. |
| 4.3b bench | **Added** | Shallow leagues punish hoarding middling depth. Churn it. |
| 4.5 dormancy | **Validated** | "Being one of the most active managers is paramount" in short-bench leagues — the core thesis holds. |
| 4.2 consolidation | **Caveat added** | Trading depth for a star is right *with true surplus*; don't do it with a thin bench. |

**Sources:**
[4for4 — Ultimate Guide to Waiver Wire & FAAB Strategy](https://www.4for4.com/2025/preseason/ultimate-guide-waiver-wire-faab-strategy-2025) ·
[FantasyPros — FAAB Waiver Wire Strategy](https://www.fantasypros.com/2025/09/fantasy-football-faab-waiver-wire-strategy-advice/) ·
[FantasyPros — Shallow League Tips](https://www.fantasypros.com/2026/08/fantasy-football-strategy-4-tips-for-shallow-leagues-2026/) ·
[Athlon — Short-Bench Leagues](https://athlonsports.com/fantasy/fantasy-football-strategy-shallow-bench-leagues) ·
[DraftSharks — Streaming Defense](https://www.draftsharks.com/article/streaming-defense) ·
[SI — Positional Streaming Strategies](https://www.si.com/onsi/fantasy/nfl/fantasy-football-positional-streaming-strategies-redraft-leagues) ·
[FantraxHQ — In-Season Trade Strategy](https://fantraxhq.com/in-season-fantasy-football-trade-strategy-for-2026/)

**Standing caution 1 — verify league settings before importing advice.** The FAAB
rework above was researched carefully and was still useless, because I never
checked that this league actually runs FAAB. It does not. Read the settings *and*
a completed transaction before building strategy on a setting's presence.

**Standing caution 2:** this advice is written for 10–12 team leagues. In a 6-team
league the wire is far richer than any of these authors assume, which makes the
shallow-league and churn advice *more* applicable, and any "scarcity" claim
*less* so. Check scarcity against the actual wire before believing it.
