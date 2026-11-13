# Paper constants: page check

Date: 2026-11-10. Method: each cited PDF page rendered as an image and read; every constant in
src/pbo/paper_values.py compared with the printed value. Replaces the removed text-search script,
which could not read values inside equation images.

Pages viewed: PSEUDO 7, 9, 11. DSR 9, 10. PBO 9, 11, 13, 25, 26. SF 9, 10, 11, 12.
(PSEUDO = backtest-pseudo.pdf, DSR = deflated-sharpe.pdf, PBO = backtest-prob.pdf, SF = sharpe-frontier.pdf.)

Result: 45 match, 0 mismatch, 7 derived (tolerances, aliases, monthly = 12). 52 constants.

| Constant | Value | Page | Printed on the page | Verdict |
|---|---|---|---|---|
| PERIODS_PER_YEAR | 250 | DSR 10 | "with 250 observations per year" | match |
| EMAX_N, EMAX_N10 | 10, 1.57 | PSEUDO 9 | "N = 10 alternative configurations", "Sharpe ratio IS of 1.57" | match |
| MINBTL_YEARS, _MAX_N, _TARGET | 5, 45, 1 | PSEUDO 11 | "only 5 years of data", "no more than 45", "fixed at 1" | match |
| DSR_EX_N, DSR_EX_V_ANNUAL | 100, 0.5 | DSR 9 | "N = 100", "V = 1/2" | match ("annualized" inferred from p.10) |
| DSR_EX_SR0 | 0.1132 | DSR 10 | "sqrt(1/(2*250)) (...) ~= 0.1132" | match |
| PBO_RANK_EX_* | (0.5,1.1,0.7) (1,3,2) (0.6,0.7,1.3) (1,2,3) | PBO 9 | same tuples | match |
| PBO_FIG1_S, PBO_FIG1_SPLITS | 4, AB/CD ... CD/AB | PBO 13 | Figure 1, same rows and order | match |
| PBO_S16, PBO_S16_PRINTED | 16, 12780 | PBO 11 | "if S = 16, we will form 12,780" (C(16,8) = 12,870: typo) | match |
| PBO_EX_T | 1000 | PBO 25, 26 | "1,000 daily prices (about 4 years)" in both examples | match |
| PSR_EX_YEARS, _LONG | 2, 3 | SF 9, 10 | "last two years", "3 years instead of 2" | match |
| PSR_EX_SR, _SKEW, _KURT | 0.458, -2.448, 10.164 | SF 10 | same values | match |
| PSR_EX_NORMAL, _NON_NORMAL, _LONG | 0.982, 0.913, 0.953 | SF 10 | same values; 0.953 includes skew and kurt | match |
| MINTRL_EX_SR_ANNUAL, _SR_STAR, _CONFIDENCE | 2, 1, 0.95 | SF 11 | "Sharpe of 2 ... greater than 1 at a 95% confidence level" | match |
| MINTRL_EX_YEARS_DAILY/WEEKLY/MONTHLY | 2.73, 2.83, 3.24 | SF 11 | same values | match |
| MINTRL_EX_HFR_SKEW, _KURT, _YEARS_HFR | -0.72, 5.78, 4.99 | SF 11 | same values | match |
| DSR_EX_SR_ANNUAL, _T, _SKEW, _KURT | 2.5, 1250, -3, 10 | DSR 9 | same values | match |
| DSR_EX_DSR | 0.9004 | DSR 10 | "= 0.9004 < 0.95", formula uses sqrt(1249) = sqrt(T - 1) | match |
| DSR_EX_N_ALT, _DSR_ALT | 46, 0.9505 | DSR 10 | "N=46 ... 0.9505" | match |
| DSR_EX_N_NORMAL, _DSR_NORMAL | 88, 0.9505 | DSR 10 | "Normal returns ... 0.9505 after N=88" | match |
| PBO_ACCEPT_LEVEL | 0.05 | PBO 14 | "reject models for which PBO is estimated to be greater than 0.05" (text extraction) | match |
| *_TOL, DSR_EX_PPY, PSR_EX_PPY | | | half unit of last printed digit; alias of 250; monthly = 12 | derived |

Notes from the check, now fixed in paper_values.py comments: PBO_EX_T cites pp.25-26; MinTRL cites p.11 only;
V = 1/2 "annualized" and PSR n = 24 marked as inferences; module docstring now names PBO and SF.

## Second visual check (2026-11-10)
Separate eye-check of the values that sit inside equation images. All match, no discrepancies:
- SF p.10: 0.458, -2.448, 10.164, 0.982, 0.913, 0.953
- SF p.11: -0.72, 5.78
- DSR p.9: -3, 10
- DSR p.10: 0.9004, 0.9505, and SR0 ~= 0.1132

## Third visual check (2026-11-12)
Pages rendered as images and read: DSR 8, 9, 10, 14, 15. SF 4, 8, 9, 10, 11. PBO 9, 10, 12, 13. PSEUDO 9, 11.
All match the code and docs:
- DSR p.8 Eq. 2: sqrt(T - 1), -g3 SR, (g4 - 1)/4 SR^2, SR0 = sqrt(V) E[max]. p.14 Eq. 8 and 9, rho bound
  (-1/(M-1), 1]. p.15: "for short samples T < 1/2 M(M - 1)" ... "pointless".
- SF p.8 Eq. 8 (variance over n; sigma-hat uses n - 1, Bessel). p.9 Eq. 11 sqrt(n - 1). p.11 Eq. 13 and
  "applies to an asymptotic distribution".
- PBO p.9 Def 2.1 (<= N/2), p.10 Def 2.2 (< N/2), p.12 steps f-g, p.13 Sec 3.1 integral up to 0.
- PSEUDO p.9 Eq. 2.4 and bound sqrt(2 ln N); p.11 Eq. 3.2.
Cited in step 4 text but checked in extracted text only (not as images): PBO 4, 14, 21, 22, 23; SF 15.

Re-run this check whenever paper_values.py changes.


## Publication source review (text inspection, 2026-11-12)
This is not a repeat of the rendered-page constant audit above. No numerical paper constant was changed.
- Version-specific bibliography: PBO February 27, 2015 author copy; SF July 2012 author copy; DSR July 31,
  2014 author copy; PSEUDO April 1, 2014 author copy. Journal and working-copy pagination are distinguished
  in docs/writeup.md. Publisher/author bibliographic records were consulted for the reference metadata.
- Lo (2002), The Statistics of Sharpe Ratios: journal PDF hosted at
  https://traders.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf , text of printed pp.39-40 and
  Appendix A p.47 read for non-IID inference, time aggregation, and GMM/Newey-West context. Earlier notes
  saying the paper was unavailable describe the earlier source set.
- Ledoit-Wolf: January 2008 Zurich Working Paper 320, printed pp.4-6; text inspection. Journal-PDF retrieval
  was not completed. The distinction remains explicit in the manuscript.
- Lopez de Prado and Porcu, The Deflated Sharpe Ratio: A Unified Framework for Search-Adjusted Performance
  Inference: author publication metadata and SSRN 7198158 indexed abstract consulted. Full proofs and
  alternative implementations were not assessed. The original 2014 formula remains the experimental target.
