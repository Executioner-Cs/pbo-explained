"""Best-of-N zero-edge strategies. Compares simulation to PSEUDO Eq. 2.4 scaled by Eq. 3.1.

Paper inputs come from pbo.paper_values. TRIALS and SEED are simulation choices, not paper values.
Run: .venv/Scripts/python.exe experiments/best_of_n.py
"""
import math
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pbo import paper_values as pv  # noqa: E402
from pbo.minbtl import expected_max_normal  # noqa: E402
from pbo.sharpe import sharpe  # noqa: E402

YEARS = pv.MINBTL_YEARS                                  # PSEUDO p.11
Q = pv.PERIODS_PER_YEAR                                  # DSR p.10
NS = (pv.EMAX_N, pv.MINBTL_MAX_N, pv.DSR_EX_N)           # N = 10 (PSEUDO p.9), 45 (p.11), 100 (DSR p.10)
TRIALS, SEED = 2000, 20261109                            # our choice

rng = np.random.default_rng(SEED)
single, best = [], {n: [] for n in NS}
for _ in range(TRIALS):
    # True SR = 0 (PSEUDO p.8). Sharpe is scale-free, so standard normal draws are enough.
    r = rng.standard_normal(size=(max(NS), YEARS * Q))
    s = np.array([sharpe(row, Q) for row in r])
    single.append(s[0])
    for n in NS:
        best[n].append(s[:n].max())

# PSEUDO Eq. 2.3 (p.8) with SR = 0: variance of annualized SR = 1 / y.
se_closed = math.sqrt(1 / YEARS)

lines = [f"trials={TRIALS} years={YEARS} periods_per_year={Q} seed={SEED}", ""]
lines.append(f"SE of one {YEARS}y annual Sharpe: sim {np.std(single):.3f} | PSEUDO Eq. 2.3, SR=0: {se_closed:.3f}")
lines.append("")
lines.append(f"N    sim mean best (+/- MC SE)   Eq. 2.4 * y^-1/2   sim minus formula")
for n in NS:
    b = np.array(best[n])
    f = expected_max_normal(n) / math.sqrt(YEARS)  # PSEUDO Eq. 3.1 (p.9)
    lines.append(f"{n:<4d} {b.mean():.3f} (+/- {b.std() / math.sqrt(TRIALS):.3f})          {f:.3f}              {b.mean() - f:+.3f}")

out = "\n".join(lines)
print(out)
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "best_of_n.txt").write_text(out + "\n")
