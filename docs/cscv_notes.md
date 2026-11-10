# CSCV notes (step 2)

Source: papers/backtest-prob.pdf. Bailey, Borwein, Lopez de Prado, Zhu,
"The Probability of Backtest Overfitting". Page = PDF page. Pages read as images: 9 to 14, 25 to 27. p.28 seen only as extracted text.

## Procedure (Algorithm 2.3, pp.11-12)
1. M is a T x N matrix. Column n = P&L of trial n. Rows synchronous. (p.11, First)
2. Split rows into an even number S of disjoint blocks, each T/S rows. (p.11, Second)
3. Form all C(S, S/2) combinations of blocks. Eq. 2.3. (p.11, Third)
4. For each combination c (p.11-12, Fourth):
   a. J = the S/2 blocks in c, original order. IS set, T/2 x N.
   b. J-bar = the other S/2 blocks, original order. OOS set.
   c. R^c = performance of each column on J. r^c = its ranks.
   d. Same on J-bar: R-bar^c, r-bar^c.
   e. n* = best IS strategy.
   f. omega_c = r-bar^c_{n*} / (N + 1). Relative OOS rank, in (0, 1).
   g. lambda_c = ln(omega_c / (1 - omega_c)). The logit.
5. f(lambda) = relative frequency of the logits. Eq. 2.4 (p.12).
6. PBO = phi = integral of f from -inf to 0 (p.13, Sec 3.1). So PBO = share of logits <= 0.

Ranks: 1 = worst, N = best. Example on p.9: R = (0.5, 1.1, 0.7) gives r = (1, 3, 2).
Figure 1 (p.13): S = 4, blocks A B C D. IS/OOS pairs in order:
AB|CD, AC|BD, AD|BC, BC|AD, BD|AC, CD|AB.

## Our choices (not fixed by the paper)
- Metric: per-period Sharpe (paper p.11 uses Sharpe as its example). Ranking ignores annualization.
- PBO counts logits <= 0, i.e. OOS rank <= (N+1)/2. RESOLVED 2026-11-10, reasons:
  1. The estimator the paper actually defines for CSCV is phi = integral of f up to 0 (Sec 3.1, p.13).
  2. With zero-edge strategies this gives PBO = 1/2 exactly for even N (closed form, and RECOMPUTED
     0.515 +/- 0.025 in results/null_checks.txt). Def 2.2's literal rank < N/2 would give
     (N/2 - 1)/N = 0.49 at N = 100: a no-information selection would not score 1/2.
  3. Two public implementations count lambda <= 0 (fetched 2026-11-10, code read, not run):
     R pbo (github.com/mrbcuda/pbo, R/pbo.R): phi <- sum(ifelse(lambda<=0,1,0))/ncol(cs)
     pypbo (github.com/esvhd/pypbo, pypbo/pbo.py): 1.0 if lam <= 0
  Def 2.2 (p.10) stays a noted inconsistency in the paper. For even N, <= 0 and < 0 give the same PBO.
- omega = rank / (N + 1), as on p.12 and in pypbo. The R pbo package divides by N instead
  (omega = 1 at the top rank, logit = inf). We follow the paper.
- Ties: average ranks (scipy rankdata "average"). RESOLVED 2026-11-10. The paper ranks permutations
  (p.9), so it has no ties. R pbo (rank default) and pypbo (rankdata default) both use average.
  Matters for duplicate strategies. Tests: test_rank_ties_get_average, test_duplicate_strategies_share_rank.
  IS ties pick the first column (np.argmax), as pypbo does. For identical columns this does not change omega.

## Paper inconsistencies to flag
- p.11: "if S = 16, we will form 12,780 combinations". C(16, 8) = 12,870. Typo in the paper. RESOLVED:
  code counts by Eq. 2.3; test_paper_s16_count_is_a_typo asserts 12,870 and != the printed 12,780;
  the page review (docs/paper_check.md) confirms 12,780 is what p.11 prints.
- p.25: grid "[0,...,10] for Stop_loss" is 11 values, so 22 x 20 x 11 x 2 = 9,680, not the 8,800 printed.
- p.26: says "(1.54 vs. 1.3)" but p.25 gives the first Sharpe as 1.27.
- p.28 summary says "underperforms the mean OOS" (extracted text, not seen as image). Def 2.2 says median.

## The paper's own two checks (pp.25-27)
1. Random walk, 1,000 daily prices, seasonal rule searched over a parameter grid. PBO = 55%. (p.25)
2. Same, but first 5 days of each month shifted to mean +0.25 sd. Real edge. PBO = 13%. (p.26-27)
Both are single runs with an unknown seed. We cannot match 55% and 13% exactly.
The rule's code is in "Bailey et al. [1], Appendix 4" (p.27). Not yet opened.

## Our two null checks (closed form, no paper number needed)
1. All N strategies iid, zero edge. The IS pick's OOS rank is uniform on 1..N.
   With N even, P(rank <= N/2) = 1/2 exactly. So PBO should sit near 0.5.
2. One strategy has a real edge. As edge grows, it wins IS and OOS, so PBO goes to 0.
