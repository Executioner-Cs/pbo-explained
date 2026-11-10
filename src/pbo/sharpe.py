import numpy as np


def sharpe(returns, periods_per_year):
    """Annualized Sharpe ratio, SR = (mu / sigma) * sqrt(q) (PSEUDO Eq. 2.2, p.7).

    returns: excess returns, as the paper defines them. q = periods_per_year.
    ddof=0 is our choice. The paper says "sample standard deviation" and does not fix ddof.
    """
    r = np.asarray(returns, dtype=float)
    if np.ptp(r) == 0:
        raise ValueError("returns have zero variance; Sharpe is undefined")
    return r.mean() / r.std(ddof=0) * np.sqrt(periods_per_year)
