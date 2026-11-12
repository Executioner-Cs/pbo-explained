import math

import pytest
from scipy import integrate
from scipy.stats import norm

from pbo import paper_values as pv
from pbo.minbtl import expected_max_normal, min_btl_years


PAPER_NS = [pv.EMAX_N, pv.MINBTL_MAX_N, pv.DSR_EX_N]  # N = 10 (PSEUDO p.9), 45 (p.11), 100 (DSR p.9)
LARGE_N = 1000          # our choice: one N well above the paper's examples
TARGETS = [0.5, 1, 2]   # our choice: synthetic targets around the paper's target of 1
REL = 1e-12             # our choice: exact identities, so only float rounding is allowed


def exact_emax(n):
    # E[max of n iid N(0,1)] by numerical integration of x * n * phi(x) * Phi(x)^(n-1). No paper input.
    # Our choice: cut at +/-12 sd. The normal tail beyond that is below 1e-30.
    f = lambda x: x * n * norm.pdf(x) * norm.cdf(x) ** (n - 1)  # noqa: E731
    return integrate.quad(f, -12, 12)[0]


# --- expected_max_normal: PSEUDO Prop 2.1, Eq. 2.4 (p.9); same formula as DSR Eq. 1 (p.7) and Eq. 5 (p.12)

def test_paper_value_n10():
    # PSEUDO p.9: "N = 10 ... a Sharpe ratio IS of 1.57"
    assert expected_max_normal(pv.EMAX_N) == pytest.approx(pv.EMAX_N10, abs=pv.EMAX_N10_TOL)


def test_dsr_example_sr0():
    # DSR p.10: SR0 = sqrt(V/250) * E[max_100] ~= 0.1132
    sr0 = math.sqrt(pv.DSR_EX_V_ANNUAL / pv.DSR_EX_PPY) * expected_max_normal(pv.DSR_EX_N)
    assert sr0 == pytest.approx(pv.DSR_EX_SR0, abs=pv.DSR_EX_SR0_TOL)


@pytest.mark.parametrize("n", PAPER_NS + [LARGE_N])
def test_formula_overstates_exact_mean(n):
    # Eq. 2.4 is an approximation "for a large N". Documents that it sits above the exact mean.
    assert expected_max_normal(n) > exact_emax(n)


@pytest.mark.parametrize("n", PAPER_NS + [LARGE_N])
def test_below_paper_upper_bound(n):
    # PSEUDO p.9: "An upper bound to Eq. (2.4) is sqrt(2 ln[N])"
    assert expected_max_normal(n) < math.sqrt(2 * math.log(n))


def test_increases_with_n():
    values = [expected_max_normal(n) for n in [2] + PAPER_NS + [LARGE_N]]
    assert values == sorted(values)


@pytest.mark.parametrize("n", [1, 0, -5])
def test_n_below_2_raises(n):
    with pytest.raises(ValueError):
        expected_max_normal(n)


# --- min_btl_years: PSEUDO Theorem 3.1, Eq. 3.2 (p.11)

def test_paper_45_configurations_in_5_years():
    # PSEUDO p.11: 5 years of data -> "no more than 45 independent model configurations"
    assert min_btl_years(pv.MINBTL_MAX_N, pv.MINBTL_TARGET) <= pv.MINBTL_YEARS
    assert min_btl_years(pv.MINBTL_MAX_N + 1, pv.MINBTL_TARGET) > pv.MINBTL_YEARS


@pytest.mark.parametrize("n", PAPER_NS)
@pytest.mark.parametrize("target", TARGETS)
def test_below_paper_bound_2_ln_n(n, target):
    # PSEUDO Eq. 3.2: MinBTL < 2 ln[N] / E[max_N]^2
    assert min_btl_years(n, target) < 2 * math.log(n) / target**2


def test_doubling_target_quarters_years():
    # closed form from Eq. 3.2: years scale as 1 / target**2
    n = pv.MINBTL_MAX_N
    assert min_btl_years(n, 2) == pytest.approx(min_btl_years(n, 1) / 4, rel=REL)


@pytest.mark.parametrize("target", [0, -1])
def test_nonpositive_target_raises(target):
    with pytest.raises(ValueError):
        min_btl_years(pv.MINBTL_MAX_N, target)


@pytest.mark.parametrize("n", [math.nan, math.inf, -math.inf, [10]])
def test_invalid_trial_count_raises(n):
    with pytest.raises(ValueError, match="n must"):
        expected_max_normal(n)
    with pytest.raises(ValueError, match="n must"):
        min_btl_years(n, 1)


@pytest.mark.parametrize("target", [math.nan, math.inf, -math.inf, [1]])
def test_invalid_target_raises(target):
    with pytest.raises(ValueError, match="target_sharpe"):
        min_btl_years(pv.MINBTL_MAX_N, target)


def test_fractional_effective_trial_count_is_supported():
    # Effective independent-trial counts are real; the quantile formula is monotone between integers.
    assert expected_max_normal(2) < expected_max_normal(2.5) < expected_max_normal(3)


def test_large_trial_count_stays_finite_below_normal_maximum_bound():
    # The Gaussian maximum bound sqrt(2 log n) is independent of the quantile approximation.
    n = 1e20
    assert 0 < expected_max_normal(n) <= math.sqrt(2 * math.log(n))
