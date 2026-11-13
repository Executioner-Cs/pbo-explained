"""Small helpers for reporting Monte Carlo results and saving them to results/."""
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

RESULTS_DIR = Path(__file__).resolve().parents[2] / "results"   # repo/results, wherever the script is run from


def rate_with_ci(flags):
    """Share of True values, with an exact (Clopper-Pearson) 95% confidence interval.

    Returns (rate, hits, total, low, high). Exact intervals stay valid for rates near 0 or 1.
    """
    flags = np.asarray(flags)
    if flags.dtype != bool or flags.size == 0:
        raise ValueError("flags must be a nonempty sequence of booleans")
    hits, total = int(flags.sum()), flags.size
    ci = binomtest(hits, total).proportion_ci()
    return hits / total, hits, total, ci.low, ci.high


def mean_with_se(values):
    """Mean and its Monte Carlo standard error, sd / sqrt(n) with ddof = 1."""
    values = np.asarray(values, dtype=float)
    return values.mean(), values.std(ddof=1) / np.sqrt(values.size)


def format_rate(flags):
    """'rate [low, high] (hits/total)' with the exact 95% interval."""
    rate, hits, total, low, high = rate_with_ci(flags)
    return f"{rate:.4f} [{low:.4f}, {high:.4f}] ({hits}/{total})"


def format_mean(values):
    """'mean +/- standard error'."""
    mean, se = mean_with_se(values)
    return f"{mean:.3f} +/- {se:.3f}"


def save_results(name, lines):
    """Write lines to results/<name>.txt, one per line."""
    RESULTS_DIR.mkdir(exist_ok=True)
    (RESULTS_DIR / f"{name}.txt").write_text("\n".join(lines) + "\n")


def read_results(name):
    """Text of results/<name>.txt."""
    return (RESULTS_DIR / f"{name}.txt").read_text()
