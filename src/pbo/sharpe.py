import numpy as np


def sharpe(returns, periods_per_year):
    """Annualized Sharpe ratio, SR = (mu / sigma) * sqrt(q) (PSEUDO Eq. 2.2, p.7).

    returns: excess returns, as the paper defines them. q = periods_per_year.
    ddof=0 is our choice; PSEUDO says only "sample standard deviation". Precedent: the SF appendix A.4 code
    (get_Moments, pp.27-28) divides moments by the number of observations.
    """
    r = np.asarray(returns, dtype=float)
    if r.ndim != 1 or r.size == 0 or not np.isfinite(r).all():
        raise ValueError("returns must be a finite nonempty 1-D array")
    if (isinstance(periods_per_year, (bool, np.bool_)) or np.ndim(periods_per_year) != 0
            or not np.isfinite(periods_per_year) or periods_per_year <= 0):
        raise ValueError("periods_per_year must be a positive finite scalar")
    if np.ptp(r) == 0:
        raise ValueError("returns have zero variance; Sharpe is undefined")
    r = np.ldexp(r, -np.frexp(np.abs(r).max())[1])  # exact power-of-two rescale: squares cannot overflow or underflow
    return r.mean() / r.std(ddof=0) * np.sqrt(periods_per_year)
