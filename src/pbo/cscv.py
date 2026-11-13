"""CSCV and PBO. PBO paper (papers/backtest-prob.pdf), Algorithm 2.3, pp.11-12, and Sec 3.1, p.13."""
from itertools import combinations

import numpy as np
from scipy.stats import rankdata


def rank(values):
    """Ranks with 1 = worst, N = best (PBO p.9 example).

    Ties get the average of their ranks. The paper ranks permutations (p.9) and never has ties.
    Average is our choice; the R pbo and Python pypbo packages do the same.
    """
    return rankdata(values, method="average")


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
    if m.ndim != 2:
        raise ValueError("M must be a T x N matrix")
    t, n = m.shape
    if t < s:
        raise ValueError("T must be at least S")
    if n < 2:
        raise ValueError("CSCV needs at least 2 strategies")
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
        with np.errstate(divide="ignore", invalid="ignore"):  # a zero variance is caught just below
            sharpes[start:start + len(chosen)] = (offset + means) / np.sqrt(variances)
    if not np.isfinite(sharpes).all():                # near-constant columns can cancel the variance to 0
        raise ValueError("a subsample Sharpe is not finite (near-constant strategy)")

    combination_index = {is_b: i for i, (is_b, _) in enumerate(pairs)}
    complements = np.asarray([combination_index[oos_b] for _, oos_b in pairs])
    best = np.argmax(sharpes, axis=1)                 # c, e. best IS strategy n*; IS ties go to the first column
    # d, f. OOS rank of the IS-best strategy, by the same average-rank rule as rank(): the number of strategies
    # below it, plus half of the ties counting itself. Equal to ranking all N and picking n*, without the full sort.
    oos = sharpes[complements]
    selected = oos[np.arange(len(pairs)), best][:, None]   # OOS Sharpe of n* in each split
    oos_rank = (oos < selected).sum(axis=1) + ((oos == selected).sum(axis=1) + 1) / 2
    w = oos_rank / (n + 1)                            # relative OOS rank omega
    logits = np.log(w / (1 - w))                     # g. logit lambda
    # Sec 3.1: PBO = integral of f up to 0. Counting logit = 0 is our reading; Def 2.2 (p.10) uses rank < N/2.
    # See docs/cscv_notes.md.
    return np.mean(logits <= 0), logits
