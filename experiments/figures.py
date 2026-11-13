"""Paper figures 2-7 (figure 1, PSR under AR(1), is experiments/figure_psr_ar1.py).

Numbers come from saved results; the two curves computed here (DSR against N, growth of $1) are saved to results/
before they are plotted. Run after the experiments, from the repository root:
    .venv/bin/python experiments/figures.py
"""
import math
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kurtosis, skew

from pbo import paper_values as pv
from pbo.french import load_market
from pbo.psr_dsr import dsr
from pbo.reporting import RESULTS_DIR, read_results, save_results
from pbo.strategies import crossover_panel, ma_crossover

BLUE, ORANGE, GREY, RED = "#0072B2", "#E69F00", "#7f7f7f", "#D55E00"
SETTINGS = [(f, s) for f in range(5, 55, 5) for s in range(25, 275, 25) if f < s]   # step 5 design
Q, S, LEVEL, COST, SELECTED = pv.PERIODS_PER_YEAR, pv.PBO_S16, pv.MINTRL_EX_CONFIDENCE, 0.0005, (15, 225)
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / f"{name}.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def rate(text, pattern):
    """(rate, low, high) from a result line whose pattern captures low, high, hits, total."""
    low, high, hits, total = (float(v) for v in re.search(pattern, text).groups())
    return hits / total, low, high


CI = r"\[([\d.]+), ([\d.]+)\] \((\d+)/(\d+)\)"


def cscv_diagram():
    """Figure 2: S = 4 blocks, the 6 in-sample / out-of-sample splits (PBO p.13, Figure 1)."""
    fig, ax = plt.subplots(figsize=(6.2, 2.6))
    for row, is_b in enumerate(((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))):
        for b in range(4):
            colour = BLUE if b in is_b else ORANGE
            ax.add_patch(plt.Rectangle((b, -row), 0.95, 0.8, color=colour))
            ax.text(b + 0.47, -row + 0.4, "ABCD"[b], ha="center", va="center", color="white", fontsize=9)
        ax.text(4.15, -row + 0.4, f"split {row + 1}", va="center", fontsize=9)
    ax.text(0, 1.6, "in-sample (blue): pick the best strategy", color=BLUE, fontsize=9)
    ax.text(0, 1.1, "out-of-sample (orange): where does that strategy rank?", color=ORANGE, fontsize=9)
    ax.set_xlim(-0.1, 5.2), ax.set_ylim(-5.3, 2.1), ax.axis("off")
    ax.set_title("CSCV with S = 4 blocks: every half is in-sample once, out-of-sample once", fontsize=10)
    save(fig, "fig2_cscv_splits")


def real_data():
    """Figure 3: PSR(0) > 0.95 on bootstrapped industry returns with zero true edge."""
    boot, follow, g6 = (read_results(n) for n in ("french_bootstrap", "french_followups", "g6_corrected"))
    data = [(f"full, L={L}", rate(boot, rf"L = {L}\b[^\n]*\n  PSR[^\n]*? " + CI)) for L in (1, 5, 20, 60)]
    data += [("full, L=20 (rerun)", rate(follow, r"L = 20: plain [\d.]+ " + CI)),
             ("1971-1998", rate(g6, r"1971-1998: simulated [\d.]+ " + CI)),
             ("1999-2026", rate(g6, r"1999-2026: simulated [\d.]+ " + CI))]
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    for i, (label, (r, lo, hi)) in enumerate(data):
        colour = RED if label == "1971-1998" else BLUE if label == "1999-2026" else GREY
        ax.errorbar(i, 100 * r, yerr=[[100 * (r - lo)], [100 * (hi - r)]], fmt="o", color=colour, capsize=4)
    ax.axhline(5, color="black", linestyle=":", linewidth=1)
    ax.set_xticks(range(len(data)), [l for l, _ in data], rotation=25, ha="right", fontsize=8)
    ax.set_ylabel("PSR(0) > 0.95, % (95% CI)")
    ax.set_title("Real returns, zero true edge: PSR's error follows the period", fontsize=10)
    save(fig, "fig3_real_data")


def dsr_panels():
    """Figure 4: PSR vs DSR on the best of 100 noise strategies, and DSR as strategies become correlated."""
    dfp, cal = read_results("dsr_false_positives"), read_results("calibration")
    psr_best = float(re.search(r"PSR\(0\) > 0.95: ([\d.]+)", dfp).group(1))
    dsr_best = float(re.search(r"DSR    > 0.95: ([\d.]+)", dfp).group(1))
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.6, 2.9), gridspec_kw={"width_ratios": [1, 1.4]})
    a.bar(["PSR(0)", "DSR"], [100 * psr_best, 100 * dsr_best], color=[GREY, BLUE])
    a.axhline(5, color="black", linestyle=":", linewidth=1)
    a.set_ylabel("flags the best of 100 as skilled, %")
    a.set_title("Best of 100 noise strategies", fontsize=10)
    for x, v in enumerate((psr_best, dsr_best)):
        a.text(x, 100 * v + 2, f"{100 * v:.2f}%", ha="center", fontsize=9)
    labels, n100, implied = ["IID", "rho 0.3", "rho 0.7"], [], []
    for head in ("iid Normal", "correlated rho=0.3", "correlated rho=0.7"):
        block = cal.split(head)[1]
        n100.append(100 * float(re.search(r"DSR > 0.95 on best of 100, N = 100: +([\d.]+)", block).group(1)))
        m = re.search(r"N = implied N[^:]*: ([\d.]+)", block.split("\n\n")[0])
        implied.append(100 * float(m.group(1)) if m else np.nan)
    x = np.arange(3)
    b.bar(x - 0.2, n100, 0.4, color=BLUE, label="N = 100")
    b.bar(x + 0.2, implied, 0.4, color=ORANGE, label="implied N")
    b.axhline(5, color="black", linestyle=":", linewidth=1)
    b.set_xticks(x, labels), b.set_ylabel("DSR > 0.95, %"), b.legend(frameon=False, fontsize=8)
    b.set_title("DSR rises with correlation", fontsize=10)
    save(fig, "fig4_dsr")


def case_study():
    """Figures 5-7: growth of $1, the market test against what it could detect, DSR against N."""
    dates, mkt_rf, rf = load_market()
    prices = np.cumprod(1 + mkt_rf + rf)
    start, m = crossover_panel(prices, mkt_rf, SETTINGS, COST, S)
    strat = ma_crossover(prices, mkt_rf, *SELECTED, COST)[start:] + rf[start:]
    market = mkt_rf[start:] + rf[start:]
    grow_s, grow_m = np.cumprod(1 + strat), np.cumprod(1 + market)
    years = (np.arange(len(strat)) / Q) + 1972.55
    save_results("fig5_growth", ["year market strategy_15_225"] +
                 [f"{y:.3f} {a:.6f} {b:.6f}" for y, a, b in zip(years[::21], grow_m[::21], grow_s[::21])])
    saved = np.loadtxt(RESULTS_DIR / "fig5_growth.txt", skiprows=1)
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    ax.semilogy(saved[:, 0], saved[:, 1], color=GREY, label="buy and hold market (Sharpe 0.458)")
    ax.semilogy(saved[:, 0], saved[:, 2], color=BLUE, label="best MA rule 15/225 (Sharpe 0.588)")
    ax.set_ylabel("growth of $1 (log scale)"), ax.legend(frameon=False, fontsize=8)
    ax.set_title("In-sample winner vs the market, 1972-2026, 5 bps per trade", fontsize=10)
    save(fig, "fig5_growth")

    checks, numbers = read_results("case_study_checks"), read_results("manuscript_numbers")
    rows = [("baseline", re.search(r"delay 1:.*?difference \+([\d.]+) \(se ([\d.]+)", checks)),
            ("+1 day lag", re.search(r"delay 2:.*?difference \+([\d.]+) \(se ([\d.]+)", checks)),
            ("1972-1998", re.search(r"1972-1998.*?difference \+([\d.]+) \(se ([\d.]+)", checks)),
            ("1999-2026", re.search(r"1999-2026.*?difference \+([\d.]+) \(se ([\d.]+)", checks))]
    mde = float(re.search(r"lags 11:.*?\(unadjusted\), ([\d.]+) \(Bonferroni", numbers).group(1))
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    for i, (label, match) in enumerate(rows):
        d, se = float(match.group(1)), float(match.group(2))
        ax.errorbar(d, -i, xerr=1.96 * se, fmt="o", color=BLUE, capsize=4)
        ax.text(-0.42, -i, label, va="center", ha="left", fontsize=9)
    ax.axvline(0, color="black", linewidth=1)
    ax.axvline(mde, color=RED, linestyle="--", linewidth=1)
    ax.text(mde + 0.01, -1.5, "smallest edge the\ncorrected test could\ndetect (80% power)", color=RED, fontsize=8,
            va="center")
    ax.set_xlim(-0.45, 0.65), ax.set_yticks([]), ax.set_xlabel("annual Sharpe edge over the market, 95% CI")
    ax.set_title("The edge is positive but within noise, and the test could not see it", fontsize=10)
    save(fig, "fig6_market_test")

    x = m[:, SETTINGS.index(SELECTED)]
    sharpes = m.mean(axis=0) / m.std(axis=0)
    sr, v, g3, g4 = sharpes[SETTINGS.index(SELECTED)], sharpes.var(ddof=1), skew(x), kurtosis(x, fisher=False)
    grid = np.unique(np.round(np.logspace(np.log10(2), 8, 60)))
    save_results("fig7_dsr_vs_n", ["N DSR"] + [f"{n:.0f} {dsr(sr, len(x), g3, g4, n, v):.6f}" for n in grid])
    saved = np.loadtxt(RESULTS_DIR / "fig7_dsr_vs_n.txt", skiprows=1)
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.semilogx(saved[:, 0], saved[:, 1], color=BLUE)
    ax.axhline(LEVEL, color="black", linestyle=":", linewidth=1)
    ax.axvline(93, color=GREY, linestyle="--", linewidth=1)
    ax.text(110, 0.90, "93 settings tried", color=GREY, fontsize=8)
    ax.set_xlabel("number of trials N (log scale)"), ax.set_ylabel("DSR of rule 15/225")
    ax.set_title("DSR stays near 1 until about 740,000 trials", fontsize=10)
    save(fig, "fig7_dsr_vs_n")


def main():
    cscv_diagram()
    real_data()
    dsr_panels()
    case_study()
    print("saved figures 2-7 and results/fig5_growth.txt, results/fig7_dsr_vs_n.txt")


if __name__ == "__main__":
    main()
