"""Step 3: how often PSR(0) and DSR call the best of N zero-edge strategies skilled.

Each dataset: N strategies, T daily returns, all with true Sharpe 0. Pick the best by sample Sharpe.
Call it skilled when PSR(0) > 0.95 or DSR > 0.95. DSR uses N and the sample variance of the N Sharpes
(DSR Eq. 2, p.8).

Paper inputs: T = 1250 and N = 100 (DSR p.9), 95% level (SF p.11).
Our choices: number of datasets, seed, Normal returns, population skew and raw kurtosis estimators,
ddof = 1 for the variance across trials.

Run from the repository root:  .venv\\Scripts\\python.exe experiments\\dsr_false_positives.py
"""
from pathlib import Path

import numpy as np
from scipy.stats import kurtosis, norm, skew

from pbo import paper_values as pv
from pbo.minbtl import expected_max_normal
from pbo.psr_dsr import dsr, psr
from pbo.reporting import format_rate

RESULTS_FILE = Path(__file__).parent.parent / "results" / "dsr_false_positives.txt"

# Settings
T, N = pv.DSR_EX_T, pv.DSR_EX_N                   # DSR p.9
LEVEL = pv.MINTRL_EX_CONFIDENCE                   # SF p.11
DATASETS = 2000                                   # our choice
SEED = 20261110                                   # our choice


def main():
    rng = np.random.default_rng(SEED)
    psr_says_skilled, dsr_says_skilled, dsr_values = [], [], []

    for _ in range(DATASETS):
        returns = rng.standard_normal((T, N))
        sharpes = returns.mean(axis=0) / returns.std(axis=0)        # per-period Sharpe, ddof 0
        best = int(np.argmax(sharpes))
        best_skew = skew(returns[:, best])
        best_kurt = kurtosis(returns[:, best], fisher=False)        # raw kurtosis, 3 for Normal
        psr_value = psr(sharpes[best], 0.0, T, best_skew, best_kurt)   # benchmark 0 (SF p.8, note 4)
        dsr_value = dsr(sharpes[best], T, best_skew, best_kurt, N, sharpes.var(ddof=1))
        psr_says_skilled.append(psr_value > LEVEL)
        dsr_says_skilled.append(dsr_value > LEVEL)
        dsr_values.append(dsr_value)

    # Approximation for Normal returns: DSR > LEVEL roughly means max_N > E[max_N] + z, z = Z^-1[LEVEL],
    # and P(max of N iid N(0,1) > x) = 1 - Phi(x)^N. Assumes V is known and ignores noise in skew and
    # kurtosis, so it is an approximation, not a bound.
    approx = 1 - norm.cdf(expected_max_normal(N) + norm.ppf(LEVEL)) ** N

    lines = [
        f"T={T} N={N} datasets={DATASETS} seed={SEED}, all strategies zero edge, Normal returns",
        "",
        f"Best of {N} flagged skilled at {LEVEL:.0%}. Rate [exact 95% CI] (hits/total):",
        f"  PSR(0) > {LEVEL}: {format_rate(psr_says_skilled)}",
        f"  DSR    > {LEVEL}: {format_rate(dsr_says_skilled)}",
        f"  closed-form approximation with V known: {approx:.4f} (assumes V known; an approximation, not a bound)",
        f"  mean DSR of the best strategy: {np.mean(dsr_values):.3f}",
    ]
    text = "\n".join(lines)
    print(text)
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    RESULTS_FILE.write_text(text + "\n")


if __name__ == "__main__":
    main()
