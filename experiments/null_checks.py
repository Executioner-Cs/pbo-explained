"""Step 2: two null checks for CSCV / PBO.

Null 1: all N strategies have zero edge. In each split the in-sample pick's out-of-sample rank is uniform
on 1..N, so with N even the expected PBO is exactly 1/2.
Null 2: one strategy gets a real annual Sharpe SR. As SR grows it wins in and out of sample, so PBO -> 0.
Step 4 (G4): Null 2 repeated with AR(1) and GARCH noise, to see whether PBO keeps its power under dependence.

Paper inputs: T from PBO p.25 (1,000 daily), S = 16 from PBO p.11 (example) and p.22 (rationale), periods per year from DSR p.10.
Our choices: N, edge sizes, number of datasets, seed, trimming T so S divides it, pairing S = 16 with T.

Run from the repository root:  .venv/bin/python experiments/null_checks.py
"""
import math

import numpy as np

from pbo import paper_values as pv
from pbo import scenarios
from pbo.cscv import cscv
from pbo.reporting import format_mean, mean_with_se, save_results

# Settings
S_MAIN = pv.PBO_S16                               # PBO p.11, p.22
S_ALT = 8                                         # our choice: sensitivity check
T = pv.PBO_EX_T // S_MAIN * S_MAIN                # PBO p.25 gives 1,000; 992 so S = 16 divides it
PERIODS_PER_YEAR = pv.PERIODS_PER_YEAR            # DSR p.10
N = 100                                           # our choice
EDGES = (0.0, 0.5, 1.0, 2.0, 3.0)                 # our choice: true annual Sharpe of the one real strategy
DATASETS_NULL1, DATASETS_NULL2 = 40, 20           # our choice
SEED = 20261110                                   # our choice
SEED_DEPENDENT = 20261114                         # our choice: G4, separate stream so lines above are unchanged
NOISES = {                                        # G4: noise for Null 2 under dependence (step 4 levels)
    "AR(1) phi=0.3": lambda rng: scenarios.ar1(rng, T, N, 0.3),
    "GARCH a=0.10 b=0.85": lambda rng: scenarios.garch(rng, T, N, 0.10, 0.85),
}


def summary(pbos):
    return f"mean {format_mean(pbos)} (MC SE)  min {min(pbos):.3f}  max {max(pbos):.3f}"


def main():
    rng = np.random.default_rng(SEED)
    expected_null1 = (N + 1) // 2 / N             # P(uniform rank on 1..N is <= (N+1)/2); 1/2 for even N
    lines = [f"T={T} N={N} q={PERIODS_PER_YEAR} seed={SEED}", ""]

    lines.append(f"Null 1: all {N} strategies zero edge. Closed form expected PBO = {expected_null1}")
    for s in (S_MAIN, S_ALT):
        pbos = [cscv(rng.standard_normal((T, N)), s)[0] for _ in range(DATASETS_NULL1)]
        lines.append(f"  S={s:<3d} {DATASETS_NULL1} datasets: {summary(pbos)}")
        print(lines[-1], flush=True)

    lines += ["", f"Null 2: one strategy with true annual Sharpe SR, S={S_MAIN}, {DATASETS_NULL2} datasets each"]
    iid = {}
    for sr in EDGES:
        pbos = []
        for _ in range(DATASETS_NULL2):
            returns = rng.standard_normal((T, N))
            returns[:, 0] += sr / math.sqrt(PERIODS_PER_YEAR)   # per-period mean = SR / sqrt(q), sd 1 (PSEUDO Eq. 2.2)
            pbos.append(cscv(returns, S_MAIN)[0])
        iid[sr] = mean_with_se(pbos)
        lines.append(f"  SR={sr:<4} {summary(pbos)}")
        print(lines[-1], flush=True)

    # G4 (step 4): the same check with dependent noise (unit variance, so the edge is the same Sharpe)
    rng = np.random.default_rng(SEED_DEPENDENT)
    for name, noise in NOISES.items():
        lines += ["", f"Null 2 with {name} noise (G4), seed={SEED_DEPENDENT}; z = difference from the IID row"]
        for sr in EDGES:
            pbos = []
            for _ in range(DATASETS_NULL2):
                returns = noise(rng)
                returns[:, 0] += sr / math.sqrt(PERIODS_PER_YEAR)
                pbos.append(cscv(returns, S_MAIN)[0])
            mean, se = mean_with_se(pbos)
            z = (mean - iid[sr][0]) / math.hypot(se, iid[sr][1])
            lines.append(f"  SR={sr:<4} {summary(pbos)}  z = {z:+.2f}")
            print(lines[-1], flush=True)

    save_results("null_checks", lines)


if __name__ == "__main__":
    main()
