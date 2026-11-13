"""Case-study checks after the panel review: execution lag, turnover, sub-periods, DSR break-even N, Hansen SPA.

Design: PROGRESS.md, "Planned runs", recorded before this run. Exploratory: the owner waived predictions.
Step 5 grid, days and 5 bps cost unless stated. Our choices: 1-day extra lag, split 1999-01-01, SPA with a
stationary bootstrap (mean block 20 days, 2000 resamples), seed.

Run from the repository root:  .venv/bin/python experiments/case_study_checks.py
"""
import math

import numpy as np
from scipy.optimize import brentq
from scipy.stats import kurtosis, norm, skew

from pbo import paper_values as pv
from pbo.cscv import cscv
from pbo.french import load_market
from pbo.psr_dsr import dsr, sharpe_diff, spa_sharpe
from pbo.reporting import save_results
from pbo.scenarios import stationary_bootstrap_indices
from pbo.strategies import crossover_panel, ma_crossover

Q, S, LEVEL = pv.PERIODS_PER_YEAR, pv.PBO_S16, pv.MINTRL_EX_CONFIDENCE
SETTINGS = [(f, s) for f in range(5, 55, 5) for s in range(25, 275, 25) if f < s]   # step 5 design
COST, SELECTED, LAGS = 0.0005, (15, 225), 11                                      # step 5 main cost, winner, lags
SPLIT, MEAN_BLOCK, RESAMPLES, SEED = 19990101, 20, 2000, 20261115


def paired(x, y):
    d, se = (v * math.sqrt(Q) for v in sharpe_diff(x, y, LAGS))
    return f"difference {d:+.3f} (se {se:.3f}, one-sided p {norm.sf(d / se):.4f})"


def main():
    dates, mkt_rf, rf = load_market()
    prices = np.cumprod(1 + mkt_rf + rf)
    lines = [f"Case-study checks, 5 bps unless stated, paired tests with {LAGS} Bartlett lags, annualized.", ""]

    # 1. One extra day of execution lag
    lines.append("1. Execution lag: position set by the signal two closes earlier (baseline: one)")
    for delay in (1, 2):
        start, m = crossover_panel(prices, mkt_rf, SETTINGS, COST, S, delay)
        market = mkt_rf[start:]
        sharpes = m.mean(axis=0) / m.std(axis=0)
        best = int(np.argmax(sharpes))
        x = m[:, best]
        d = dsr(sharpes[best], len(x), skew(x), kurtosis(x, fisher=False), len(SETTINGS), sharpes.var(ddof=1))
        lines.append(f"  delay {delay}: best {SETTINGS[best][0]}/{SETTINGS[best][1]} Sharpe {sharpes[best] * math.sqrt(Q):.3f} "
                     f"(market {market.mean() / market.std() * math.sqrt(Q):.3f}), PBO {cscv(m, S)[0]:.3f}, DSR {d:.4f}, "
                     f"vs market {paired(x, market)}; {np.sum(sharpes > market.mean() / market.std())} of 93 above market")
        if delay == 1:
            base_start, base_m, base_market, base_sharpes = start, m, market, sharpes

    # 2. Turnover and break-even cost of the selected setting
    position = ma_crossover(prices, np.ones(len(prices)), *SELECTED, 0.0)[base_start:]
    changes = np.abs(np.diff(position, prepend=ma_crossover(prices, np.ones(len(prices)), *SELECTED, 0.0)[base_start - 1]))
    years = len(position) / Q
    target = base_market.mean() / base_market.std()

    def excess_sharpe(cost):
        r = ma_crossover(prices, mkt_rf, *SELECTED, cost)[base_start:]
        return r.mean() / r.std() - target

    lines += ["", "2. Turnover and break-even cost, setting 15/225",
              f"  changes in position: {int(changes.sum())} over {years:.1f} years = {changes.sum() / years:.2f} per year",
              f"  cost per change at which its Sharpe equals the market's: {brentq(excess_sharpe, 0.0, 0.5) * 1e4:.0f} bps"]

    # 3. Sub-periods
    x, kept = base_m[:, SETTINGS.index(SELECTED)], dates[base_start:]
    lines += ["", f"3. Setting 15/225 vs market by period (split {SPLIT})"]
    for label, mask in (("1972-1998", kept < SPLIT), ("1999-2026", kept >= SPLIT)):
        xs, ms = x[mask], base_market[mask]
        lines.append(f"  {label} ({mask.sum()} days): Sharpe {xs.mean() / xs.std() * math.sqrt(Q):.3f} vs market "
                     f"{ms.mean() / ms.std() * math.sqrt(Q):.3f}; {paired(xs, ms)}")

    # 4. DSR break-even N for the selected setting, V held at its observed value
    sr, v = base_sharpes[SETTINGS.index(SELECTED)], base_sharpes.var(ddof=1)
    g3, g4 = skew(x), kurtosis(x, fisher=False)
    above = lambda n: dsr(sr, len(x), g3, g4, n, v) >= LEVEL
    low, high = 2, 4
    while above(high) and high < 1e300:
        low, high = high, high * high
    while high - low > 1 and high / low > 1.001:
        mid = int(math.sqrt(low * high)) if high > 1e6 else (low + high) // 2
        low, high = (mid, high) if above(mid) else (low, mid)
    lines += ["", "4. DSR break-even N, setting 15/225, V fixed",
              f"  DSR at N = 93: {dsr(sr, len(x), g3, g4, 93, v):.4f}; DSR falls below {LEVEL} at N of about {high:.3g}"]

    # 5. Hansen SPA on Sharpe differences, 93 settings vs market
    rng = np.random.default_rng(SEED)
    indices = (stationary_bootstrap_indices(rng, len(base_market), len(base_market), MEAN_BLOCK) for _ in range(RESAMPLES))
    statistic, p = spa_sharpe(base_m, base_market, indices)
    lines += ["", f"5. Hansen SPA (consistent), 93 settings vs market, stationary bootstrap mean block {MEAN_BLOCK}, "
                  f"{RESAMPLES} resamples, seed {SEED}",
              f"  statistic {statistic:.3f}, p-value {p:.4f}"]
    print("\n".join(lines))
    save_results("case_study_checks", lines)


if __name__ == "__main__":
    main()
