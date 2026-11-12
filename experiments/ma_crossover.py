"""Step 5: is the best moving-average crossover rule on the US market overfit?

93 settings of one rule (fast 5-50, slow 25-250 days) on the Fama-French market, 1971-07 to 2026-09, at three cost
levels. For each: PBO (CSCV, S = 16), and the best setting's PSR(0) and DSR (N = 93 and implied N).
Design: PROGRESS.md, step 5. Paper inputs: S = 16 (PBO p.22), 95% (SF p.11), PBO <= 0.05 rule (PBO p.14),
250 days per year (DSR p.10). Our choices: the grid, costs, warm-up.

Run from the repository root:  .venv/bin/python experiments/ma_crossover.py
"""
import numpy as np
from scipy.stats import kurtosis, skew

from pbo import paper_values as pv
from pbo.cscv import cscv
from pbo.french import load_market
from pbo.psr_dsr import dsr, implied_n, psr
from pbo.reporting import save_results
from pbo.strategies import ma_crossover

# Settings
S = pv.PBO_S16                                    # PBO p.11, p.22
LEVEL = pv.MINTRL_EX_CONFIDENCE                   # SF p.11
ACCEPT = pv.PBO_ACCEPT_LEVEL                      # PBO p.14
Q = pv.PERIODS_PER_YEAR                           # DSR p.10, only to annualize printed Sharpes
SETTINGS = [(f, s) for f in range(5, 55, 5) for s in range(25, 275, 25) if f < s]   # our choice: 93
COSTS = (0.0, 0.0005, 0.0010)                     # our choice: 0, 5 (main), 10 bps per change in position
WARMUP = 250                                      # the longest slow MA


def main():
    dates, mkt_rf, rf = load_market()
    prices = np.cumprod(1 + mkt_rf + rf)          # total-return index of the market
    start = WARMUP + (len(dates) - WARMUP) % S    # drop the warm-up, then trim so S divides T
    market = mkt_rf[start:]
    n = len(SETTINGS)
    lines = [f"Market {dates[start]} to {dates[-1]}, T={len(market)}, {n} settings, S={S}. Sharpes annualized x sqrt({Q}).",
             f"Buy-and-hold market: annual Sharpe {market.mean() / market.std() * np.sqrt(Q):.3f}", ""]

    for cost in COSTS:
        m = np.column_stack([ma_crossover(prices, mkt_rf, f, s, cost) for f, s in SETTINGS])[start:]
        sharpes = m.mean(axis=0) / m.std(axis=0)  # per-period, ddof 0
        best = int(np.argmax(sharpes))
        x, t, v = m[:, best], len(m), sharpes.var(ddof=1)
        g3, g4, n_implied = skew(x), kurtosis(x, fisher=False), implied_n(np.corrcoef(m.T))
        pbo = cscv(m, S)[0]
        lines += [
            f"Cost {cost * 1e4:g} bps per change in position",
            f"  best setting fast={SETTINGS[best][0]} slow={SETTINGS[best][1]}: annual Sharpe {sharpes[best] * np.sqrt(Q):.3f}",
            f"  settings above buy-and-hold: {np.sum(sharpes > market.mean() / market.std())} of {n}",
            f"  PSR(0) of the best: {psr(sharpes[best], 0.0, t, g3, g4):.4f}",
            f"  DSR, N = {n}: {dsr(sharpes[best], t, g3, g4, n, v):.4f}",
            f"  DSR, implied N = {n_implied:.1f}: {dsr(sharpes[best], t, g3, g4, n_implied, v):.4f}",
            f"  PBO: {pbo:.3f} ({'passes' if pbo <= ACCEPT else 'fails'} the PBO <= {ACCEPT} rule)",
            "",
        ]
    print("\n".join(lines))
    save_results("ma_crossover", lines)


if __name__ == "__main__":
    main()
