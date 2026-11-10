# Step 2 review packet (TODO 2.4 and 2.21)

For the reviewer. Each item: what to check, where, and how. Sign at the bottom.
Code commit at time of writing: see `git log`. Paper = papers/backtest-prob.pdf (PDF page numbers).

## 1. Procedure matches the paper
- [ ] src/pbo/cscv.py against Algorithm 2.3 (pp.11-12) and Sec 3.1 (p.13). Line comments name each step.
- [ ] Rank direction 1 = worst: p.9 example. Test: test_rank_paper_example.
- [ ] Split order matches Figure 1 (p.13). Test: test_splits_match_figure_1.
- [ ] Fast block-sum version equals the plain step-by-step loop. Test: test_fast_cscv_matches_plain_algorithm.

## 2. The two null checks (TODO 2.4: approve the design)
Script experiments/null_checks.py, output results/null_checks.txt. N = 100, T = 992, S = 16 (and 8), seed fixed.
- [ ] Null 1, all zero edge. Claim: expected PBO = 1/2 exactly for even N. Argument in the script docstring:
      per split the IS pick uses IS rows only, OOS rows are independent and columns exchangeable,
      so its OOS rank is uniform on 1..N. Result 0.515 +/- 0.025 (S = 16), 0.502 +/- 0.025 (S = 8).
- [ ] Null 2, one strategy with true annual SR 0 to 3 (per-period mean SR/sqrt(250), PSEUDO Eq. 2.2).
      Expectation: PBO falls to 0. Result 0.516, 0.511, 0.433, 0.189, 0.026.
- [ ] Agree these two are the right null checks, or name a different one.

## 3. Decisions to accept or overrule
- [ ] PBO counts logit <= 0, not Def 2.2's rank < N/2. Reasons in docs/cscv_notes.md.
- [ ] Ties get average ranks. Reasons in docs/cscv_notes.md.
- [ ] Metric is per-period Sharpe, ddof = 0.
- [ ] Paper typo: 12,780 on p.11 should be 12,870 (Eq. 2.3).

## 4. Run it yourself
```
.venv\Scripts\python.exe -m pytest -q                       # expect all pass
.venv\Scripts\python.exe experiments\null_checks.py         # about 30 s; expect results/null_checks.txt unchanged
```

## Sign-off
- TODO 2.4 null checks approved: Mayo (project owner)  date: 2026-11-10
- TODO 2.21 step 2 signed off:   Mayo (project owner)  date: 2026-11-10
