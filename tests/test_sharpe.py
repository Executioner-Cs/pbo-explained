import numpy as np
import pytest

from pbo import paper_values as pv
from pbo.sharpe import sharpe

# Synthetic inputs, not paper values. Any mean and sd work; the expected value is derived from them.
MU, SD = 0.0004, 0.01
Q = pv.PERIODS_PER_YEAR
EXPECTED = MU / SD * np.sqrt(Q)  # PSEUDO Eq. 2.2


def alternating(n):
    # mean exactly MU, population sd (ddof=0) exactly SD
    return MU + SD * np.resize([1.0, -1.0], n)


def test_closed_form():
    assert sharpe(alternating(1000), Q) == pytest.approx(EXPECTED, rel=1e-12)


def test_ddof_zero():
    # with ddof=1 the sd becomes SD*sqrt(2), so the answer would be smaller by sqrt(2)
    assert sharpe(alternating(2), Q) == pytest.approx(EXPECTED, rel=1e-12)


def test_scale_invariance():
    r = alternating(1000)
    assert sharpe(2 * r, Q) == pytest.approx(sharpe(r, Q), rel=1e-12)


def test_constant_raises():
    with pytest.raises(ValueError):
        sharpe(np.full(100, MU), Q)
