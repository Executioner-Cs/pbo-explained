# Values read from the papers

Read on 2026-11-09 and 2026-11-10 from rendered PDF pages. Constants live in src/pbo/paper_values.py. Page = PDF page of the file in papers/.
papers/ is not committed (copyright, size). Download links at the bottom.

## PSEUDO: papers/backtest-pseudo.pdf
Bailey, Borwein, Lopez de Prado, Zhu. "Pseudo-Mathematics and Financial Charlatanism".
Author copy dated April 1, 2014. Journal version: Notices of the AMS 61(5), 2014.
Page numbers are the author copy's, not the printed journal's.

| Item | Page | What the paper says | Used in |
|---|---|---|---|
| Eq. 2.2 | 7 | SR = (mu / sigma) sqrt(q), q = returns per year, on excess returns | sharpe |
| Eq. 2.3 | 8 | Annual SR estimate ~ N(SR, (1 + SR^2/(2q)) / y). SR = 0 gives SE 1/sqrt(y) | experiments/best_of_n.py |
| Prop 2.1, Eq. 2.4 | 9 | E[max_N] ~ (1-g) Zinv[1-1/N] + g Zinv[1-(1/N) e^-1], g ~ 0.5772156649, N >> 1 | expected_max_normal |
| Upper bound | 9 | "An upper bound to Eq. (2.4) is sqrt(2 ln[N])" | test_below_paper_upper_bound |
| Worked number | 9 | N = 10 gives an expected max IS Sharpe of 1.57 | test_paper_value_n10 |
| Eq. 3.1 | 9 | Annualized: multiply by y^(-1/2), y = years | experiments/best_of_n.py |
| Theorem 3.1, Eq. 3.2 | 11 | MinBTL ~ ((1-g) Zinv[1-1/N] + g Zinv[1-(1/N) e^-1]) / E[max_N])^2 < 2 ln[N] / E[max_N]^2 | min_btl_years |
| Worked number | 11 | 5 years of data: no more than 45 independent configurations, target Sharpe 1 | test_paper_45_configurations_in_5_years |

## DSR: papers/deflated-sharpe.pdf
Bailey, Lopez de Prado. "The Deflated Sharpe Ratio". J. Portfolio Management, 2014.

| Item | Page | What the paper says | Used in |
|---|---|---|---|
| Eq. 1 | 7 | E[max SR_n] ~ E[SR_n] + sqrt(V[SR_n]) * (same bracket as PSEUDO Eq. 2.4) | expected_max_normal |
| Eq. 5, 6 | 12 | Same formula, standard normal and rescaled | cross-check |
| Snippet 1 | 13 | Python: emc=0.5772156649; (1-emc)*norm.ppf(1-1/N) + emc*norm.ppf(1-1/(N*e)) | cross-check |
| q = 250 | 10 | 250 observations per year in the example | PERIODS_PER_YEAR |
| Example inputs | 9 | N = 100, V[{SR_n}] = 1/2, T = 1250, skew -3, kurt 10 | DSR_EX_N, DSR_EX_V_ANNUAL |
| Example SR0 | 10 | sqrt(1/(2*250)) * E[max_100] ~ 0.1132, non-annualized | test_dsr_example_sr0 |
| Example DSR (step 3) | 10 | SR 2.5 annual, T = 1250, skew -3, kurt 10, N = 100, V = 1/2: DSR ~ 0.9004 | tests/test_psr_dsr.py |
| Example DSR (step 3) | 10 | Same but N = 46: DSR = 0.9505 | tests/test_psr_dsr.py |
| Example DSR (step 3) | 10 | Normal returns (skew 0, kurt 3), N = 88: DSR = 0.9505 | tests/test_psr_dsr.py |
| Kurtosis convention (step 3) | 10 | Denominator uses (kurt - 1)/4 with kurt = 3 for normal: raw kurtosis, not excess | TODO 3.2 closed |
| T in DSR (step 3) | 10 | Uses sqrt(T - 1) = sqrt(1249) | tests/test_psr_dsr.py |

## SF: papers/sharpe-frontier.pdf
PSR (Eq. 11, p.9), MinTRL (Eq. 13, p.11) and their worked examples (pp.10-11): see docs/psr_dsr_notes.md
and src/pbo/paper_values.py (PSR_EX_*, MINTRL_EX_*).

## Claims from the original brief that the papers do NOT support
- "about 2 years for N = 7": not found in PSEUDO text. Dropped from tests.
- Oracle 2.4794 for N = 10 and the "2.46" in the formula notes: neither is printed in the paper. Dropped.

## Read later
- PBO paper (papers/backtest-prob.pdf): pp.9-14 and 25-27 read in step 2. Its values and pages are in
  docs/cscv_notes.md and src/pbo/paper_values.py.
- papers/sharpe-frontier.pdf (PSR, MinTRL). Read in step 3.
- papers/overfit-tools.pdf p.2 repeats the 45 configurations / 5 years claim, citing PSEUDO.

## Download links
- PSEUDO: https://www.davidhbailey.com/dhbpapers/backtest-pseudo.pdf
- DSR: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf
- PBO: https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf
- PSR: https://www.davidhbailey.com/dhbpapers/sharpe-frontier.pdf
- Tools: https://www.davidhbailey.com/dhbpapers/overfit-tools.pdf
- Christie (2005), "Is the Sharpe ratio useful in asset allocation?", Macquarie Applied Finance Centre, SSRN 720801
  (papers/christie-2005.pdf)
- Opdyke (2007), "Comparing Sharpe ratios: So where are the p-values?", Journal of Asset Management 8(5),
  preprint SSRN 886728 (papers/opdyke-2007.pdf)
