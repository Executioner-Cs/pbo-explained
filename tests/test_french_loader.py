"""Parser and cleaning of the French file, on a tiny hand-written fixture (no network, no real data)."""
import numpy as np
import pytest

from pbo.french import ar_residuals, parse_table, prepare

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
