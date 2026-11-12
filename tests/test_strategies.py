"""MA crossover: closed forms and a no-lookahead check."""
import numpy as np
import pytest

from pbo.strategies import ma_crossover, moving_average


def test_moving_average_closed_form():
    # mean of (0, 1, 2) is 1, of (1, 2, 3) is 2; undefined before 3 values
    assert np.allclose(moving_average(np.arange(5.0), 3), [np.nan, np.nan, 1, 2, 3], equal_nan=True)


def test_rising_prices_long_from_next_day_with_one_cost():
    # Rising prices: fast MA (2) is above slow MA (5) from day 4, when the slow MA first exists, so the position
    # is long from day 5. One trade, so the cost is charged once, on day 5.
    r = ma_crossover(np.arange(1.0, 21), np.full(20, 0.01), 2, 5, 0.001)
    assert r[:5] == pytest.approx(0)
    assert r[5] == pytest.approx(0.01 - 0.001)
    assert r[6:] == pytest.approx(0.01)


def test_no_lookahead():
    # A rising market crashes from day k on, which flips the signal to flat at day k. A strategy that trades on
    # day k's own close would then differ on day k; ours trades a day later, so returns up to day k are unchanged.
    excess = np.full(400, 0.01)
    prices = np.arange(1.0, 401)
    k = 300
    crashed = prices.copy()
    crashed[k:] *= 0.01
    assert np.array_equal(ma_crossover(prices, excess, 10, 50, 0.0005)[:k + 1],
                          ma_crossover(crashed, excess, 10, 50, 0.0005)[:k + 1])
    assert not np.array_equal(ma_crossover(prices, excess, 10, 50, 0.0005),
                              ma_crossover(crashed, excess, 10, 50, 0.0005))   # the crash does act, one day later


@pytest.mark.parametrize("prices, excess, fast, slow, cost", [
    (np.ones(10), np.ones(9), 2, 5, 0.0),                 # lengths differ
    (np.ones((10, 2)), np.ones((10, 2)), 2, 5, 0.0),      # not 1-D
    (np.r_[np.nan, np.ones(9)], np.ones(10), 2, 5, 0.0),  # non-finite
    (np.ones(10), np.ones(10), 5, 5, 0.0),                # fast not below slow
    (np.ones(10), np.ones(10), 2, 11, 0.0),               # slow longer than the series
    (np.ones(10), np.ones(10), 2, 5, -0.001),             # negative cost
    (np.ones(10), np.ones(10), 2, 5, np.inf),             # non-finite cost
])
def test_ma_crossover_rejects_bad_input(prices, excess, fast, slow, cost):
    with pytest.raises(ValueError):
        ma_crossover(prices, excess, fast, slow, cost)
