import numpy as np


def sharpe(returns, periods_per_year):
    """Annualized Sharpe ratio, SR = (mu / sigma) * sqrt(q) (PSEUDO Eq. 2.2, p.7).

    returns: excess returns, as the paper defines them. q = periods_per_year.
    ddof=0 is our choice; PSEUDO says only "sample standard deviation". Precedent: the SF appendix A.4 code
    (get_Moments, pp.27-28) divides moments by the number of observations.
    """
    r = np.asarray(returns, dtype=float)
    if np.ptp(r) == 0:
        raise ValueError("returns have zero variance; Sharpe is undefined")
    return r.mean() / r.std(ddof=0) * np.sqrt(periods_per_year)
