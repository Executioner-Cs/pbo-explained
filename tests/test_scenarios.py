"""Each scenario is checked against closed-form moments.

Coverage, stated honestly:
- Mean, AR(1) autocorrelation, cross-correlation: tolerance K standard errors (closed-form SE).
- Variance, GARCH squared-return autocorrelation, GARCH and Student-t kurtosis: relative tolerances (3 to 15%),
  because their sampling SE has no simple closed form and heavy tails make them unstable.
- Student-t kurtosis is tested at nu = 12 and 20, not the experiment's nu = 8 and 5: for nu <= 8 the sample
  kurtosis has infinite variance, so no finite tolerance would be honest. Their unit variance is tested directly.
"""
import math

import numpy as np
import pytest
from scipy.stats import kurtosis

from pbo.scenarios import ar1, correlated, garch, iid, shuffle_time, student_t

K = 4             # our choice: tolerance in standard errors (false alarm about 1 in 16,000 per check)
T_BIG = 400_000   # our choice: long series so sample moments are tight
SEED = 7          # our choice


def lag1(x):
    x = x - x.mean()
    return float(np.dot(x[1:], x[:-1]) / np.dot(x, x))


@pytest.mark.parametrize("make", [
    lambda rng: iid(rng, T_BIG, 1),
    lambda rng: ar1(rng, T_BIG, 1, 0.3),
    lambda rng: garch(rng, T_BIG, 1, 0.05, 0.90),
    lambda rng: student_t(rng, T_BIG, 1, 12),
    lambda rng: correlated(rng, T_BIG, 2, 0.5),
])
def test_zero_mean_unit_variance(make):
    # Every scenario has true mean 0 (zero edge) and unconditional variance 1.
    x = make(np.random.default_rng(SEED))[:, 0]
    assert x.shape == (T_BIG,)
    # mean SE: sd / sqrt(T), inflated for AR(1) by sqrt((1+phi)/(1-phi)) <= sqrt(1.3/0.7)
    assert abs(x.mean()) < K * math.sqrt(1.3 / 0.7) / math.sqrt(T_BIG)
    assert x.var() == pytest.approx(1.0, rel=0.03)  # our choice: 3%, loose enough for GARCH's heavy tails


@pytest.mark.parametrize("nu", [5, 8])
def test_grid_student_t_has_unit_variance(nu):
    # For variance 1, asymptotic SE(sample variance) is sqrt((kurtosis - 1) / T).
    x = student_t(np.random.default_rng(SEED), T_BIG, 1, nu)[:, 0]
    raw_kurtosis = 3 + 6 / (nu - 4)
    tolerance = K * math.sqrt((raw_kurtosis - 1) / T_BIG)
    assert x.var() == pytest.approx(1.0, abs=tolerance)


@pytest.mark.parametrize("phi", [0.1, 0.3])
def test_ar1_lag1_autocorrelation(phi):
    # closed form: lag-1 autocorrelation = phi, SE about sqrt((1 - phi^2) / T)
    x = ar1(np.random.default_rng(SEED), T_BIG, 1, phi)[:, 0]
    assert lag1(x) == pytest.approx(phi, abs=K * math.sqrt((1 - phi**2) / T_BIG))


def test_ar1_columns_independent():
    x = ar1(np.random.default_rng(SEED), T_BIG, 2, 0.3)
    assert abs(np.corrcoef(x.T)[0, 1]) < K / math.sqrt(T_BIG) * math.sqrt(1.3 / 0.7)


def test_garch_squared_return_autocorrelation():
    # closed form, GARCH(1,1) with Normal shocks: lag-1 autocorrelation of r^2 is
    # alpha (1 - alpha*beta - beta^2) / (1 - 2*alpha*beta - beta^2). Returns themselves are uncorrelated.
    a, b = 0.10, 0.85
    x = garch(np.random.default_rng(SEED), T_BIG, 1, a, b)[:, 0]
    expected = a * (1 - a * b - b**2) / (1 - 2 * a * b - b**2)
    assert lag1(x**2) == pytest.approx(expected, rel=0.15)   # our choice: 15%, r^2 has heavy tails
    assert abs(lag1(x)) < K / math.sqrt(T_BIG)


def test_garch_kurtosis():
    # closed form: kurtosis 3 (1 - (a+b)^2) / (1 - (a+b)^2 - 2 a^2) = 3.774 here, so the 5% band
    # [3.59, 3.96] excludes Normal (3.0). E[(a z^2 + b)^4] = 0.96 < 1, so the sample kurtosis is stable.
    a, b = 0.10, 0.85
    x = garch(np.random.default_rng(SEED), T_BIG, 1, a, b)[:, 0]
    expected = 3 * (1 - (a + b) ** 2) / (1 - (a + b) ** 2 - 2 * a**2)
    assert kurtosis(x, fisher=False) == pytest.approx(expected, rel=0.05)   # our choice: 5%


@pytest.mark.parametrize("nu", [12, 20])
def test_student_t_kurtosis(nu):
    # closed form: kurtosis 3 + 6 / (nu - 4). nu > 8 here so the sample kurtosis has finite variance.
    x = student_t(np.random.default_rng(SEED), T_BIG, 1, nu)[:, 0]
    assert kurtosis(x, fisher=False) == pytest.approx(3 + 6 / (nu - 4), rel=0.05)   # our choice: 5%


@pytest.mark.parametrize("rho", [0.3, 0.7])
def test_correlated_pairwise_correlation(rho):
    # closed form: every pair has correlation rho. SE of a sample correlation about (1 - rho^2) / sqrt(T).
    x = correlated(np.random.default_rng(SEED), T_BIG, 5, rho)
    c = np.corrcoef(x.T)[np.triu_indices(5, 1)]
    assert np.allclose(c, rho, atol=K * (1 - rho**2) / math.sqrt(T_BIG))


@pytest.mark.parametrize("bad", [
    lambda rng: ar1(rng, 10, 1, 1.0),
    lambda rng: garch(rng, 10, 1, 0.5, 0.5),
    lambda rng: student_t(rng, 10, 1, 4),
    lambda rng: correlated(rng, 10, 2, 1.5),
    lambda rng: garch(rng, 10, 1, math.nan, 0.5),
    lambda rng: student_t(rng, 10, 1, math.nan),
])
def test_bad_parameters_raise(bad):
    # stationarity / finite variance / valid correlation conditions
    with pytest.raises(ValueError):
        bad(np.random.default_rng(0))


def test_shuffle_time_keeps_values_removes_clustering():
    a, b = 0.10, 0.85
    x = garch(np.random.default_rng(SEED), T_BIG, 2, a, b)
    y_all = shuffle_time(np.random.default_rng(SEED + 1), x)
    # each column keeps exactly its own values
    assert np.array_equal(np.sort(x, axis=0), np.sort(y_all, axis=0))
    # one common permutation: every row of the result is a whole row of the input
    order = np.lexsort(x.T[::-1]), np.lexsort(y_all.T[::-1])
    assert np.array_equal(x[order[0]], y_all[order[1]])
    y = y_all[:, 0]
    # systematic clustering is removed in expectation: realized lag-1 r^2 correlation is within K SE of 0
    assert abs(lag1(y**2)) < K / math.sqrt(T_BIG)


def test_shuffle_time_leaves_psr_dsr_inputs_unchanged():
    # PSR and DSR use only Sharpe, skew and kurtosis, which ignore order: shuffling cannot change them.
    from scipy.stats import skew
    x = garch(np.random.default_rng(SEED), 5000, 3, 0.10, 0.85)
    y = shuffle_time(np.random.default_rng(SEED + 1), x)
    for f in (lambda a: a.mean(0) / a.std(0), lambda a: skew(a), lambda a: kurtosis(a, fisher=False)):
        assert np.allclose(f(x), f(y), rtol=1e-10, atol=0)   # only float summation order differs
