# Week 1 — opened 2026-09-08, updated 2026-09-13

**Record:** 0-0 · **Opponent:** TuR7L3z · **Status:** leading 26.20 — 9.00 with
Sunday's games still to play

Baseline entry for the season, started pre-kickoff and updated as Week 1 played
out. Later weeks diff against this.

---

## 1. Result

In progress. Through the Thursday/Friday openers:

| | Score |
|---|---|
| Me | **26.20** |
| TuR7L3z | 9.00 |

All 26.2 came from Jaxon Smith-Njigba in the 09-09 opener. Everyone else played
or plays on 09-13.

Mike Evans scored 16.9 **on the bench** — not an avoidable miss, since starting
him would have meant benching London or a FLEX back before any had played.

---

## 2. Lineup audit — the important one

| Starter | Pos | Status | Depth | Flag? |
|---|---|---|---|---|
| Jayden Daniels | QB-WAS | — | 1 | ok |
| Jonathan Taylor | RB-IND | — | 1 | ok |
| Derrick Henry | RB-BAL | — | 1 | ok |
| Jaxon Smith-Njigba | WR-SEA | — | 1 | ok |
| Drake London | WR-ATL | — | 1 | ok |
| Tyler Warren | TE-IND | Questionable (groin) | 1 | monitor |
| Jeremiyah Love | RB-ARI | Questionable (ankle) | 1 | monitor |
| **Josh Jacobs** | **RB-GB** | **NA (groin)** | **4** | **🚨 BENCH** |
| Harrison Mevis | K-LAR | — | — | replace (see §4) |
| Houston | DEF-HOU | — | — | ok |

### Problems found

**Josh Jacobs is a starter and cannot produce.** Listed `NA` (not active) with a
groin injury, and he has fallen to **4th on Green Bay's running back depth
chart** behind MarShawn Lloyd, Chris Brooks, and Kaleb Johnson — all three of
whom are unowned free agents. He was drafted as a stud (rank 20 overall), which
is exactly why the autodraft slotted him into the lineup and why this is easy to
miss.

**Resolved:** dropped him outright and moved Travis Etienne into the FLEX.
Dropping beat benching because there is no IR slot and five other RBs made an
injured 4th-stringer a luxury. See §5.

The other "Questionable" tags (Odunze, Warren, Love, Evans, Hall) are all
players sitting **1st on their depth chart** — normal Week 1 noise, not
actionable.

### Bye-week conflicts

None. There are no byes in Weeks 1–4.

---

## 3. What the other managers did

| Manager | Moves | Active? |
|---|---|---|
| **TuR7L3z** | 3 free-agent moves (09-07) | **active** |
| **HntrRundas** | 1 move (09-12): +Mark Andrews / −Brock Bowers | **active — woke up** |
| ajolson77 | none | dormant |
| sworthy92 | none | dormant |
| stalbot8 | none | dormant |

**Dormant count: 3 of 5** — down from 4. HntrRundas logged in on 09-12 and
correctly reacted to Brock Bowers being ruled `Out` by replacing him with Mark
Andrews. That is real management, not a cleanup of autodraft damage.

**This matters for the trade timeline.** The edge assumed four dormant
opponents; it is now three, and the two active managers (TuR7L3z, HntrRundas)
are the two best trade targets. Front-load the approach rather than waiting for
Weeks 5–8 as originally planned — see `docs/trade-targets.md`.

**Dormant managers are already leaking points:** ajolson77 started A.J. Brown
(on IR, a certain zero) in Week 1.

TuR7L3z logged in ~25 minutes after the draft ended and cleaned up the worst of
the bot damage:

| Added | Dropped |
|---|---|
| Jayden Reed (WR-GB) | BUF DEF |
| Khalil Shakir (WR-BUF) | Cam Little (K-JAX) |
| Devaughn Vele (WR-NO) | **Drake Maye (QB-NE)** |

He dumped a spare kicker, spare defense, and his 4th QB for three receivers.
Notably he **did not fix his running back problem** — still only Gibbs and
Barkley — and still carries 3 QBs and 2 kickers.

**Trades league-wide: 0.** Traded draft picks: 0.

---

## 4. Waiver wire

**Waiver system:** rolling **priority**, not FAAB (confirmed 09-15 — see
`docs/api-notes.md`). My `waiver_position` was **2nd** before the Cam Little
claim and **6th (last)** after winning it. Claims cost position, not money.

### Best available, by position

Only 90 of ~660 relevant players are rostered in this 6-team league, so the wire
is unusually rich.

| Pos | Best available | Rank | Bye |
|---|---|---|---|
| **QB** | **Drake Maye (NE)** | **8** | 11 |
| QB | Justin Herbert (LAC) | 33 | 7 |
| RB | Rhamondre Stevenson (NE) | 58 | 11 |
| WR | Carnell Tate (TEN) | 61 | 9 |
| WR | Christian Watson (GB) | 64 | 11 |
| TE | Tucker Kraft (GB) | 65 | 11 |
| TE | Oronde Gadsden (LAC) | 83 | 7 |
| K | Cam Little (JAX) | 134 | 7 |

Also: **25 of 32 defenses are unowned**, so DEF is fully streamable.

### Decisions

**Do now — free upgrade, no roster spot needed:**
> Drop Harrison Mevis → add **Cam Little (K-JAX)**. Better rank (134 vs 154)
> *and* a Week 7 bye instead of Week 11, which is one of my two crunch weeks.
> (Ironically, TuR7L3z just dropped him.)
>
> **Retrospect (09-15): this was recommended as costing "$1" and it was not.**
> The league uses waiver priority, not FAAB — the claim spent my 2nd-best
> waiver position in the league on a kicker and dropped me to last. It returned
> +11 points in Week 1 (12.00 vs Mevis's 1.00) and fixed the Week 11 bye, so it
> paid off, but the cost was misstated. Never spend a high waiver position on a
> streamer again.

**Deferred — Drake Maye (8), still unowned:**
> The best player on the wire, but a backup QB cannot be started. His only value
> is as a trade chip, and the bench spot went to TE insurance instead. Revisit
> once Warren's status settles.
>
> Checked and rejected: trading Maye for a TE later. Only TuR7L3z holds a spare
> TE, and he already has three elite QBs, so Maye is worth nothing to him. Every
> other manager rosters exactly one TE and cannot give it up. Maye's real trade
> path is **WR from sworthy92**, not TE.

**Done — TE insurance:**
> Added Oronde Gadsden (bye 7). Originally scheduled for Week 10, pulled forward
> because Warren is Questionable now. Note the justification is *this week's
> risk*, not scarcity: 156 TEs are unowned and ~14 are startable, so the position
> will not dry up in a 6-team league.

---

## 5. My roster changes

| In | Out | Reason |
|---|---|---|
| — | Josh Jacobs (RB-GB) | `NA` with groin injury, 4th on GB depth chart. Dropped rather than benched: no IR slot, and five other RBs made him a luxury. |
| Oronde Gadsden (TE-LAC) | — | Insurance behind Tyler Warren, who is my only TE, Questionable this week, and on bye Week 13. Bye week 7 avoids both crunch weeks. |

| Cam Little (K-JAX) | Harrison Mevis (K-LAR) | **Waiver claim won 09-09.** Better rank and, more importantly, a Week 7 bye instead of Week 11 — one of my two crunch weeks. |
| — | Tyler Warren (TE-IND) | Dropped 09-13 04:13. **See the post-mortem below — this looks like a mistake.** |

Travis Etienne moved into the vacated FLEX slot. Roster now **14/15**.

### Post-mortem: dropping Tyler Warren

Dropped him hours before Indianapolis played on 09-13, which left the **TE slot
empty** — an empty starting slot scores zero. Caught by the report's "Cannot
play" column; fixed by moving Gadsden off the bench into the slot.

Two things make this a genuine loss rather than a wash:

1. **Warren was healthy again.** The groin injury cleared — `injury_status` null,
   still 1st on the IND depth chart. The reason he was worth insuring against had
   already gone away.
2. **He outranks his replacement**, 48 to Gadsden's 83, and he played that day.

He is now unowned but **on waivers** (I dropped him, so the 2-day clear applies),
meaning a waiver claim is needed and it cannot help in Week 1 regardless.

**Process lesson:** run `scripts/fantasy_report.py` *after* making roster moves,
not just before. §2's "Cannot play" column flags an empty slot instantly.

### "Unowned" means two different things

The Gadsden pickup posted as `free_agent` / `complete` with no waiver period —
he was never rostered, so he was a true free agent.

**But Cam Little and Drake Maye are not.** TuR7L3z dropped both on 09-07, which
puts them in the 2-day waiver period: they require a waiver claim that processes
on the waiver run, not an instant add. The API shows all three simply as "unowned".

Practical rule: before assuming an unowned player can be grabbed on the spot,
check whether they appear in a recent `drops`. Detail in `docs/api-notes.md`.

### Note on the drop

Dropping Jacobs was right on the roster math, but it does put **MarShawn Lloyd
(RB-GB, rank 102)** — the back who leapfrogged him — on the open market. Not
worth chasing while TE is a single point of failure, but worth noting if the RB
room thins out.

### Week 1 game timing

Most starters play Sunday 09-13, but two lock earlier:

| Player | Team | Game |
|---|---|---|
| Jaxon Smith-Njigba | SEA | **2026-09-09** (season opener, NE @ SEA) |
| Harrison Mevis | LAR | **2026-09-10** (SF @ LAR) |

Original note said the Mevis→Little swap had to land before 09-10. That assumed
an instant add — it is actually a **waiver claim** (Little was dropped 09-07), so
the processing time is not mine to control. Submit the claim and let it run.

---

## 6. Strategy check

`STRATEGY.md` written fresh this week — it *is* the plan, no changes to log.

### The central play, restated

Waivers **cannot** fix wide receiver — best available WRs rank 61–75, my WR3–5
rank 60–74. Lateral. Only a trade fixes it, and trades die at Week 11.

**sworthy92** has the league's best roster and its **worst QB** (Stafford, rank
66), plus four quality WRs. Drake Maye (rank 8) is free on waivers. Claim Maye,
offer a QB to sworthy92 for a receiver.

**Risk, stated plainly:** sworthy92 is dormant. If they never log in, this plan
has no counterparty.

**Better first target: TuR7L3z.** He is the only active manager and rosters just
**two** RBs (Gibbs, Barkley) against my five. Ask: Hall (27) or Etienne (34) for
Ladd McConkey (35), upgrading my WR3 over Mike Evans (60). Full playbook in
`docs/trade-targets.md`.

Correction to an earlier read: ajolson77's RB room is **not** weak — Omarion
Hampton is rank 12, a real RB2. Pitch him on WR *redundancy* (six receivers,
starts three), not need.

### Open questions

- **Does anyone wake up?** Four of five opponents have made zero moves. The whole
  edge rests on this. Watch §4 of the report each week.
- **sworthy92 responsive?** The Maye/QB trade depends on it. Re-evaluate ~Week 6.
- **Tyler Warren at TE:** Questionable, and now backed up by Gadsden. If Warren
  underperforms outright, Gadsden or a better free-agent TE takes the job.
- **MarShawn Lloyd (RB-GB, 102):** unowned, inherited Jacobs's carries. Only
  relevant if my RB room thins.

**Keeper candidates:** none yet — nothing has been played.

---

## 7. Next week

**Week 2 opponent:** HntrRundas · **My byes:** 0 · **Their byes:** 0

### Actions before Week 1 kickoff

- [x] **Remove Josh Jacobs from the lineup** — dropped outright; Etienne in FLEX
- [x] **Add a backup TE** — Oronde Gadsden (bye 7) added; roster 15/15
- [x] **Waiver claim for Cam Little** — won 09-09, Mevis dropped
- [ ] **URGENT 09-13:** TE slot is **empty** after the Warren drop. Move Oronde
      Gadsden off the bench into it. ARI @ LAC is still `pre_game`.
- [ ] **Consider:** waiver claim to bring Tyler Warren back (healthy, rank 48 vs
      Gadsden 83). Roster is 14/15 so no drop needed. ~$2–3. Will not help Week 1.
- [ ] Do **not** send trade offers yet — nothing has happened to argue from.
      Playbook and timing in `docs/trade-targets.md`.
