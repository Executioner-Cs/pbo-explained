# TODO

Tick a box only when its check passes. One step at a time.
Formulas named here are UNVERIFIED until checked on the paper page.

## Step 0. Setup
- [x] 0.1 Write project rules
- [x] 0.2 Create PROGRESS.md (Done, Verified vs UNVERIFIED, Questions)
- [x] 0.3 Add .gitignore (.venv, caches)
- [x] 0.4 Add pyproject.toml so pytest finds src/
- [x] 0.5 Install numpy, scipy, pytest. Freeze requirements.txt
- [x] 0.6 Write oracle table (deleted 2026-11-10, replaced by src/pbo/paper_values.py)
- [x] 0.7 Oracle check script (deleted 2026-11-10, values not in paper)
- [x] 0.8 Put the paper PDFs in a papers/ folder (not committed)
- [ ] 0.9 Reviewer approves setup

## Step 1. Sharpe, best-of-N, MinBTL
### sharpe(returns, periods_per_year)
- [x] 1.1 Predict: value for mean 0.0004, sd 0.01, 252 days (historical; q is now 250, DSR p.10)
- [x] 1.2 Predict: effect of doubling all returns
- [x] 1.3 Predict: behaviour when all returns are equal
- [x] 1.4 Create src/pbo/__init__.py and tests/
- [x] 1.5 Write tests/test_sharpe.py: closed form case (mean/sd * sqrt(q), q = 250 since 2026-11-10)
- [x] 1.6 Add test: scale invariance (doubling returns, same Sharpe)
- [x] 1.7 Add test: zero variance input (decide: raise or return nan)
- [x] 1.8 Add test: ddof=0 is used
- [x] 1.9 Run pytest. Watch it fail
- [x] 1.10 Write sharpe() in src/pbo/sharpe.py
- [x] 1.11 Line by line review
- [x] 1.12 pytest passes

### expected_max_normal(n)
- [x] 1.13 Predict: does E[max] grow fast or slow with n?
- [x] 1.14 Write test: expected_max_normal(10) = 1.57 (PSEUDO p.9), abs 0.005
- [x] 1.15 Write gap test: formula above exact E[max] (exact by integration)
- [x] 1.16 Add test: n=1 or n<1 input (decide behaviour)
- [x] 1.17 Add test: increases with n
- [x] 1.18 Run pytest. Watch it fail
- [x] 1.19 Write expected_max_normal() in src/pbo/minbtl.py
- [x] 1.20 Line by line review
- [x] 1.21 pytest passes

### min_btl_years(n, target_sharpe)
- [x] 1.22 Predict: years needed for n=45, target 1
- [x] 1.23 Write test: 45 configurations fit in 5 years at target 1 (PSEUDO p.11)
- [x] 1.24 Write test: n=46 needs more than 5 years
- [x] 1.25 Write test: result is below the loose bound 2*ln(n)/target^2
- [x] 1.26 Run pytest. Watch it fail
- [x] 1.27 Write min_btl_years()
- [x] 1.28 Line by line review
- [x] 1.29 pytest passes

### Simulation
- [x] 1.30 Predict: standard error of 5 year annual Sharpe when true Sharpe is 0
- [x] 1.31 Predict: expected best Sharpe among 10, 45, 100 zero-edge strategies (5 years)
- [x] 1.32 Write experiments/best_of_n.py (fixed seed)
- [x] 1.33 Compare simulation to expected_max_normal(n)/sqrt(5)
- [x] 1.34 Compare simulation to your predictions. Note the misses
- [x] 1.35 Save plot or table to results/

### Close step 1
- [x] 1.36 Update PROGRESS.md
- [x] 1.37 List what is still UNVERIFIED
- [x] 1.38 List three paper claims for the reviewer to check on the printed pages
- [x] 1.39 Step 1 signed off by Mayo (project owner), 2026-11-10

## Step 2. CSCV and the two null checks
- [x] 2.1 Read the CSCV procedure on the paper page. Write it in docs/cscv_notes.md
- [x] 2.2 Predict: PBO when every strategy has zero edge
- [x] 2.3 Predict: PBO when one strategy has real edge
- [x] 2.4 Two null checks approved by Mayo (project owner), 2026-11-10 (packet: docs/review_step2.md)
- [x] 2.5 Test: split T rows into S equal blocks
- [x] 2.6 Test: number of combinations is C(S, S/2)
- [x] 2.7 Test: in-sample and out-of-sample blocks never overlap
- [x] 2.8 Test: rank and logit on a tiny hand-worked example
- [x] 2.9 Test: PBO on a hand-worked 4-strategy example
- [x] 2.10 Run pytest. Watch it fail
- [x] 2.11 Write block split in src/pbo/cscv.py
- [x] 2.12 Write combination loop
- [x] 2.13 Write in-sample pick and out-of-sample rank
- [x] 2.14 Write logit and PBO
- [x] 2.15 Line by line review (two review passes, 2026-11-10)
- [x] 2.16 pytest passes
- [x] 2.17 Null check 1: all zero edge. Run experiment, compare to prediction
- [x] 2.18 Null check 2: one real edge strategy. Run experiment, compare to prediction
- [x] 2.19 Check S sensitivity (S = 8, 16)
- [x] 2.20 Save results/
- [x] 2.21 Update PROGRESS.md. Step 2 signed off by Mayo (project owner), 2026-11-10 (packet: docs/review_step2.md)

## Step 3. PSR, MinTRL, DSR
- [x] 3.1 Read PSR, MinTRL, DSR formulas on the paper pages. Write docs/psr_dsr_notes.md
- [x] 3.2 Kurtosis convention: raw. Confirmed on SF p.10, DSR p.10, and by computation
- [x] 3.3 Predict: PSR for Sharpe 0 against benchmark 0
- [x] 3.4 Predict: how negative skew moves PSR
- [x] 3.5 Test: PSR closed form case, normal returns
- [x] 3.6 Test: PSR = 0.5 when observed Sharpe equals benchmark
- [x] 3.7 Test: MinTRL closed form case
- [x] 3.8 Test: DSR benchmark built from expected_max_normal and trial Sharpe variance
- [x] 3.9 Run pytest. Watch it fail
- [x] 3.10 Write psr() in src/pbo/psr_dsr.py
- [x] 3.11 Write min_trl()
- [x] 3.12 Write dsr()
- [x] 3.13 Line by line review
- [x] 3.14 pytest passes
- [x] 3.15 Experiment: DSR false positive rate on zero-edge strategies
- [x] 3.16 Update PROGRESS.md. Step 3 signed off by Mayo (project owner), 2026-11-10

## Step 4. Calibration study
- [x] 4.1 Write data generators: iid normal baseline
- [x] 4.2 Generator: AR(1) autocorrelation
- [x] 4.3 Generator: GARCH(1,1) volatility clustering
- [x] 4.4 Generator: Student-t fat tails
- [x] 4.5 Generator: correlated strategy variants
- [x] 4.6 Test each generator against its known moments
- [x] 4.7 Predict: which condition breaks PBO most. Which breaks DSR most
- [x] 4.8 Fix grid: number of strategies, sample length, parameter levels
- [x] 4.9 Run PBO across the grid
- [x] 4.10 Run DSR across the grid
- [x] 4.11 Measure false positive rate vs nominal level
- [x] 4.12 Report Monte Carlo standard errors for every number
- [x] 4.13 Calibration table saved to results/; plot deferred to step 6
- [x] 4.14 Predictions compared and PROGRESS.md updated; part a signed off 2026-11-12 (part b, French bootstrap, open)

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
