# Oracle table, step 1

Status: RECOMPUTED by experiments/check_oracle.py on 2026-11-07, all rows pass. Paper text claims stay UNVERIFIED.
Tolerance follows the digits given. Half a unit in the last digit.

| Quantity | Value | Tolerance | Label | Note |
|---|---|---|---|---|
| expected_max_normal(10) | 1.5746 | abs 5e-5 | RECOMPUTED | Formula value. Paper text says about 1.57 (UNVERIFIED, page not opened). |
| exact E[max of 10 iid N(0,1)] | 1.5388 | 3 MC standard errors | RECOMPUTED (MC 1.53923 +/- 0.00059) | Gap test: formula minus exact is about 0.036. |
| min_btl_years(45, 1) | 4.998 | abs 5e-4 | RECOMPUTED | Paper says about 5 years. |
| min_btl_years(7, 1) | 1.92 | abs 5e-3 | RECOMPUTED | Paper says about 2 years. |
| min_btl_years(10, 1) | 2.4794 | abs 5e-5 | RECOMPUTED | Formula notes say 2.46. Conflict, see PROGRESS.md. |
| smallest n with min_btl_years(n, 1) > 5 | 46 | exact | RECOMPUTED | Integer. Also assert n=45 is not > 5. |
| 2*ln(45) | 7.61 | abs 5e-3 | closed form | Derivable on paper. Upper bound, must exceed 4.998. |
| expected best annual Sharpe, 5y, n=45, zero edge | about 1 | none | RECOMPUTED closed form 0.9998 | Paper logic UNVERIFIED. Simulation version belongs in experiments/. |

## How the labels get upgraded
experiments/check_oracle.py (Mayo types it) must not import src/pbo.
Independent routes:
- Formula values: stdlib `statistics.NormalDist().inv_cdf`, not scipy.
- Exact E[max of 10]: Monte Carlo, at least 1e6 draws, fixed seed. Report the mean and its standard error.
  The check passes only if 1.5388 sits within 3 standard errors.
- Integer row: loop n upward with the stdlib version.
If a value fails, the oracle is wrong, not the test. Stop and tell the reviewer.
