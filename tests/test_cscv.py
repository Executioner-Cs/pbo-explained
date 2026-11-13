import math

import numpy as np
import pytest

from pbo import paper_values as pv
from pbo.cscv import cscv, rank, splits


# --- rank: PBO p.9, 1 = worst, N = best

def test_rank_paper_example():
    assert list(rank(pv.PBO_RANK_EX_R_IS)) == list(pv.PBO_RANK_EX_RANK_IS)
    assert list(rank(pv.PBO_RANK_EX_R_OOS)) == list(pv.PBO_RANK_EX_RANK_OOS)


# --- splits: Algorithm 2.3, Third and Fourth (pp.11-12), Figure 1 (p.13)

def test_splits_match_figure_1():
    assert splits(pv.PBO_FIG1_S) == [tuple(map(tuple, p)) for p in pv.PBO_FIG1_SPLITS]


@pytest.mark.parametrize("s", [2, 4, 8, pv.PBO_S16])
def test_number_of_splits_eq_2_3(s):
    assert len(splits(s)) == math.comb(s, s // 2)


def test_paper_s16_count_is_a_typo():
    # Documents the typo on p.11. If this fails, the paper was right and our reading is wrong.
    assert len(splits(pv.PBO_S16)) == math.comb(pv.PBO_S16, pv.PBO_S16 // 2) != pv.PBO_S16_PRINTED


@pytest.mark.parametrize("s", [2, 4, 8])
def test_is_and_oos_disjoint_and_cover_all(s):
    for is_b, oos_b in splits(s):
        assert len(is_b) == len(oos_b) == s // 2
        assert set(is_b).isdisjoint(oos_b)
        assert set(is_b) | set(oos_b) == set(range(s))


@pytest.mark.parametrize("s", [3, 0, -2])
def test_s_must_be_positive_even(s):
    with pytest.raises(ValueError):
        splits(s)


def test_t_not_divisible_by_s_raises():
    # Algorithm 2.3, Second: blocks "of equal dimensions"
    with pytest.raises(ValueError):
        cscv(np.ones((10, 3)), 4)


# --- cscv: hand-worked cases. Each block has 2 rows, [m + d, m - d], so its Sharpe is m / d.
# Values with Sharpe +3: [2, 1]. Sharpe -3: [-1, -2]. Sharpe +1: [2, 0].

UP, DOWN, MID = [2.0, 1.0], [-1.0, -2.0], [2.0, 0.0]


def matrix(*columns):
    # each column is a list of blocks; stack blocks top to bottom
    return np.column_stack([np.concatenate(c) for c in columns])


def test_winner_stays_winner_gives_pbo_0():
    # strategy 0 best in both blocks. IS pick = 0, OOS rank 2 of 2: omega = 2/3, logit = ln 2.
    pbo, logits = cscv(matrix([UP, UP], [DOWN, DOWN]), 2)
    assert pbo == 0
    assert logits == pytest.approx([math.log(2)] * 2)


def test_winner_flips_to_loser_gives_pbo_1():
    # strategy 0 best in block A, worst in B. Strategy 1 the opposite.
    pbo, logits = cscv(matrix([UP, DOWN], [DOWN, UP]), 2)
    assert pbo == 1
    assert logits == pytest.approx([-math.log(2)] * 2)


def test_median_oos_rank_counts_as_overfit():
    # N = 3. IS winner always lands at OOS rank 2 = the median: omega = 1/2, logit = 0.
    # Our choice: logit 0 counts (integral up to 0, p.13). FLAGGED in docs/methods/cscv.md.
    pbo, logits = cscv(matrix([UP, MID], [MID, UP], [DOWN, DOWN]), 2)
    assert logits == pytest.approx([0.0, 0.0])
    assert pbo == 1


def test_logit_formula():
    # Step g (p.12): lambda = ln(omega / (1 - omega)), omega = rank / (N + 1). Closed form for N = 2, rank 2: ln 2.
    _, logits = cscv(matrix([UP, UP, UP, UP], [DOWN, DOWN, DOWN, DOWN]), 4)
    assert len(logits) == math.comb(4, 2)
    assert logits == pytest.approx([math.log(2)] * math.comb(4, 2))


def test_zero_variance_column_raises():
    # Same rule as sharpe(): Sharpe is undefined, so a silent nan/inf pick is not allowed.
    with pytest.raises(ValueError):
        cscv(matrix([UP, UP], [[1.0, 1.0], [1.0, 1.0]]), 2)


# Four strategies, four blocks, a fractional PBO. Block Sharpes: UP +3, DOWN -3, MID +1, LOW -1, HIGH +2.
# Strategy 0 = UP UP DOWN DOWN: Sharpe +3 on AB, -3 on CD, 0 on any mixed pair. Strategies 1-3 are constant.
# AB|CD: pick 0, OOS ranks it 1 of 4 -> omega 1/5, logit ln(1/4).
# 4 mixed splits: pick 3 (Sharpe 2 > 1 > 0 > -1), OOS still best -> omega 4/5, logit ln 4.
# CD|AB: pick 3, OOS strategy 0 has +3 so 3 ranks 3 of 4 -> omega 3/5, logit ln(3/2).
# PBO = 1/6. Also checks which blocks go to IS, since the blocks differ.
LOW, HIGH = [0.0, -2.0], [3.0, 1.0]


def test_four_strategy_hand_worked_pbo():
    m = matrix([UP, UP, DOWN, DOWN], [MID] * 4, [LOW] * 4, [HIGH] * 4)
    pbo, logits = cscv(m, 4)
    expected = [math.log(1 / 4)] + [math.log(4)] * 4 + [math.log(3 / 2)]
    assert logits == pytest.approx(expected)
    assert pbo == pytest.approx(1 / 6)


def test_nan_raises():
    m = matrix([UP, UP], [DOWN, DOWN])
    m[0, 1] = np.nan
    with pytest.raises(ValueError):
        cscv(m, 2)


def test_constant_column_with_rounding_raises():
    # np.full(n, 0.1).std() is not exactly 0 in floating point. Must still be rejected.
    m = np.column_stack([np.resize([1.0, -1.0], 992), np.full(992, 0.1)])
    with pytest.raises(ValueError):
        cscv(m, 16)


@pytest.mark.parametrize("s", [0, -2, 3])
def test_cscv_bad_s_raises_value_error(s):
    with pytest.raises(ValueError):
        cscv(np.ones((12, 2)), s)


def plain_algorithm_2_3(m, s):
    # Step-by-step Algorithm 2.3 (pp.11-12): copy J and J-bar per split, two-pass std. Slow but direct.
    t, n = m.shape
    rows = np.arange(t).reshape(s, t // s)
    odds = []
    for is_b, oos_b in splits(s):
        j, jbar = m[rows[list(is_b)].ravel()], m[rows[list(oos_b)].ravel()]
        best = np.argmax(j.mean(0) / j.std(0))
        w = rank(jbar.mean(0) / jbar.std(0))[best] / (n + 1)
        odds.append(w / (1 - w))
    # Keep the independent two-pass Sharpe/rank oracle, but use the same final log kernel:
    # scalar libm and vector NumPy logs need not be bit-identical across CPUs/platforms.
    return np.log(np.asarray(odds))


@pytest.mark.parametrize("s", [4, 8, 16])
def test_fast_cscv_matches_plain_algorithm(s):
    # cscv uses block sums for speed. It must give the same logits as the direct loop.
    # Random input, shifted and scaled (our choice), to stress the sum-of-squares variance.
    rng = np.random.default_rng(s)
    m = 37.0 + 5.0 * rng.standard_normal((s * 31, 50))
    assert np.array_equal(cscv(m, s)[1], plain_algorithm_2_3(m, s))


# --- ties: average ranks (our choice, same as R pbo and pypbo; the paper has no ties)

def test_cscv_needs_two_strategies():
    with pytest.raises(ValueError):
        cscv(np.random.default_rng(0).standard_normal((8, 1)), 2)


def test_cscv_rejects_near_constant_strategy():
    # Column values 1 + 1e-9 noise with row 0 at 0: the one-pass variance cancels to 0 in some halves.
    m = 1 + 1e-9 * np.random.default_rng(0).standard_normal((32, 3))
    m[0] = 0.0
    with pytest.raises(ValueError):
        cscv(m, 4)


def test_rank_ties_get_average():
    # closed form: values 1, 2, 2, 3 take ranks 1, 2.5, 2.5, 4
    assert list(rank([1.0, 2.0, 2.0, 3.0])) == [1, 2.5, 2.5, 4]


def test_duplicate_strategies_share_rank():
    # Strategies 0 and 1 are identical. Strategy 2 is the mirror.
    # IS = A: Sharpes 3, 3, -3, pick 0. OOS B: -3, -3, 3, average ranks 1.5, 1.5, 3.
    #   omega = 1.5 / 4, logit = ln(0.375 / 0.625) = ln 0.6.
    # IS = B: pick 2. OOS A: strategy 2 has -3, rank 1, omega = 1/4, logit = ln(1/3).
    pbo, logits = cscv(matrix([UP, DOWN], [UP, DOWN], [DOWN, UP]), 2)
    assert logits == pytest.approx([math.log(0.6), math.log(1 / 3)])
    assert pbo == 1


@pytest.mark.parametrize("s", [2, 4, 8])
def test_cscv_matches_plain_algorithm_with_ties(s):
    # Duplicated strategies tie exactly in every split. cscv must still match the direct loop.
    rng = np.random.default_rng(100 + s)          # our choice: fixed seed
    base = rng.standard_normal((s * 6, 8))
    m = np.column_stack([base, base[:, :3]])      # strategies 8-10 copy strategies 0-2
    assert np.allclose(cscv(m, s)[1], plain_algorithm_2_3(m, s), rtol=0, atol=1e-12)


def test_cscv_rejects_too_few_rows():
    with pytest.raises(ValueError):
        cscv(np.empty((0, 2)), 2)
