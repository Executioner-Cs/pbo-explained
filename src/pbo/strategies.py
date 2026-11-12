"""Moving-average crossover strategy family (step 5)."""
import numpy as np


def moving_average(x, window):
    """Mean of the last `window` values at each day; NaN before the first full window."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or not np.isfinite(x).all():
        raise ValueError("x must be a finite 1-D array")
    if isinstance(window, (bool, np.bool_)) or not isinstance(window, (int, np.integer)) or not 1 <= window <= len(x):
        raise ValueError("window must be an integer between 1 and the series length")
    c = np.concatenate([[0.0], np.cumsum(x)])
    out = np.full(len(x), np.nan)
    out[window - 1:] = (c[window:] - c[:-window]) / window
    return out


def ma_crossover(prices, excess, fast, slow, cost):
    """Daily excess return: long the market while the fast MA of prices is above the slow MA, otherwise flat.

    The signal at the close of day t sets the position for day t + 1, so day t's return never depends on day t's
    price. cost is charged per unit change in position (0.0005 = 5 bps).
    """
    prices, excess = np.asarray(prices, dtype=float), np.asarray(excess, dtype=float)
    if prices.ndim != 1 or prices.shape != excess.shape or not (np.isfinite(prices).all() and np.isfinite(excess).all()):
        raise ValueError("prices and excess must be finite 1-D arrays of the same length")
    if not 1 <= fast < slow:
        raise ValueError("need 1 <= fast < slow")
    if not cost >= 0 or not np.isfinite(cost):
        raise ValueError("cost must be a finite number >= 0")
    signal = moving_average(prices, fast) > moving_average(prices, slow)   # False until both averages exist
    position = np.concatenate([[0.0], signal[:-1]])
    return position * excess - cost * np.abs(np.diff(position, prepend=0.0))


def crossover_panel(prices, excess, settings, cost, blocks):
    """Return (start, return matrix) for fast/slow pairs on common complete blocks.

    Drop the longest slow window and any leading remainder. Build positions before trimming so positions and
    trading costs carry through the boundary, rather than starting each retained sample flat.
    """
    if not settings:
        raise ValueError("settings must contain at least one fast/slow pair")
    if isinstance(blocks, (bool, np.bool_)) or not isinstance(blocks, (int, np.integer)) or blocks < 1:
        raise ValueError("blocks must be a positive integer")
    panel = np.column_stack([ma_crossover(prices, excess, fast, slow, cost) for fast, slow in settings])
    warmup = max(slow for _, slow in settings)
    start = warmup + (len(panel) - warmup) % blocks
    if start >= len(panel):
        raise ValueError("not enough observations after warm-up for one complete block")
    return start, panel[start:]
