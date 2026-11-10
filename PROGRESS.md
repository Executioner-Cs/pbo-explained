# PROGRESS

## Done
- Setup: PROGRESS.md, .gitignore, pyproject.toml.
- Packages installed: numpy 2.5.4, scipy 1.18.1, pytest 9.2.0. requirements.txt frozen.
- 2026-11-10: deleted experiments/check_oracle.py and docs/oracle_step1.md. Their numbers were typed in, and some are not in the paper.
- 2026-11-10: all paper numbers now live in src/pbo/paper_values.py, each with page and equation. Tests and experiments import from there.
- sharpe() in src/pbo/sharpe.py: 4 tests pass (closed form, ddof=0, scale invariance, zero variance raises).
- expected_max_normal() and min_btl_years() in src/pbo/minbtl.py, tested against paper values. Suite: 31 passed.
- experiments/best_of_n.py: 2000 trials, 5 years daily, seed 20261109. Output in results/best_of_n.txt.
- Step 1 code complete. Awaiting reviewer sign-off (task 1.39).

## Predictions vs results (step 1)
| Prediction | Mayo said | Result | Label |
|---|---|---|---|
| sharpe(), mean 0.0004, sd 0.01, 252 | about 0.04 (wrong) | 0.04*sqrt(252) = 0.635 | closed form, PSEUDO Eq. 2.2 |
| Doubling returns | Sharpe unchanged (right) | unchanged | closed form, tested |
| All returns equal | infinity (weak) | chose ValueError | design decision, tested |
| Growth of E[max] with N | like sqrt(ln N) (right) | grows like sqrt(2 ln N) | closed form bound, tested |
| MinBTL n=45, target 1 | about 5 years (right) | under 5 years; paper says 45 fit in 5 | PAPER (PSEUDO p.11), tested |
| SE of 5y annual Sharpe, zero edge | about 0.45 (right) | sim 0.443, PSEUDO Eq. 2.3 gives 0.447 | RECOMPUTED (best_of_n.py) |
| Best of 10/45/100, 5y | 0.7/1.0/1.1 (right) | sim 0.688/0.984/1.119 | RECOMPUTED (best_of_n.py) |

Simulation sits about 0.012 to 0.016 below the formula for every N. That matches the known overstatement
of the Gumbel approximation (0.036 at n=10, divided by sqrt(5) is 0.016).

## Verified vs UNVERIFIED
- PAPER (docs/paper_values.md): E[max] formula = PSEUDO Prop 2.1, Eq. 2.4, p.9, and DSR Eq. 1, p.7.
  MinBTL = PSEUDO Theorem 3.1, Eq. 3.2, p.11. Upper bounds sqrt(2 ln N) (p.9) and 2 ln N / target^2 (p.11).
- PAPER: 1.57 for N=10 (PSEUDO p.9). 45 configurations in 5 years (PSEUDO p.11). SR0 = 0.1132 (DSR p.10).
  All three are now tests, read from src/pbo/paper_values.py. Suite: 31 passed.
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
