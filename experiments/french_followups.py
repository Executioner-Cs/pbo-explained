"""Step 4(b) follow-ups A, B, C. Design recorded in PROGRESS.md before the run.

A (description, our derivation): lag-1 autocorrelation of each industry's daily returns by period, and the PSR(0)
  false-positive rate that the industries' own autocorrelations predict for the 4(b) bootstrap at each block length,
  compared with the observed 4(b) rates (results/french_bootstrap.txt).
B (SF's own remedy, SF p.4 footnote 2 and p.15: sample at a frequency where autocorrelation is insignificant):
  weekly returns (non-overlapping 5-day sums), then the 4(b) PSR test with only the frequency changed.
  SF's claim holds if the exact 95% CI contains 5%.
C (our method check): PBO paired difference (original minus time-shuffled) with fixed block positions, as in 4(b),
  and with random block positions, at L = 20 and 60.
G1 (our correction): PSR(0) with a Newey-West long-run variance, on the same datasets as the plain PSR, L = 20, 60.
G2 (attribution): the PSR test on AR(5) residuals of each industry (linear autocorrelation removed), L = 20, 60.
G6 (sub-periods): the PSR test at L = 20 on 1971-1998 and on 1999-2026 separately.

Same frozen data, window and T as experiments/french_bootstrap.py. Our choices: 400 PBO datasets per C cell,
4-week blocks in B, seed.

Run from the repository root (a few minutes):  .venv/bin/python experiments/french_followups.py
"""
import re
from concurrent.futures import ProcessPoolExecutor   # runs the checks on several CPU cores

import numpy as np
from scipy.stats import kurtosis, skew

import french_bootstrap as fb
from french_bootstrap import LEVEL, S, T
from pbo import scenarios
from pbo.cscv import cscv
from pbo.french import ar_residuals, load_returns
from pbo.psr_dsr import newey_west_factor, psr, psr_false_positive, psr_long_run
from pbo.reporting import format_mean, format_rate, mean_with_se, read_results, save_results

# Settings
SPLIT = 19990101                                  # our choice: two halves of the window, 1971-1998 and 1999-2026
BLOCKS = (1, 5, 20, 60)                           # the 4(b) block lengths
WEEK = 5                                          # trading days per week
WEEKLY_BLOCK = 4                                  # our choice: 4 weeks, the calendar span of 20 days
DATASETS = 2000                                   # as in 4(b)
PBO_DATASETS = 400                                # our choice: twice 4(b), for a smaller paired SE
SEED = 20261113                                   # our choice, new
NW_LAGS = int(4 * (T / 100) ** (2 / 9))           # G1, Newey-West rule of thumb, our choice: 7
AR_ORDER = 5                                      # G2, our choice


def lag1(x):
    """Lag-1 sample autocorrelation of each column."""
    d = x - x.mean(axis=0)
    return (d[:-1] * d[1:]).sum(axis=0) / (d * d).sum(axis=0)


def describe_lag1(label, x):
    rho = lag1(x)
    band = 2 / np.sqrt(len(x))
    return (f"  {label}: {len(x)} rows, lag-1 autocorrelation mean {rho.mean():+.3f}, min {rho.min():+.3f}, "
            f"max {rho.max():+.3f}; {np.sum(np.abs(rho) > band)} of {x.shape[1]} industries outside +/- {band:.3f}")


def predicted_rate(x, block):
    """Average over industries of the PSR(0) false-positive rate predicted for a block bootstrap of x."""
    return psr_false_positive(scenarios.block_bootstrap_factor(x, block), T, LEVEL).mean()


def observed_rates():
    """{L: (hits, total)} of PSR(0) > LEVEL from the 4(b) results file."""
    text = read_results("french_bootstrap")          # observed 4(b) rates, compared in A
    header = f"T={T} N=49 S={S} datasets: {fb.DATASETS} (PSR, DSR), {fb.PBO_DATASETS} (PBO), seed={fb.SEED}."
    if header not in text:
        raise ValueError(f"french_bootstrap.txt is not from the current french_bootstrap.py settings; rerun it")
    blocks = [int(b) for b in re.findall(r"Block length L = (\d+)", text)]
    counts = re.findall(rf"PSR\(0\) > {re.escape(str(LEVEL))} on a random industry.*\((\d+)/(\d+)\)", text)
    if not len(blocks) == len(counts) == len(BLOCKS):
        raise ValueError(f"could not read one PSR count per block length from french_bootstrap.txt")
    return {b: (int(h), int(n)) for b, (h, n) in zip(blocks, counts)}


def psr_flags(panel, block, seed):
    """PSR(0) > LEVEL on a random industry of a block bootstrap of panel: (plain flags, Newey-West flags, G1)."""
    data_rng, target_rng = (np.random.default_rng(s) for s in seed.spawn(2))
    flags, nw_flags = [], []
    for _ in range(DATASETS):
        r = scenarios.block_bootstrap(data_rng, panel, T, block)
        x = r[:, target_rng.integers(r.shape[1])]
        value = psr(x.mean() / x.std(), 0.0, T, skew(x), kurtosis(x, fisher=False))
        flags.append(value > LEVEL)
        nw_flags.append(psr_long_run(value, newey_west_factor(x, NW_LAGS)) > LEVEL)
    return flags, nw_flags


def pbo_paired(data, block, random_start, seed):
    """C: PBO of each dataset minus PBO of the same dataset with its days shuffled."""
    data_rng, shuffle_rng = (np.random.default_rng(s) for s in seed.spawn(2))
    differences = []
    for _ in range(PBO_DATASETS):
        if random_start:                          # start inside the first block: edges no longer at multiples of L
            longer = scenarios.block_bootstrap(data_rng, data, T + block, block)
            start = data_rng.integers(block)
            r = longer[start:start + T]
        else:
            r = scenarios.block_bootstrap(data_rng, data, T, block)
        shuffled = scenarios.shuffle_time(shuffle_rng, r)
        differences.append(cscv(r, S)[0] - cscv(shuffled, S)[0])
    return differences


def main():
    dates, data, facts = load_returns()
    early, late = data[dates < SPLIT], data[dates >= SPLIT]
    weeks = len(data) // WEEK
    weekly = data[:weeks * WEEK].reshape(weeks, WEEK, -1).sum(axis=1)
    weekly = weekly - weekly.mean(axis=0)
    lines = facts + ["", f"T={T} S={S} seed={SEED}. Rates: exact 95% CI. Means: +/- one Monte Carlo SE.", ""]

    lines.append("A. Daily lag-1 autocorrelation by period (each period demeaned on its own)")
    lines.append(describe_lag1(f"full {dates[0]} to {dates[-1]}", data))
    lines.append(describe_lag1(f"early {dates[0]} to {dates[dates < SPLIT][-1]}", early))
    lines.append(describe_lag1(f"late {dates[dates >= SPLIT][0]} to {dates[-1]}", late))
    lines.append(f"A. PSR(0) > {LEVEL} rate predicted from the industries' autocorrelations vs observed in 4(b)")
    observed = observed_rates()
    for block in BLOCKS:
        p = predicted_rate(data, block)
        hits, total = observed[block]
        z = (hits / total - p) / np.sqrt(p * (1 - p) / total)
        lines.append(f"  L = {block}: predicted {p:.4f}, observed {hits / total:.4f} ({hits}/{total}), z = {z:+.2f}")
    lines.append(f"  by period at L = 20: early predicted {predicted_rate(early, 20):.4f}, "
                 f"late predicted {predicted_rate(late, 20):.4f}")
    lines.append("")

    residuals = ar_residuals(data, AR_ORDER)
    seeds = np.random.SeedSequence(SEED).spawn(11)   # children 0-4 as in the first follow-up run, 5-10 for G1, G2, G6
    cells = [(20, False), (20, True), (60, False), (60, True)]
    with ProcessPoolExecutor() as pool:           # one task per CPU core; each has its own seed
        weekly_job = pool.submit(psr_flags, weekly, WEEKLY_BLOCK, seeds[0])
        pbo_jobs = [pool.submit(pbo_paired, data, block, rand, seed) for (block, rand), seed in zip(cells, seeds[1:5])]
        g1_jobs = [pool.submit(psr_flags, data, block, seed) for block, seed in zip((20, 60), seeds[5:7])]
        g2_jobs = [pool.submit(psr_flags, residuals, block, seed) for block, seed in zip((20, 60), seeds[7:9])]
        g6_jobs = [pool.submit(psr_flags, half, 20, seed) for half, seed in zip((early, late), seeds[9:11])]
        weekly_flags = weekly_job.result()[0]
        differences = [job.result() for job in pbo_jobs]
        g1, g2, g6 = ([job.result() for job in jobs] for jobs in (g1_jobs, g2_jobs, g6_jobs))

    lines.append(f"B. Weekly returns: {weeks} weeks x {weekly.shape[1]} industries")
    lines.append(describe_lag1("weekly", weekly))
    lines.append(f"  predicted PSR(0) > {LEVEL} rate at {WEEKLY_BLOCK}-week blocks: {predicted_rate(weekly, WEEKLY_BLOCK):.4f}")
    lines.append(f"  PSR(0) > {LEVEL} on a random industry, T = {T} weeks, {WEEKLY_BLOCK}-week blocks "
                 f"(nominal 0.05): {format_rate(weekly_flags)}")
    lines.append("")

    lines.append(f"C. PBO paired difference, original minus time-shuffled, {PBO_DATASETS} datasets per cell")
    for (block, rand), diff in zip(cells, differences):
        mean, se = mean_with_se(diff)
        position = "random block positions" if rand else "fixed block positions "
        lines.append(f"  L = {block:>2}, {position}: {format_mean(diff)} (z = {mean / se:+.2f})")

    lines.append("")
    lines.append(f"G1. PSR(0) > {LEVEL} plain vs Newey-West variance ({NW_LAGS} lags), same datasets, random industry")
    for block, (plain, nw) in zip((20, 60), g1):
        lines.append(f"  L = {block}: plain {format_rate(plain)}; Newey-West {format_rate(nw)}")
    lines.append(f"G2. PSR(0) > {LEVEL} on AR({AR_ORDER}) residuals (linear autocorrelation removed)")
    lines.append(describe_lag1("residuals", residuals))
    for block, (plain, _) in zip((20, 60), g2):
        lines.append(f"  L = {block}: {format_rate(plain)}")
    lines.append(f"G6. PSR(0) > {LEVEL} by sub-period at L = 20, simulated vs follow-up A's prediction")
    for label, half, (plain, _) in zip(("early", "late"), (early, late), g6):
        p = predicted_rate(half, 20)
        z = (np.mean(plain) - p) / np.sqrt(p * (1 - p) / len(plain))
        lines.append(f"  {label}: predicted {p:.4f}, simulated {format_rate(plain)}, z = {z:+.2f}")

    print("\n".join(lines))
    save_results("french_followups", lines)


if __name__ == "__main__":
    main()
