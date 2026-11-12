"""PSR, MinTRL (SF = papers/sharpe-frontier.pdf) and DSR (papers/deflated-sharpe.pdf).

All Sharpe ratios are non-annualized, in the frequency of the returns (SF p.9).
kurt is raw kurtosis, 3 for Normal returns (SF p.10, DSR p.10), not excess kurtosis.
"""
import math

import numpy as np
from scipy.stats import norm

from pbo.minbtl import expected_max_normal


def _check_finite(**values):
    for name, v in values.items():
        if not math.isfinite(v):
            raise ValueError(f"{name} must be a finite number, got {v}")


def _sr_variance_factor(sr, skew, kurt):
    # 1 - skew*SR + (kurt - 1)/4 * SR^2. Equals Eq. 8's 1 + SR^2/2 - skew*SR + (kurt - 3)/4 * SR^2 (SF p.8).
    v = 1 - skew * sr + (kurt - 1) / 4 * sr**2
    if v <= 0:
        raise ValueError("1 - skew*SR + (kurt-1)/4*SR^2 must be positive")
    return v


def psr(sr, sr_star, n, skew=0.0, kurt=3.0):
    """Probability that the true SR exceeds sr_star, given n observations (SF Eq. 11, p.9)."""
    _check_finite(sr=sr, sr_star=sr_star, n=n, skew=skew, kurt=kurt)
    if n < 2:
        raise ValueError("n must be at least 2: Eq. 11 uses sqrt(n - 1)")
    return norm.cdf((sr - sr_star) * math.sqrt(n - 1) / math.sqrt(_sr_variance_factor(sr, skew, kurt)))


def min_trl(sr, sr_star, alpha, skew=0.0, kurt=3.0):
    """Observations needed so that PSR(sr_star) = 1 - alpha (SF Eq. 13, p.11). Defined for sr > sr_star."""
    _check_finite(sr=sr, sr_star=sr_star, alpha=alpha, skew=skew, kurt=kurt)
    if sr <= sr_star:
        raise ValueError("MinTRL needs sr > sr_star (SF p.10)")
    if not 0 < alpha < 0.5:
        # Squaring Z_alpha hides its sign: alpha > 0.5 would return the n for 1 - alpha instead.
        raise ValueError("alpha must be in (0, 0.5)")
    return 1 + _sr_variance_factor(sr, skew, kurt) * (norm.ppf(1 - alpha) / (sr - sr_star)) ** 2


def sr0(n_trials, var_trials):
    """Expected max SR of n_trials zero-skill trials with SR variance var_trials (DSR Eq. 2, p.8)."""
    _check_finite(n_trials=n_trials, var_trials=var_trials)
    if var_trials < 0:
        raise ValueError("var_trials is a variance and cannot be negative")
    return math.sqrt(var_trials) * expected_max_normal(n_trials)


def dsr(sr, t, skew, kurt, n_trials, var_trials):
    """Deflated Sharpe Ratio: PSR with benchmark SR0 (DSR Eq. 2, p.8). t = sample length."""
    return psr(sr, sr0(n_trials, var_trials), t, skew, kurt)


def psr_false_positive(factor, t, level):
    """Rate of PSR(0) > level at true SR = 0 when the variance of the sample mean is factor times its IID value.

    Our derivation: sqrt(t) SR -> N(0, factor), and SF Eq. 11 uses sqrt(t - 1) with factor 1.
    """
    return 1 - norm.cdf(norm.ppf(level) / np.sqrt(np.asarray(factor) * (t - 1) / t))


def ar1_psr_false_positive(phi, t, level):
    """Rate of PSR(0) > level for a zero-Sharpe stationary Gaussian AR(1). Our derivation, not a paper result.

    At SR = 0, sqrt(t) * SR -> N(0, F) with F the long-run variance factor of the sample mean, while SF Eq. 11
    assumes F = 1. Returns (finite-t rate with F_t = 1 + 2 sum_{k<t} (1 - k/t) phi^k and Eq. 11's sqrt(t - 1),
    large-t rate with F = (1 + phi)/(1 - phi)).
    """
    k = np.arange(1, t)
    f_t = 1 + 2 * np.sum((1 - k / t) * phi**k)
    finite = psr_false_positive(f_t, t, level)
    limit = 1 - norm.cdf(norm.ppf(level) / math.sqrt((1 + phi) / (1 - phi)))
    return finite, limit


def newey_west_factor(x, lags):
    """Long-run variance of the sample mean of x divided by its IID value, Bartlett weights (Newey and West 1987).

    F = 1 + 2 sum_{h=1}^{lags} (1 - h/(lags + 1)) rho_h. Our correction for serial correlation; not in SF.
    """
    d = np.asarray(x, dtype=float) - np.mean(x)
    if not 0 <= lags < len(d):
        raise ValueError("lags must be at least 0 and below the series length")
    var = d @ d
    if var == 0:
        raise ValueError("x has zero variance")
    return 1 + 2 * sum((1 - h / (lags + 1)) * (d[:-h] @ d[h:]) / var for h in range(1, lags + 1))


def psr_long_run(psr_value, factor):
    """PSR with its variance multiplied by factor (our correction; tested at SR* = 0 only)."""
    if not factor > 0:
        raise ValueError("factor must be positive")
    return norm.cdf(norm.ppf(psr_value) / math.sqrt(factor))


def implied_n(corr):
    """Implied number of independent trials from an M x M correlation matrix (DSR Appendix 3, p.14).

    Eq. 8: rho = average off-diagonal correlation. Eq. 9: N = rho + (1 - rho) M.
    """
    c = np.asarray(corr, dtype=float)
    m = len(c)
    if c.shape != (m, m) or m < 2:
        raise ValueError("corr must be a square matrix, at least 2 x 2")
    if not np.isfinite(c).all():
        raise ValueError("corr has NaN or inf (a strategy with zero variance gives NaN)")
    if not np.allclose(np.diag(c), 1.0):
        raise ValueError("corr must have a unit diagonal (a covariance matrix was passed?)")
    rho = (c.sum() - m) / (m * (m - 1))
    # p.14: Eq. 9 runs from rho = 0 (N = M) to rho = 1 (N = 1). Our choice (the paper does not clamp): a slightly
    # negative sample rho is noise around 0 for unrelated strategies, so it counts as 0 (N = M), never above M.
    rho = max(rho, 0.0)
    return rho + (1 - rho) * m


def sharpe_diff(x, y, lags):
    """Per-period Sharpe difference and paired Bartlett HAC standard error, with ddof=0.

    Derived from Ledoit-Wolf (2008), January working paper p.4 Eqs.1-5: projecting their four-moment
    covariance onto the gradient gives each series' influence z - SR*(z^2 - 1)/2, z=(return-mean)/sd.
    Differencing the influences retains all cross-covariances without forming a 4x4 covariance matrix.
    Our choices: Bartlett kernel, specified lag count, no T/(T-4) scaling. Zero lags omits serial covariance.
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 1 or x.shape != y.shape or not (np.isfinite(x).all() and np.isfinite(y).all()):
        raise ValueError("x and y must be finite 1-D arrays of the same length")
    t = len(x)
    if isinstance(lags, (bool, np.bool_)) or not isinstance(lags, (int, np.integer)) or not 0 <= lags < t:
        raise ValueError("lags must be an integer, at least 0 and below the series length")
    values = np.column_stack([x, y])
    # Power-of-two normalization is exact in binary and avoids overflow/underflow when squaring returns.
    values = np.ldexp(values, -np.frexp(np.max(np.abs(values), axis=0))[1])
    mean, sd = values.mean(axis=0), values.std(axis=0)
    if not (sd > 0).all():
        raise ValueError("x and y must have positive variance")
    sr, z = mean / sd, (values - mean) / sd
    influence = z - sr * (z*z - 1) / 2
    paired = influence[:, 0] - influence[:, 1]
    paired -= paired.mean()
    long_run = paired @ paired + 2 * sum(
        (1 - h / (lags + 1)) * (paired[h:] @ paired[:-h]) for h in range(1, lags + 1))
    if not np.isfinite(long_run) or not np.isfinite(sr).all():
        raise ValueError("Sharpe difference or its variance is not finite")
    # Bartlett is positive semidefinite; clip negative floating-point roundoff at zero.
    return sr[0] - sr[1], math.sqrt(max(0., long_run)) / t
