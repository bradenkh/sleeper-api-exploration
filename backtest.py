"""Backtest Sleeper's weekly projections against actual results.

Our optimizer trusts Sleeper's projections (scored by the league's rules). This
checks whether that trust is earned: for each completed week it scores every
player's *projection* and their *actual* result with the same scoring weights,
then reports how close they were and -- the part that actually matters for
lineup decisions -- how often the higher-projected of two players really did
outscore the other.

It is fully self-contained (Sleeper gives us both projections and actuals; no
nflverse / pandas / external model needed) so it validates the exact numbers the
optimizer consumes, not some other source's projections.

Key metrics, overall and by position:
  * corr   -- Pearson correlation of projected vs actual (higher = better).
  * MAE    -- mean absolute error in points (lower = better).
  * bias   -- mean (projected - actual): + = Sleeper over-projects.
  * s/s%   -- start/sit accuracy: over all same-position player pairs, how often
              the higher projection had the higher actual score. 50% = coin flip;
              this is the number that says whether the tool helps you choose.
  * vs base-- projection MAE compared with a naive "season-to-date average"
              baseline, so we see whether projections beat just guessing form.

Sample size matters: run it on a COMPLETED season (e.g. 2025, weeks 1-17) for a
real read. On the in-progress season only a week or two exist.

Usage:
    python backtest.py [season] [--weeks A-B] [--min PTS]
"""
from __future__ import annotations

import sys
from collections import defaultdict

import sleeper_client as api

LEAGUE_ID = "1401765585515237376"  # scoring weights come from here


def score(stats, scoring):
    return sum(w * stats.get(k, 0) for k, w in scoring.items())


def pearson(pairs):
    n = len(pairs)
    if n < 2:
        return None
    sx = sum(x for x, _ in pairs); sy = sum(y for _, y in pairs)
    mx, my = sx / n, sy / n
    num = sum((x - mx) * (y - my) for x, y in pairs)
    dx = sum((x - mx) ** 2 for x, _ in pairs) ** 0.5
    dy = sum((y - my) ** 2 for _, y in pairs) ** 0.5
    return num / (dx * dy) if dx and dy else None


def startsit_accuracy(rows):
    """Over all pairs in `rows` [(proj, actual)], how often proj order == actual
    order. Ties (in either dimension) are skipped."""
    correct = total = 0
    for i in range(len(rows)):
        pi, ai = rows[i]
        for j in range(i + 1, len(rows)):
            pj, aj = rows[j]
            if pi == pj or ai == aj:
                continue
            total += 1
            if (pi > pj) == (ai > aj):
                correct += 1
    return (correct / total, total) if total else (None, 0)


def main(argv) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    state = api.get_nfl_state() or {}
    season = args[0] if args else state.get("season", "2025")

    weeks = None
    min_pts = 5.0
    for a in argv:
        if a.startswith("--weeks"):
            spec = a.split("=", 1)[1] if "=" in a else argv[argv.index(a) + 1]
            lo, hi = (spec.split("-") + [spec])[:2]
            weeks = list(range(int(lo), int(hi) + 1))
        if a.startswith("--min"):
            min_pts = float(a.split("=", 1)[1] if "=" in a else argv[argv.index(a) + 1])
    if weeks is None:
        # completed weeks: whole season if it's a past one, else up to last week.
        last = 17 if str(season) < str(state.get("season", season)) else (state.get("week", 1) - 1)
        weeks = list(range(1, max(1, last) + 1))

    scoring = api.get_league(LEAGUE_ID)["scoring_settings"]
    players = api.get_players()

    def pos_of(pid):
        return (players.get(str(pid), {}) or {}).get("position")

    # collect (proj, actual) per player per week, plus actuals history for baseline
    per_pos = defaultdict(list)          # pos -> [(proj, actual)]
    overall = []                          # [(proj, actual)]
    ss_by_week_pos = defaultdict(list)    # (week,pos) -> [(proj, actual)] for start/sit
    actual_hist = defaultdict(list)       # pid -> [actual pts, in week order]
    proj_err, base_err = [], []           # abs errors for MAE-vs-baseline

    for wk in weeks:
        proj = {str(p["player_id"]): (p.get("stats") or {}) for p in api.get_projections(season, wk)}
        act = {str(p["player_id"]): (p.get("stats") or {}) for p in api.get_stats(season, wk)}
        for pid, pstats in proj.items():
            pos = pos_of(pid)
            if pos not in api.DEFAULT_POSITIONS:
                continue
            pj = score(pstats, scoring)
            if pj < min_pts:            # only judge startable-relevant projections
                continue
            if pid not in act:
                continue
            ac = score(act[pid], scoring)
            overall.append((pj, ac))
            per_pos[pos].append((pj, ac))
            ss_by_week_pos[(wk, pos)].append((pj, ac))
            # baseline: this player's mean actual over prior weeks
            hist = actual_hist[pid]
            if hist:
                base = sum(hist) / len(hist)
                base_err.append(abs(base - ac))
                proj_err.append(abs(pj - ac))
        # after using history for baseline, record this week's actuals
        for pid, astats in act.items():
            if pos_of(pid) in api.DEFAULT_POSITIONS:
                actual_hist[pid].append(score(astats, scoring))

    if not overall:
        print(f"No completed data for {season} weeks {weeks[0]}-{weeks[-1]}. "
              "Try a past season, e.g. `python backtest.py 2025`.")
        return 1

    def mae(rows):
        return sum(abs(p - a) for p, a in rows) / len(rows)

    def rmse(rows):
        return (sum((p - a) ** 2 for p, a in rows) / len(rows)) ** 0.5

    def bias(rows):
        return sum(p - a for p, a in rows) / len(rows)

    print(f"Backtest -- Sleeper projections vs actuals, {season} weeks "
          f"{weeks[0]}-{weeks[-1]} (startable-relevant: projected >= {min_pts:g})")
    print("=" * 70)
    print(f"\nOVERALL  (n={len(overall)})")
    print(f"  corr {pearson(overall):.3f} | MAE {mae(overall):.2f} | "
          f"RMSE {rmse(overall):.2f} | bias {bias(overall):+.2f}")

    print(f"\nBY POSITION")
    print(f"  {'pos':4} {'n':>5} {'corr':>6} {'MAE':>6} {'bias':>6}")
    for pos in api.DEFAULT_POSITIONS:
        rows = per_pos.get(pos)
        if not rows:
            continue
        c = pearson(rows)
        print(f"  {pos:4} {len(rows):>5} {(f'{c:.3f}' if c is not None else '  -'):>6} "
              f"{mae(rows):>6.2f} {bias(rows):>+6.2f}")

    # start/sit accuracy: pool pairwise results across weeks within a position.
    print(f"\nSTART/SIT ACCURACY (higher projection actually outscored the other)")
    for pos in api.DEFAULT_POSITIONS:
        corr = tot = 0
        for (wk, p), rows in ss_by_week_pos.items():
            if p != pos:
                continue
            acc, n = startsit_accuracy(rows)
            if n:
                corr += acc * n; tot += n
        if tot:
            print(f"  {pos:4} {corr / tot * 100:5.1f}%  ({tot} pairs)")

    if proj_err:
        pm = sum(proj_err) / len(proj_err)
        bm = sum(base_err) / len(base_err)
        verdict = "projections BEAT the baseline" if pm < bm else "projections LOSE to the baseline"
        print(f"\nVS NAIVE BASELINE (season-to-date average), n={len(proj_err)}")
        print(f"  projection MAE {pm:.2f}  vs  baseline MAE {bm:.2f}  ->  {verdict}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
