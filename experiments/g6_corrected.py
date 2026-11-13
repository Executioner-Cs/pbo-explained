"""Corrected G6 (step 4): PSR(0) > 0.95 by sub-period at L = 20, each period demeaned within itself.

Correction of G6 in experiments/french_followups.py (original output kept in results/french_followups.txt): the
original resampled each period without re-centring, so industry means were not zero. Design and prediction:
PROGRESS.md, "Corrected G6 design", recorded before this run. Everything else is as in the original: frozen data,
split, T, L = 20, 2000 datasets, random industry, and the same seeds (children 9 and 10 of SeedSequence(SEED).spawn(11)).

Run from the repository root:  .venv/bin/python experiments/g6_corrected.py
"""
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from french_bootstrap import LEVEL, T
from french_followups import DATASETS, SEED, SPLIT, predicted_rate, psr_flags
from pbo.french import demean_by_period, load_returns
from pbo.reporting import rate_with_ci, save_results

BLOCK = 20


def main():
    dates, data, facts = load_returns()
    periods = demean_by_period(dates, data, SPLIT)
    if max(np.abs(p.mean(axis=0)).max() for p in periods) >= 1e-12:
        raise ValueError("a period column does not have mean 0")
    seeds = np.random.SeedSequence(SEED).spawn(11)[9:11]   # the original G6 streams
    with ProcessPoolExecutor() as pool:
        flags = list(pool.map(psr_flags, periods, (BLOCK, BLOCK), seeds))

    lines = facts + ["", f"Corrected G6: PSR(0) > {LEVEL}, L = {BLOCK}, T = {T}, {DATASETS} datasets per period, "
                         f"seed {SEED} children 9 and 10, each period demeaned within itself.",
                     "Approximation: our derivation with the partial-block factor, averaged over industries (not exact).",
                     "Original (uncentred) G6: results/french_followups.txt.", ""]
    for label, period, (plain, _) in zip(("1971-1998", "1999-2026"), periods, flags):
        p = predicted_rate(period, BLOCK)
        rate, hits, total, low, high = rate_with_ci(plain)
        lines.append(f"{label}: simulated {rate:.4f} [{low:.4f}, {high:.4f}] ({hits}/{total}); approximation "
                     f"{p:.4f}; simulated minus approximation {rate - p:+.4f}; approximation inside the 95% CI: "
                     f"{'yes' if low <= p <= high else 'no'}")
    print("\n".join(lines))
    save_results("g6_corrected", lines)


if __name__ == "__main__":
    main()
