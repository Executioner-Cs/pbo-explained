import math

import numpy as np
import pytest
from scipy.stats import norm

from pbo import paper_values as pv
from pbo.psr_dsr import (ar1_psr_false_positive, dsr, implied_n, min_trl, newey_west_factor, psr,
                         psr_false_positive, psr_long_run, sr0)

REL = 1e-12             # our choice: exact identities, so only float rounding is allowed
WEEKS = 52              # calendar convention for the SF p.11 weekly example (paper does not print it)
MONTHS = pv.PSR_EX_PPY  # monthly, 12 per year
N_EX = pv.PSR_EX_YEARS * pv.PSR_EX_PPY  # 24 monthly observations in the SF p.10 example


SR_HALF_UNIT = 0.0005  # SF p.10 prints SR = 0.458, so the true input lies within +/- half a unit of the last digit


def psr_range(n, skew=0.0, kurt=3.0):
    # PSR is increasing in SR, so the paper's rounded input maps to this interval of outputs.
    lo = psr(pv.PSR_EX_SR - SR_HALF_UNIT, 0, n, skew, kurt)
    hi = psr(pv.PSR_EX_SR + SR_HALF_UNIT, 0, n, skew, kurt)
    return lo - pv.PSR_EX_TOL, hi + pv.PSR_EX_TOL


# --- psr: SF Eq. 11, p.9. Inputs are non-annualized (SF p.9: "All calculations are done in the original frequency").

def test_psr_paper_example_normal():
    # SF p.10: monthly SR 0.458, two years, assuming Normality -> PSR(0) = 0.982
    lo, hi = psr_range(pv.PSR_EX_YEARS * pv.PSR_EX_PPY)
    assert lo <= pv.PSR_EX_NORMAL <= hi


def test_psr_paper_example_non_normal():
    # SF p.10: same track record with skew -2.448 and kurtosis 10.164 -> PSR(0) = 0.913
    lo, hi = psr_range(pv.PSR_EX_YEARS * pv.PSR_EX_PPY, pv.PSR_EX_SKEW, pv.PSR_EX_KURT)
    assert lo <= pv.PSR_EX_NON_NORMAL <= hi


def test_psr_paper_example_three_years():
    # SF p.10: "should we have 3 years instead of 2, PSR(0) = 0.953", four moments included
    # Only passes once the rounding of the printed SR (0.458) is allowed for; see psr_range.
    lo, hi = psr_range(pv.PSR_EX_YEARS_LONG * pv.PSR_EX_PPY, pv.PSR_EX_SKEW, pv.PSR_EX_KURT)
    assert lo <= pv.PSR_EX_LONG <= hi


@pytest.mark.parametrize("sr", [0.0, 0.1, -0.2])  # our choice: any SR, any moments
def test_psr_is_half_when_sr_equals_benchmark(sr):
    # closed form: the numerator of Eq. 11 is 0, and Z[0] = 1/2
    assert psr(sr, sr, 100, -1.0, 6.0) == pytest.approx(0.5, rel=REL)


def test_psr_direction_of_skew_and_kurtosis():
    # SF p.9: PSR increases with skewness and decreases with fatter tails (for SR > 0)
    # our choice: skew -1 / +1 and kurt 6 as moves away from Normal (0, 3)
    base = psr(pv.PSR_EX_SR, 0, N_EX)
    assert psr(pv.PSR_EX_SR, 0, N_EX, skew=-1.0) < base < psr(pv.PSR_EX_SR, 0, N_EX, skew=1.0)
    assert psr(pv.PSR_EX_SR, 0, N_EX, kurt=6.0) < base


def test_psr_rejects_negative_variance():
    # Eq. 11 denominator 1 - skew*SR + (kurt-1)/4*SR^2 must be positive. skew 5, SR 1, kurt 1: 1 - 5 + 0 < 0.
    with pytest.raises(ValueError):
        psr(1.0, 0, 100, skew=5.0, kurt=1.0)


# --- min_trl: SF Eq. 13, p.11. Result is a number of observations.

@pytest.mark.parametrize("q, years", [
    (pv.PERIODS_PER_YEAR, pv.MINTRL_EX_YEARS_DAILY),
    (WEEKS, pv.MINTRL_EX_YEARS_WEEKLY),
    (MONTHS, pv.MINTRL_EX_YEARS_MONTHLY),
])
def test_min_trl_paper_examples_normal(q, years):
    # SF p.11: annual SR 2 vs SR* 1 at 95%, IID Normal: 2.73 y daily, 2.83 y weekly, 3.24 y monthly
    n = min_trl(pv.MINTRL_EX_SR_ANNUAL / math.sqrt(q), pv.MINTRL_EX_SR_STAR_ANNUAL / math.sqrt(q),
                1 - pv.MINTRL_EX_CONFIDENCE)
    assert n / q == pytest.approx(years, abs=pv.MINTRL_EX_TOL)


def test_min_trl_paper_example_hfr():
    # SF p.11: monthly, HFR skew -0.72 and kurt 5.78 -> 4.99 years
    q = MONTHS
    n = min_trl(pv.MINTRL_EX_SR_ANNUAL / math.sqrt(q), pv.MINTRL_EX_SR_STAR_ANNUAL / math.sqrt(q),
                1 - pv.MINTRL_EX_CONFIDENCE, pv.MINTRL_EX_HFR_SKEW, pv.MINTRL_EX_HFR_KURT)
    assert n / q == pytest.approx(pv.MINTRL_EX_YEARS_HFR, abs=pv.MINTRL_EX_TOL)


def test_min_trl_inverts_psr():
    # closed form: Eq. 13 solves Eq. 12, PSR(SR*) = 1 - alpha, for n
    sr, sr_star, alpha, skew, kurt = 0.15, 0.05, 0.05, -0.5, 5.0  # our choice: arbitrary non-Normal case
    n = min_trl(sr, sr_star, alpha, skew, kurt)
    assert psr(sr, sr_star, n, skew, kurt) == pytest.approx(1 - alpha, rel=REL)


@pytest.mark.parametrize("sr", [0.05, 0.01])
def test_min_trl_needs_sr_above_benchmark(sr):
    # SF p.10: MinTRL is defined "for SR > SR*"
    with pytest.raises(ValueError):
        min_trl(sr, 0.05, 0.05)


# --- dsr: DSR Eq. 2, p.8. DSR = PSR(SR0), SR0 = sqrt(V[{SR_n}]) * E[max_N].

def per_period(annual):
    return annual / math.sqrt(pv.PERIODS_PER_YEAR)


V_PER_PERIOD = pv.DSR_EX_V_ANNUAL / pv.PERIODS_PER_YEAR  # a variance of annual SRs scales by 1/q


def test_sr0_paper_example():
    # DSR p.10: SR0 ~= 0.1132
    assert sr0(pv.DSR_EX_N, V_PER_PERIOD) == pytest.approx(pv.DSR_EX_SR0, abs=pv.DSR_EX_SR0_TOL)


@pytest.mark.parametrize("n_trials, skew, kurt, expected", [
    (pv.DSR_EX_N, pv.DSR_EX_SKEW, pv.DSR_EX_KURT, pv.DSR_EX_DSR),      # DSR p.10: 0.9004
    (pv.DSR_EX_N_ALT, pv.DSR_EX_SKEW, pv.DSR_EX_KURT, pv.DSR_EX_DSR_ALT),  # p.10: N = 46 -> 0.9505
    (pv.DSR_EX_N_NORMAL, 0, 3, pv.DSR_EX_DSR_NORMAL),                  # p.10: Normal, N = 88 -> 0.9505
])
def test_dsr_paper_examples(n_trials, skew, kurt, expected):
    got = dsr(per_period(pv.DSR_EX_SR_ANNUAL), pv.DSR_EX_T, skew, kurt, n_trials, V_PER_PERIOD)
    assert got == pytest.approx(expected, abs=pv.DSR_EX_DSR_TOL)


def test_dsr_is_psr_at_sr0():
    # closed form, DSR Eq. 2: DSR = PSR(SR0)
    sr, t, skew, kurt, n, v = 0.12, 1000, -0.4, 4.5, 30, 0.002  # our choice: arbitrary inputs
    assert dsr(sr, t, skew, kurt, n, v) == pytest.approx(psr(sr, sr0(n, v), t, skew, kurt), rel=REL)


# --- bad inputs (our choice: raise rather than return a wrong number)

@pytest.mark.parametrize("n", [1, 0])
def test_psr_needs_two_observations(n):
    with pytest.raises(ValueError):
        psr(0.1, 0, n)


@pytest.mark.parametrize("alpha", [0.0, 0.5, 0.7, 1.0])
def test_min_trl_alpha_range(alpha):
    # alpha = 0.7 used to return the n for alpha = 0.3, silently
    with pytest.raises(ValueError):
        min_trl(0.1, 0, alpha)


def test_sr0_negative_variance_raises():
    with pytest.raises(ValueError):
        sr0(pv.DSR_EX_N, -0.001)


@pytest.mark.parametrize("bad", [math.nan, math.inf])
def test_non_finite_inputs_raise(bad):
    # NaN compares False with everything, so it would slip past the range checks and return NaN
    with pytest.raises(ValueError):
        psr(bad, 0, 100)
    with pytest.raises(ValueError):
        psr(0.1, 0, 100, kurt=bad)
    with pytest.raises(ValueError):
        min_trl(0.1, 0, bad)
    with pytest.raises(ValueError):
        sr0(pv.DSR_EX_N, bad)
    with pytest.raises(ValueError):
        sr0(bad, 0.1)


# --- implied number of independent trials: DSR Appendix 3, Eq. 8 and 9 (p.14)

def test_implied_n_limits():
    # p.14: as rho -> 1, N -> 1; as rho -> 0, N -> M
    m = 50
    assert implied_n(np.eye(m)) == pytest.approx(m)
    assert implied_n(np.ones((m, m))) == pytest.approx(1)


def test_implied_n_constant_correlation():
    # Eq. 8 on a constant-rho matrix returns rho; Eq. 9 then gives rho + (1 - rho) M
    m, rho = 40, 0.3
    c = np.full((m, m), rho)
    np.fill_diagonal(c, 1.0)
    assert implied_n(c) == pytest.approx(rho + (1 - rho) * m, rel=REL)



def test_implied_n_rejects_covariance_matrix():
    with pytest.raises(ValueError):
        implied_n(np.array([[2.0, 0.5], [0.5, 2.0]]))


def test_psr_false_positive_factor_one_large_t():
    # factor 1 and t -> infinity: exactly 1 - level
    assert psr_false_positive(1.0, 10**9, 0.95) == pytest.approx(0.05)


def test_ar1_rate_without_autocorrelation():
    # phi = 0: F = 1, so the finite-t rate is 1 - Z[z sqrt(t/(t-1))] and the large-t rate is exactly 1 - level
    finite, limit = ar1_psr_false_positive(0.0, 100, 0.95)
    assert finite == pytest.approx(1 - norm.cdf(norm.ppf(0.95) * math.sqrt(100 / 99)))
    assert limit == pytest.approx(0.05)


def test_ar1_rate_short_series_closed_form():
    # t = 3: F_3 = 1 + 2 (2/3 phi + 1/3 phi^2); the rate uses sqrt(F (t-1)/t)
    phi = 0.5
    f3 = 1 + 2 * (2 / 3 * phi + 1 / 3 * phi**2)
    expected = 1 - norm.cdf(norm.ppf(0.95) / math.sqrt(f3 * 2 / 3))
    assert ar1_psr_false_positive(phi, 3, 0.95)[0] == pytest.approx(expected)


def test_newey_west_factor_closed_forms():
    # alternating +1, -1 (100 values): rho_1 = -99/100, so with 1 lag F = 1 + 2 (1/2)(-0.99) = 0.01
    x = np.tile([1.0, -1.0], 50)
    assert newey_west_factor(x, 1) == pytest.approx(0.01)
    assert newey_west_factor(x, 0) == pytest.approx(1.0)


def test_psr_long_run_factor_one_is_unchanged():
    assert psr_long_run(0.97, 1.0) == pytest.approx(0.97)
    assert psr_long_run(0.5, 4.0) == pytest.approx(0.5)      # Z[0 / 2] = 1/2


def test_long_run_helpers_reject_bad_input():
    with pytest.raises(ValueError):
        newey_west_factor(np.arange(5.0), 5)            # lags must be below the length
    with pytest.raises(ValueError):
        newey_west_factor(np.ones(5), 1)                # zero variance
    with pytest.raises(ValueError):
        psr_long_run(0.9, 0.0)                          # factor must be positive


def test_ar1_rate_converges_to_limit():
    # F_t -> (1 + phi)/(1 - phi) and (t - 1)/t -> 1 as t grows
    finite, limit = ar1_psr_false_positive(0.3, 200_000, 0.95)
    assert finite == pytest.approx(limit, abs=1e-4)
    assert limit == pytest.approx(1 - norm.cdf(norm.ppf(0.95) / math.sqrt(1.3 / 0.7)))


def test_implied_n_negative_average_correlation_counts_as_zero():
    # rho = -0.5 is treated as 0, so N = M = 2. Our choice: p.14 allows rho down to -1/(M-1), where Eq. 9 gives N > M
    assert implied_n(np.array([[1.0, -0.5], [-0.5, 1.0]])) == pytest.approx(2)


@pytest.mark.parametrize("bad", [np.ones((3, 2)), np.ones((1, 1))])   # not square; smaller than 2 x 2
def test_implied_n_needs_square_matrix(bad):
    with pytest.raises(ValueError):
        implied_n(bad)


def test_implied_n_rejects_nan():
    with pytest.raises(ValueError):
        implied_n(np.array([[1.0, np.nan], [np.nan, 1.0]]))
