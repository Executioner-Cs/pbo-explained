"""Small helpers for reporting Monte Carlo results."""
import numpy as np
from scipy.stats import binomtest


def rate_with_ci(flags):
    """Share of True values, with an exact (Clopper-Pearson) 95% confidence interval.

    Returns (rate, hits, total, low, high). Exact intervals stay valid for rates near 0 or 1.
    """
    hits, total = int(np.sum(flags)), len(flags)
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
