"""Independent check of docs/oracle_step1.md. Does not import src/pbo.

Uses stdlib NormalDist, not scipy, and Monte Carlo for the exact E[max]. Run: .venv/Scripts/python.exe experiments/check_oracle.py
"""
import math
from statistics import NormalDist

import numpy as np

G = 0.5772156649015329  # Euler-Mascheroni
zinv = NormalDist().inv_cdf


def emax(n):
    return (1 - G) * zinv(1 - 1 / n) + G * zinv(1 - 1 / (n * math.e))


def minbtl(n, target):
    return (emax(n) / target) ** 2


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"{'PASS' if ok else 'FAIL'}  {name:40s} got {got:.6f}  oracle {want}  tol {tol}")
    return ok


results = [
    check("expected_max_normal(10)", emax(10), 1.5746, 5e-5),
    check("min_btl_years(45, 1)", minbtl(45, 1), 4.998, 5e-4),
    check("min_btl_years(7, 1)", minbtl(7, 1), 1.92, 5e-3),
    check("min_btl_years(10, 1)", minbtl(10, 1), 2.4794, 5e-5),
    check("2*ln(45)", 2 * math.log(45), 7.61, 5e-3),
]

n = next(n for n in range(2, 1000) if minbtl(n, 1) > 5)
print(f"{'PASS' if n == 46 else 'FAIL'}  smallest n with minbtl > 5: {n} (oracle 46)")
results.append(n == 46)

# Exact E[max of 10 iid N(0,1)] by Monte Carlo.
rng = np.random.default_rng(20261107)
m = rng.standard_normal((1_000_000, 10)).max(axis=1)
mean, se = m.mean(), m.std() / math.sqrt(m.size)
ok = abs(mean - 1.5388) <= 3 * se
print(f"{'PASS' if ok else 'FAIL'}  MC E[max of 10]: {mean:.5f} +/- {se:.5f} (oracle 1.5388, within 3 SE)")
results.append(ok)

# Zero-edge best Sharpe, 5y, n=45: emax(45)/sqrt(5). Closed form, not a simulation.
print(f"info  emax(45)/sqrt(5) = {emax(45) / math.sqrt(5):.4f} (oracle 'about 1')")

print("ALL PASS" if all(results) else "SOME FAIL")
