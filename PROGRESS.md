# PROGRESS

## Done
- Setup: PROGRESS.md, .gitignore, pyproject.toml.
- Packages: numpy, scipy, pytest, exact pins in requirements.txt (pytest's own dependencies install with it).
  2026-11-12: matplotlib and its 8 helper packages removed (unused, about 20 MB); add back for the step 6 plot.
  2026-11-12: environment moved to WSL (.venv/bin/python, Python 3.13).
- 2026-11-10: deleted experiments/check_oracle.py and docs/oracle_step1.md. Their numbers were typed in, and some are not in the paper.
- 2026-11-10: all paper numbers now live in src/pbo/paper_values.py, each with page and equation. Tests and experiments import from there.
- sharpe() in src/pbo/sharpe.py: 4 tests pass (closed form, ddof=0, scale invariance, zero variance raises).
- expected_max_normal() and min_btl_years() in src/pbo/minbtl.py, tested against paper values. Suite at end of step 1: 31 passed.
- 2026-11-10: paper constants are verified by a page-by-page review of rendered PDF pages, recorded in docs/paper_check.md.
  The earlier text-search script (experiments/check_paper_values.py) was removed at Mayo's request: it could not read
  values inside equation images.
- experiments/best_of_n.py: 2000 trials, 5 years daily, seed 20261109. Output in results/best_of_n.txt.
- Step 1 code complete and signed off (TODO 1.39).

## Step 2 (done)
- src/pbo/cscv.py: Algorithm 2.3 and Sec 3.1 of the PBO paper. tests/test_cscv.py. Notes in docs/cscv_notes.md.
- 2026-11-10 review by two read-only checks: formulas match the paper pages; no unlabelled numbers left.
  Fixed: DSR example inputs cited on p.9 (was p.10), lambda <= 0 note corrected, zero variance now raises in cscv.
- 2026-11-10 second review (hardcoding audit + logic review of cscv and null checks). Fixed: NaN input and
  float-rounded constant columns used to give PBO 0 silently, now raise; bad S now raises ValueError;
  added a hand-worked 4-strategy, 4-block test with PBO = 1/6.
- 2026-11-10 flags resolved (details in docs/cscv_notes.md):
  PBO uses logit <= 0 (paper Sec 3.1 integral; null gives exactly 1/2 for even N; same as R pbo and pypbo).
  Ties use average ranks (same as R pbo and pypbo). S = 16 count is 12,870; the paper's 12,780 is a typo.
  Null check output unchanged after the tie change (continuous data has no ties).
- Suite: 61 passed.
- Signed off by Mayo 2026-11-10 (TODO 2.4, 2.21). Packet: docs/review_step2.md.

## Step 4 (done; signed off by Mayo 2026-11-12)
Question: how PSR, DSR and PBO behave, with zero true edge, when one IID Normal assumption breaks: (a) synthetic
scenarios, (b) real dependence from the French 49 industries. Each design and prediction was written here before its
run (the order is recorded by the author, not by git; from step 5 on, designs are committed before running).
Decision rule (completed after the 4(b) run): tests against a fixed value use the null SE, differences the paired SE;
|z| < 2 no detected effect, 2 to 3 suggestive, >= 3 or Bonferroni p < 0.05 within one table detected. A rate
"contains 5%" when its exact 95% CI contains 0.05.
Paper readings: SF p.12 reads PSR(0) > 0.95 as 95% confidence ("nominal 5%" is our phrase). DSR p.10 reads DSR > 0.95
on the selected strategy as 95% confidence; no paper states a false-positive rate. PBO p.14: PBO <= 0.05 is "a
customary approach". S = 16: PBO p.11 (example), p.22 (rationale). PBO counts logit <= 0 (Sec 3.1, p.13; our reading,
Def 2.2 on p.10 uses rank < N/2): reference 0.5 for N = 100, 25/49 = 0.5102 for N = 49.
Suite: 153 passed (WSL, Python 3.13.18, numpy 2.5.4, scipy 1.18.1). Setup: python3.13 -m venv .venv, then
.venv/bin/pip install -r requirements.txt (installs pbo itself with -e .).

### 4(a) synthetic (experiments/calibration.py, results/calibration.txt), RECOMPUTED
N = 100, T = 1248 (DSR p.9's 1250 trimmed so S = 16 divides it), 2000 datasets (PSR, DSR), 200 (PBO), seed 20261110.
Levels (our choice): AR(1) phi 0.1, 0.3; GARCH(1,1) (0.05, 0.90), (0.10, 0.85), clustering and fat tails together, with
a paired time-shuffle PBO control; Student-t nu 8, 5; one-factor correlation rho 0.3, 0.7. PSR on a fixed, unselected
strategy. DSR on the best of 100, V = variance of the 100 Sharpes (ddof 1, our choice).
Predictions (Mayo, 2026-11-10, before any run): PSR moved most by autocorrelation; DSR by correlated strategies; mean
PBO by none, stays near 0.5.

| Scenario | PSR(0) > 0.95 | same, Newey-West (G1) | DSR, N = 100 | DSR, implied N | PBO mean |
|---|---|---|---|---|---|
| IID Normal | 4.95% [4.0, 6.0] | 5.10% | 0.00% | | 0.520 |
| AR(1) phi 0.1 | 6.35% [5.3, 7.5] | 5.30% | 0.10% | | 0.495 |
| AR(1) phi 0.3 | 11.85% [10.5, 13.4] | 7.10% [6.0, 8.3] | 0.70% | | 0.482 |
| GARCH (0.05, 0.90) | 4.70% | 4.60% | 0.15% | | 0.481 |
| GARCH (0.10, 0.85) | 5.45% | 5.80% | 0.10% | | 0.501 |
| Student-t nu 8 | 4.35% | 4.65% | 0.15% | | 0.511 |
| Student-t nu 5 | 4.85% | 5.20% | 0.05% | | 0.504 |
| Correlated rho 0.3 | 5.35% | 5.55% | 0.70% | 1.05% (N 70.3) | 0.512 |
| Correlated rho 0.7 | 4.95% | 5.20% | 2.60% | 5.05% (N 30.7) | 0.504 |
PBO SE 0.010 to 0.011; PBO <= 0.05 accepted a zero-edge set at most 1 time in 200. GARCH paired PBO (original minus
shuffled): -0.002 +/- 0.004, +0.009 +/- 0.004.
Verdicts: all three predictions right. Both AR(1) cells exclude 5%; every other PSR CI contains 5%. The DSR rate rises
with correlation; 5.05% at rho 0.7 is where that curve crosses 5%, not a calibrated level. Implied N (DSR Eq. 9) was
chosen as lead row after these results were seen; both rows are reported. The estimate 30.715 matches the true 30.7
although T < M(M-1)/2 (1248 < 4950), the regime DSR p.15 calls "pointless". Why correlation moves DSR (our reasoning):
correlated Sharpes cluster, so V and SR0 = sqrt(V) E[max] shrink while the best strategy keeps the common noise.
G1 (our correction, design recorded before the run): PSR with a Newey-West long-run variance (7 lags, rule of thumb,
our choice) contains 5% in 8 of 9 cells; at AR(1) phi 0.3 it cuts 11.85% to 7.10%, not to 5%.

### Paper finding: PSR's variance under serial correlation
- SF p.4: "Opdyke (2007) has shown that Mertens' equation has a limiting distribution that is valid under the more
  general assumption of stationary and ergodic returns [...] Thus, our results are valid under such conditions". p.8:
  Christie (2005) allows "serial correlation"; Opdyke "proved that the expressions [...] are in fact identical". p.11:
  Eqs. 11 and 13 rest on "an asymptotic distribution". Footnote 2 (p.4) and p.15 point the other way.
- Our derivation (not from any paper): at SR = 0, sqrt(T) SR -> N(0, 1 + 2 sum rho_k) by the CLT for the mean and
  Slutsky; Eq. 8 assumes the factor is 1. For a stationary Gaussian AR(1) the factor is (1 + phi)/(1 - phi) for every
  large T, so the error does not vanish asymptotically.

| AR(1) | Analytic rate, finite T / large T (RECOMPUTED, psr_dsr.ar1_psr_false_positive) | Simulated (4(a)) |
|---|---|---|
| phi 0.1 | 6.83% / 6.84% | 6.35% [5.3, 7.5] |
| phi 0.3 | 11.36% / 11.37% | 11.85% [10.5, 13.4] |
- Conclusion: SF's p.4 sentence, read as applying the unchanged Eq. 8 / Eq. 11 variance to serially correlated
  stationary returns, is contradicted by a stationary Gaussian AR(1). SF's IID non-Normal results, examples and
  formulas stand; the code reproduces them. The GARCH cells (serially uncorrelated) are consistent with SF at SR = 0.
  Only SR* = 0 was tested.
- Where the claim comes from (papers/christie-2005.pdf, papers/opdyke-2007.pdf, text extraction): Christie's GMM
  estimates use an autocorrelation-consistent S (footnote 13, p.10) and are valid under serial correlation. His eq. 8-9
  (p.10) write S0 = E[F F^T], the long-run covariance only when F is serially uncorrelated, while p.7 says the setup
  "still permits serial correlation". His Appendix B closed form (pp.33-35) is lag-0 and is presented as dropping
  normality (p.22, p.33); its plug-in value 1.1202463 (p.23) is lag-0. Opdyke (2007) first states explicitly that this
  closed form, and so Mertens', holds under serial correlation (abstract p.1; p.4; footnote 9, p.3, contrasts it with
  Lo's Newey-West estimator). SF p.4 and p.8 repeat this, although SF p.5 follows Lo (2002).
- Novelty: no prior statement of this failure found in the papers read. Variance inflation under serial correlation is
  known (Lo 2002, not available to us, not cited as a source).

### 4(b) French 49 industries (experiments/french_bootstrap.py, results/french_bootstrap.txt), RECOMPUTED
Design (approved before the run): Kenneth French 49 Industry Portfolios, daily, value-weighted; frozen snapshot
SHA-256 b9d36d571e968d71f7b03207e7fed6398554f953719b8c1bf3ee3ad8d00e7520 (202609 CRSP, downloaded 2026-11-12); window
1971-07-01 to 2026-09-30, 13,929 days x 49 (Softw has missing values until 1971-03-11). Each industry demeaned once.
Circular block bootstrap of whole days, L = 1, 5, 20 (primary), 60; it keeps same-day relationships and fat tails,
partly keeps short-lag dependence (two days h apart stay together with probability 1 - h/L, averaged over positions),
destroys longer dependence. 2000 datasets (PSR, DSR), 200 (PBO), T = 1248, S = 16, seed 20261112. PSR on a uniformly
drawn industry; DSR with implied N (lead) and N = 49; DSR p.15's inequality is not triggered (1248 > 1176, by 72);
PBO with a paired time-shuffle control. This measures calibration under real dependence; it is not a
strategy-overfitting study (step 5), and the fixed-length bootstrap is not strictly stationary.
Predictions (Mayo, before the run): 1 PSR above 5%, below 11.85%. 2 implied N well below 49, higher acceptance, N = 49
conservative. 3 mean PBO 0.45 to 0.55, spread changes more than the mean. 4 time order moves PSR more than PBO. 5 overall
confirms 4(a). 6 PSR: L = 1 closest to 5%, modest rise at 5 and 20, plateau at 60; amended before the run to two
hypotheses: paper (5% at every L) vs project. 7 implied-N DSR may rise at L = 60, N = 49 lower and flatter; amended
before the run: implied N stable, no DSR direction, N = 49 more conservative. 8 mean PBO near 25/49, paired effect small.

| L | PSR(0) > 0.95 | DSR implied N (mean N, SD) | DSR N = 49 | PBO mean (SD) | PBO orig - shuffled |
|---|---|---|---|---|---|
| 1 | 5.35% [4.4, 6.4] | 3.05% (23.0, 1.14) | 1.45% | 0.511 (0.191) | |
| 5 | 5.15% [4.2, 6.2] | 3.55% (23.0, 1.50) | 1.90% | 0.520 (0.183) | +0.002 +/- 0.004 |
| 20 | 6.25% [5.2, 7.4] | 3.05% (23.2, 2.24) | 1.30% | 0.505 (0.191) | -0.008 +/- 0.005 |
| 60 | 6.25% [5.2, 7.4] | 3.10% (23.3, 2.93) | 1.25% | 0.517 (0.176) | +0.017 +/- 0.005 |
z and p below are one-off calculations from the counts (UNVERIFIED as code).
- 1: consistent. L = 20 and 60: z = 2.56 each (suggestive); pooled L >= 5: 353/6000 = 5.88%, z = 3.14, p = 0.0012
  (pooling chosen after the run). 6: the pooled excess is inconsistent with SF's claim read literally; the formal
  counterexample stays 4(a). The project's L-shape is untestable here: expected differences of 0.1 to 0.5 points
  against a resolution of about 2 points.
- 2: right. Implied-N rate 1.9 to 2.5 times the N = 49 rate; the paired difference (+1.6 to +1.8 points) is
  non-negative by construction (same V, same best strategy). Both rows are below the 5% reading of DSR p.10.
- 7 amended: right (implied N 23.0 to 23.3, SD widens 1.1 to 2.9 with L, no DSR trend). 7 original: not supported.
- 3: mean right; spread was not defined before the run and shows no detected change (SD 0.176 to 0.196).
- 4: ill-posed (a rate against a mean probability). 8: means within about 1 SE of 0.5102; the L = 60 paired value
  (3.4 SE) did not replicate (follow-up C). 5: partly right.

### 4(b) follow-ups (experiments/french_followups.py, results/french_followups.txt, seed 20261113), RECOMPUTED
Designs recorded before the runs: A predicted PSR rate from each industry's autocorrelations, F_L = 1 + 2 sum (1 - h/L)
rho_h (our derivation, approximate when L does not divide T); B weekly returns (5-day sums), 4-week blocks; C PBO
paired difference with fixed and random block positions, 400 datasets; G1 Newey-West PSR; G2 PSR on AR(5) residuals
(our choice of order); G6 the L = 20 PSR test on 1971-1998 and 1999-2026 separately.

| Check | Result | Verdict (preset rule) |
|---|---|---|
| A: daily lag-1 autocorrelation | 1971-98 mean +0.157 (49 of 49 significant); 1999-2026 -0.026; full +0.036 | description |
| A: predicted vs observed 4(b) PSR | 4.99 / 5.42 / 5.50 / 5.38% vs 5.35 / 5.15 / 6.25 / 6.25%, z +0.73 / -0.53 / +1.48 / +1.72 | agree; accounts for about half the pooled excess |
| B: weekly PSR | 4.35% [3.50, 5.34]; 17 of 49 industries still autocorrelated | contains 5%; tests weekly sampling, not SF p.15's condition |
| C: PBO, L = 20 | fixed -0.004 +/- 0.003; random -0.003 +/- 0.004 | no effect |
| C: PBO, L = 60 | fixed +0.001 +/- 0.004; random -0.001 +/- 0.004 | 4(b)'s +0.017 did not replicate |
| G1: Newey-West PSR | L = 20: 5.60% (plain 5.90%); L = 60: 5.70% (plain 6.00%) | contains 5% |
| G2: AR(5) residuals | L = 20: 5.30%; L = 60: 5.35% (residual lag-1 autocorrelation 0.000) | contains 5%: the excess is linear autocorrelation |
| G6: 1971-98 | simulated 10.45% [9.1, 11.9] vs predicted 8.38%, z = +3.34 | prediction too low |
| G6: 1999-2026 | simulated 3.30% [2.6, 4.2] vs predicted 3.94%, z = -1.47 | agree |
Reading (ours): PSR's real-data error depends on the period, about 10% in 1971-98 and about 3% after 1999, and it is
removed by deleting linear autocorrelation (G2) or by a Newey-West variance (G1).

### PBO power under dependence (G4, experiments/null_checks.py, results/null_checks.txt, seed 20261114), RECOMPUTED
Step 2's Null 2 (one strategy with true annual Sharpe SR, T = 992, N = 100, S = 16, 20 datasets per edge), noise
changed. Mean PBO; z against the IID row:
| SR | IID | AR(1) phi 0.3 | GARCH (0.10, 0.85) |
|---|---|---|---|
| 0 | 0.516 | 0.478 (z -0.73) | 0.566 (z +1.05) |
| 1 | 0.433 | 0.404 (z -0.60) | 0.373 (z -1.13) |
| 2 | 0.189 | 0.391 (z +3.55) | 0.189 (z +0.00) |
| 3 | 0.026 | 0.098 (z +3.62) | 0.019 (z -0.77) |
Verdict: power kept under GARCH; under AR(1) phi 0.3 PBO detects a real edge less well at SR 2 and 3.

### Limits (for step 6)
Only SR* = 0 was tested (PSR at SR* > 0 and MinTRL under GARCH untested). 4(b) intervals are Monte Carlo error given
one 1971-2026 history. The Newey-West lag is a rule of thumb and under-corrects at phi 0.3. DSR results are relative
to the p.10 reading. No plot yet (step 6).

### Engineering in step 4 (no result changed; every rerun compared line by line)
CSCV ranks only the IS-best strategy out of sample (the same average rank, ties included; tested against the plain
algorithm); CSCV refuses N < 2 and non-finite Sharpes; implied_n refuses a non-unit diagonal; AR(1) is a plain loop
(bit-identical to lfilter); experiments use several CPU cores; requirements are numpy, scipy, pytest and the package.
Experiments hold only settings, the loop and output: data download and checks live in pbo.french.load_returns,
file writing in pbo.reporting.save_results (all six results files reran identical).

## Step 5 (in progress): a real strategy search
### Design, approved 2026-11-12 before any run
- 5.1 Data: Kenneth French, Fama-French research factors, daily (Mkt-RF and RF), percent to decimal. Frozen snapshot
  SHA-256 96c23b88e651cbfff3740a53f8225e59ee39893371e96385a1d8125ec2cd9c89 (202609 CRSP, downloaded 2026-11-12),
  same window as step 4: 1971-07-01 to 2026-09-30.
- 5.2 Strategy family: moving-average crossover on the market's total-return index (Mkt-RF + RF compounded): long
  the market when the fast MA is above the slow MA, otherwise flat (earns RF, so excess return 0). Grid (our choice):
  fast 5, 10, ..., 50 days, slow 25, 50, ..., 250 days, fast < slow: 93 settings. The signal at the close of day t
  sets the position for day t + 1. The first 250 days are dropped so every setting is defined; T is then trimmed to a
  multiple of S = 16.
- 5.3 Costs (our choice): 5 bps per unit change in position, with 0 and 10 bps as sensitivity.
- 5.5-5.6: one strategy-return matrix (T x 93) per cost level; a test checks that changing future prices leaves past
  strategy returns unchanged.
- 5.8-5.9 Measures: PBO (CSCV, S = 16, PBO p.14 rule PBO <= 0.05); the best setting by in-sample Sharpe over the
  whole sample; its PSR(0); DSR with N = 93 and with implied N (DSR Eq. 9); buy-and-hold market Sharpe as reference.
  Script: experiments/ma_crossover.py, output results/ma_crossover.txt.

### Predictions before the run (TODO 5.7), recorded 2026-11-12
Proposed by a reviewer and forwarded by Mayo as the step 5 predictions; UNVERIFIED, not results or paper claims.
| # | Question | Prediction | Reason given |
|---|---|---|---|
| 1 | PBO at 5 bps | between 0.05 and 0.5 | some settings may rank consistently, but a very low PBO seems optimistic across regimes |
| 2 | Best setting's DSR, N = 93 | above 0.95 | long sample and similar settings could give a high DSR |
| 3 | PBO from 0 to 10 bps | about the same | costs lower returns, but PBO is about relative ranks |
| 4 | Best setting's Sharpe vs holding the market, 5 bps | higher, in sample | picking the best of 93 favours it; says nothing about the future |

## Step 3 (done)
- src/pbo/psr_dsr.py: psr (SF Eq. 11), min_trl (SF Eq. 13), sr0 and dsr (DSR Eq. 2). Notes: docs/psr_dsr_notes.md.
- tests/test_psr_dsr.py: all paper examples (SF pp.10-11, DSR pp.9-10) plus closed forms and bad-input guards. Suite: 90 passed.
- Kurtosis is raw (TODO 3.2 closed).
- Results, experiments/dsr_false_positives.py, RECOMPUTED:

| Check | Result | Mayo said | Verdict |
|---|---|---|---|
| PSR at SR = benchmark | 0.5 (closed form, tested) | 0.5 | right |
| Negative skew | lowers PSR (tested) | lowers | right |
| Paper hedge fund | 0.913 (PAPER, SF p.10; ours 0.9134, RECOMPUTED by tests/test_psr_dsr.py) | about 0.91 | right (value was shown in the question) |
| Best of 100 zero-edge, PSR(0) > 0.95 | 1983/2000 = 0.9915 (CI 0.986 to 0.995) | about 100% | right |
| Best of 100 zero-edge, DSR > 0.95 | 1/2000 = 0.0005 (CI 0 to 0.0028); approx with V known 0.0015 | about 5% | wrong: DSR is much stricter |
- 2026-11-10 review (paper check + hardcoding/logic audit): formulas and all step-3 constants match SF pp.8-11 and
  DSR pp.8-10. Fixed: min_trl silently wrong for alpha > 0.5, now raises; psr n < 2 and sr0 negative variance raise;
  experiment reports exact binomial intervals and states the V-known assumption.
- 2026-11-10 external review of step 3: math correct, all paper examples reproduced. Fixed its findings:
  NaN/inf inputs raise; unsupported "about 0.0008" claim removed;
  "upper bound" wording removed; ddof = 1 for V listed as our choice. Committed in 7355d1f.
- Step 1 and step 2 signed off by Mayo (project owner) on 2026-11-10: TODO 1.39, 2.4, 2.21.
- 2026-11-10 page check of all 51 constants: 44 match, 0 mismatch, 7 derived (docs/paper_check.md); 52 and 45 after
  PBO_ACCEPT_LEVEL was added (2026-11-12).
  Second visual check of the 12 image-only values and SR0: all match.
- Step 3 signed off by Mayo (project owner), 2026-11-10.

## Predictions (step 3), recorded 2026-11-10 before any run
| Check | Mayo said |
|---|---|
| PSR when observed Sharpe = benchmark | 0.5 |
| Negative skew, positive Sharpe | lowers PSR |
| Paper hedge fund (SF p.10), with skew and kurtosis | about 0.91 (note: the paper value 0.913 was shown in the question) |
| Best of 100 zero-edge strategies, 5y daily: share flagged skilled | PSR(0) > 0.95 about 100%, DSR > 0.95 about 5% |

## Predictions (step 2), recorded 2026-11-10 before any run
| Check | Mayo said |
|---|---|
| Null 1: 100 zero-edge strategies, T about 1000, S = 16 | PBO about 0.5 |
| Null 2: one strategy with true annual SR 0, 0.5, 1, 2, 3 | PBO falls, then flattens |
| Null 2: SR where PBO first drops below 0.1 | about 2 |

## Results (step 2), experiments/null_checks.py, results/null_checks.txt
T = 992 (PBO p.25 gives 1,000, trimmed for S = 16), N = 100, q = 250, seed 20261110. All RECOMPUTED.
| Check | Result | Closed form / expectation | Mayo said | Verdict |
|---|---|---|---|---|
| Null 1, S = 16 | 0.515 +/- 0.025 | 0.5 exactly (N even) | about 0.5 | right |
| Null 1, S = 8 | 0.502 +/- 0.025 | 0.5 | | S does not move the mean |
| Null 2, SR 0 / 0.5 / 1 / 2 / 3 | 0.516 / 0.511 / 0.433 / 0.189 / 0.026 | falls to 0 | falls, then flattens | half right: it stays flat first, then falls |
| Null 2, first SR with PBO < 0.1 | between 2 and 3 (only these grid points tried) | | about 2 | close, a bit low |

Why flat at low SR: with 496 IS days the best of 99 noise strategies has an annual Sharpe of about 1.8 (closed form E[max_99] x sqrt(250/496) = 1.79;
UNVERIFIED, no repo code)
(logic review, approximate). A real SR below that rarely wins IS, so PBO stays at the noise level 0.5.
The spread is wide: one zero-edge dataset gave PBO 0.141, another 0.836. One CSCV run on one dataset is noisy.
Consistent in direction with the paper's own examples: random walk PBO 55% (p.25), real seasonal effect 13% (p.27).

- cscv.py speed-up by Mayo (block sums, each half computed once): 19x faster (0.20 s vs 3.73 s at S = 16; UNVERIFIED one-off timing, no script).
  Same logits as the plain loop: tests/test_fast_cscv_matches_plain_algorithm. Null checks rerun: identical output.

## Predictions vs results (step 1)
| Prediction | Mayo said | Result | Label |
|---|---|---|---|
| sharpe(), mean 0.0004, sd 0.01, 252 (historical; tests now use q=250) | about 0.04 (wrong) | 0.04*sqrt(252) = 0.635 | closed form, PSEUDO Eq. 2.2 |
| Doubling returns | Sharpe unchanged (right) | unchanged | closed form, tested |
| All returns equal | infinity (weak) | chose ValueError | design decision, tested |
| Growth of E[max] with N | like sqrt(ln N) (right) | grows like sqrt(2 ln N) | closed form bound, tested |
| MinBTL n=45, target 1 | about 5 years (right) | under 5 years; paper says 45 fit in 5 | PAPER (PSEUDO p.11), tested |
| SE of 5y annual Sharpe, zero edge | about 0.45 (right) | sim 0.443, PSEUDO Eq. 2.3 gives 0.447 | RECOMPUTED (best_of_n.py) |
| Best of 10/45/100, 5y | 0.7/1.0/1.1 (right) | sim 0.688/0.984/1.119 | RECOMPUTED (best_of_n.py) |

Simulation sits about 0.012 to 0.016 below the formula for every N. That matches the known overstatement
of the Gumbel approximation: UNVERIFIED 0.0358 at n=10 (one-off run, no repo code) (Eq. 2.4 minus the integral used in tests/test_minbtl.py;
one-off run 2026-11-10, the test itself only asserts the sign),
divided by sqrt(5) is 0.016.

## Verified vs UNVERIFIED
- PAPER (docs/paper_values.md): E[max] formula = PSEUDO Prop 2.1, Eq. 2.4, p.9, and DSR Eq. 1, p.7.
  MinBTL = PSEUDO Theorem 3.1, Eq. 3.2, p.11. Upper bounds sqrt(2 ln N) (p.9) and 2 ln N / target^2 (p.11).
- PAPER: 1.57 for N=10 (PSEUDO p.9). 45 configurations in 5 years (PSEUDO p.11). SR0 = 0.1132 (DSR p.10, inputs on p.9).
  All three are now tests, read from src/pbo/paper_values.py.
- PAPER: Sharpe = mu/sigma * sqrt(q), PSEUDO Eq. 2.2, p.7. SE of annual Sharpe with SR=0 is 1/sqrt(y), PSEUDO Eq. 2.3, p.8.
- PAPER: q = 250 per year, from DSR p.10. PSEUDO does not fix q. Was 252 before 2026-11-10.
- RECOMPUTED (experiments/best_of_n.py, q=250): SE 0.443 and best-of-N 0.688/0.984/1.119, MC SE 0.004 to 0.006.
- Exact E[max] is now computed in the test by numerical integration, not typed in.
- DROPPED: "about 2 years for N=7", oracle 2.4794 and the "2.46" note. Not printed in the paper.
- Page numbers are the PSEUDO author copy (April 1, 2014), not the printed Notices pages.
- Our choice, not a paper claim: ddof=0 in sharpe(). PSEUDO p.8 says "sample standard deviation" only.
  Precedent: SF appendix A.4 code (get_Moments, pp.27-28, text extraction) divides moments by the number of
  observations.
- Our choice: TRIALS=2000 and the seed in best_of_n.py.
- Assumption in all of step 1: iid returns. Annualizing with sqrt(periods) is wrong under autocorrelation (step 4).

## For the reviewer
1. Check docs/paper_values.md against the PDFs in papers/. Each row has a page number.
2. The PSEUDO pages are from the author copy. Confirm they match the Notices version if you hold that one.
