"""Paper revision (IMRaD): descriptive statistics, performance metrics, crisis stress tests, walk-forward test.

Exploratory (designed before the run, no recorded predictions). Our choices: crisis windows below, Sortino with
a zero target, walk-forward re-selection each January on all prior data from 1972 (at least 10 years).

Run from the repository root:  .venv/bin/python experiments/performance_checks.py
"""
import math

import numpy as np
from scipy.stats import kurtosis, norm, skew

from pbo import paper_values as pv
from pbo.french import load_market, load_returns
from pbo.psr_dsr import sharpe_diff
from pbo.reporting import save_results
from pbo.strategies import crossover_panel, ma_crossover, position_returns

Q, S = pv.PERIODS_PER_YEAR, pv.PBO_S16
SETTINGS = [(f, s) for f in range(5, 55, 5) for s in range(25, 275, 25) if f < s]   # step 5 design
COST, SELECTED, LAGS, MIN_YEARS = 0.0005, (15, 225), 11, 10
CRISES = [("1973-74 bear market", 19730111, 19741003), ("1987 crash", 19870825, 19871204),
          ("2000-02 dot-com", 20000324, 20021009), ("2007-09 financial crisis", 20071009, 20090309),
          ("2020 Covid crash", 20200219, 20200323), ("2022 rate shock", 20220103, 20221012)]


def metrics(excess, total):
    """Annual mean and volatility of total return, Sharpe and Sortino of excess return, max drawdown, worst day."""
    wealth = np.cumprod(1 + total)
    drawdown = 1 - wealth / np.maximum.accumulate(wealth)
    downside = math.sqrt(np.mean(np.minimum(excess, 0) ** 2))
    return (f"return {total.mean() * Q * 100:5.1f}%/yr, vol {total.std() * math.sqrt(Q) * 100:4.1f}%, "
            f"Sharpe {excess.mean() / excess.std() * math.sqrt(Q):.3f}, Sortino {excess.mean() / downside * math.sqrt(Q):.3f}, "
            f"max drawdown {drawdown.max() * 100:4.1f}%, worst day {total.min() * 100:5.1f}%")


def main():
    dates, mkt_rf, rf = load_market()
    prices = np.cumprod(1 + mkt_rf + rf)
    start, m = crossover_panel(prices, mkt_rf, SETTINGS, COST, S)
    days, market, rate = dates[start:], mkt_rf[start:], rf[start:]
    rule = m[:, SETTINGS.index(SELECTED)]
    lines = ["1. Data, descriptive statistics (daily, decimal)"]
    lines.append(f"  market excess {days[0]}-{days[-1]} ({len(market)} days): mean {market.mean():.5f}, sd {market.std():.5f}, "
                 f"skew {skew(market):.2f}, kurtosis {kurtosis(market, fisher=False):.1f}, "
                 f"lag-1 autocorrelation {np.corrcoef(market[:-1], market[1:])[0, 1]:+.3f}")
    ind_dates, industries, _ = load_returns()
    lag1 = [np.corrcoef(c[:-1], c[1:])[0, 1] for c in industries.T]
    lines.append(f"  49 industries {ind_dates[0]}-{ind_dates[-1]} ({len(industries)} days, demeaned): sd median "
                 f"{np.median(industries.std(axis=0)):.4f}, kurtosis median {np.median(kurtosis(industries, axis=0, fisher=False)):.1f}, "
                 f"lag-1 autocorrelation median {np.median(lag1):+.3f}")
    lines.append(f"  rule 15/225 is long {np.mean(rule != 0) * 100:.0f}% of days")

    lines += ["", "2. Performance, 5 bps, full sample (total return = excess + risk-free)",
              f"  market:     {metrics(market, market + rate)}",
              f"  rule 15/225: {metrics(rule, rule + rate)}"]

    lines += ["", "3. Crisis windows, cumulative total return (peak to trough of the market, our choice of dates)"]
    for name, a, b in CRISES:
        w = (days >= a) & (days <= b)
        lines.append(f"  {name} ({a}-{b}): market {(np.prod(1 + market[w] + rate[w]) - 1) * 100:+6.1f}%, "
                     f"rule {(np.prod(1 + rule[w] + rate[w]) - 1) * 100:+6.1f}%")

    # 4. Walk-forward: each January pick the best setting by Sharpe on all earlier days, hold it for the year.
    # Costs are charged on the actual held position path, flat before the first test day. Corrected 2026-11-12:
    # the first version stitched each setting's own costed returns, which missed costs at rule switches
    # (original output kept in results/performance_checks_v1_stitched_costs.txt).
    positions = np.column_stack([ma_crossover(prices, np.ones(len(prices)), f, s, 0.0) for f, s in SETTINGS])[start:]
    years = days // 10000
    held, picks = np.zeros(len(days)), []
    first = years[0] + MIN_YEARS
    for year in range(first, years[-1] + 1):
        past, now = years < year, years == year
        sharpes = m[past].mean(axis=0) / m[past].std(axis=0)
        best = int(np.argmax(sharpes))
        picks.append(SETTINGS[best])
        held[now] = positions[now, best]
    test = years >= first
    oos = np.zeros(len(days))
    oos[test] = position_returns(held[test], market[test], COST)
    d, se = (v * math.sqrt(Q) for v in sharpe_diff(oos[test], market[test], LAGS))
    lines += ["", f"4. Walk-forward out of sample, {first}-{years[-1]} ({test.sum()} days), re-selected each January",
              f"  out-of-sample: {metrics(oos[test], oos[test] + rate[test])}",
              f"  market:        {metrics(market[test], market[test] + rate[test])}",
              f"  difference in Sharpe {d:+.3f} (se {se:.3f}, one-sided p {norm.sf(d / se):.4f}, {LAGS} lags)",
              f"  settings picked: {len(set(picks))} distinct; most often {max(set(picks), key=picks.count)} "
              f"({picks.count(max(set(picks), key=picks.count))} of {len(picks)} years)"]
    print("\n".join(lines))
    save_results("performance_checks", lines)


if __name__ == "__main__":
    main()
