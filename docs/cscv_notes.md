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
- PBO counts logits <= 0, i.e. OOS rank <= (N+1)/2, the median rank. Follows "underperform the median"
  (Sec 3, p.13) and the integral up to 0 (p.13). Def 2.1 (p.9) is about the expected rank (<= N/2),
  not a probability, so it does not settle this.
  Def 2.2 / Eq. 2.2 (p.10) writes rank < N/2. That differs for every N: N=4 counts {1} not {1,2}.
  Whether the point lambda = 0 (odd N only) counts is not settled by the integral. FLAG for reviewer.
- Ties in rank: not handled. Continuous data makes them unlikely.

## Paper inconsistencies to flag
- p.11: "if S = 16, we will form 12,780 combinations". C(16, 8) = 12,870. Typo in the paper.
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
