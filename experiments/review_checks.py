"""Post hoc checks added during the internal review (design in PROGRESS.md, "Review-stage checks").

Period controls and history-level uncertainty for the sub-period PSR result; one-family Holm for the real-data table;
market alpha, market-benchmarked DSR, signal-index sensitivity, studentized bootstrap and a walk-forward window
diagnostic for the case study. All post hoc. Output: results/review_checks.txt.

Run from the repository root:  .venv/bin/python experiments/review_checks.py
"""
import math

import numpy as np
from scipy.stats import binomtest, kurtosis, norm, skew

from pbo import paper_values as pv
from pbo import scenarios
from pbo.cscv import cscv
from pbo.french import ar_residuals, demean_by_period, load_market, load_returns
from pbo.psr_dsr import alpha_hac, dsr, psr_false_positive, psr_z, sharpe_diff, spa_pvalue
from pbo.reporting import format_rate, save_results
from pbo.strategies import crossover_panel

Q, S, LEVEL = pv.PERIODS_PER_YEAR, pv.PBO_S16, pv.MINTRL_EX_CONFIDENCE
T, SPLIT, LAGS, COST, SELECTED = 1248, 19990101, 11, 0.0005, (15, 225)
SETTINGS = [(f, s) for f in range(5, 55, 5) for s in range(25, 275, 25) if f < s]   # step 5 design
SEED = 20261116


def psr_flags(rng, panel, block, datasets):
    """PSR(0) > LEVEL on a uniformly drawn column of each block-bootstrapped dataset."""
    flags = []
    for _ in range(datasets):
        x = scenarios.block_bootstrap(rng, panel, T, block)[:, rng.integers(panel.shape[1])]
        flags.append(norm.cdf(psr_z(x.mean() / x.std(), 0.0, T, skew(x), kurtosis(x, fisher=False))) > LEVEL)
    return np.array(flags)


def predicted(panel, block):
    return psr_false_positive(scenarios.block_bootstrap_factor(panel, block, T), T, LEVEL).mean()


def holm(pvalues):
    order, m, out, running = np.argsort(pvalues), len(pvalues), np.empty(len(pvalues)), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvalues[i]))
        out[i] = running
    return out


def main():
    streams = iter([np.random.default_rng(child) for child in np.random.SeedSequence(SEED).spawn(9)])
    lines = ["Post hoc review checks (design: PROGRESS.md, 'Review-stage checks'). PSR rates: exact 95% CI.", ""]

    dates, data, _ = load_returns()
    early, late = demean_by_period(dates, data, SPLIT)
    lines.append(f"1. Period controls, split {SPLIT}, T = {T}")
    for name, panel in (("1971-1998", early), ("1999-2026", late)):
        lines.append(f"  {name}, L = 1 (dependence removed): {format_rate(psr_flags(next(streams), panel, 1, 4000))}")
        resid = ar_residuals(panel, 5)
        lines.append(f"  {name}, AR(5) residuals, L = 20: {format_rate(psr_flags(next(streams), resid, 20, 4000))}")

    lines += ["", "2. History-level uncertainty of the predicted rate at L = 20 (200 resamples, 250-day blocks)"]
    rng = next(streams)
    for name, panel in (("1971-1998", early), ("1999-2026", late)):
        values = []
        for _ in range(200):
            resampled = scenarios.block_bootstrap(rng, panel, len(panel), 250)
            values.append(predicted(resampled - resampled.mean(axis=0), 20))
        low, high = np.percentile(values, [2.5, 97.5])
        lines.append(f"  {name}: point {predicted(panel, 20):.4f}; 2.5-97.5% [{low:.4f}, {high:.4f}]; "
                     f"share below 0.05: {np.mean(np.array(values) < 0.05):.3f}")

    lines += ["", "3. Split-date sensitivity of the predicted rate at L = 20"]
    for split in (19930101, 19960101, 20010101, 20040101):
        e, l = demean_by_period(dates, data, split)
        lines.append(f"  split {split}: early {predicted(e, 20):.4f}, late {predicted(l, 20):.4f}")

    rows = [("full L=1", 107), ("full L=5", 103), ("full L=20", 125), ("full L=60", 125), ("replicate L=20", 118),
            ("replicate L=60", 120), ("1971-1998", 167), ("1999-2026", 77)]       # counts out of 2000, results/*.txt
    exact = np.array([binomtest(k, 2000, 0.05).pvalue for _, k in rows])
    lines += ["", "4. Holm over the eight real-data PSR rows as one family"]
    lines += [f"  {name}: {k}/2000, exact p {p:.4f}, Holm p {h:.4f}" for (name, k), p, h in zip(rows, exact, holm(exact))]

    _, mkt, rf = load_market()
    start, m = crossover_panel(np.cumprod(1 + mkt + rf), mkt, SETTINGS, COST, S)
    market = mkt[start:]
    k = SETTINGS.index(SELECTED)
    alphas = [alpha_hac(m[:, j], market, LAGS) for j in range(len(SETTINGS))]
    tstats = np.array([a / se for a, _, se in alphas])
    a, b, se = alphas[k]
    lines += ["", f"5. Market alpha, OLS with Bartlett HAC ({LAGS} lags), 5 bps",
              f"  15/225: beta {b:.3f}, alpha {a * Q * 100:.2f}%/yr, t {a / se:.2f}, one-sided p {norm.sf(a / se):.4f}",
              f"  largest t {tstats.max():.2f} ({SETTINGS[int(tstats.argmax())]}); t > 1.645: {(tstats > 1.645).sum()} of 93; "
              f"t > {norm.isf(0.05 / 93):.3f} (Bonferroni): {(tstats > norm.isf(0.05 / 93)).sum()} of 93"]

    excess = m - market[:, None]
    sharpes = excess.mean(axis=0) / excess.std(axis=0)
    x = excess[:, k]
    lines += ["", "6. DSR with the market as benchmark (selected setting minus market; V from the 93 differences; N = 93)",
              f"  DSR {dsr(sharpes[k], len(x), skew(x), kurtosis(x, fisher=False), 93, sharpes.var(ddof=1)):.4f}"]

    s2, m2 = crossover_panel(np.cumprod(1 + mkt), mkt, SETTINGS, COST, S)
    mk2 = mkt[s2:]
    sh2 = m2.mean(axis=0) / m2.std(axis=0)
    best = int(np.argmax(sh2))
    d, sd = (v * math.sqrt(Q) for v in sharpe_diff(m2[:, best], mk2, LAGS))
    lines += ["", "7. Signal on the excess-return index cumprod(1 + Mkt-RF), 5 bps",
              f"  best {SETTINGS[best]}: Sharpe {sh2[best] * math.sqrt(Q):.3f}; {(sh2 > mk2.mean() / mk2.std()).sum()} of 93 "
              f"above market; PBO {cscv(m2, S)[0]:.3f}; difference {d:+.3f} (se {sd:.3f}, z {d / sd:.2f}); "
              f"15/225 Sharpe {sh2[k] * math.sqrt(Q):.3f}"]

    y = m[:, k]
    d0, s0 = sharpe_diff(y, market, LAGS)
    lines += ["", f"8. Studentized stationary bootstrap, 15/225 vs market, 1000 resamples (t observed {d0 / s0:.3f}, "
                  f"Normal p {norm.sf(d0 / s0):.4f})"]
    rng = next(streams)
    for block in (20, 250):
        stats = []
        for _ in range(1000):
            idx = scenarios.stationary_bootstrap_indices(rng, len(y), len(y), block)
            db, sb = sharpe_diff(y[idx], market[idx], LAGS)
            stats.append((db - d0) / sb)
        lines.append(f"  mean block {block}: p {np.mean(np.array(stats) >= d0 / s0):.3f}")

    days = load_market()[0][start:]
    window = days // 10000 >= days[0] // 10000 + 10
    fixed = m[window].mean(axis=0) / m[window].std(axis=0) * math.sqrt(Q)
    mw = market[window]
    market_sharpe = mw.mean() / mw.std() * math.sqrt(Q)
    lines += ["", f"9. Walk-forward window ({window.sum()} days), fixed settings held throughout (hindsight diagnostic)",
              f"  market {market_sharpe:.3f}; fixed 15/225 {fixed[k]:.3f}; median of 93 {np.median(fixed):.3f}; "
              f"{(fixed > market_sharpe).sum()} of 93 above the market"]

    def alphas_of(rows):
        xs, ys = market[rows], m[rows]
        beta = ((ys - ys.mean(axis=0)) * (xs - xs.mean())[:, None]).mean(axis=0) / xs.var()
        return ys.mean(axis=0) - beta * xs.mean()

    def alpha_spa(rng, block):
        boot = np.array([alphas_of(scenarios.stationary_bootstrap_indices(rng, len(market), len(market), block))
                         for _ in range(2000)])
        return spa_pvalue(alphas_of(slice(None)), boot, len(market))

    statistic, p = alpha_spa(next(streams), 20)
    lines += ["", "10. Hansen consistent SPA on the 93 market alphas (stationary bootstrap, mean block 20, 2000 resamples)",
              f"  statistic {statistic:.3f}, p-value {p:.4f}",
              "", "11. Sensitivity of item 10 (2000 resamples each)"]
    extra = np.random.SeedSequence(SEED + 1).spawn(4)
    for child, block in zip(extra, (5, 60, 250, 20)):
        statistic, p = alpha_spa(np.random.default_rng(child), block)
        lines.append(f"  mean block {block}{' (second seed)' if block == 20 else ''}: statistic {statistic:.3f}, p-value {p:.4f}")
    print("\n".join(lines))
    save_results("review_checks", lines)


if __name__ == "__main__":
    main()
