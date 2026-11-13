"""Step 5 follow-up (TODO 5.12): does any MA crossover setting beat holding the market after dependence and selection?

At 5 bps, for each of the 93 settings: Sharpe minus the market's Sharpe on the same days, paired HAC standard error
(pbo.psr_dsr.sharpe_diff), one-sided z-test with a Bonferroni adjustment over the 93 settings.
Design: PROGRESS.md, step 5 follow-up. Our choices: Bartlett bandwidth, its sensitivity values, Bonferroni, one-sided.

Run from the repository root:  .venv/bin/python experiments/market_comparison.py
"""
import numpy as np
from scipy.stats import norm

from pbo import paper_values as pv
from pbo.french import load_market
from pbo.psr_dsr import sharpe_diff
from pbo.reporting import save_results
from pbo.strategies import crossover_panel

Q, S = pv.PERIODS_PER_YEAR, pv.PBO_S16
SETTINGS = [(f, s) for f in range(5, 55, 5) for s in range(25, 275, 25) if f < s]  # step 5 design
COST = 0.0005                                     # the main cost level of step 5
ALPHA = 0.05                                      # family-wise level, our choice
SENSITIVITY_MULTIPLE = 4                          # sensitivity bandwidths: 0 and 4 x primary (44 at T = 13664)


def main():
    dates, mkt_rf, rf = load_market()
    prices = np.cumprod(1 + mkt_rf + rf)
    start, m = crossover_panel(prices, mkt_rf, SETTINGS, COST, S)
    market = mkt_rf[start:]
    PRIMARY = int(4 * (len(market) / 100) ** (2 / 9))   # Newey-West (1994) rule, as in step 4: 11 at T = 13664
    SENSITIVITY = (0, SENSITIVITY_MULTIPLE * PRIMARY)   # reported only; not extra chances to pass
    n = len(SETTINGS)
    best = int(np.argmax(m.mean(axis=0) / m.std(axis=0)))
    z_crit = norm.ppf(1 - ALPHA / n)
    lines = [f"Market {dates[start]} to {dates[-1]}, T={len(market)}, {n} settings, cost {COST * 1e4:g} bps.",
             f"H0: Sharpe(setting) <= Sharpe(market). One-sided, Bonferroni {ALPHA}/{n}: reject when z > {z_crit:.3f}.",
             f"Best setting by Sharpe: fast={SETTINGS[best][0]} slow={SETTINGS[best][1]}.", ""]
    adjusted = {}
    for lags in (PRIMARY, *SENSITIVITY):
        diff, se = np.array([sharpe_diff(m[:, i], market, lags) for i in range(n)]).T
        if not (np.isfinite(diff).all() and np.isfinite(se).all() and (se > 0).all()):
            raise ValueError("comparison requires finite differences and positive finite standard errors")
        p = norm.sf(diff / se)
        adjusted[lags] = np.minimum(1, n * p)                 # Bonferroni-adjusted p
        tag = "primary" if lags == PRIMARY else "sensitivity"
        lines += [f"Bartlett lags = {lags} ({tag}): best setting adjusted p = {adjusted[lags][best]:.4f} "
                  f"({'passes' if adjusted[lags][best] < ALPHA else 'fails'}); "
                  f"settings with adjusted p < {ALPHA}: {np.sum(adjusted[lags] < ALPHA)} of {n}"]
        if lags == PRIMARY:
            primary = diff, se, p
    diff, se, p = primary
    lines += ["", f"All settings, lags = {PRIMARY} unless named. Difference and se annualized.",
              f"{'fast':>4} {'slow':>4} {'diff':>7} {'se':>6} {'raw p':>7} {'adj p':>7} "
              + " ".join(f"{f'adj p L{L}':>9}" for L in SENSITIVITY)]
    for i, (f, s) in enumerate(SETTINGS):
        lines.append(f"{f:>4} {s:>4} {diff[i] * np.sqrt(Q):>7.3f} {se[i] * np.sqrt(Q):>6.3f} {p[i]:>7.4f} "
                     f"{adjusted[PRIMARY][i]:>7.4f} " + " ".join(f"{adjusted[L][i]:>9.4f}" for L in SENSITIVITY))
    print("\n".join(lines))
    save_results("market_comparison", lines)


if __name__ == "__main__":
    main()
