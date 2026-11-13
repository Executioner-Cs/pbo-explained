"""Derived statistics for the manuscript revision, from saved results and the frozen market data (no simulation).

1. PSR rejection counts tested against 5%: exact two-sided binomial p and Holm-adjusted p within each family
   (one family per table: synthetic scenarios, French first run, French replicate, corrected G6). Verdict rule
   adopted in revision, after all results were seen: detected if Holm p < 0.05, suggestive if only the unadjusted
   p < 0.05. The recorded z-band verdict is shown alongside.
2. Paired market test for the selected setting (15/225, 5 bps): difference, se, 95% CI, minimum detectable
   difference at 80% power and power at the observed difference, at 0, 11 and 44 lags (deterministic).
3. Newey-West at AR(1) phi 0.3 with 7 Bartlett lags: rejection rate predicted from truncation bias alone.
4. Exact expected maximum of N standard Normals by quadrature, against PSEUDO Eq. 2.4.

Run from the repository root:  .venv/bin/python experiments/manuscript_numbers.py
"""
import math
import re

import numpy as np
from scipy.integrate import quad
from scipy.stats import binomtest, norm

from pbo import paper_values as pv
from pbo.french import load_market
from pbo.minbtl import expected_max_normal
from pbo.psr_dsr import sharpe_diff
from pbo.reporting import read_results, save_results
from pbo.strategies import crossover_panel

Q, S, LEVEL = pv.PERIODS_PER_YEAR, pv.PBO_S16, pv.MINTRL_EX_CONFIDENCE
SETTINGS = [(f, s) for f in range(5, 55, 5) for s in range(25, 275, 25) if f < s]   # step 5 design
SELECTED, COST, OBSERVED = (15, 225), 0.0005, 0.130                               # step 5 results


def counts(name, pattern):
    return [(label, int(hits), int(total)) for label, hits, total in re.findall(pattern, read_results(name))]


def family_lines(title, rows):
    p = np.array([binomtest(h, n, 0.05).pvalue for _, h, n in rows])
    order, holm, running = np.argsort(p), np.empty(len(p)), 0.0
    for rank, i in enumerate(order):                     # Holm step-down, kept monotone
        running = max(running, min(1.0, (len(p) - rank) * p[i]))
        holm[i] = running
    lines = [title]
    for (label, h, n), pi, hi in zip(rows, p, holm):
        z = (h / n - 0.05) / math.sqrt(0.05 * 0.95 / n)
        old = "detected" if abs(z) >= 3 else "suggestive" if abs(z) >= 2 else "none"
        new = "detected" if hi < 0.05 else "suggestive" if pi < 0.05 else "none"
        lines.append(f"  {label}: {h}/{n} = {h / n:.4f}, z = {z:+.2f}, exact p = {pi:.4f}, Holm p = {hi:.4f}; "
                     f"verdict {new} (recorded z-band rule: {old})")
    return lines


def main():
    lines = ["1. PSR(0) > 0.95 against 5%: exact two-sided binomial test, Holm within each family"]
    lines += family_lines("Synthetic, results/calibration.txt", counts(
        "calibration", r"\n(\S[^\n]*)\n  PSR\(0\) > 0.95 on a fixed strategy[^\n]*\((\d+)/(\d+)\)"))
    lines += family_lines("French first run, results/french_bootstrap.txt", counts(
        "french_bootstrap", r"Block length (L = \d+)[^\n]*\n  PSR\(0\)[^\n]*\((\d+)/(\d+)\)"))
    lines += family_lines("French replicate (G1 plain), results/french_followups.txt", counts(
        "french_followups", r"  (L = \d+): plain [^(]*\((\d+)/(\d+)\)"))
    lines += family_lines("Corrected G6, results/g6_corrected.txt", counts(
        "g6_corrected", r"(\d{4}-\d{4}): simulated [^(]*\((\d+)/(\d+)\)"))

    dates, mkt_rf, rf = load_market()
    start, m = crossover_panel(np.cumprod(1 + mkt_rf + rf), mkt_rf, SETTINGS, COST, S)
    x, market = m[:, SETTINGS.index(SELECTED)], mkt_rf[start:]
    z_bonf = norm.ppf(1 - 0.05 / len(SETTINGS))
    lines += ["", f"2. Paired market test, setting {SELECTED[0]}/{SELECTED[1]}, 5 bps, T = {len(x)}, annualized"]
    for lags in (11, 0, 44):
        d, se = (v * math.sqrt(Q) for v in sharpe_diff(x, market, lags))
        lines.append(f"  lags {lags}: difference {d:.3f}, se {se:.3f}, z {d / se:.2f}, one-sided p {norm.sf(d / se):.4f}, "
                     f"95% CI [{d - 1.96 * se:.3f}, {d + 1.96 * se:.3f}], minimum detectable difference at 80% "
                     f"power {se * (norm.ppf(0.95) + norm.ppf(0.8)):.3f} (unadjusted), "
                     f"{se * (z_bonf + norm.ppf(0.8)):.3f} (Bonferroni z {z_bonf:.3f}); power at {OBSERVED}: "
                     f"{norm.sf(norm.ppf(0.95) - OBSERVED / se):.3f} (unadjusted), {norm.sf(z_bonf - OBSERVED / se):.3f} (Bonferroni)")

    phi, lags = 0.3, 7
    expected = 1 + 2 * sum((1 - h / (lags + 1)) * phi ** h for h in range(1, lags + 1))
    true = (1 + phi) / (1 - phi)
    lines += ["", f"3. Newey-West, AR(1) phi {phi}, {lags} Bartlett lags: expected factor {expected:.4f} vs true "
                  f"{true:.4f}; truncation bias alone predicts a rejection rate of "
                  f"{norm.sf(norm.ppf(LEVEL) * math.sqrt(expected / true)):.4f} (simulated 0.0710, results/calibration.txt)"]

    lines += ["", "4. Expected maximum of N standard Normals: exact (quadrature) vs PSEUDO Eq. 2.4, times 5^(-1/2)"]
    for n in (10, 45, 100):
        exact = quad(lambda v: v * n * norm.pdf(v) * norm.cdf(v) ** (n - 1), -np.inf, np.inf)[0]
        lines.append(f"  N = {n}: exact {exact / math.sqrt(5):.4f}, Eq. 2.4 {expected_max_normal(n) / math.sqrt(5):.4f}")
    print("\n".join(lines))
    save_results("manuscript_numbers", lines)


if __name__ == "__main__":
    main()
