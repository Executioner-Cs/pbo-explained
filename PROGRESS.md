# PROGRESS

## Done
- Setup: PROGRESS.md, .gitignore, pyproject.toml.
- Packages installed: numpy, scipy, pytest, pypdf (for check_paper_values.py). matplotlib installed, not used yet. Exact pins in requirements.txt.
- 2026-11-10: deleted experiments/check_oracle.py and docs/oracle_step1.md. Their numbers were typed in, and some are not in the paper.
- 2026-11-10: all paper numbers now live in src/pbo/paper_values.py, each with page and equation. Tests and experiments import from there.
- sharpe() in src/pbo/sharpe.py: 4 tests pass (closed form, ddof=0, scale invariance, zero variance raises).
- expected_max_normal() and min_btl_years() in src/pbo/minbtl.py, tested against paper values. Suite at end of step 1: 31 passed.
- 2026-11-10: experiments/check_paper_values.py opens each PDF and confirms every constant in paper_values.py is on its cited page. 13 pass by text. 5 sit in equation images or Figure 1: Mayo checked them by eye on 2026-11-10, all match. Fails on any constant it does not know. Local only (needs papers/).
- experiments/best_of_n.py: 2000 trials, 5 years daily, seed 20261109. Output in results/best_of_n.txt.
- Step 1 code complete. Awaiting reviewer sign-off (task 1.39).

## Step 2 (in progress)
- src/pbo/cscv.py: Algorithm 2.3 and Sec 3.1 of the PBO paper. tests/test_cscv.py. Notes in docs/cscv_notes.md.
- 2026-11-10 review by two read-only checks: formulas match the paper pages; no unlabelled numbers left.
  Fixed: DSR example inputs cited on p.9 (was p.10), lambda <= 0 note corrected, zero variance now raises in cscv.
- 2026-11-10 second review (hardcoding audit + logic review of cscv and null checks). Fixed: NaN input and
  float-rounded constant columns used to give PBO 0 silently, now raise; bad S now raises ValueError;
  added a hand-worked 4-strategy, 4-block test with PBO = 1/6.
- Suite: 59 passed.
- Open: reviewer flags in docs/cscv_notes.md. Ties in rank are not handled (matters for discrete P&L in step 5).

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
