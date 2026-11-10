"""Numbers quoted from the papers in papers/. Page = PDF page of that file.

Every constant used by tests/ or experiments/ that comes from a paper lives here, with its source.
Tolerance rule: half a unit in the last digit the paper prints.

PSEUDO = papers/backtest-pseudo.pdf
    Bailey, Borwein, Lopez de Prado, Zhu, "Pseudo-Mathematics and Financial Charlatanism",
    author copy dated April 1, 2014 (journal version: Notices of the AMS 61(5), 2014).
DSR = papers/deflated-sharpe.pdf
    Bailey, Lopez de Prado, "The Deflated Sharpe Ratio", J. Portfolio Management, 2014.
"""

# DSR p.10, numerical example: 250 observations per year (daily data).
# PSEUDO Eq. 2.2 (p.7) leaves q, "the number of returns per year", open. We use the DSR figure.
PERIODS_PER_YEAR = 250

# PSEUDO p.9, text after Prop 2.1 (Eq. 2.4): N = 10 trials gives an expected max IS Sharpe of 1.57.
EMAX_N = 10
EMAX_N10 = 1.57
EMAX_N10_TOL = 0.005

# PSEUDO p.11, text after Theorem 3.1 (Eq. 3.2): with 5 years of data,
# "no more than 45 independent model configurations should be tried" for a target Sharpe of 1.
MINBTL_YEARS = 5
MINBTL_MAX_N = 45
MINBTL_TARGET = 1

# DSR p.10, numerical example: SR0 = sqrt(1/(2*250)) * E[max_100] ~= 0.1132 (non-annualized).
# V[{SR_n}] = 1/2 annualized, 250 observations per year, N = 100.
DSR_EX_N = 100
DSR_EX_V_ANNUAL = 0.5
DSR_EX_PPY = PERIODS_PER_YEAR
DSR_EX_SR0 = 0.1132
DSR_EX_SR0_TOL = 0.00005
