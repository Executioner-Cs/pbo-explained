import numpy as np
from scipy.stats import norm


def expected_max_normal(n):
    """Approximate E[max of n iid N(0,1)] (PSEUDO Prop 2.1, Eq. 2.4, p.9; DSR Eq. 1, p.7)."""
    if n < 2:
        raise ValueError("n must be at least 2")
    g = np.euler_gamma
    return (1 - g) * norm.ppf(1 - 1 / n) + g * norm.ppf(1 - 1 / (n * np.e))


def min_btl_years(n, target_sharpe):
    """Years of data so the expected best annual Sharpe of n zero-edge trials equals target_sharpe (PSEUDO Theorem 3.1, Eq. 3.2, p.11)."""
    if target_sharpe <= 0:
        raise ValueError("target_sharpe must be positive")
    return (expected_max_normal(n) / target_sharpe) ** 2
