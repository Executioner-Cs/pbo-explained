"""Numbers quoted from the papers in papers/. Page = PDF page of that file.

Every constant used by tests/ or experiments/ that comes from a paper lives here, with its source.
Tolerance rule: half a unit in the last digit the paper prints.

PSEUDO = papers/backtest-pseudo.pdf
    Bailey, Borwein, Lopez de Prado, Zhu, "Pseudo-Mathematics and Financial Charlatanism",
    author copy dated April 1, 2014 (journal version: Notices of the AMS 61(5), 2014).
DSR = papers/deflated-sharpe.pdf
    Bailey, Lopez de Prado, "The Deflated Sharpe Ratio", J. Portfolio Management, 2014.
PBO = papers/backtest-prob.pdf
    Bailey, Borwein, Lopez de Prado, Zhu, "The Probability of Backtest Overfitting".
SF = papers/sharpe-frontier.pdf
    Bailey, Lopez de Prado, "The Sharpe Ratio Efficient Frontier", J. of Risk, 2012.
Verification record: docs/paper_check.md.
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

# DSR p.9, numerical example inputs: N = 100, V[{SR_n}] = 1/2, T = 1250. p.9 does not say "annualized";
# that follows from p.10 dividing V by 250 (sqrt(1/(2*250))).
# DSR p.10: SR0 = sqrt(1/(2*250)) * E[max_100] ~= 0.1132 (non-annualized, 250 observations per year).
DSR_EX_N = 100
DSR_EX_V_ANNUAL = 0.5
DSR_EX_PPY = PERIODS_PER_YEAR
DSR_EX_SR0 = 0.1132
DSR_EX_SR0_TOL = 0.00005

# PBO = papers/backtest-prob.pdf. Bailey, Borwein, Lopez de Prado, Zhu, "The Probability of Backtest Overfitting".
# PBO p.9: Sharpe ratios IS and OOS for N = 3, and their ranks (1 = worst).
PBO_RANK_EX_R_IS = (0.5, 1.1, 0.7)
PBO_RANK_EX_RANK_IS = (1, 3, 2)
PBO_RANK_EX_R_OOS = (0.6, 0.7, 1.3)
PBO_RANK_EX_RANK_OOS = (1, 2, 3)

# PBO p.13, Figure 1: S = 4 blocks A, B, C, D (here 0, 1, 2, 3). IS blocks, OOS blocks, in printed order.
PBO_FIG1_S = 4
PBO_FIG1_SPLITS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
    ((1, 2), (0, 3)),
    ((1, 3), (0, 2)),
    ((2, 3), (0, 1)),
)

# PBO p.11: "if S = 16, we will form 12,780 combinations". Typo: Eq. 2.3 gives C(16, 8) = 12,870.
# Kept to document the typo. Tests use Eq. 2.3, not this number.
PBO_S16 = 16
PBO_S16_PRINTED = 12780

# PBO pp.25-26: "1,000 daily prices (about 4 years)" in both worked examples (first p.25, second p.26).
PBO_EX_T = 1000

# SF = papers/sharpe-frontier.pdf. Bailey, Lopez de Prado, "The Sharpe Ratio Efficient Frontier", J. of Risk, 2012.
# SF pp.9-10, PSR example: hedge fund, "monthly track record over the last two years" (p.9).
# Non-annualized monthly SR 0.458. PSR(0) = 0.982 if Normal (skew 0, kurt 3), 0.913 with skew -2.448 and
# kurt 10.164, and 0.953 with 3 years instead of 2 (p.10).
PSR_EX_PPY = 12                 # monthly (pp.9-10 say monthly; 12 per year is the calendar).
# The paper never prints n; n = 2 * 12 = 24 is inferred.
PSR_EX_YEARS = 2
PSR_EX_YEARS_LONG = 3
PSR_EX_SR = 0.458
PSR_EX_SKEW = -2.448
PSR_EX_KURT = 10.164
PSR_EX_NORMAL = 0.982
PSR_EX_NON_NORMAL = 0.913
PSR_EX_LONG = 0.953
PSR_EX_TOL = 0.0005            # half a unit in the last printed digit

# SF p.11, MinTRL examples at 95% confidence, IID Normal returns: annual SR 2 against SR* 1 needs
# 2.73 years daily, 2.83 weekly, 3.24 monthly. Monthly with HFR skew -0.72 and kurt 5.78: 4.99 years.
MINTRL_EX_SR_ANNUAL = 2
MINTRL_EX_SR_STAR_ANNUAL = 1
MINTRL_EX_CONFIDENCE = 0.95
MINTRL_EX_YEARS_DAILY = 2.73
MINTRL_EX_YEARS_WEEKLY = 2.83
MINTRL_EX_YEARS_MONTHLY = 3.24
MINTRL_EX_HFR_SKEW = -0.72
MINTRL_EX_HFR_KURT = 5.78
MINTRL_EX_YEARS_HFR = 4.99
MINTRL_EX_TOL = 0.005          # half a unit in the last printed digit

# DSR p.9, numerical example: annualized SR 2.5 over a daily sample of 5 years, T = 1250, skew -3, kurt 10.
# DSR p.10: DSR ~= 0.9004 at N = 100; 0.9505 at N = 46; Normal returns (skew 0, kurt 3) give 0.9505 at N = 88.
DSR_EX_SR_ANNUAL = 2.5
DSR_EX_T = 1250
DSR_EX_SKEW = -3
DSR_EX_KURT = 10
DSR_EX_DSR = 0.9004
DSR_EX_N_ALT = 46
DSR_EX_DSR_ALT = 0.9505
DSR_EX_N_NORMAL = 88
DSR_EX_DSR_NORMAL = 0.9505
DSR_EX_DSR_TOL = 0.00005       # half a unit in the last printed digit
