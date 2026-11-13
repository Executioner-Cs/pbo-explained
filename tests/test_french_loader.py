"""Parser and cleaning of the French file, on a tiny hand-written fixture (no network, no real data)."""
import numpy as np
import pytest

from pbo.french import DATA, FACTORS, INDUSTRIES, ar_residuals, demean_by_period, load_market, load_returns, parse_table, prepare

# Same layout as the real file: notes, value-weighted table, blank line, equal-weighted table.
FIXTURE = """This file was created using the 202609 CRSP database.

  Average Value Weighted Returns -- Daily
,Agric,Food
19710630,   9.00,   9.00
19710701,   1.00,  -2.00
19710702,   3.00,   0.00

  Average Equal Weighted Returns -- Daily
,Agric,Food
19710701,   7.00,   7.00
"""


def test_parse_reads_only_the_value_weighted_table():
    dates, values = parse_table(FIXTURE)
    assert list(dates) == [19710630, 19710701, 19710702]
    assert values.tolist() == [[9.0, 9.0], [1.0, -2.0], [3.0, 0.0]]     # the 7.00 rows are never read


def test_prepare_cuts_window_converts_percent_and_demeans():
    dates, returns = prepare(*parse_table(FIXTURE), 19710701, 19710702)
    assert list(dates) == [19710701, 19710702]
    # decimal returns 0.01, 0.03 and -0.02, 0.00; means 0.02 and -0.01 removed
    assert returns == pytest.approx(np.array([[-0.01, -0.01], [0.01, 0.01]]))


@pytest.mark.parametrize("bad", [-99.99, -999.0, np.nan])
def test_prepare_rejects_missing_values(bad):
    dates, values = parse_table(FIXTURE)
    values[1, 0] = bad
    with pytest.raises(ValueError):
        prepare(dates, values, 19710701, 19710702)


def test_prepare_rejects_duplicate_dates():
    dates, values = parse_table(FIXTURE)
    dates[1] = dates[0]
    with pytest.raises(ValueError):
        prepare(dates, values, 19710630, 19710702)


def test_prepare_rejects_unsorted_dates():
    dates, values = parse_table(FIXTURE)
    with pytest.raises(ValueError):
        prepare(dates[::-1], values, 19710630, 19710702)


def test_ar_residuals_remove_exact_ar1():
    # x_t = 0.5 x_(t-1) + 1 exactly: an AR(1) fit with intercept leaves zero residuals
    x = np.empty(50)
    x[0] = 3.0
    for t in range(1, 50):
        x[t] = 0.5 * x[t - 1] + 1
    assert ar_residuals(x[:, None], 1) == pytest.approx(np.zeros((49, 1)), abs=1e-9)


@pytest.mark.skipif(not (DATA / FACTORS[0]).exists(), reason="frozen factors file not downloaded (git-ignored)")
def test_load_market_frozen_snapshot():
    # Same calendar as the step 4 industry window: 13,929 days from 1971-07-01 to 2026-09-30, finite decimals.
    dates, mkt_rf, rf = load_market()
    assert len(dates) == len(mkt_rf) == len(rf) == 13929
    assert (dates[0], dates[-1]) == (19710701, 20260930)
    assert np.isfinite(mkt_rf).all() and np.isfinite(rf).all()
    assert np.abs(mkt_rf).max() < 0.5 and (rf >= 0).all()    # decimals, not percent


@pytest.mark.parametrize("text", [
    "19600101,1,2,3,0\n",                 # no observations in the frozen window
    "19710701,1,2,3,0\n20260930,1,2,3,0\n",  # endpoints alone do not establish calendar coverage
    "19710701,1,2\n",                    # missing factor columns
])
def test_load_market_rejects_incomplete_frozen_schema(monkeypatch, text):
    monkeypatch.setattr("pbo.french.read_snapshot", lambda *args: text)
    with pytest.raises(ValueError, match="factors|window"):
        load_market()


def test_demean_by_period_closed_form():
    dates = np.array([1, 2, 3, 4])
    data = np.array([[1.0, 5.0], [3.0, 7.0], [10.0, 0.0], [20.0, 2.0]])
    early, late = demean_by_period(dates, data, 3)
    assert np.allclose(early, [[-1, -1], [1, 1]]) and np.allclose(late, [[-5, -1], [5, 1]])
    with pytest.raises(ValueError):
        demean_by_period(dates, data, 9)


@pytest.mark.skipif(not (DATA / INDUSTRIES[0]).exists(), reason="frozen industries file not downloaded (git-ignored)")
def test_corrected_g6_populations_have_zero_mean():
    # The corrected G6 null: every industry has mean 0 within each period (1971-98 and 1999-2026).
    dates, data, _ = load_returns()
    for period in demean_by_period(dates, data, 19990101):
        assert np.abs(period.mean(axis=0)).max() < 1e-12


@pytest.mark.parametrize("dates, data, split", [
    ([[1, 2]], [[1.], [2.]], 2),         # dates must be 1-D
    ([1, 2], [1., 2.], 2),              # returns must be a panel
    ([1, 2, 3], [[1.], [2.]], 2),       # one date per panel row
    ([1, np.nan, 3], [[1.], [2.], [3.]], 2),
    ([1, 2], [[np.nan], [2.]], 2),
    ([1, 2], [[], []], 2),              # no industry columns
    ([1, 2], [[1.], [2.]], np.nan),
    ([1, 2], [[1.], [2.]], [2]),         # split must be scalar
])
def test_demean_by_period_rejects_invalid_panels(dates, data, split):
    with pytest.raises(ValueError):
        demean_by_period(np.asarray(dates), np.asarray(data), split)
