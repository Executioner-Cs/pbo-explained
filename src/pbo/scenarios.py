"""Return scenarios for the step 4 calibration study.

Each function returns a T x N array of returns with true mean 0 (zero edge) and unconditional variance 1.
Parameter levels are chosen by the caller. What each one departs from the IID Normal baseline:
  ar1: serial correlation only (Normal marginals).
  garch: volatility clustering AND fat tails together (Gaussian GARCH has unconditional excess kurtosis).
  shuffle_time: control for garch. One common row permutation preserves the rows and randomizes temporal order.
     Paired use: score PBO on a GARCH matrix and on its shuffle. Only order-dependent statistics (PBO via
     CSCV blocks) can differ. PSR and DSR are order-invariant, so they are identical by algebra.
     garch vs iid = combined departure (clustering plus fat tails).
  student_t: fat tails only (independent draws).
  correlated: correlation across strategies only.
"""
import math

import numpy as np
from scipy.signal import lfilter

GARCH_BURN_IN = 500  # our choice: steps discarded so the variance process forgets its starting value


def iid(rng, t, n):
    """Baseline: IID standard Normal."""
    return rng.standard_normal((t, n))


def ar1(rng, t, n, phi):
    """Autocorrelation: x_t = phi x_(t-1) + sqrt(1 - phi^2) e_t, started in its stationary distribution."""
    if not -1 < phi < 1:
        raise ValueError("AR(1) needs |phi| < 1 to be stationary")
    e = rng.standard_normal((t, n))
    x_prev = rng.standard_normal((1, n))                  # stationary N(0, 1) value before t = 0
    return lfilter([math.sqrt(1 - phi**2)], [1, -phi], e, axis=0, zi=phi * x_prev)[0]


def garch(rng, t, n, alpha, beta):
    """Volatility clustering: GARCH(1,1), s2_t = w + alpha r_(t-1)^2 + beta s2_(t-1), w = 1 - alpha - beta."""
    if not (alpha >= 0 and beta >= 0 and alpha + beta < 1):
        raise ValueError("GARCH(1,1) needs alpha, beta >= 0 and alpha + beta < 1")
    w = 1 - alpha - beta                                  # unconditional variance w / (1 - alpha - beta) = 1
    z = rng.standard_normal((t + GARCH_BURN_IN, n))
    r = np.empty_like(z)
    s2 = np.ones(n)
    for i in range(len(z)):
        r[i] = np.sqrt(s2) * z[i]
        s2 = w + alpha * r[i] ** 2 + beta * s2
    return r[GARCH_BURN_IN:]


def shuffle_time(rng, x):
    """Randomize row order with one permutation while keeping every cross-section intact."""
    return x[rng.permutation(len(x))]


def student_t(rng, t, n, nu):
    """Fat tails: Student-t with nu degrees of freedom, scaled to variance 1 (kurtosis 3 + 6/(nu - 4))."""
    if not nu > 4:
        raise ValueError("Student-t needs nu > 4 for a finite kurtosis (formula 3 + 6/(nu - 4))")
    return rng.standard_t(nu, (t, n)) * math.sqrt((nu - 2) / nu)


def correlated(rng, t, n, rho):
    """Correlated strategy variants: one common factor, every pair of columns has correlation rho."""
    if not 0 <= rho < 1:
        raise ValueError("rho must be in [0, 1)")
    common = rng.standard_normal((t, 1))
    return math.sqrt(rho) * common + math.sqrt(1 - rho) * rng.standard_normal((t, n))
