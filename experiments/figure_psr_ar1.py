"""Figure 1 (step 6): uncorrected PSR(0) > 0.95 rate under AR(1), simulation vs large-sample approximation.

Simulated rates and exact 95% intervals come from results/calibration.txt (step 4a). The curve is our derivation
(pbo.psr_dsr.ar1_psr_false_positive, large-T value); it is saved to results/psr_ar1_curve.txt and read back
before plotting, so the figure uses saved results only.

Run from the repository root:  .venv/bin/python experiments/figure_psr_ar1.py
"""
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from pbo import paper_values as pv
from pbo.psr_dsr import ar1_psr_false_positive
from pbo.reporting import RESULTS_DIR, read_results, save_results

LEVEL = pv.MINTRL_EX_CONFIDENCE                   # SF p.11, 95%
T = 1248                                          # step 4a sample length (results/calibration.txt header)
PHIS = np.round(np.arange(0, 0.3501, 0.005), 3)   # our choice: covers the tested values 0, 0.1, 0.3
SCENARIOS = {0.0: "iid Normal (baseline)", 0.1: "AR(1) phi=0.1", 0.3: "AR(1) phi=0.3"}


def main():
    save_results("psr_ar1_curve", ["phi large_T_rate (our derivation, asymptotic approximation)"]
                 + [f"{phi:.3f} {ar1_psr_false_positive(phi, T, LEVEL)[1]:.6f}" for phi in PHIS])
    curve = np.loadtxt(RESULTS_DIR / "psr_ar1_curve.txt", skiprows=1)

    text = read_results("calibration")
    points = []
    for phi, header in SCENARIOS.items():
        block = text.split(header + "\n")[1]
        found = re.search(r"PSR\(0\) > 0\.95 .*?: ([\d.]+) \[([\d.]+), ([\d.]+)\]", block)
        points.append((phi, *map(float, found.groups())))
    phi, rate, low, high = np.array(points).T

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(curve[:, 0], 100 * curve[:, 1], "--", color="tab:blue",
            label="Large-sample approximation (our derivation)")
    ax.errorbar(phi, 100 * rate, yerr=100 * np.array([rate - low, high - rate]), fmt="o", color="black",
                capsize=4, label="Simulated, 2000 datasets, exact 95% CI")
    ax.axhline(5, color="gray", linestyle=":", label="Nominal 5% (SF Eq. 11 at 95%)")
    ax.set_xlabel("AR(1) coefficient phi")
    ax.set_ylabel("Share with PSR(0) > 0.95 (%)")
    ax.set_title(f"Uncorrected PSR under AR(1), zero true Sharpe, T = {T}")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "figure1_psr_ar1.png", dpi=150)
    print("saved results/psr_ar1_curve.txt and results/figure1_psr_ar1.png")


if __name__ == "__main__":
    main()
