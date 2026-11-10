"""CSCV and PBO. PBO paper (papers/backtest-prob.pdf), Algorithm 2.3, pp.11-12, and Sec 3.1, p.13."""
from itertools import combinations

import numpy as np


def rank(values):
    """Ranks with 1 = worst, N = best (PBO p.9 example). Ties are not handled."""
    return np.argsort(np.argsort(values)) + 1


def splits(s):
    """All (IS blocks, OOS blocks) pairs for S blocks, in Figure 1 order (p.13). Count is Eq. 2.3."""
    if s <= 0 or s % 2:
        raise ValueError("S must be a positive even number")
    blocks = range(s)
    return [(c, tuple(b for b in blocks if b not in c)) for c in combinations(blocks, s // 2)]


def cscv(m, s):
    """Return (PBO, logits) for a T x N matrix of per-period P&L, using S blocks."""
    m = np.asarray(m, dtype=float)
    if not np.isfinite(m).all():
        raise ValueError("M has NaN or inf; argmax and ranks would silently misplace them")
    pairs = splits(s)                                 # checks S is positive and even
    t, n = m.shape
    if t % s:
        raise ValueError("T must divide into S equal blocks")
    blocks = m.reshape(s, t // s, n)                  # Second: S disjoint blocks, original order

    # Every half of the blocks occurs once as IS and once as another split's OOS. Compute its
    # Sharpe vector once, in batches, from block sums instead of repeatedly copying T/2 rows.
    offset = m[0]
    centered = blocks - offset                        # keeps the sum-of-squares variance stable
    block_sum = centered.sum(axis=1)
    block_sumsq = np.square(centered).sum(axis=1)
    block_min = blocks.min(axis=1)
    block_max = blocks.max(axis=1)
    combinations_array = np.asarray([is_b for is_b, _ in pairs], dtype=int)
    observations = t // 2
    sharpes = np.empty((len(pairs), n))
    batch_size = 256                                  # bounds temporary arrays to a few MB
    for start in range(0, len(pairs), batch_size):
        chosen = combinations_array[start:start + batch_size]
        if np.any(block_max[chosen].max(axis=1) - block_min[chosen].min(axis=1) == 0):
            raise ValueError("a strategy has zero variance in a subsample; Sharpe is undefined")
        sums = block_sum[chosen].sum(axis=1)
        sumsqs = block_sumsq[chosen].sum(axis=1)
        means = sums / observations
        variances = np.maximum(sumsqs / observations - means * means, 0.0)
        sharpes[start:start + len(chosen)] = (offset + means) / np.sqrt(variances)

    combination_index = {is_b: i for i, (is_b, _) in enumerate(pairs)}
    complements = np.asarray([combination_index[oos_b] for _, oos_b in pairs])
    best = np.argmax(sharpes, axis=1)                 # c, e. best IS strategy n*
    oos_order = np.argsort(sharpes[complements], axis=1)
    oos_ranks = np.empty_like(oos_order)
    np.put_along_axis(oos_ranks, oos_order, np.arange(1, n + 1), axis=1)
    w = oos_ranks[np.arange(len(pairs)), best] / (n + 1)  # d, f. relative OOS rank omega
    logits = np.log(w / (1 - w))                     # g. logit lambda
    return np.mean(logits <= 0), logits               # Sec 3.1: PBO = share of logits <= 0
