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

GARCH_BURN_IN = 500  # our choice: steps discarded so the variance process forgets its starting value


def iid(rng, t, n):
    """Baseline: IID standard Normal."""
    return rng.standard_normal((t, n))


def ar1(rng, t, n, phi):
    """Autocorrelation: x_t = phi x_(t-1) + sqrt(1 - phi^2) e_t, started in its stationary distribution."""
    if not -1 < phi < 1:
        raise ValueError("AR(1) needs |phi| < 1 to be stationary")
    e = rng.standard_normal((t, n))
    x = rng.standard_normal(n)                            # stationary N(0, 1) value before t = 0
    out = np.empty((t, n))
    for i in range(t):
        x = phi * x + math.sqrt(1 - phi**2) * e[i]
        out[i] = x
    return out


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


def block_bootstrap(rng, x, t, block):
    """Circular block bootstrap of whole rows: t rows built from blocks of `block` consecutive rows of x.

    Block starts are uniform over all rows and wrap past the end (circular), so every row of x is
    equally likely at every output position. Whole rows keep same-day relationships across columns.
    Two rows h apart (h < block) stay neighbours only if they fall in one block: probability 1 - h/block
    averaged over output positions (block edges are at fixed multiples of block).
    block = 1 resamples days independently.
    """
    x = np.asarray(x)
    if x.ndim != 2 or len(x) == 0:
        raise ValueError("x must be a non-empty T x N matrix")
    if t < 1 or block < 1:
        raise ValueError("t and block must be at least 1")
    starts = rng.integers(0, len(x), size=math.ceil(t / block))
    rows = (starts[:, None] + np.arange(block)) % len(x)
    return x[rows.ravel()[:t]]


def block_bootstrap_factor(x, block):
    """Per column: variance of the circular block bootstrap mean divided by its value for independent days.

    Our derivation: F = 1 + 2 sum_{h=1}^{block-1} (1 - h/block) rho_h, with rho_h the circular lag-h
    autocorrelation of the column. Exact when t is a multiple of block. block = 1 gives F = 1.
    """
    d = np.asarray(x, dtype=float) - np.mean(x, axis=0)
    var = (d * d).sum(axis=0)
    if np.any(var == 0):
        raise ValueError("a column has zero variance")
    f = np.ones(d.shape[1])
    for h in range(1, block):
        f += 2 * (1 - h / block) * (d * np.roll(d, -h, axis=0)).sum(axis=0) / var
    return f
