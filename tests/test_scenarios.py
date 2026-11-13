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

from pbo.scenarios import ar1, block_bootstrap, block_bootstrap_factor, correlated, garch, iid, shuffle_time, student_t

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


def test_ar1_starts_stationary():
    # Many short columns: x_0 must already have variance 1 and corr(x_0, x_1) = phi (a start at 0 gives 1 - phi^2).
    n, phi = 200_000, 0.3
    x = ar1(np.random.default_rng(SEED), 2, n, phi)
    assert x[0].var() == pytest.approx(1.0, abs=K * math.sqrt(2 / n))       # SE of a Normal sample variance
    assert np.corrcoef(x)[0, 1] == pytest.approx(phi, abs=K * (1 - phi**2) / math.sqrt(n))


def test_ar1_columns_independent():
    x = ar1(np.random.default_rng(SEED), T_BIG, 2, 0.3)
    # SE of the sample correlation of two independent AR(1) series: sqrt((1 + phi^2) / (1 - phi^2) / T)
    assert abs(np.corrcoef(x.T)[0, 1]) < K / math.sqrt(T_BIG) * math.sqrt(1.09 / 0.91)


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


# --- block bootstrap: closed-form structure checks on a matrix whose rows encode their own index

def test_block_bootstrap_takes_whole_consecutive_rows():
    x = np.column_stack([np.arange(10.0), 100 + np.arange(10.0)])   # column 1 = column 0 + 100
    y = block_bootstrap(np.random.default_rng(SEED), x, 23, 4)
    assert y.shape == (23, 2)
    assert np.array_equal(y[:, 1], y[:, 0] + 100)                   # same-day rows stay whole
    blocks = y[:20, 0].reshape(5, 4)                                 # the 5 full blocks of 4 rows
    assert np.all(np.diff(blocks, axis=1) % 10 == 1)                 # each step is the next row, 9 wraps to 0
    assert np.all(np.diff(y[20:, 0]) % 10 == 1)                      # the last, partial block too


def test_block_bootstrap_every_row_equally_likely():
    # Circular: each output position is uniform over the 10 rows, so each row has probability 1/10.
    x = np.arange(10.0)[:, None]
    y = block_bootstrap(np.random.default_rng(SEED), x, 20_000, 5)
    counts = np.bincount(y[:, 0].astype(int), minlength=10)
    # 4000 blocks of 5 of the 10 rows: each block holds a given row exactly once with probability 1/2,
    # so its count is Binomial(4000, 1/2), SD sqrt(4000 * 0.5 * 0.5) = 31.6.
    se = math.sqrt(4000 * 0.5 * 0.5)
    assert np.all(np.abs(counts - 2000) < K * se)


@pytest.mark.parametrize("x, t, block", [
    (np.ones((5, 1)), 5, 0),       # block 0
    (np.ones((5, 1)), 0, 2),       # t 0
    (np.ones(5), 5, 2),            # not a matrix
    (np.ones((0, 3)), 5, 2),       # no rows
])
def test_block_bootstrap_rejects_bad_input(x, t, block):
    with pytest.raises(ValueError):
        block_bootstrap(np.random.default_rng(0), x, t, block)


def test_block_bootstrap_factor_closed_forms():
    # block 1: independent days, F = 1. Alternating +1, -1: circular rho_1 = -1, so with block 2
    # F = 1 + 2 (1/2)(-1) = 0 (every block of two sums to zero, so the bootstrap mean never moves).
    x = np.tile([1.0, -1.0], 50)[:, None]
    assert block_bootstrap_factor(x, 1, 100) == pytest.approx([1.0])
    assert block_bootstrap_factor(x, 2, 100) == pytest.approx([0.0], abs=1e-12)


def test_block_bootstrap_factor_partial_final_block():
    # Source (+1, -1), block 2, t = 3: one full block (sum 0) plus one day drawn uniformly (+1 or -1).
    # The mean is that day / 3, variance 1/9; independent days give var(x)/3 = 1/3. Factor = (1/9)/(1/3) = 1/3.
    x = np.array([[1.0], [-1.0]])
    assert block_bootstrap_factor(x, 2, 3) == pytest.approx([1 / 3])


def test_block_bootstrap_factor_rejects_constant_column():
    with pytest.raises(ValueError):
        block_bootstrap_factor(np.ones((10, 1)), 2, 10)


def test_block_bootstrap_factor_matches_bootstrap_variance():
    # Monte Carlo check of the formula on an AR(1) column, t = 405 not a multiple of block 10 (partial last block)
    x = ar1(np.random.default_rng(SEED), 400, 1, 0.5)
    rng = np.random.default_rng(SEED + 1)
    means = [block_bootstrap(rng, x, 405, 10).mean() for _ in range(20_000)]
    expected = block_bootstrap_factor(x, 10, 405)[0] * x.var() / 405
    assert np.var(means) == pytest.approx(expected, rel=0.05)   # our choice: 5%, MC SE of a variance is about 1%


def test_block_bootstrap_factor_never_negative():
    # A variance ratio cannot be negative; roundoff used to give -1.7e-16 here.
    assert block_bootstrap_factor(np.array([[1.0], [-1.0], [2.0]]), 5, 3)[0] >= 0


def test_stationary_bootstrap_indices_follow_blocks():
    # Within a block the index steps by 1 (mod n); with mean block 1 every day starts a new block.
    from pbo.scenarios import stationary_bootstrap_indices
    rng = np.random.default_rng(5)
    idx = stationary_bootstrap_indices(rng, 50, 20_000, 20)
    steps = np.diff(idx) % 50
    assert idx.min() >= 0 and idx.max() < 50 and len(idx) == 20_000
    # a step other than +1 can only happen at a block start; starts occur with probability 1/20
    assert np.mean(steps != 1) == pytest.approx(1 / 20 * (1 - 1 / 50), abs=0.005)
    assert np.isin(stationary_bootstrap_indices(rng, 7, 100, 1), np.arange(7)).all()
