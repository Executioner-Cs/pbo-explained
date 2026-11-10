# PSR, MinTRL, DSR notes (step 3)

Sources (page = PDF page):
- SF = papers/sharpe-frontier.pdf, Bailey and Lopez de Prado, "The Sharpe Ratio Efficient Frontier". Read pp.8-11.
- DSR = papers/deflated-sharpe.pdf, Bailey and Lopez de Prado, "The Deflated Sharpe Ratio". Read pp.8-10, 13.

## Formulas (code: src/pbo/psr_dsr.py)
- SR estimator variance, SF Eq. 8 (p.8): (1 + SR^2/2 - g3 SR + (g4 - 3)/4 SR^2) / n.
  Same as (1 - g3 SR + (g4 - 1)/4 SR^2) / n, the form used in Eq. 11 and 13.
- PSR, SF Eq. 11 (p.9): Z[(SR - SR*) sqrt(n - 1) / sqrt(1 - g3 SR + (g4 - 1)/4 SR^2)].
  Non-annualized SR, in the frequency of the returns (SF p.9).
- MinTRL, SF Eq. 13 (p.11): 1 + (1 - g3 SR + (g4 - 1)/4 SR^2) (Z_alpha / (SR - SR*))^2. Observations, not years.
  Defined for SR > SR* (p.10). Z_alpha = Z^-1[1 - alpha].
- DSR, DSR Eq. 2 (p.8): PSR(SR0) with sqrt(T - 1), SR0 = sqrt(V[{SR_n}]) E[max_N] (E[max] as in step 1).
- Kurtosis g4 is raw: Normal is g3 = 0, g4 = 3 (SF p.10, DSR p.10). TODO 3.2 closed.
  Also checked by computation: excess kurtosis gives 0.920 vs the paper's 0.913, and 0.9018 vs 0.9004.

## Paper examples used as tests (constants in src/pbo/paper_values.py)
- PSR (SF p.10): monthly SR 0.458, 2 years: 0.982 Normal, 0.913 with skew -2.448 and kurt 10.164,
  0.953 with 3 years. The SR is printed to 3 digits; the tests allow for that rounding (psr_range).
  Without it the 3-year case misses by 0.000005 (0.95351 vs 0.953).
- MinTRL (SF p.11): annual SR 2 vs 1 at 95%: 2.73 y daily, 2.83 weekly, 3.24 monthly; 4.99 monthly with HFR
  skew -0.72, kurt 5.78. Our choice: q = 250 daily (DSR p.10), 52 weekly, 12 monthly. q = 252 also gives 2.73.
- DSR (DSR pp.9-10): annual SR 2.5, T = 1250, skew -3, kurt 10, V = 1/2 annual, N = 100: 0.9004.
  N = 46: 0.9505. Normal returns, N = 88: 0.9505. V is converted to per period by dividing by 250.

## Our choices
- Skew and kurtosis in experiments: scipy population estimators (skew, kurtosis(fisher=False)). Papers do not fix them.
- V[{SR_n}] in the experiment: sample variance of the N per-period Sharpes, ddof = 1. DSR p.8 names the
  variance across trials but not the estimator.
- PSR rejects inputs where 1 - g3 SR + (g4 - 1)/4 SR^2 <= 0 (variance would be negative), and n < 2.
- MinTRL rejects alpha outside (0, 0.5): squaring Z_alpha would hide its sign. sr0 rejects negative variance.
- Benchmark 0 in the experiment: the skill-less default (SF p.8, note 4).

## Snippet 1 (DSR p.13)
The paper's Python code. getExpMaxSR is the same formula as our expected_max_normal (step 1).
getDistMaxSR checks it by Monte Carlo. We check the same thing by numerical integration
(tests/test_minbtl.py) and by simulation (experiments/best_of_n.py). Not copied, not needed later.

## Experiment 3.15 (experiments/dsr_false_positives.py)
Best of 100 zero-edge strategies, T = 1250, 2000 datasets. Flagged skilled at 95%:
PSR(0) 1983/2000 = 0.9915 (exact 95% CI 0.986 to 0.995). DSR 1/2000 = 0.0005 (exact 95% CI 0.0000 to 0.0028).
Closed-form approximation with V known: 1 - Phi(E[max_N] + z_0.95)^N = 0.0015. The code estimates V from the
same trials instead. That makes SR0 random too; this repo does not establish whether it moves the rate up or down.
The observed interval (0 to 0.0028) contains 0.0015. Both say the same thing: far below 5%.
So DSR is far stricter than 5% for the best-of-N pick: it compares the max to E[max] but uses the
standard error of a single SR, and the max varies much less than a single SR.
Assumptions of the approximation: IID Normal strategies, skew 0, kurt 3, Eq. 2.4 for E[max].
