# PROGRESS

## Done
- Setup: PROGRESS.md, .gitignore, pyproject.toml.
- Packages installed: numpy, scipy, pytest. matplotlib installed, not used yet. Exact pins in requirements.txt.
- 2026-11-10: deleted experiments/check_oracle.py and docs/oracle_step1.md. Their numbers were typed in, and some are not in the paper.
- 2026-11-10: all paper numbers now live in src/pbo/paper_values.py, each with page and equation. Tests and experiments import from there.
- sharpe() in src/pbo/sharpe.py: 4 tests pass (closed form, ddof=0, scale invariance, zero variance raises).
- expected_max_normal() and min_btl_years() in src/pbo/minbtl.py, tested against paper values. Suite at end of step 1: 31 passed.
- 2026-11-10: paper constants are verified by a page-by-page review of rendered PDF pages, recorded in docs/paper_check.md.
  The earlier text-search script (experiments/check_paper_values.py) was removed at Mayo's request: it could not read
  values inside equation images.
- experiments/best_of_n.py: 2000 trials, 5 years daily, seed 20261109. Output in results/best_of_n.txt.
- Step 1 code complete. Awaiting reviewer sign-off (task 1.39).

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

## Step 4 (part a signed off 2026-11-12; part b open)
Plan (approved 2026-11-10): (a) controlled simulations, one broken assumption at a time, true edge zero;
(b) robustness: Kenneth French industry portfolios, circular or stationary block bootstrap, with a stated list of
what the resampling keeps and destroys. Demeaning removes the average return, not every exploitable pattern.
Conclusions of (a) and (b) are reported separately. Reference implementations (pypbo, R pbo) are used to
cross-check outputs, not as inputs.

Grid for (a), approved: N = 100, T = 1248 (DSR p.9's 1250 trimmed so S = 16 divides it), S = 16 (PBO p.11).
AR(1) phi 0.1, 0.3. GARCH(1,1) (alpha, beta) = (0.05, 0.90), (0.10, 0.85). Student-t nu 8, 5. Cross-strategy
correlation rho 0.3, 0.7. 2000 datasets per cell for PSR/DSR, 200 for PBO. Levels are our choice.
Review changes (2026-11-10): GARCH is labelled a combined departure (clustering plus fat tails). Each GARCH
cell adds a paired control: PBO of the same matrix shuffled in time, reported as a paired difference with
its MC SE. PSR and DSR are order-invariant, so they cannot differ under the shuffle (algebra, tested).
PBO 0.5 is the IID-null benchmark, exact only under temporal independence.
The first 9-cell run is a pilot. The rerun with paired controls is the recorded step 4 result.
Paper check of step 4 citations (2026-11-10): implied N matches DSR Eq. 8-9 (p.14); PBO <= 0.05 matches PBO p.14
("a customary approach"). Caveats now stated: DSR p.15 calls the average correlation unreliable when
T < M(M-1)/2 (here 1248 < 4950), so implied-N rows are indicative only. SF does "not explicitly address
serially-conditioned processes" (p.4); its serial-correlation wording is Christie's, hedged with "appears" (p.8).
S = 16 rationale is PBO p.22 (quarterly blocks for 4 years daily); our blocks are 78 days. No paper sets a target
false positive rate for DSR on a best-of-N pick: "nominal 5%" applies to single-strategy PSR only (SF p.12).

### Predictions (step 4), recorded 2026-11-10 before any run
| Question | Mayo said |
|---|---|
| Condition that moves single-strategy PSR false positive (nominal 5%) most | autocorrelation |
| Condition that moves best-of-100 DSR false positive most | correlated strategies |
| Condition that moves mean PBO furthest from 0.5 | none, stays near 0.5 |

### Step 4 results (RECOMPUTED, experiments/calibration.py, output results/calibration.txt)
2000 datasets per scenario for PSR and DSR, 200 for PBO, seed 20261110. Brackets: exact 95% CI.

| Scenario | PSR(0) > 0.95, fixed strategy | DSR > 0.95, best of 100 (N = 100) | PBO mean |
|---|---|---|---|
| IID Normal (baseline) | 4.95% [4.0, 6.0] | 0.00% [0, 0.18] | 0.520 +/- 0.010 |
| AR(1) phi 0.1 | 6.35% [5.3, 7.5] | 0.10% | 0.495 +/- 0.010 |
| AR(1) phi 0.3 | 11.85% [10.5, 13.4] | 0.70% | 0.482 +/- 0.011 |
| GARCH (0.05, 0.90) | 4.70% | 0.15% | 0.481 +/- 0.011 |
| GARCH (0.10, 0.85) | 5.45% | 0.10% | 0.501 +/- 0.011 |
| Student-t nu 8 | 4.35% | 0.15% | 0.511 +/- 0.011 |
| Student-t nu 5 | 4.85% | 0.05% | 0.504 +/- 0.011 |
| Correlated rho 0.3 | 5.35% | 0.70%; implied N (70.3): 1.05% | 0.512 +/- 0.011 |
| Correlated rho 0.7 | 4.95% | 2.60% [1.95, 3.40]; implied N (30.7): 5.05% [4.1, 6.1] | 0.504 +/- 0.011 |

PBO <= 0.05 (PBO p.14 rule) accepted a zero-edge set at most once in 200 in any scenario.
GARCH paired control, PBO original minus time-shuffled: -0.002 +/- 0.004 and +0.009 +/- 0.004 (about 2 SE,
one of two comparisons: weak evidence). GARCH vs baseline remains a combined clustering-plus-fat-tails comparison.

| Prediction | Mayo said | Result | Verdict |
|---|---|---|---|
| Moves PSR false positive most | autocorrelation | AR(1) phi 0.3: 11.85% vs nominal 5%; all others inside the 5% CI | right |
| Moves best-of-100 DSR most | correlated strategies | rho 0.7: 2.6% (baseline 0%); next largest 0.7% | right |
| Moves mean PBO from 0.5 most | none, stays near 0.5 | all scenarios 0.481 to 0.520, each within about 2 SE of 0.5 | right |

Why correlation moves DSR: correlated strategies have Sharpes that cluster, so V and SR0 = sqrt(V) E[max] shrink,
while the best strategy still carries the common noise. The implied-N adjustment (DSR Eq. 9) lowers N and so
makes DSR less strict, landing at 5.05% at rho 0.7.
Lead row for correlated strategies: implied N (decided 2026-11-12). DSR defines N as the number of independent
trials, so N = 100 is knowingly misspecified here. The generator's true rho 0.7 gives N = 30.7 by Eq. 9, and the
estimate 30.715 +/- 0.019 matches it. N = 100 stays as the naive comparator.
Limitation: on real data the average correlation is estimated, and DSR p.15 warns it is unreliable when
T < M(M-1)/2 (here 1248 < 4950).

Cleanup on 2026-11-10 after review: reverted the unrequested CSCV speed-up (cached split plan, single-rank
shortcut), README and extra .gitignore entries, and extra input validation. implied_n now treats a slightly
negative sample correlation as 0 (N = M) instead of raising. Full backup of the removed code: tmp/backup_before_trim/.
Every result number was unchanged by the cleanup (rerun compared line by line).
Signed off by Mayo 2026-11-12 (part a). Plot deferred to step 6. Open: French-data bootstrap robustness (part b).

## Step 3 (done)
- src/pbo/psr_dsr.py: psr (SF Eq. 11), min_trl (SF Eq. 13), sr0 and dsr (DSR Eq. 2). Notes: docs/psr_dsr_notes.md.
- tests/test_psr_dsr.py: all paper examples (SF pp.10-11, DSR pp.9-10) plus closed forms and bad-input guards. Suite: 90 passed.
- Kurtosis is raw (TODO 3.2 closed).
- Results, experiments/dsr_false_positives.py, RECOMPUTED:

| Check | Result | Mayo said | Verdict |
|---|---|---|---|
| PSR at SR = benchmark | 0.5 (closed form, tested) | 0.5 | right |
| Negative skew | lowers PSR (tested) | lowers | right |
| Paper hedge fund | 0.913 (PAPER, SF p.10; ours 0.9134) | about 0.91 | right (value was shown in the question) |
| Best of 100 zero-edge, PSR(0) > 0.95 | 1983/2000 = 0.9915 (CI 0.986 to 0.995) | about 100% | right |
| Best of 100 zero-edge, DSR > 0.95 | 1/2000 = 0.0005 (CI 0 to 0.0028); approx with V known 0.0015 | about 5% | wrong: DSR is much stricter |
- 2026-11-10 review (paper check + hardcoding/logic audit): formulas and all step-3 constants match SF pp.8-11 and
  DSR pp.8-10. Fixed: min_trl silently wrong for alpha > 0.5, now raises; psr n < 2 and sr0 negative variance raise;
  experiment reports exact binomial intervals and states the V-known assumption.
- 2026-11-10 external review of step 3: math correct, all paper examples reproduced. Fixed its findings:
  NaN/inf inputs raise; unsupported "about 0.0008" claim removed;
  "upper bound" wording removed; ddof = 1 for V listed as our choice. Files unstaged until Mayo commits.
- Step 1 and step 2 signed off by Mayo (project owner) on 2026-11-10: TODO 1.39, 2.4, 2.21.
- 2026-11-10 page check of all 51 constants: 44 match, 0 mismatch, 7 derived (docs/paper_check.md).
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

Why flat at low SR: with 496 IS days the best of 99 noise strategies has an annual Sharpe near 1.7
(logic review, approximate). A real SR below that rarely wins IS, so PBO stays at the noise level 0.5.
The spread is wide: one zero-edge dataset gave PBO 0.141, another 0.836. One CSCV run on one dataset is noisy.
Consistent in direction with the paper's own examples: random walk PBO 55% (p.25), real seasonal effect 13% (p.27).

- cscv.py speed-up by Mayo (block sums, each half computed once): 19x faster (0.20 s vs 3.73 s at S = 16).
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
of the Gumbel approximation: RECOMPUTED 0.0358 at n=10 (Eq. 2.4 minus the integral used in tests/test_minbtl.py;
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
- Our choice: TRIALS=2000 and the seed in best_of_n.py.
- Assumption in all of step 1: iid returns. Annualizing with sqrt(periods) is wrong under autocorrelation (step 4).

## For the reviewer
1. Check docs/paper_values.md against the PDFs in papers/. Each row has a page number.
2. The PSEUDO pages are from the author copy. Confirm they match the Notices version if you hold that one.
3. Sign off step 1 (TODO 1.39).
