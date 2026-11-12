"""Step 2: two null checks for CSCV / PBO.

Null 1: all N strategies have zero edge. In each split the in-sample pick's out-of-sample rank is uniform
on 1..N, so with N even the expected PBO is exactly 1/2.
Null 2: one strategy gets a real annual Sharpe SR. As SR grows it wins in and out of sample, so PBO -> 0.

Paper inputs: T from PBO p.25 (1,000 daily), S = 16 from PBO p.11, periods per year from DSR p.10.
Our choices: N, edge sizes, number of datasets, seed, trimming T so S divides it, pairing S = 16 with T.

Run from the repository root:  .venv\\Scripts\\python.exe experiments\\null_checks.py
"""
import math
from pathlib import Path

import numpy as np

from pbo import paper_values as pv
from pbo.cscv import cscv
from pbo.reporting import format_mean

RESULTS_FILE = Path(__file__).parent.parent / "results" / "null_checks.txt"

# Settings
S_MAIN = pv.PBO_S16                               # PBO p.11
S_ALT = 8                                         # our choice: sensitivity check
T = pv.PBO_EX_T // S_MAIN * S_MAIN                # PBO p.25 gives 1,000; 992 so S = 16 divides it
PERIODS_PER_YEAR = pv.PERIODS_PER_YEAR            # DSR p.10
N = 100                                           # our choice: even, so the null-1 answer is exactly 1/2
EDGES = (0.0, 0.5, 1.0, 2.0, 3.0)                 # our choice: true annual Sharpe of the one real strategy
DATASETS_NULL1, DATASETS_NULL2 = 40, 20           # our choice
SEED = 20261110                                   # our choice


def summary(pbos):
    return f"mean {format_mean(pbos)} (MC SE)  min {min(pbos):.3f}  max {max(pbos):.3f}"


def main():
    rng = np.random.default_rng(SEED)
    assert N % 2 == 0, "the closed form below needs N even"
    expected_null1 = (N // 2) / N                 # P(uniform rank on 1..N is <= (N+1)/2)
    lines = [f"T={T} N={N} q={PERIODS_PER_YEAR} seed={SEED}", ""]

    lines.append(f"Null 1: all {N} strategies zero edge. Closed form expected PBO = {expected_null1}")
    for s in (S_MAIN, S_ALT):
        pbos = [cscv(rng.standard_normal((T, N)), s)[0] for _ in range(DATASETS_NULL1)]
        lines.append(f"  S={s:<3d} {DATASETS_NULL1} datasets: {summary(pbos)}")
        print(lines[-1], flush=True)

    lines += ["", f"Null 2: one strategy with true annual Sharpe SR, S={S_MAIN}, {DATASETS_NULL2} datasets each"]
    for sr in EDGES:
        pbos = []
        for _ in range(DATASETS_NULL2):
            returns = rng.standard_normal((T, N))
            returns[:, 0] += sr / math.sqrt(PERIODS_PER_YEAR)   # per-period mean = SR / sqrt(q), sd 1 (PSEUDO Eq. 2.2)
            pbos.append(cscv(returns, S_MAIN)[0])
        lines.append(f"  SR={sr:<4} {summary(pbos)}")
        print(lines[-1], flush=True)

    RESULTS_FILE.parent.mkdir(exist_ok=True)
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
