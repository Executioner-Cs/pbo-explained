"""Step 4(b): PSR, DSR and PBO on real dependence, with the edge removed.

An extension, not a reproduction of a paper: the 49 columns are industries, not 49 settings of one
trading rule. It measures how the paper statistics behave when candidate return series have real-market
distributions and dependence (observed calibration error). It does not estimate whether a real strategy
search was overfit; that is step 5. PSR is derived for IID returns (SF p.4, p.15), but SF also states its
results stay valid for stationary, ergodic returns (p.4, citing Opdyke). That claim is asymptotic (SF p.11).
4(b) measures finite-sample calibration at T = 1248 on real data, a consequence of the claim, not a proof
against it. L = 1 is SF's IID non-Normal setting.

Data: Kenneth French 49 Industry Portfolios, daily, value-weighted, fixed window 1971-07-01 to 2026-09-30.
The series starts in 1926; Softw has missing values until 1971-03-11. Our choice: start at the first July
(portfolios are formed at the end of June) with all 49 industries present, a modern market period.
Each industry is demeaned once over the window, so its average return is 0. This removes the unconditional
average only. Autocorrelation, volatility clustering and lead/lag patterns between industries stay.

Each dataset is a circular block bootstrap of whole days (all 49 industries of one day stay together):
  keeps: the empirical distribution and fat tails; same-day relationships between industries.
  partly keeps: autocorrelation and volatility clustering at short lags. Two days h apart stay neighbours
    with probability 1 - h/L averaged over output positions (block edges sit at fixed multiples of L),
    so dependence fades as h approaches the block length L.
  destroys: dependence across block edges, long regimes, and the order of regimes.
Block lengths L = 1 (independent days, the benchmark), 5, 20 (primary), 60, fixed before any run.

For each L, 2,000 datasets of T days x 49 industries:
  PSR: PSR(0) of one industry drawn uniformly at random (own random stream, never chosen by performance).
  DSR: DSR of the best industry by Sharpe, with implied N (DSR Eq. 9, lead row) and N = 49 (comparator).
       Also the paired per-dataset difference of the two accept decisions, with its paired MC SE.
       DSR p.15's short-sample inequality T < M(M-1)/2 is not triggered, 1248 > 1176, but only by 72
       observations; the paper does not claim that exceeding it guarantees a reliable implied N.
       Our reasoning, not the paper's: block dependence lowers the effective sample.
  PBO: CSCV on the first 200 datasets. PBO counts logit <= 0 (PBO Sec 3.1, p.13), i.e. OOS rank <= 25
       of 49 with rank 1 = worst. Counting the logit = 0 atom (rank 25) is our reading of the integral bound;
       Def 2.2's strict median (p.10) would give 24/49. For exchangeable trials P = 25/49 = 0.5102. The
       industries differ in volatility, tails and correlation, so 25/49 is a reference, not an exact null.
       For L > 1 also the same matrix with its days shuffled (paired control for time order).
       PSR and DSR ignore order, so the shuffle cannot change them.

Paper inputs: T = 1250 (DSR p.9), S = 16 (PBO p.11 example, p.22 rationale), 95% (SF p.11). Our choices: window, block lengths,
datasets, seed, and the resampling method (fixed-length circular block bootstrap, defined here).

Run from the repository root (takes several minutes):  .venv/bin/python experiments/french_bootstrap.py
"""
from concurrent.futures import ProcessPoolExecutor   # runs the block lengths on several CPU cores

import numpy as np
from scipy.stats import kurtosis, skew

from pbo import paper_values as pv
from pbo import scenarios
from pbo.cscv import cscv
from pbo.french import load_returns
from pbo.psr_dsr import dsr, implied_n, psr
from pbo.reporting import format_mean, format_rate, save_results

# Settings (data window and snapshot: src/pbo/french.py)
S = pv.PBO_S16                                    # PBO p.11, p.22; 78-day partitions here (L = 60 often spans two)
T = pv.DSR_EX_T // S * S                          # DSR p.9 gives 1250; 1248 so S = 16 divides it
LEVEL = pv.MINTRL_EX_CONFIDENCE                   # SF p.11
ACCEPT = pv.PBO_ACCEPT_LEVEL                      # PBO p.14
BLOCKS = (1, 5, 20, 60)                           # our choice, 20 is primary
DATASETS = 2000                                   # our choice: per block length, for PSR and DSR
PBO_DATASETS = 200                                # our choice: CSCV is slower
SEED = 20261112                                   # our choice


def run_block(data, block, seed):
    """Run one block length and return its lines for the results file."""
    data_rng, target_rng, shuffle_rng = (np.random.default_rng(s) for s in seed.spawn(3))
    n = data.shape[1]
    psr_flags, dsr_flags, dsr_implied_flags, implied_ns, dsr_differences = [], [], [], [], []
    pbos, shuffled_pbos, pbo_differences = [], [], []

    for dataset in range(DATASETS):
        returns = scenarios.block_bootstrap(data_rng, data, T, block)
        sharpes = returns.mean(axis=0) / returns.std(axis=0)    # per-period Sharpe, ddof 0

        # PSR on one industry drawn at random, not by performance
        target = target_rng.integers(n)
        x = returns[:, target]
        psr_flags.append(psr(sharpes[target], 0.0, T, skew(x), kurtosis(x, fisher=False)) > LEVEL)

        # DSR on the best industry, with implied N and with N = 49
        best = int(np.argmax(sharpes))
        best_skew = skew(returns[:, best])
        best_kurt = kurtosis(returns[:, best], fisher=False)
        variance = sharpes.var(ddof=1)                          # our choice: DSR Eq. 2 does not fix ddof
        # implied N < 2 would need average correlation > 47/48; dsr raises if it ever happens
        n_independent = implied_n(np.corrcoef(returns.T))
        implied_ns.append(n_independent)
        dsr_implied_flags.append(dsr(sharpes[best], T, best_skew, best_kurt, n_independent, variance) > LEVEL)
        dsr_flags.append(dsr(sharpes[best], T, best_skew, best_kurt, n, variance) > LEVEL)
        dsr_differences.append(int(dsr_implied_flags[-1]) - int(dsr_flags[-1]))   # same dataset: paired

        # PBO on the first PBO_DATASETS datasets
        if dataset < PBO_DATASETS:
            pbos.append(cscv(returns, S)[0])
            if block > 1:
                shuffled_pbo = cscv(scenarios.shuffle_time(shuffle_rng, returns), S)[0]
                shuffled_pbos.append(shuffled_pbo)
                pbo_differences.append(pbos[-1] - shuffled_pbo)

    pbos = np.array(pbos)
    reference = (n + 1) // 2 / n                             # share of ranks with logit <= 0
    lines = [
        f"Block length L = {block}" + (" (primary)" if block == 20 else ""),
        f"  PSR(0) > {LEVEL} on a random industry (nominal 0.05):   {format_rate(psr_flags)}",
        f"  DSR > {LEVEL} on best, N = implied N ({format_mean(implied_ns)}): {format_rate(dsr_implied_flags)}",
        f"  implied N per-dataset SD:                             {np.std(implied_ns, ddof=1):.2f}",
        f"  DSR > {LEVEL} on best, N = {n} (naive comparator):        {format_rate(dsr_flags)}",
        f"  DSR paired: implied-N accepts minus N = {n} accepts:     {format_mean(dsr_differences)}",
        f"  PBO mean (exchangeable reference {(n + 1) // 2}/{n} = {reference:.4f}): {format_mean(pbos)}",
        f"  PBO per-dataset SD:                                   {pbos.std(ddof=1):.3f}",
        f"  PBO <= {ACCEPT} (zero-edge set accepted):              {format_rate(pbos <= ACCEPT)}",
    ]
    if block > 1:
        lines.append(f"  PBO mean after time shuffle:                          {format_mean(shuffled_pbos)}")
        lines.append(f"  PBO per-dataset SD after time shuffle:                {np.std(shuffled_pbos, ddof=1):.3f}")
        lines.append(f"  PBO paired: original minus time-shuffled:            {format_mean(pbo_differences)}")
    lines.append("")
    return lines


def main():
    _, data, facts = load_returns()
    lines = facts + [
        "",
        f"T={T} N={data.shape[1]} S={S} datasets: {DATASETS} (PSR, DSR), {PBO_DATASETS} (PBO), seed={SEED}.",
        "Rates: share flagged, exact 95% CI in brackets. Means: +/- one Monte Carlo SE.",
        "Both cover Monte Carlo error only, conditional on the observed 1971-2026 sample.",
        "",
    ]
    print("\n".join(lines), flush=True)
    seeds = np.random.SeedSequence(SEED).spawn(len(BLOCKS))   # one independent stream per block length
    # One block length per CPU core. Each has its own seed, so the results do not depend on which core runs it.
    with ProcessPoolExecutor() as pool:
        for block_lines in pool.map(run_block, [data] * len(BLOCKS), BLOCKS, seeds):
            print("\n".join(block_lines), flush=True)
            lines += block_lines
    save_results("french_bootstrap", lines)


if __name__ == "__main__":
    main()
