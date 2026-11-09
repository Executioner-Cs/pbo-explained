# TODO

Tick a box only when its check passes. One step at a time.
Formulas named here are UNVERIFIED until checked on the paper page.

## Step 0. Setup
- [x] 0.1 Write project rules
- [x] 0.2 Create PROGRESS.md (Done, Verified vs UNVERIFIED, Questions)
- [x] 0.3 Add .gitignore (.venv, caches)
- [x] 0.4 Add pyproject.toml so pytest finds src/
- [x] 0.5 Install numpy, scipy, pytest. Freeze requirements.txt
- [x] 0.6 Write docs/oracle_step1.md with tolerances
- [x] 0.7 Run experiments/check_oracle.py. All rows pass
- [ ] 0.8 Put the paper PDFs in a papers/ folder
- [ ] 0.9 Reviewer approves setup

## Step 1. Sharpe, best-of-N, MinBTL
### sharpe(returns, periods_per_year)
- [ ] 1.1 Predict: value for mean 0.0004, sd 0.01, 252 days
- [ ] 1.2 Predict: effect of doubling all returns
- [ ] 1.3 Predict: behaviour when all returns are equal
- [ ] 1.4 Create src/pbo/__init__.py and tests/
- [ ] 1.5 Write tests/test_sharpe.py: closed form case (mean/sd * sqrt(252))
- [ ] 1.6 Add test: scale invariance (doubling returns, same Sharpe)
- [ ] 1.7 Add test: zero variance input (decide: raise or return nan)
- [ ] 1.8 Add test: ddof=0 is used
- [ ] 1.9 Run pytest. Watch it fail
- [ ] 1.10 Write sharpe() in src/pbo/sharpe.py
- [ ] 1.11 Line by line review
- [ ] 1.12 pytest passes

### expected_max_normal(n)
- [ ] 1.13 Predict: does E[max] grow fast or slow with n?
- [ ] 1.14 Write test: expected_max_normal(10) = 1.5746, abs 5e-5
- [ ] 1.15 Write gap test: formula minus exact 1.5388 is about 0.036, abs 1e-3
- [ ] 1.16 Add test: n=1 or n<1 input (decide behaviour)
- [ ] 1.17 Add test: increases with n
- [ ] 1.18 Run pytest. Watch it fail
- [ ] 1.19 Write expected_max_normal() in src/pbo/minbtl.py
- [ ] 1.20 Line by line review
- [ ] 1.21 pytest passes

### min_btl_years(n, target_sharpe)
- [ ] 1.22 Predict: years needed for n=45, target 1
- [ ] 1.23 Write tests: n=45 gives 4.998, n=7 gives 1.92, n=10 gives 2.4794
- [ ] 1.24 Write test: smallest n with result > 5 is 46
- [ ] 1.25 Write test: result is below the loose bound 2*ln(n)/target^2
- [ ] 1.26 Run pytest. Watch it fail
- [ ] 1.27 Write min_btl_years()
- [ ] 1.28 Line by line review
- [ ] 1.29 pytest passes

### Simulation
- [ ] 1.30 Predict: standard error of 5 year annual Sharpe when true Sharpe is 0
- [ ] 1.31 Predict: expected best Sharpe among 10, 45, 100 zero-edge strategies (5 years)
- [ ] 1.32 Write experiments/best_of_n.py (fixed seed)
- [ ] 1.33 Compare simulation to expected_max_normal(n)/sqrt(5)
- [ ] 1.34 Compare simulation to your predictions. Note the misses
- [ ] 1.35 Save plot or table to results/

### Close step 1
- [ ] 1.36 Update PROGRESS.md
- [ ] 1.37 List what is still UNVERIFIED
- [ ] 1.38 List three paper claims for the reviewer to check on the printed pages
- [ ] 1.39 Reviewer signs off step 1

## Step 2. CSCV and the two null checks
- [ ] 2.1 Read the CSCV procedure on the paper page. Write it in docs/cscv_notes.md
- [ ] 2.2 Predict: PBO when every strategy has zero edge
- [ ] 2.3 Predict: PBO when one strategy has real edge
- [ ] 2.4 Agree the exact two null checks with the reviewer
- [ ] 2.5 Test: split T rows into S equal blocks
- [ ] 2.6 Test: number of combinations is C(S, S/2)
- [ ] 2.7 Test: in-sample and out-of-sample blocks never overlap
- [ ] 2.8 Test: rank and logit on a tiny hand-worked example
- [ ] 2.9 Test: PBO on a hand-worked 4-strategy example
- [ ] 2.10 Run pytest. Watch it fail
- [ ] 2.11 Write block split in src/pbo/cscv.py
- [ ] 2.12 Write combination loop
- [ ] 2.13 Write in-sample pick and out-of-sample rank
- [ ] 2.14 Write logit and PBO
- [ ] 2.15 Line by line review
- [ ] 2.16 pytest passes
- [ ] 2.17 Null check 1: all zero edge. Run experiment, compare to prediction
- [ ] 2.18 Null check 2: one real edge strategy. Run experiment, compare to prediction
- [ ] 2.19 Check S sensitivity (S = 8, 16)
- [ ] 2.20 Save results/
- [ ] 2.21 Update PROGRESS.md. Reviewer signs off step 2

## Step 3. PSR, MinTRL, DSR
- [ ] 3.1 Read PSR, MinTRL, DSR formulas on the paper pages. Write docs/psr_dsr_notes.md
- [ ] 3.2 Decide kurtosis convention (raw or excess). Write it down
- [ ] 3.3 Predict: PSR for Sharpe 0 against benchmark 0
- [ ] 3.4 Predict: how negative skew moves PSR
- [ ] 3.5 Test: PSR closed form case, normal returns
- [ ] 3.6 Test: PSR = 0.5 when observed Sharpe equals benchmark
- [ ] 3.7 Test: MinTRL closed form case
- [ ] 3.8 Test: DSR benchmark built from expected_max_normal and trial Sharpe variance
- [ ] 3.9 Run pytest. Watch it fail
- [ ] 3.10 Write psr() in src/pbo/psr_dsr.py
- [ ] 3.11 Write min_trl()
- [ ] 3.12 Write dsr()
- [ ] 3.13 Line by line review
- [ ] 3.14 pytest passes
- [ ] 3.15 Experiment: DSR false positive rate on zero-edge strategies
- [ ] 3.16 Update PROGRESS.md. Reviewer signs off step 3

## Step 4. Calibration study
- [ ] 4.1 Write data generators: iid normal baseline
- [ ] 4.2 Generator: AR(1) autocorrelation
- [ ] 4.3 Generator: GARCH(1,1) volatility clustering
- [ ] 4.4 Generator: Student-t fat tails
- [ ] 4.5 Generator: correlated strategy variants
- [ ] 4.6 Test each generator against its known moments
- [ ] 4.7 Predict: which condition breaks PBO most. Which breaks DSR most
- [ ] 4.8 Fix grid: number of strategies, sample length, parameter levels
- [ ] 4.9 Run PBO across the grid
- [ ] 4.10 Run DSR across the grid
- [ ] 4.11 Measure false positive rate vs nominal level
- [ ] 4.12 Report Monte Carlo standard errors for every number
- [ ] 4.13 Save tables and plots to results/
- [ ] 4.14 Compare to predictions. Update PROGRESS.md. Reviewer signs off step 4

## Step 5. Real-data case study with costs
- [ ] 5.1 Pick data source and asset. Record source and date range
- [ ] 5.2 Pick strategy family (one family, many parameter settings)
- [ ] 5.3 Pick cost model (bps per trade). Write it down
- [ ] 5.4 Clean data. Check gaps and splits
- [ ] 5.5 Build strategy return matrix, no lookahead
- [ ] 5.6 Test: no lookahead (shifted signal)
- [ ] 5.7 Predict: PBO and DSR before running
- [ ] 5.8 Run CSCV, PSR, DSR without costs
- [ ] 5.9 Run with costs
- [ ] 5.10 Compare. Save to results/
- [ ] 5.11 Update PROGRESS.md. Reviewer signs off step 5

## Step 6. Short write-up
- [ ] 6.1 Outline: question, method, results, limits
- [ ] 6.2 Every number labelled PAPER, RECOMPUTED or UNVERIFIED
- [ ] 6.3 Figures from results/ only
- [ ] 6.4 Limits section: what the calibration showed breaks
- [ ] 6.5 Reviewer reads it
- [ ] 6.6 Final pass on UNVERIFIED list
- [ ] 6.7 Mayo decides on git commit and push
