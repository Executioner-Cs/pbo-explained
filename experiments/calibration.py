"""Step 4: how PSR, DSR and PBO behave when one IID Normal assumption is broken.

Every fixed strategy-return column has zero unconditional mean and Sharpe. AR(1) remains conditionally predictable.

For each scenario, 2,000 datasets of T days x N strategies:
  PSR: PSR(0) of strategy 0, a fixed strategy nobody selected. Should say "skilled" 5% of the time
       (SF p.12 reads PSR(0) > 0.95 as 95% confidence).
  DSR: DSR of the best strategy by Sharpe, with N = 100 and V = variance of the 100 Sharpes (ddof 1).
       No paper gives a target rate for a best-of-N pick, so compare each row with the IID baseline row.
       Correlated scenarios also report DSR with the implied number of independent trials (DSR Eq. 9, p.14).
       Implied N is the lead row (DSR defines N as independent trials); N = 100 is the naive comparator.
       Caveat (DSR p.15): with T < M(M-1)/2, here 1248 < 4950, that average correlation is unreliable.
  PBO: CSCV on the first 200 datasets. Mean PBO (0.5 is exact only for returns independent over time)
       and the share accepted by the "customary" rule PBO <= 0.05 (PBO p.14).
  GARCH scenarios also score PBO on the same matrix with its days shuffled (one common row order).
       The paired difference is the effect of randomized time order on PBO, conditional on the same return rows.
       PSR and DSR ignore order, so the shuffle cannot change them.

Paper inputs: N = 100 and T = 1250 (DSR p.9); S = 16 (PBO p.11, motivated on p.22); 95% (SF p.11).
Our choices: T = 1248 so 16 blocks fit, scenario levels, datasets, seed, moment estimators.

Run from the repository root (takes several minutes):  .venv\\Scripts\\python.exe experiments\\calibration.py
"""
from pathlib import Path

import numpy as np
from scipy.stats import kurtosis, skew

from pbo import paper_values as pv
from pbo import scenarios
from pbo.cscv import cscv
from pbo.psr_dsr import dsr, implied_n, psr
from pbo.reporting import format_mean, format_rate

RESULTS_FILE = Path(__file__).parent.parent / "results" / "calibration.txt"

# Settings
N = pv.DSR_EX_N                                   # DSR p.9
S = pv.PBO_S16                                    # PBO p.11
T = pv.DSR_EX_T // S * S                          # DSR p.9 gives 1250; 1248 so S = 16 divides it
LEVEL = pv.MINTRL_EX_CONFIDENCE                   # SF p.11
ACCEPT = pv.PBO_ACCEPT_LEVEL                      # PBO p.14
DATASETS = 2000                                   # our choice: per scenario, for PSR and DSR
PBO_DATASETS = 200                                # our choice: CSCV is slower
SEED = 20261110                                   # our choice

# (name, make returns, extra check). Levels: our choice (approved grid).
# Extra checks: "shuffle" = paired time-shuffled PBO control (GARCH); "implied_n" = DSR with implied N.
SCENARIOS = [
    ("iid Normal (baseline)", lambda rng: scenarios.iid(rng, T, N), None),
    ("AR(1) phi=0.1", lambda rng: scenarios.ar1(rng, T, N, 0.1), None),
    ("AR(1) phi=0.3", lambda rng: scenarios.ar1(rng, T, N, 0.3), None),
    ("GARCH a=0.05 b=0.90", lambda rng: scenarios.garch(rng, T, N, 0.05, 0.90), "shuffle"),
    ("GARCH a=0.10 b=0.85", lambda rng: scenarios.garch(rng, T, N, 0.10, 0.85), "shuffle"),
    ("Student-t nu=8", lambda rng: scenarios.student_t(rng, T, N, 8), None),
    ("Student-t nu=5", lambda rng: scenarios.student_t(rng, T, N, 5), None),
    ("correlated rho=0.3", lambda rng: scenarios.correlated(rng, T, N, 0.3), "implied_n"),
    ("correlated rho=0.7", lambda rng: scenarios.correlated(rng, T, N, 0.7), "implied_n"),
]


def run_scenario(name, make_returns, extra, seed):
    """Run one scenario and return its lines for the results file."""
    rng = np.random.default_rng(seed)
    shuffle_rng = np.random.default_rng(seed.spawn(1)[0])    # own stream, so the data match earlier runs
    is_garch = extra == "shuffle"
    is_correlated = extra == "implied_n"

    psr_flags, dsr_flags, dsr_implied_flags, implied_ns = [], [], [], []
    pbos, shuffled_pbos, pbo_differences = [], [], []

    for dataset in range(DATASETS):
        returns = make_returns(rng)
        sharpes = returns.mean(axis=0) / returns.std(axis=0)    # per-period Sharpe, ddof 0

        # PSR on a fixed strategy that was not selected
        fixed = returns[:, 0]
        psr_value = psr(sharpes[0], 0.0, T, skew(fixed), kurtosis(fixed, fisher=False))
        psr_flags.append(psr_value > LEVEL)

        # DSR on the best strategy
        best = int(np.argmax(sharpes))
        best_skew = skew(returns[:, best])
        best_kurt = kurtosis(returns[:, best], fisher=False)
        variance = sharpes.var(ddof=1)
        dsr_flags.append(dsr(sharpes[best], T, best_skew, best_kurt, N, variance) > LEVEL)

        if is_correlated:
            n_independent = implied_n(np.corrcoef(returns.T))
            implied_ns.append(n_independent)
            # Eq. 2.4 needs N >= 2. Does not bind here: Eq. 9 gives 0.7 + 0.3 * 100 = 30.7 at rho = 0.7.
            n_used = max(n_independent, 2)
            dsr_implied_flags.append(dsr(sharpes[best], T, best_skew, best_kurt, n_used, variance) > LEVEL)

        # PBO on the first PBO_DATASETS datasets
        if dataset < PBO_DATASETS:
            pbos.append(cscv(returns, S)[0])
            if is_garch:
                shuffled = scenarios.shuffle_time(shuffle_rng, returns)
                shuffled_pbo = cscv(shuffled, S)[0]
                shuffled_pbos.append(shuffled_pbo)
                pbo_differences.append(pbos[-1] - shuffled_pbo)

    pbos = np.array(pbos)
    lines = [
        name,
        f"  PSR(0) > {LEVEL} on a fixed strategy (nominal 0.05): {format_rate(psr_flags)}",
        f"  DSR > {LEVEL} on best of {N}, N = {N}:            {format_rate(dsr_flags)}",
    ]
    if is_correlated:
        lines.append(f"  DSR > {LEVEL} on best, N = implied N (mean +/- MC SE "
                     f"{format_mean(implied_ns)}): {format_rate(dsr_implied_flags)}")
    lines += [
        f"  PBO mean (IID-null benchmark 0.5):                {format_mean(pbos)}",
        f"  PBO <= {ACCEPT} (zero-edge set accepted):          {format_rate(pbos <= ACCEPT)}",
    ]
    if is_garch:
        lines.append(f"  PBO mean after time shuffle:                    {format_mean(shuffled_pbos)}")
        lines.append(f"  PBO paired: original minus time-shuffled:         {format_mean(pbo_differences)}")
    lines.append("")
    return lines


def main():
    lines = [
        f"T={T} N={N} S={S} datasets: {DATASETS} (PSR, DSR), {PBO_DATASETS} (PBO), seed={SEED}. "
        "All fixed strategy columns have zero unconditional mean and Sharpe.",
        "Rates: share flagged, exact 95% CI in brackets. Means: +/- one Monte Carlo SE.",
        "",
    ]
    seeds = np.random.SeedSequence(SEED).spawn(len(SCENARIOS))   # one independent stream per scenario
    for (name, make_returns, extra), seed in zip(SCENARIOS, seeds):
        block = run_scenario(name, make_returns, extra, seed)
        print("\n".join(block), flush=True)
        lines += block
    RESULTS_FILE.parent.mkdir(exist_ok=True)
    RESULTS_FILE.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
