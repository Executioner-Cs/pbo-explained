"""Vector figures for docs/submission/research-paper.tex, read only from saved results/ files.

No simulation runs here and no file in results/ is written. Analytic curves are evaluated from documented
expressions (PSEUDO Eq. 2.4 and exact Normal-maximum quadrature). Output: docs/submission/figures/*.pdf.

Run from the repository root, after the experiments:  .venv/bin/python experiments/submission_figures.py
"""
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.stats import norm

from pbo.minbtl import expected_max_normal
from pbo.reporting import read_results

OUT = Path(__file__).resolve().parents[1] / "docs" / "submission" / "figures"
BLUE, ORANGE, GREY, RED, GREEN = "#0072B2", "#E69F00", "#6b6b6b", "#D55E00", "#009E73"
CI = r"\[([\d.]+), ([\d.]+)\] \((\d+)/(\d+)\)"
plt.rcParams.update({"font.size": 9, "font.family": "serif", "axes.spines.top": False,
                     "axes.spines.right": False, "pdf.fonttype": 42, "axes.linewidth": 0.6,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def rate(text, pattern):
    """(rate, low, high) from a result line; pattern captures low, high, hits, total."""
    low, high, hits, total = (float(v) for v in re.search(pattern, text).groups())
    return hits / total, low, high


def exact_emax(n):
    """E[max of n iid N(0,1)] by quadrature of x n phi(x) Phi(x)^(n-1)."""
    return integrate.quad(lambda x: x * n * norm.pdf(x) * norm.cdf(x) ** (n - 1), -12, 12, limit=200)[0]


def fig_best_of_n():
    text = read_results("best_of_n")
    rows = re.findall(r"^(\d+)\s+([\d.]+) \(\+/- ([\d.]+)\)", text, re.M)
    years = 5
    grid = np.unique(np.round(np.logspace(np.log10(2), np.log10(1000), 60)).astype(int))
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    ax.plot(grid, [expected_max_normal(n) / np.sqrt(years) for n in grid], color=GREY, ls="--", lw=1,
            label="Eq. (4) approximation / $\\sqrt{5}$")
    ax.plot(grid, [exact_emax(n) / np.sqrt(years) for n in grid], color=BLUE, lw=1.2,
            label="exact $E[\\max]$ (quadrature) / $\\sqrt{5}$")
    for n, m, se in rows:
        ax.errorbar(int(n), float(m), yerr=1.96 * float(se), fmt="o", ms=4, color=RED, capsize=3)
    ax.plot([], [], "o", color=RED, ms=4, label="simulation, 2000 searches ($\\pm$1.96 MC s.e.)")
    ax.set_xscale("log")
    ax.set_xlabel("number of zero-skill strategies $N$ (log scale)")
    ax.set_ylabel("expected best annual Sharpe")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    save(fig, "fig1_best_of_n")


def fig_psr_ar1():
    cal, curve = read_results("calibration"), read_results("psr_ar1_curve")
    pts = np.array([[float(a), float(b)] for a, b in re.findall(r"^([\d.]+) ([\d.]+)$", curve, re.M)])
    fig, ax = plt.subplots(figsize=(5.2, 2.9))
    ax.plot(pts[:, 0], 100 * pts[:, 1], color=BLUE, lw=1.2, label="large-sample rate, Eq. (9)")
    for phi, head in ((0.0, "iid Normal"), (0.1, "AR(1) phi=0.1"), (0.3, "AR(1) phi=0.3")):
        block = cal.split(head)[1]
        r, lo, hi = rate(block, r"PSR\(0\) > 0.95 on a fixed strategy[^:]*: [\d.]+ " + CI)
        ax.errorbar(phi, 100 * r, yerr=[[100 * (r - lo)], [100 * (hi - r)]], fmt="o", ms=4, color=RED, capsize=3)
        r, lo, hi = rate(block, r"Newey-West variance[^:]*: +[\d.]+ " + CI)
        ax.errorbar(phi + 0.006, 100 * r, yerr=[[100 * (r - lo)], [100 * (hi - r)]], fmt="s", ms=3.5,
                    color=GREEN, capsize=3)
    ax.plot([], [], "o", color=RED, ms=4, label="simulated, uncorrected PSR (95% CI)")
    ax.plot([], [], "s", color=GREEN, ms=3.5, label="simulated, Newey-West variance, 7 lags")
    ax.axhline(5, color="black", ls=":", lw=0.8)
    ax.set_xlabel("AR(1) coefficient $\\phi$")
    ax.set_ylabel("rate of PSR(0) $>$ 0.95, %")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    save(fig, "fig2_psr_ar1")


def fig_calibration():
    cal = read_results("calibration")
    heads = [("iid Normal", "IID Normal"), ("AR(1) phi=0.1", "AR(1) $\\phi$=0.1"), ("AR(1) phi=0.3", "AR(1) $\\phi$=0.3"),
             ("GARCH a=0.05 b=0.90", "GARCH (0.05, 0.90)"), ("GARCH a=0.10 b=0.85", "GARCH (0.10, 0.85)"),
             ("Student-t nu=8", "Student-$t$ $\\nu$=8"), ("Student-t nu=5", "Student-$t$ $\\nu$=5"),
             ("correlated rho=0.3", "equicorr. $\\rho$=0.3"), ("correlated rho=0.7", "equicorr. $\\rho$=0.7")]
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 3.0), sharey=True)
    for i, (head, label) in enumerate(heads):
        block = cal.split("\n" + head)[1].split("\n\n")[0]
        y = -i
        r, lo, hi = rate(block, r"PSR\(0\) > 0.95 on a fixed strategy[^:]*: [\d.]+ " + CI)
        a.errorbar(100 * r, y, xerr=[[100 * (r - lo)], [100 * (hi - r)]], fmt="o", ms=3.5, color=RED, capsize=2)
        r, lo, hi = rate(block, r"DSR > 0.95 on best of 100, N = 100: +[\d.]+ " + CI)
        b.errorbar(100 * r, y + 0.15, xerr=[[100 * (r - lo)], [100 * (hi - r)]], fmt="o", ms=3.5, color=BLUE, capsize=2)
        m = re.search(r"N = implied N[^:]*: [\d.]+ " + CI, block)
        if m:
            r, lo, hi = rate(block, r"N = implied N[^:]*: [\d.]+ " + CI)
            b.errorbar(100 * r, y - 0.15, xerr=[[100 * (r - lo)], [100 * (hi - r)]], fmt="s", ms=3.5,
                       color=ORANGE, capsize=2)
    for ax in (a, b):
        ax.axvline(5, color="black", ls=":", lw=0.8)
    a.set_yticks([-i for i in range(len(heads))], [l for _, l in heads])
    a.set_xlabel("PSR(0) $>$ 0.95, fixed strategy, %")
    b.set_xlabel("DSR $>$ 0.95, best of 100, %")
    b.plot([], [], "o", color=BLUE, ms=3.5, label="$N$ = 100")
    b.plot([], [], "s", color=ORANGE, ms=3.5, label="implied $N$, Eq. (6)")
    b.legend(frameon=False, fontsize=7.5, loc="upper right")
    save(fig, "fig3_calibration")


def fig_real_data():
    boot, follow, g6 = (read_results(n) for n in ("french_bootstrap", "french_followups", "g6_corrected"))
    pred = dict(re.findall(r"L = (\d+): predicted ([\d.]+)", follow))
    rows = [(f"full, $L$={L}", rate(boot, rf"Block length L = {L}\b[^\n]*\n  PSR[^\n]*? [\d.]+ " + CI), float(pred[str(L)]))
            for L in (1, 5, 20, 60)]
    rows += [("full, $L$=20, rerun", rate(follow, r"L = 20: plain [\d.]+ " + CI), float(pred["20"])),
             ("full, $L$=60, rerun", rate(follow, r"L = 60: plain [\d.]+ " + CI), float(pred["60"]))]
    for p in ("1971-1998", "1999-2026"):
        rows.append((p + ", centred", rate(g6, p + r": simulated [\d.]+ " + CI),
                     float(re.search(p + r".*?approximation ([\d.]+);", g6).group(1))))
    fig, ax = plt.subplots(figsize=(6.0, 2.9))
    for i, (label, (r, lo, hi), approx) in enumerate(rows):
        ax.errorbar(i, 100 * r, yerr=[[100 * (r - lo)], [100 * (hi - r)]], fmt="o", ms=4, color=RED if i >= 6 else GREY,
                    capsize=3)
        ax.plot(i + 0.22, 100 * approx, "x", color=BLUE, ms=5)
    ax.plot([], [], "o", color=GREY, ms=4, label="simulated rate (exact 95% CI)")
    ax.plot([], [], "x", color=BLUE, ms=5, label="autocorrelation approximation, Eqs. (9)-(10)")
    ax.axhline(5, color="black", ls=":", lw=0.8)
    ax.set_xticks(range(len(rows)), [l for l, _, _ in rows], rotation=25, ha="right", fontsize=7.5)
    ax.set_ylabel("rate of PSR(0) $>$ 0.95, %")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left")
    save(fig, "fig4_real_data")


def market_rows():
    text = read_results("market_comparison")
    return np.array([[float(v) for v in m] for m in
                     re.findall(r"^\s+(\d+)\s+(\d+)\s+(-?[\d.]+)\s+([\d.]+)\s+([\d.]+)\s", text, re.M)])


def fig_grid():
    rows = market_rows()
    fasts, slows = np.unique(rows[:, 0]), np.unique(rows[:, 1])
    z = np.full((len(fasts), len(slows)), np.nan)
    for f, s, d, *_ in rows:
        z[np.searchsorted(fasts, f), np.searchsorted(slows, s)] = d
    lim = np.nanmax(np.abs(z))
    fig, ax = plt.subplots(figsize=(5.6, 3.1))
    im = ax.imshow(z, cmap="RdBu", vmin=-lim, vmax=lim, origin="lower", aspect="auto")
    ax.set_xticks(range(len(slows)), [f"{int(s)}" for s in slows])
    ax.set_yticks(range(len(fasts)), [f"{int(f)}" for f in fasts])
    ax.set_xlabel("slow window (days)"), ax.set_ylabel("fast window (days)")
    i, j = np.searchsorted(fasts, 15), np.searchsorted(slows, 225)
    ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, ec="black", lw=1.2))
    cb = fig.colorbar(im, ax=ax, shrink=0.9)
    cb.set_label("annual Sharpe minus market", fontsize=8)
    ax.spines[:].set_visible(False)
    save(fig, "fig5_grid")


def fig_z():
    rows = market_rows()
    z = np.sort(rows[:, 2] / rows[:, 3])[::-1]
    fig, ax = plt.subplots(figsize=(5.6, 2.7))
    ax.plot(np.arange(1, len(z) + 1), z, "o", ms=3, color=BLUE)
    ax.axhline(norm.isf(0.05), color=GREY, ls="--", lw=0.9)
    ax.axhline(norm.isf(0.05 / len(z)), color=RED, ls="--", lw=0.9)
    ax.text(len(z), norm.isf(0.05) + 0.08, "one-sided 5%, single test (1.645)", ha="right", fontsize=7.5, color=GREY)
    ax.text(len(z), norm.isf(0.05 / len(z)) - 0.32, "Bonferroni over 93 (3.270)", ha="right", fontsize=7.5, color=RED)
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xlabel("setting, ranked by HAC $z$-statistic")
    ax.set_ylabel("$z$ = difference / s.e.")
    save(fig, "fig6_z")


def fig_dsr_n():
    text = read_results("fig7_dsr_vs_n")
    pts = np.array([[float(a), float(b)] for a, b in re.findall(r"^(\d+) ([\d.]+)$", text, re.M)])
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.semilogx(pts[:, 0], pts[:, 1], color=BLUE, lw=1.2)
    ax.axhline(0.95, color="black", ls=":", lw=0.8)
    ax.axvline(93, color=GREY, ls="--", lw=0.8)
    ax.text(110, 0.90, "$N$ = 93 enumerated", color=GREY, fontsize=7.5)
    ax.set_xlabel("assumed number of trials $N$ (log scale)"), ax.set_ylabel("DSR of setting 15/225")
    save(fig, "fig7_dsr_vs_n")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in (fig_best_of_n, fig_psr_ar1, fig_calibration, fig_real_data, fig_grid, fig_z, fig_dsr_n):
        f()
    print(f"saved 7 figures to {OUT}")


if __name__ == "__main__":
    main()
