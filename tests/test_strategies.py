"""MA crossover: closed forms and a no-lookahead check."""
import numpy as np
import pytest

from pbo.strategies import crossover_panel, ma_crossover, moving_average, position_returns


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


@pytest.mark.parametrize("x, window", [
    (np.r_[1.0, np.nan, 3.0], 2),     # non-finite
    (np.ones((3, 2)), 2),             # not 1-D
    (np.ones(5), 2.5),                # fractional window
    (np.ones(5), 0),                  # window too short
    (np.ones(5), 6),                  # window longer than the series
    (np.ones(5), True),               # Boolean is not a window length
    (np.ones(5), np.bool_(True)),
])
def test_moving_average_rejects_bad_input(x, window):
    with pytest.raises(ValueError):
        moving_average(x, window)


def test_panel_trims_common_days_and_preserves_positions_and_costs():
    # The first five rows are dropped: longest MA is 4, then 1 extra row to divide by 2.
    # Both rules enter before the cut; their exits and reentries occur on different days.
    prices = [1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5]
    start, panel = crossover_panel(prices, np.full(13, 0.01), [(1, 3), (2, 4)], 0.001, 2)
    assert start == 5
    assert panel == pytest.approx(np.array([
        [0.01, 0.01], [-0.001, 0.01], [0, -0.001], [0, 0],
        [0, 0], [0.009, 0], [0.01, 0.009], [0.01, 0.01],
    ]))


@pytest.mark.parametrize("settings, blocks", [([], 2), ([(1, 3)], 0), ([(1, 3)], 1.5), ([(1, 3)], 20)])
def test_panel_rejects_empty_search_or_invalid_partition(settings, blocks):
    with pytest.raises(ValueError):
        crossover_panel(np.arange(1., 14.), np.full(13, 0.01), settings, 0.001, blocks)


def test_delay_two_is_delay_one_shifted_by_a_day():
    # delay = 2: the signal at close t sets the position for day t + 2, so positions are those of delay 1, one day
    # later. With zero cost the returns are position * excess; check against that closed form.
    rng = np.random.default_rng(3)
    excess = rng.normal(0, 0.01, 300)
    prices = np.cumprod(1 + excess)
    one = ma_crossover(prices, np.ones(300), 10, 50, 0.0)       # excess 1: returns equal positions
    two = ma_crossover(prices, np.ones(300), 10, 50, 0.0, delay=2)
    assert np.array_equal(two[1:], one[:-1]) and two[0] == 0


@pytest.mark.parametrize("delay", [0, 1.5, True])
def test_delay_must_be_a_positive_integer(delay):
    with pytest.raises(ValueError):
        ma_crossover(np.arange(1.0, 21), np.ones(20), 2, 5, 0.0, delay=delay)


def test_position_returns_closed_form():
    # Path flat, long, long, flat, long; excess 0.01 a day, cost 0.001 per unit change.
    # Hand-worked: day 1 enters (0.01 - 0.001), day 2 holds, day 3 exits (-0.001), day 4 re-enters.
    r = position_returns([0, 1, 1, 0, 1], np.full(5, 0.01), 0.001)
    assert r == pytest.approx([0, 0.009, 0.01, -0.001, 0.009])


def test_switching_rules_charges_the_actual_position_change():
    # Rule A is always flat, rule B always long. Holding A on days 0-1 and B on days 2-3 changes the actual
    # position once, on day 2, so day 2 pays one cost. Stitching each rule's own returns would miss it, because
    # B never trades on its own path.
    a, b = np.zeros(4), np.ones(4)
    path = np.r_[a[:2], b[2:]]
    assert position_returns(path, np.full(4, 0.01), 0.001) == pytest.approx([0, 0, 0.009, 0.01])


def test_start_position_sets_the_first_day_cost():
    # Already long before day 0: no entry cost on day 0.
    assert position_returns([1, 1], np.full(2, 0.01), 0.001, start=1.0) == pytest.approx([0.01, 0.01])


@pytest.mark.parametrize("position, excess, cost", [
    (np.ones(3), np.ones(2), 0.0),            # lengths differ
    (np.r_[np.nan, 1, 1], np.ones(3), 0.0),   # non-finite
    (np.ones(3), np.ones(3), -0.001),         # negative cost
])
def test_position_returns_rejects_bad_input(position, excess, cost):
    with pytest.raises(ValueError):
        position_returns(position, excess, cost)
