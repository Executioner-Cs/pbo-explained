"""Step 1: the best of N zero-edge strategies looks skilled.

Simulates N strategies with true Sharpe 0 over 5 years, picks the best, and compares the result with
the formula E[max_N] / sqrt(years) (PSEUDO Eq. 2.4 and Eq. 3.1).

Run from the repository root:  .venv/bin/python experiments/best_of_n.py
"""
import math

import numpy as np

from pbo import paper_values as pv
from pbo.minbtl import expected_max_normal
from pbo.reporting import mean_with_se, save_results
from pbo.sharpe import sharpe

# Settings
YEARS = pv.MINBTL_YEARS                           # PSEUDO p.11
PERIODS_PER_YEAR = pv.PERIODS_PER_YEAR            # DSR p.10
NUMBERS_OF_TRIALS = (pv.EMAX_N, pv.MINBTL_MAX_N, pv.DSR_EX_N)   # 10 (PSEUDO p.9), 45 (p.11), 100 (DSR p.9)
SIMULATIONS = 2000                                # our choice
SEED = 20261109                                   # our choice


def main():
    rng = np.random.default_rng(SEED)
    one_strategy = []
    best_of = {n: [] for n in NUMBERS_OF_TRIALS}

    for _ in range(SIMULATIONS):
        # True Sharpe 0 (PSEUDO p.8). Sharpe ignores scale, so standard Normal returns are enough.
        returns = rng.standard_normal(size=(max(NUMBERS_OF_TRIALS), YEARS * PERIODS_PER_YEAR))
        sharpes = np.array([sharpe(row, PERIODS_PER_YEAR) for row in returns])
        one_strategy.append(sharpes[0])
        for n in NUMBERS_OF_TRIALS:
            best_of[n].append(sharpes[:n].max())

    # PSEUDO Eq. 2.3 (p.8) with SR = 0: the annual Sharpe has variance 1 / years.
    formula_se = math.sqrt(1 / YEARS)

    lines = [
        f"trials={SIMULATIONS} years={YEARS} periods_per_year={PERIODS_PER_YEAR} seed={SEED}",
        "",
        f"SE of one {YEARS}y annual Sharpe: sim {np.std(one_strategy):.3f} | PSEUDO Eq. 2.3, SR=0: {formula_se:.3f}",
        "",
        "N    sim mean best (+/- MC SE)   Eq. 2.4 * y^-1/2   sim minus formula",
    ]
    for n in NUMBERS_OF_TRIALS:
        mean, mc_se = mean_with_se(best_of[n])
        formula = expected_max_normal(n) / math.sqrt(YEARS)          # PSEUDO Eq. 3.1 (p.9)
        lines.append(f"{n:<4d} {mean:.3f} (+/- {mc_se:.3f})          {formula:.3f}"
                     f"              {mean - formula:+.3f}")

    print("\n".join(lines))
    save_results("best_of_n", lines)


if __name__ == "__main__":
    main()
