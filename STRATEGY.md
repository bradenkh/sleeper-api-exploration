# 2026 Season Strategy — "The Boys"

**Manager:** brdnhnsn (roster 3) · **Last updated:** 2026-09-08 (pre-Week 1, post-moves)

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

**Strength: running back.** Five startable backs — Jonathan Taylor (4), Derrick
Henry (7), Jeremiyah Love (15), Breece Hall (27), Travis Etienne (34). That is
more than I can start. Surplus at a scarce position is trade capital; Hall and
Etienne are the tradeable ones. (Josh Jacobs was dropped in Week 1 — see §8.)

**Weakness: wide receiver depth.** Jaxon Smith-Njigba and Drake London are
genuinely good. Behind them, Mike Evans / Rome Odunze / Marvin Harrison Jr are
all roughly interchangeable mid-tier guys. If either starter misses time, the
drop-off is steep.

**Was fragile, now covered: tight end.** Tyler Warren (48) is the starter and is
Questionable; Oronde Gadsden (83, bye 7) was added in Week 1 as insurance behind
him. TE is a required slot and Warren is out Week 13, so the backup matters.

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

**Better first target: TuR7L3z.** He is the only manager actually active, and he
rosters just **two** RBs (Gibbs, Barkley) against my five — a real hole he will
feel the moment either one misses time. Ask: Hall (27) or Etienne (34) for
**Ladd McConkey (35)**, upgrading my WR3 over Mike Evans (60). No dormant
counterparty required. Full per-manager playbook in `docs/trade-targets.md`.

### 4.3 Spend FAAB deliberately, not early

$100 for the whole season, no refill. Most league-winning pickups come from
Weeks 2–6 as injuries reshuffle roles. Guideline: don't exceed ~$25 on any
single player before Week 8 unless they're a clear every-week starter, and keep
$25+ in reserve for the Week 10–11 bye-week stocking.

### 4.4 Pre-load for Weeks 11 and 13

These are the two weeks the schedule breaks against me. Detail in §5. The fix is
boring and works: acquire the fill-ins in Week 9–10, *before* the crunch, when
they're cheap and available.

### 4.5 Exploit dormancy — and note that it is already decaying

**Updated 2026-09-13: three of five opponents are dormant, down from four.**
HntrRundas logged in on 09-12 and correctly replaced an injured Brock Bowers
with Mark Andrews — real management, not autodraft cleanup. TuR7L3z was already
active.

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

### Week 11 — 3 players out

Jaxon Smith-Njigba, Drake London (**both** starting WRs), Harrison Mevis.
Losing both starting receivers in one week, at my thinnest position. The pending
Mevis → Cam Little swap drops this to 2, since Little's bye is Week 7.

Note this is also the **trade deadline week**. A bad Week 11 score is a schedule
artifact — do not let it panic a lopsided deadline trade.

### Week 13 — 4 players out, and the hardest matchup

Jonathan Taylor, Derrick Henry, Breece Hall (three top RBs) **and** Tyler Warren.
Both required RB slots and the required TE slot, in the same week — against
stalbot8, one of the league's two best rosters, who lose only two.

**Partly solved already:** Gadsden (bye 7) now covers the TE slot. The RB hole
remains — Etienne and Love are the survivors, so a third startable RB is worth
having by Week 12. This is still the likeliest loss on the schedule.

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
— both cut by TuR7L3z on 09-07) sit in a 2-day waiver period and need a FAAB
claim. Check `/transactions` for a recent drop before assuming a player can be
grabbed on the spot. This also means a Sunday-morning injury fix only works for
never-rostered players, so bench insurance still earns its spot.
