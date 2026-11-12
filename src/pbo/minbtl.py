import numpy as np
from scipy.stats import norm


def expected_max_normal(n):
    """Approximate E[max of n iid N(0,1)] (PSEUDO Prop 2.1, Eq. 2.4, p.9; DSR Eq. 1, p.7)."""
    if np.ndim(n) != 0 or not np.isfinite(n) or n < 2:  # Eq. 2.4 is undefined at n = 1.
        raise ValueError("n must be a finite scalar at least 2")
    g = np.euler_gamma
    # Survival quantiles avoid rounding 1 - 1/n to 1 for large finite trial counts.
    return (1 - g) * norm.isf(1 / n) + g * norm.isf((1 / n) / np.e)


def min_btl_years(n, target_sharpe):
    """Years of data so the expected best annual Sharpe of n zero-edge trials equals target_sharpe (PSEUDO Theorem 3.1, Eq. 3.2, p.11)."""
    if np.ndim(target_sharpe) != 0 or not np.isfinite(target_sharpe) or target_sharpe <= 0:
        raise ValueError("target_sharpe must be a positive finite scalar")
    return (expected_max_normal(n) / target_sharpe) ** 2
