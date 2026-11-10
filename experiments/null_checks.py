"""Step 2 null checks for CSCV / PBO.

Null 1: N iid zero-edge strategies. Closed form: in each combination the IS pick's OOS rank is uniform
on 1..N (IS and OOS rows are independent), so with N even P(rank <= (N+1)/2) = 1/2. Expected PBO = 0.5.
Null 2: one strategy gets a true annual Sharpe SR. As SR grows it should win IS and stay high OOS, so PBO -> 0.

Paper inputs: T from PBO p.25 (1,000 daily), S = 16 from PBO p.11, q = 250 from DSR p.10.
Our choices: N, edges, datasets, seed, trimming T to a multiple of S, and pairing S = 16 with T
(p.25 does not say which S its examples used).
Run: .venv/Scripts/python.exe experiments/null_checks.py
"""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pbo import paper_values as pv  # noqa: E402
from pbo.cscv import cscv  # noqa: E402

S_MAIN = pv.PBO_S16                                   # PBO p.11
S_ALT = 8                                             # our choice: sensitivity check (TODO 2.19)
T = pv.PBO_EX_T // S_MAIN * S_MAIN                    # PBO p.25 gives 1,000; trimmed to 992 so S = 16 divides it
Q = pv.PERIODS_PER_YEAR                               # DSR p.10
N = 100                                               # our choice: even, so the null-1 closed form is exactly 1/2
EDGES = (0.0, 0.5, 1.0, 2.0, 3.0)                     # our choice: true annual Sharpe of the one real strategy
D_NULL1, D_NULL2, SEED = 40, 20, 20261110             # our choice: datasets per setting, seed

rng = np.random.default_rng(SEED)
assert N % 2 == 0, "closed form below needs N even"
closed_form = (N // 2) / N                            # P(uniform rank on 1..N is <= (N+1)/2)


def summary(pbos):
    a = np.array(pbos)
    return f"mean {a.mean():.3f} (+/- {a.std(ddof=1) / math.sqrt(a.size):.3f} MC SE)  min {a.min():.3f}  max {a.max():.3f}"


lines = [f"T={T} N={N} q={Q} seed={SEED}", ""]

lines.append(f"Null 1: all {N} strategies zero edge. Closed form expected PBO = {closed_form}")
for s in (S_MAIN, S_ALT):
    pbos = [cscv(rng.standard_normal((T, N)), s)[0] for _ in range(D_NULL1)]
    lines.append(f"  S={s:<3d} {D_NULL1} datasets: {summary(pbos)}")
    print(lines[-1], flush=True)

lines += ["", f"Null 2: one strategy with true annual Sharpe SR, S={S_MAIN}, {D_NULL2} datasets each"]
for sr in EDGES:
    pbos = []
    for _ in range(D_NULL2):
        m = rng.standard_normal((T, N))
        m[:, 0] += sr / math.sqrt(Q)                  # per-period mean = annual SR / sqrt(q), sd 1 (PSEUDO Eq. 2.2)
        pbos.append(cscv(m, S_MAIN)[0])
    lines.append(f"  SR={sr:<4} {summary(pbos)}")
    print(lines[-1], flush=True)

out = "\n".join(lines)
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "null_checks.txt").write_text(out + "\n")
print("\n" + out)
