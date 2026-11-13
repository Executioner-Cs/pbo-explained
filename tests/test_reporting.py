import math

import pytest

from pbo.reporting import format_mean, format_rate, mean_with_se, rate_with_ci


def test_mean_with_se_closed_form():
    # values 1, 2, 3: mean 2, sample sd 1, so SE = 1 / sqrt(3)
    mean, se = mean_with_se([1.0, 2.0, 3.0])
    assert mean == 2.0
    assert se == pytest.approx(1 / math.sqrt(3))


def test_rate_with_ci_zero_hits_closed_form():
    # Clopper-Pearson with 0 hits in n: interval [0, 1 - (0.025)^(1/n)]
    rate, hits, total, low, high = rate_with_ci([False] * 10)
    assert (rate, hits, total, low) == (0.0, 0, 10, 0.0)
    assert high == pytest.approx(1 - 0.025 ** (1 / 10))


def test_rate_with_ci_all_hits_closed_form():
    # mirror image: n hits in n gives [(0.025)^(1/n), 1]
    rate, hits, total, low, high = rate_with_ci([True] * 10)
    assert (rate, hits, total, high) == (1.0, 10, 10, 1.0)
    assert low == pytest.approx(0.025 ** (1 / 10))


def test_formatters():
    # 0 hits in 10: interval [0, 1 - 0.025^(1/10)] = [0, 0.3085]; mean of 1, 2, 3 is 2, SE 1/sqrt(3) = 0.577
    assert format_rate([False] * 10) == "0.0000 [0.0000, 0.3085] (0/10)"
    assert format_mean([1.0, 2.0, 3.0]) == "2.000 +/- 0.577"



@pytest.mark.parametrize("flags", [[0.3, 2.0], [0, 1, 1]])
def test_rate_with_ci_needs_booleans(flags):
    with pytest.raises(ValueError):
        rate_with_ci(flags)
