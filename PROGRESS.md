# PROGRESS

## Done
- Setup: PROGRESS.md, .gitignore, pyproject.toml, docs/oracle_step1.md.
- Packages installed: numpy 2.5.4, scipy 1.18.1, pytest 9.2.0. requirements.txt frozen.
- experiments/check_oracle.py: all oracle rows pass.

## Verified vs UNVERIFIED
- RECOMPUTED (experiments/check_oracle.py): every step 1 oracle value. See docs/oracle_step1.md.
- Exact E[max of 10] = 1.5388 is confirmed only to Monte Carlo precision (SE 0.0006),
  so about 3 decimals, not 4.
- UNVERIFIED: "Prop 2.1" reference, and paper text "about 1.57", "about 5 years", "about 2 years".
  Not yet checked against the paper.

## Questions for the reviewer
1. Which paper and page holds the Gumbel approximation for E[max]? Is it Prop 2.1? Exact form?
2. Does the paper define MinBTL as (E[max]/target)^2 or with the 2 ln N bound? Which equation?
3. min_btl_years(10, 1): oracle 2.4794 vs formula notes 2.46. Which source made 2.46?
