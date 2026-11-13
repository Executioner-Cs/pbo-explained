"""Exploratory delayed alpha sensitivity; design in docs/submission/evidence/delayed-alpha-design.md.

Run from repository root: .venv/bin/python experiments/delayed_alpha.py
"""
from pathlib import Path
import numpy as np
from scipy.stats import norm
from pbo.french import load_market
from pbo.strategies import crossover_panel
from pbo.psr_dsr import alpha_hac, spa_pvalue
from pbo.scenarios import stationary_bootstrap_indices

OUT = Path(__file__).resolve().parents[1] / "results"
SETTINGS = [(f, s) for f in range(5, 55, 5) for s in range(25, 275, 25) if f < s]
SEED, B, BLOCK = 20261118, 2000, 20


def main():
    dates, market, rf = load_market()
    start, panel = crossover_panel(np.cumprod(1 + market + rf), market, SETTINGS, 0.0005, 16, delay=2)
    market = market[start:]
    n = len(market)
    observed = np.array([alpha_hac(panel[:, k], market, 11) for k in range(len(SETTINGS))])
    rng = np.random.default_rng(SEED)
    boot = np.empty((B, len(SETTINGS)))
    for i in range(B):
        rows = stationary_bootstrap_indices(rng, n, n, BLOCK)
        x, y = market[rows], panel[rows]
        beta = ((y - y.mean(axis=0)) * (x - x.mean())[:, None]).mean(axis=0) / x.var()
        boot[i] = y.mean(axis=0) - beta * x.mean()
        if (i + 1) % 250 == 0:
            print(f"Bootstrap {i + 1}/{B}", flush=True)
    statistic, p = spa_pvalue(observed[:, 0], boot, n)
    np.savez_compressed(OUT / "delayed_alpha_bootstrap.npz", observed=observed, bootstrap=boot,
                        settings=np.array(SETTINGS), seed=SEED, block=BLOCK, delay=2, cost=0.0005,
                        start_date=dates[start], end_date=dates[-1], sample_size=n)
    tstats = observed[:, 0] / observed[:, 2]
    selected = int(np.argmax(panel.mean(axis=0) / panel.std(axis=0)))
    lines = ["RECOMPUTED: exploratory delay-2 alpha sensitivity; no numerical prediction.",
             f"Dates {dates[start]} to {dates[-1]}, T={n}, settings={len(SETTINGS)}, cost=5bps, delay=2.",
             f"SPA seed={SEED}, B={B}, mean block={BLOCK}, statistic={statistic:.8f}, p={p:.8f}.",
             f"Monte Carlo standard error at observed p: {np.sqrt(p * (1-p) / B):.8f}.",
             f"Delayed Sharpe winner: {SETTINGS[selected]}; original selected setting: (15, 225).",
             f"HAC t > 1.645: {(tstats > 1.645).sum()}; Bonferroni one-sided 5%: {(tstats > norm.isf(0.05 / len(SETTINGS))).sum()}.",
             "Alpha and SE are daily; annual alpha is arithmetic x250. HAC Bartlett lags=11.",
             "fast,slow,alpha_daily,beta,se_daily,t,one_sided_p,alpha_annual_percent"]
    for (f, s), (a, beta, se), t in zip(SETTINGS, observed, tstats):
        lines.append(f"{f},{s},{a:.12g},{beta:.12g},{se:.12g},{t:.12g},{norm.sf(t):.12g},{a * 25000:.12g}")
    text = "\n".join(lines) + "\n"
    (OUT / "delayed_alpha.txt").write_text(text)
    print(text, flush=True)


if __name__ == "__main__":
    main()
