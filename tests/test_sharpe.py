import numpy as np
import pytest

from pbo import paper_values as pv
from pbo.sharpe import sharpe

# Synthetic inputs, not paper values. Any mean and sd work; the expected value is derived from them.
MU, SD = 0.0004, 0.01
Q = pv.PERIODS_PER_YEAR
EXPECTED = MU / SD * np.sqrt(Q)  # PSEUDO Eq. 2.2
N_OBS = 1000  # our choice: any even length keeps mean and sd exact
REL = 1e-12   # our choice: exact identities, so only float rounding is allowed


def alternating(n):
    # mean exactly MU, population sd (ddof=0) exactly SD
    return MU + SD * np.resize([1.0, -1.0], n)


def test_closed_form():
    assert sharpe(alternating(N_OBS), Q) == pytest.approx(EXPECTED, rel=REL)


def test_ddof_zero():
    # with ddof=1 the sd becomes SD*sqrt(2), so the answer would be smaller by sqrt(2)
    assert sharpe(alternating(2), Q) == pytest.approx(EXPECTED, rel=REL)


def test_scale_invariance():
    r = alternating(N_OBS)
    assert sharpe(2 * r, Q) == pytest.approx(sharpe(r, Q), rel=REL)


def test_constant_raises():
    with pytest.raises(ValueError):
        sharpe(np.full(N_OBS, MU), Q)
