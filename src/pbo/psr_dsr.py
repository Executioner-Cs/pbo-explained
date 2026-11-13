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
    if kurt < (1 + skew**2) * (1 - 1e-12):        # relative tolerance for roundoff in sample moments only
        raise ValueError("raw kurtosis must be at least 1 + skew^2 (Pearson's inequality)")
    v = 1 - skew * sr + (kurt - 1) / 4 * sr**2
    if v <= 0:
        raise ValueError("1 - skew*SR + (kurt-1)/4*SR^2 must be positive")
    return v


def psr_z(sr, sr_star, n, skew=0.0, kurt=3.0):
    """The statistic inside SF Eq. 11 (p.9): PSR = Z[psr_z]."""
    _check_finite(sr=sr, sr_star=sr_star, n=n, skew=skew, kurt=kurt)
    if n < 2:
        raise ValueError("n must be at least 2: Eq. 11 uses sqrt(n - 1)")
    return (sr - sr_star) * math.sqrt(n - 1) / math.sqrt(_sr_variance_factor(sr, skew, kurt))


def psr(sr, sr_star, n, skew=0.0, kurt=3.0):
    """Probability that the true SR exceeds sr_star, given n observations (SF Eq. 11, p.9)."""
    return norm.cdf(psr_z(sr, sr_star, n, skew, kurt))


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

    Our derivation, an approximation: sqrt(t) SR is treated as N(0, factor), and SF Eq. 11 uses sqrt(t - 1) with
    factor 1. It does not integrate over the random sample standard deviation, skewness or kurtosis.
    """
    factor = np.asarray(factor, dtype=float)
    if not (np.isfinite(factor).all() and (factor >= 0).all()):
        raise ValueError("factor must be finite and >= 0 (a variance ratio)")
    with np.errstate(divide="ignore"):            # factor 0: the mean never moves, rate 0
        return 1 - norm.cdf(norm.ppf(level) / np.sqrt(factor * (t - 1) / t))


def ar1_psr_false_positive(phi, t, level):
    """Rate of PSR(0) > level for a zero-Sharpe stationary Gaussian AR(1). Our derivation, not a paper result.

    At SR = 0, sqrt(t) * SR -> N(0, F) with F the long-run variance factor of the sample mean, while SF Eq. 11
    assumes F = 1. Returns (finite-t approximation with F_t = 1 + 2 sum_{k<t} (1 - k/t) phi^k and Eq. 11's
    sqrt(t - 1), not an exact finite-sample law; large-t rate with F = (1 + phi)/(1 - phi)).
    """
    if not -1 < phi < 1:
        raise ValueError("phi must be strictly between -1 and 1 (stationary AR(1))")
    if isinstance(t, (bool, np.bool_)) or not isinstance(t, (int, np.integer)) or t < 2:
        raise ValueError("t must be an integer of at least 2")
    k = np.arange(1, t)
    f_t = 1 + 2 * np.sum((1 - k / t) * phi**k)
    finite = psr_false_positive(f_t, t, level)
    limit = 1 - norm.cdf(norm.ppf(level) / math.sqrt((1 + phi) / (1 - phi)))
    return finite, limit


def newey_west_factor(x, lags):
    """Long-run variance of the sample mean of x divided by its IID value, Bartlett weights (Newey and West 1987).

    F = 1 + 2 sum_{h=1}^{lags} (1 - h/(lags + 1)) rho_h. Our correction for serial correlation; not in SF.
    """
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or not np.isfinite(x).all():
        raise ValueError("x must be a finite 1-D array")
    d = x - x.mean()
    if isinstance(lags, (bool, np.bool_)) or not isinstance(lags, (int, np.integer)) or not 0 <= lags < len(d):
        raise ValueError("lags must be an integer, at least 0 and below the series length")
    var = d @ d
    if var == 0:
        raise ValueError("x has zero variance")
    return 1 + 2 * sum((1 - h / (lags + 1)) * (d[:-h] @ d[h:]) / var for h in range(1, lags + 1))


def psr_long_run(z, factor):
    """PSR with its variance multiplied by factor, from z = psr_z(...) (our correction; tested at SR* = 0 only).

    Takes z, not the PSR probability: a probability that has rounded to 1 cannot be corrected.
    """
    _check_finite(z=z, factor=factor)
    if not factor > 0:
        raise ValueError("factor must be positive")
    return norm.cdf(z / math.sqrt(factor))


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
    if not np.allclose(c, c.T) or np.abs(c).max() > 1 + 1e-12:
        raise ValueError("corr must be symmetric with entries between -1 and 1")
    if np.linalg.eigvalsh(c).min() < -1e-10 * m:   # singular is fine (duplicate strategies); negative is impossible
        raise ValueError("corr must be positive semidefinite")
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


def spa_sharpe(x, y, indices):
    """Hansen (2005) consistent SPA test of H0: no column of x has a higher Sharpe ratio than y. Not in SF or DSR.

    x: T x K strategy returns and y: T benchmark returns on the same days; indices: B x T resampled day indices (for
    example stationary bootstrap). The statistic uses Sharpe differences, as Sullivan, Timmermann and White (1999)
    do for the Reality Check. Returns (statistic, consistent p-value).
    """
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.ndim != 2 or y.ndim != 1 or len(x) != len(y) or not (np.isfinite(x).all() and np.isfinite(y).all()):
        raise ValueError("x must be T x K and y length T, both finite")
    t = len(y)

    def differences(rows):
        xs, ys = x[rows], y[rows]
        return xs.mean(axis=0) / xs.std(axis=0) - ys.mean() / ys.std()

    observed = differences(slice(None))
    boot = np.array([differences(rows) for rows in indices])
    omega = math.sqrt(t) * boot.std(axis=0)           # bootstrap sd of sqrt(t) times each difference
    if not (np.isfinite(omega).all() and (omega > 0).all()):
        raise ValueError("bootstrap standard deviations must be positive and finite")
    standardized = math.sqrt(t) * observed / omega
    statistic = max(standardized.max(), 0.0)
    # Consistent recentring: a clearly negative difference keeps its mean, every other is centred at zero.
    centre = np.where(standardized >= -math.sqrt(2 * math.log(math.log(t))), observed, 0.0)
    null = np.maximum((math.sqrt(t) * (boot - centre) / omega).max(axis=1), 0.0)
    return statistic, float(np.mean(null >= statistic))
