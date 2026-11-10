"""PSR, MinTRL (SF = papers/sharpe-frontier.pdf) and DSR (papers/deflated-sharpe.pdf).

All Sharpe ratios are non-annualized, in the frequency of the returns (SF p.9).
kurt is raw kurtosis, 3 for Normal returns (SF p.10, DSR p.10), not excess kurtosis.
"""
import math

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
