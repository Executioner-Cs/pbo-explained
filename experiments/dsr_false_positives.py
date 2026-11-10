"""TODO 3.15: how often PSR(0) and DSR call the best of N zero-edge strategies skilled.

Each dataset: N strategies, T daily returns, all true SR = 0. Pick the best by sample Sharpe.
Flag it skilled when PSR(0) > 0.95 or DSR > 0.95 (95% level as in SF p.10 and DSR p.10).
DSR uses N and the sample variance of the N Sharpe estimates (DSR Eq. 2, p.8).

Paper inputs: T = 1250 and N = 100 (DSR example, p.9), confidence 0.95 (SF p.11).
Our choices: datasets, seed, Normal returns, and the moment estimators (population skew, raw kurtosis).
Run: .venv/Scripts/python.exe experiments/dsr_false_positives.py
"""
import pathlib
import sys

import numpy as np
from scipy.stats import binomtest, kurtosis, norm, skew

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from pbo import paper_values as pv  # noqa: E402
from pbo.minbtl import expected_max_normal  # noqa: E402
from pbo.psr_dsr import dsr, psr  # noqa: E402

T, N = pv.DSR_EX_T, pv.DSR_EX_N                       # DSR p.9
LEVEL = pv.MINTRL_EX_CONFIDENCE                       # SF p.11
DATASETS, SEED = 2000, 20261110                       # our choice

rng = np.random.default_rng(SEED)
flags_psr, flags_dsr, dsrs = [], [], []
for _ in range(DATASETS):
    r = rng.standard_normal((T, N))
    srs = r.mean(axis=0) / r.std(axis=0)               # per-period Sharpe, ddof 0, as pbo.sharpe
    k = int(np.argmax(srs))
    sk, ku = skew(r[:, k]), kurtosis(r[:, k], fisher=False)   # raw kurtosis, 3 for Normal
    p = psr(srs[k], 0.0, T, sk, ku)                   # benchmark 0: skill-less default (SF p.8, note 4)
    d = dsr(srs[k], T, sk, ku, N, srs.var(ddof=1))     # V: sample variance across trials, ddof 1 (our choice)
    flags_psr.append(p > LEVEL)
    flags_dsr.append(d > LEVEL)
    dsrs.append(d)


# Closed-form approximation, Normal returns: in standard units DSR > LEVEL means max_N > E[max_N] + z,
# with z = Z^-1[LEVEL]. P(max of N iid N(0,1) > x) = 1 - Phi(x)^N.
# Assumes V is known (1/T) and ignores noise in skew and kurt. The code estimates V from the same trials
# (ddof = 1, our choice; DSR p.8 does not fix the estimator), so this is an approximation, not a bound.
approx = 1 - norm.cdf(expected_max_normal(N) + norm.ppf(LEVEL)) ** N


def rate(flags):
    # exact (Clopper-Pearson) 95% interval: the normal approximation fails for rates near 0 or 1
    k = int(np.sum(flags))
    ci = binomtest(k, len(flags)).proportion_ci()
    return f"{k / len(flags):.4f} ({k}/{len(flags)}, exact 95% CI {ci.low:.4f} to {ci.high:.4f})"


lines = [
    f"T={T} N={N} datasets={DATASETS} seed={SEED}, all strategies zero edge, Normal returns",
    "",
    f"Best of {N} flagged skilled at {LEVEL:.0%}:",
    f"  PSR(0) > {LEVEL}: {rate(flags_psr)}",
    f"  DSR    > {LEVEL}: {rate(flags_dsr)}",
    f"  closed-form approximation with V known: {approx:.4f} (assumes V known; an approximation, not a bound)",
    f"  mean DSR of the best strategy: {np.mean(dsrs):.3f}",
]
out = "\n".join(lines)
print(out)
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "dsr_false_positives.txt").write_text(out + "\n")
