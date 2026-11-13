# What backtest-overfitting statistics measure: replication and conditional calibration

> **Under correction (2026-11-12).** A publication audit (docs/publication_audit.md) found claims in the reviewed
> draft that the evidence does not support: the 1971-98 vs 1999-2026 PSR comparison (Section 3.5, withdrawn
> pending a corrected run), PBO "power" (Section 3.3, only mean PBO was measured), and the strength of the
> phi = 0.1 result (suggestive, not detected). Corrections are in progress; the original result files are kept.
> Not affected: the synthetic AR(1) counterexample at phi = 0.3, and the step 5 conclusion (insufficient evidence
> of superiority under the specified test, not evidence that skill is absent).

Step 6 write-up, reviewed 2026-11-12 (TODO 6.5), under correction. Labels: PAPER = printed in a paper (page given); RECOMPUTED = produced by this repository (file
given); UNVERIFIED = not checked by code or by a page. Our modeling choices are marked "(our choice)".

Papers (docs/paper_values.md): PBO = "The Probability of Backtest Overfitting"; SF = "The Sharpe Ratio Efficient
Frontier"; DSR = "The Deflated Sharpe Ratio"; PSEUDO = "Pseudo-Mathematics and Financial Charlatanism". All by
Bailey, Lopez de Prado and, for PBO and PSEUDO, Borwein and Zhu.

## Abstract
We reproduce published calculations for backtest-overfitting and Sharpe-ratio inference, then examine their
operating characteristics under specified synthetic departures from an IID Normal baseline and conditional
resampling of empirical returns. The statistics answer different questions: fixed-strategy confidence,
selection-adjusted performance relative to a noise benchmark, and the out-of-sample rank of an in-sample winner.
The synthetic results illustrate the known failure of an uncorrected Sharpe variance under serial dependence;
a return-mean long-run-variance adjustment reduces, but does not uniformly remove, the observed distortion.
The original location-benchmark DSR construction rarely accepts the selected winner in the IID null search
experiment, and its acceptance rate changes with cross-strategy correlation. An idealized market-factor search shows why high confidence
against a selection-adjusted zero-skill benchmark need not establish superiority to holding the market. These
findings concern the specific implementations and designs studied, not universal calibration, executable profits,
or all later DSR formulations. An invalid subperiod null discovered during review is withdrawn; its separately
centered correction remains pending. Full methods and correction provenance accompany the repository.

## 1. Question
What do these methods measure about backtest selection and statistical confidence, and what limitations appear in
our experiments? They answer different questions; none directly certifies a real edge.

| Tool | Source | Question it answers |
|---|---|---|
| PBO (via CSCV) | PBO paper | How often does the in-sample winner of a set of strategies rank at or below the out-of-sample median? |
| PSR | SF Eq. 11 | How confident are we that one strategy's Sharpe exceeds a benchmark SR*, given skew and kurtosis? |
| DSR (2014 construction) | DSR Eq. 2 | PSR for the best of N trials, against SR0, the Sharpe the best of N zero-skill trials is expected to reach. |
| MinTRL | SF Eq. 13 | Sample-length tool: how long a track record PSR needs for a given confidence. |
| MinBTL | PSEUDO Eq. 3.2 | Sample-length tool: relates the number of trials N, the sample length and the expected best Sharpe from noise alone. |

Sections 3-4 test the three statistics (PBO, PSR, DSR). MinTRL is checked against the paper examples. MinBTL is
checked against the paper examples, and its expected-maximum approximation against simulation (Section 3.1).

### 1.1 Contribution and relation to prior work
The formulas, selection problem and serial-dependence caveat are inherited from the cited literature. This
study's work is the traceable implementation and rounded-input replication, the specified simulation grid,
the conditional industry-bootstrap comparisons, and the contrast between search-noise and market benchmarks
in one idealized strategy family. These are empirical and implementation extensions; no new PBO, PSR or DSR
statistic, first discovery of the serial-correlation problem, or general calibration theorem is claimed.

Lo (2002), printed pp.39-40 and Appendix A p.47, treats dependent-return inference and time aggregation.
Ledoit and Wolf (2008), January working paper Section 3.1 and Remark 3.1, supply the paired-inference context
and the prior criticism of Opdyke's stationary formulas. Our Bartlett implementation is an explicitly documented
alternative within that delta-method framework, not a replication of their complete bootstrap procedure.

Version scope matters: the DSR results here concern Bailey and Lopez de Prado's **2014 Eq.2** and the Eq.9 trial
interpolation. Lopez de Prado and Porcu's later framework distinguishes location-only, location-scale and
full-search-distribution approaches. Only its indexed abstract and publication metadata have been inspected;
its proofs and alternative implementations have not been evaluated here. This study does not establish how
those later approaches perform. The literature review is targeted, not a completed systematic novelty search.

## 2. Method
The [methods supplement](research_methods.md) specifies the estimands, generators, resampling nulls, formulas,
uncertainty calculations and implementation conventions. The [input manifest](data_manifest.md) identifies
source snapshots and the remaining acquisition limitation. Paper equation/page citations below refer to the
specific author/working copies listed in the references, not automatically to journal pagination.

- Formulas coded from the papers, each constant with its page (src/pbo/paper_values.py). A page-by-page check of all
  52 constants: 45 match, 0 mismatch, 7 derived (docs/paper_check.md).
- Numerical expectations come from paper examples or independently derived closed forms. Additional tests
  check input validation, invariants and experiment reporting. Full suite: 253 tests pass (RECOMPUTED, 2026-11-12, after the audit fixes).
- Every experiment design and prediction was written down before its run; from step 5 on, committed before the run.
- Modeling choices (ours, not the papers'):
  - PBO counts logit <= 0 (our reading of PBO Sec. 3.1, p.13; Def. 2.2 on p.10 uses rank < N/2). Under the null the
    reference is 0.5 for N = 100 and 25/49 for N = 49. Ties take average ranks.
  - Sharpe ratios use ddof 0; the variance V of trial Sharpes in DSR uses ddof 1.
  - Implied N (DSR Eq. 8-9) clamps a negative average correlation at 0.
  - Newey-West lags int(4 (T/100)^(2/9)): 7 at T = 1248, 11 at T = 13,664.
  - Block lengths, simulation levels, the step 5 grid and costs are listed where used.

## 3. Results

### 3.1 Replication of the paper examples
All printed examples are reproduced, consistent with the printed values after accounting for rounded inputs
(RECOMPUTED, tests/). The SF three-year example needs that allowance: tests/test_psr_dsr.py checks it over the
interval of inputs that round to the printed ones, since plugging in the printed inputs directly rounds differently.

| Example | Paper value |
|---|---|
| PSR(0), hedge fund, Normal / skew and kurtosis / 3 years | 0.982 / 0.913 / 0.953 (PAPER, SF pp.9-10) |
| MinTRL, SR 2 vs SR* 1, daily / weekly / monthly / monthly HFR | 2.73 / 2.83 / 3.24 / 4.99 years (PAPER, SF p.11) |
| DSR, SR 2.5, N = 100 / N = 46 | 0.9004 / 0.9505 (PAPER, DSR p.10); SR0 0.1132 (PAPER, DSR p.10) |
| Expected maximum of N = 10 standard Normals | 1.57 (PAPER, PSEUDO p.9) |
| MinBTL, target Sharpe 1, 5 years | at most 45 configurations (PAPER, PSEUDO p.11) |

Simulation check of the expected maximum (RECOMPUTED, results/best_of_n.txt; 2000 trials, 5 years daily, zero
edge): for the best of N = 10 five-year annual Sharpe estimates, PSEUDO Eq. 2.4 times 5^(-1/2) gives 0.704; the
simulated mean is 0.688 +/- 0.006. The gap is similar at N = 45 (1.000 vs 0.984 +/- 0.005) and N = 100 (1.132 vs
1.119 +/- 0.004).

One printing error: PBO pp.11 and 22 print 12,780 splits for S = 16; Eq. 2.3 gives C(16, 8) = 12,870.

### 3.2 Selection: PSR vs DSR on the best of 100 zero-edge strategies
Five years daily, 2000 trials (RECOMPUTED, results/dsr_false_positives.txt):
- PSR(0) > 0.95 on the best: 99.15% [98.6, 99.5]. PSR ignores the selection.
- DSR > 0.95 on the best: 0.05% [0, 0.28]. DSR accounts for it, and in this setup is far below 5%.

### 3.3 Broken assumptions, zero true edge (synthetic)
N = 100 strategies, T = 1248 days, seed 20261110 (RECOMPUTED, results/calibration.txt). PSR and DSR: 2000 datasets
per scenario, rates with exact 95% CIs in percent. PBO: 200 datasets, mean +/- one Monte Carlo SE. A count of 0
gives a rate of 0% in this sample, not a zero underlying rate; its CI shows the range.

| Scenario | PSR(0) > 0.95, fixed strategy | DSR > 0.95, best, N = 100 | Mean PBO |
|---|---|---|---|
| IID Normal | 4.95 [4.04, 5.99] | 0.00 [0.00, 0.18] | 0.520 +/- 0.010 |
| AR(1) phi 0.1 | 6.35 [5.32, 7.51] | 0.10 [0.01, 0.36] | 0.495 +/- 0.010 |
| AR(1) phi 0.3 | 11.85 [10.47, 13.35] | 0.70 [0.38, 1.17] | 0.482 +/- 0.011 |
| GARCH (0.05, 0.90) | 4.70 [3.81, 5.72] | 0.15 [0.03, 0.44] | 0.481 +/- 0.011 |
| GARCH (0.10, 0.85) | 5.45 [4.50, 6.54] | 0.10 [0.01, 0.36] | 0.501 +/- 0.011 |
| Student-t nu 8 | 4.35 [3.50, 5.34] | 0.15 [0.03, 0.44] | 0.511 +/- 0.011 |
| Student-t nu 5 | 4.85 [3.95, 5.88] | 0.05 [0.00, 0.28] | 0.504 +/- 0.011 |
| Correlated rho 0.3 | 5.35 [4.40, 6.43] | 0.70 [0.38, 1.17]; implied N 1.05 [0.65, 1.60] | 0.512 +/- 0.011 |
| Correlated rho 0.7 | 4.95 [4.04, 5.99] | 2.60 [1.95, 3.40]; implied N 5.05 [4.13, 6.10] | 0.504 +/- 0.011 |

- Evidence rule (recorded in PROGRESS.md, step 4; completed after the step 4(b) run, so after these results were
  seen): |z| < 2 no detected effect, 2 to 3 suggestive, >= 3 or Bonferroni p < 0.05 within one table detected.
  AR(1) phi 0.3: z = 14.1 against 5%, detected. AR(1) phi 0.1: z = 2.77, exact two-sided binomial p = 0.0075,
  Bonferroni over the nine scenarios p = 0.068, so suggestive only. Every other PSR interval contains 5%.
  For a stationary Gaussian AR(1) at zero Sharpe our derivation gives the large-sample rate:
  6.84% at phi 0.1, 11.37% at phi 0.3 (RECOMPUTED, psr_dsr.ar1_psr_false_positive). Both values lie inside the
  simulated 95% intervals (Figure 1).
- The DSR rate rises with correlation between strategies. Mean PBO stays within about 2 SE of 0.5 in every scenario.
  Implied N 30.7 at rho 0.7 is the DSR Eq. 9 interpolation evaluated at the generating correlation (PAPER, DSR p.14,
  an interpolation), not a known true number of independent trials. Recovering it (30.715) checks the estimate of
  that formula, not the accuracy of the DSR correction.
- A Newey-West variance (our correction) cuts PSR at phi 0.3 from 11.85% to 7.10% [6.01, 8.31], not to 5%.
- Mean PBO with one real edge (T = 992, 20 datasets per cell; RECOMPUTED, results/null_checks.txt). Only mean PBO
  was measured, not the probability of passing PBO <= 0.05 or of selecting the planted strategy, so these numbers
  say nothing direct about decision power. The edge is set as a fixed daily mean/SD ratio times sqrt(250). Under
  AR(1) that keeps the daily signal fixed but lowers the Sharpe of 250-day summed returns: at phi 0.3 the label
  "Sharpe 2" corresponds to about 1.47 (RECOMPUTED in docs/publication_audit.md, finite 250-day variance factor
  1.852). With that convention: no change in mean PBO was detected at the tested GARCH level; under AR(1) phi 0.3
  mean PBO is higher than under IID noise, 0.391 +/- 0.043 vs 0.189 +/- 0.037 at label 2 (z +3.55) and 0.098 +/-
  0.019 vs 0.026 +/- 0.007 at label 3 (z +3.62).

Figure 1 (results/figure1_psr_ar1.png, made by experiments/figure_psr_ar1.py): uncorrected PSR(0) > 0.95 rate at
the tested AR(1) values (IID baseline, phi 0.1, 0.3), 2000 simulated datasets each, exact 95% intervals
(RECOMPUTED, results/calibration.txt). Dashed line: large-sample rate from our derivation, an asymptotic
approximation, not a simulation (RECOMPUTED, results/psr_ar1_curve.txt). Dotted line: nominal 5%.

![Figure 1](../results/figure1_psr_ar1.png)

### 3.4 The serial-correlation claim
SF p.4 says, citing Opdyke (2007), that its results hold for stationary and ergodic returns (PAPER, SF p.4; also p.8).
Section 3.3 contradicts this for a stationary AR(1). At zero true Sharpe, stationary Gaussian AR(1) dependence
changes the limiting variance by (1 + phi)/(1 - phi); the discrepancy persists as the sample grows (our derivation).
The claim traces to Opdyke's reading of Christie's (2005) lag-0 closed form (Christie App. B, pp.33-35; Opdyke p.4).
It is not a new finding: Ledoit and Wolf (2008), January 2008 working paper, printed p.6, Remark 3.1, already call
Opdyke's formulas for stationary time series incorrect (PAPER; checked by online text inspection, not in papers/).
SF's IID results, examples and formulas stand.

### 3.5 Real dependence: French 49 industries
Daily value-weighted industry returns, 1971-07-01 to 2026-09-30, demeaned so the true edge is zero, resampled in
whole-day blocks of L days (our choice: L = 1, 5, 20, 60; L = 20 primary), T = 1248, 2000 datasets (RECOMPUTED,
results/french_bootstrap.txt, results/french_followups.txt):
- PSR(0) > 0.95: 5.35% [4.40, 6.43] at L = 1, 6.25% [5.23, 7.40] at L = 20 and at L = 60. Pooled over L >= 5: 5.88%, z = 3.14 (UNVERIFIED as code:
  one-off calculation from the counts; pooling chosen after the run).
- Withdrawn: the period comparison (L = 20; 10.45% for 1971-1998, 3.30% for 1999-2026; original output kept in
  results/french_followups.txt). Each period was resampled without re-centring, so its industry means were not
  zero: 36 of 49 positive in 1971-1998, 13 of 49 in 1999-2026. The two rates mix mean differences with dependence
  and are not zero-edge rejection rates. A corrected run, demeaned within each period, is designed in PROGRESS.md.
- DSR rates are 1.25% to 3.55%, every upper CI bound below 5%; implied N is 23.0 to 23.3 for 49 industries. Mean PBO
  0.505 to 0.520 (SE 0.012 to 0.014; reference 25/49 = 0.510). PBO: 200 datasets per L.

### 3.6 Case study: moving-average crossover on the US market
93 settings (our choice: fast 5-50, slow 25-250 days), long the market or flat, signal acts the next day, costs 0, 5
(main) or 10 bps per change in position (our choice). Fama-French market factor, 1972-07-18 to 2026-09-30,
T = 13,664 days (RECOMPUTED, results/ma_crossover.txt, results/market_comparison.txt). This is an idealised
research-factor experiment, not an executable strategy: the market factor is a CRSP research portfolio, the signal
from the close of day t earns the whole close-t to close-(t+1) return (a fill at the same close just observed), and
costs are a flat charge per change in position. At 5 bps:

| Measure | Value | What it says |
|---|---|---|
| Best setting (15/225) annual Sharpe vs market | 0.588 vs 0.458 | Historical, in-sample advantage of +0.130 |
| PBO (S = 16) | 0.208 | 20.8% of CSCV splits put the in-sample winner at or below the OOS median; fails the PBO <= 0.05 rule (PAPER, PBO p.14) |
| DSR, N = 93 / implied N 17.2 | 0.9980 / 0.9994 | Best Sharpe is above SR0, the zero-skill selection benchmark; not a test against the market |
| Paired HAC test vs market (11 lags) | difference 0.130, se 0.099, raw one-sided p 0.094 | Insufficient evidence of superiority; 0 of 93 pass the Bonferroni test (also at 0 and 44 lags) |

At 0 and 10 bps the best setting is the same and PBO is 0.240 and 0.193. The paired test follows Ledoit and Wolf
(2008), Eqs. 1-5, with a Bartlett kernel, fixed bandwidth and no T/(T-4) scaling (our choices). Conclusion: the
selected rule had a higher historical Sharpe than the market, but this does not establish that any of the 93
settings beats it, nor that timing skill is absent.

## 4. Limits

What the calibration showed breaks, within the tested scenarios:
- PSR's variance assumes no serial correlation. Under AR(1) phi 0.3 its rejection rate exceeds 5% (detected);
  at phi 0.1 the excess is suggestive only (Section 3.3).
- A Newey-West variance with the rule-of-thumb lag reduces but does not remove the excess at phi 0.3 (7.10%).
- Mean PBO stays near 0.5 under every zero-edge scenario. With a real edge at a fixed daily signal, mean PBO is
  higher under AR(1) phi 0.3; decision power was not measured.
- DSR's rate depends on correlation between strategies; with N = 100 it stays far below 5%, with implied N (an
  interpolation, DSR Eq. 9) it reaches 5.05% at rho 0.7. Neither is a calibrated 5% test.

Scope of this study:
- Calibration experiments for PSR used only SR* = 0; MinTRL under GARCH is untested. Synthetic levels are our choices, not a survey.
- Section 3.5 intervals are Monte Carlo error given one 1971-2026 history.
- DSR rates rest on reading DSR > 0.95 as 95% confidence (DSR p.10); no paper states a false-positive rate.
- PBO is a share of overlapping CSCV splits, not a future failure probability, and has no binomial standard error.
- The case study is one market, one strategy family and one grid. The HAC test is asymptotic; Bonferroni is
  conservative. HAC validity requires suitable stationarity, mixing, finite moments and bandwidth growth;
  those conditions are not established for this long market history. Not rejecting is not proof of no skill.
- All results are historical; none says how a strategy will perform in the future.

## Unresolved claims (TODO 6.6)
- Pooled PSR rate over L >= 5 (5.88%, z = 3.14, Section 3.5): UNVERIFIED as code. A one-off calculation from the
  counts, recomputed by hand in this review ((353/6000 - 0.05) / sqrt(0.05 x 0.95 / 6000) = 3.14); pooling was chosen
  after the run.
- Ledoit and Wolf (2008): checked by online text inspection of the working paper, not of the journal version, and
  not stored in papers/.
- Period comparison (Section 3.5): withdrawn; corrected run pending.
- Step 4(b) follow-ups not used in this text change more than their names suggest (PROGRESS.md): the AR(5)
  residual check (G2) also changes marginal moments and cross-industry relationships, so it is a robustness check,
  not an isolated removal of autocorrelation; the weekly check (B) changes horizon (6,240 days), marginal moments
  and uses arithmetic five-day sums, not only the sampling frequency.
- Later DSR and dependent-Sharpe formulations have not been evaluated. The contribution is scoped to the
  cited older implementations; a complete current-literature comparison remains outstanding.
- Exact reproduction needs the frozen data files; their durable acquisition is not yet documented. SHA-256 checks detect changed data but cannot
  recover it.

## 5. References
Equation/page locators refer to the versions identified here. Journal metadata does not imply that the journal
PDF was inspected when only an author copy was available.

1. Bailey, D. H., Borwein, J. M., Lopez de Prado, M., and Zhu, Q. J. (2017). *The Probability of Backtest
   Overfitting*. Journal of Computational Finance, 20(4). [DOI](https://doi.org/10.21314/JCF.2016.322).
   Formula source: [February 27, 2015 author copy](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf).
   Journal page ranges differ across author bibliographies; working-copy page references are used here.
2. Bailey, D. H., and Lopez de Prado, M. (2012). *The Sharpe Ratio Efficient Frontier*. Journal of Risk,
   15(2), 3-44. [DOI](https://doi.org/10.21314/JOR.2012.255).
   Formula source: [July 2012 author copy](https://www.davidhbailey.com/dhbpapers/sharpe-frontier.pdf).
3. Bailey, D. H., and Lopez de Prado, M. (2014). *The Deflated Sharpe Ratio: Correcting for Selection Bias,
   Backtest Overfitting, and Non-Normality*. Journal of Portfolio Management, 40(5), 94-107.
   [DOI](https://doi.org/10.3905/jpm.2014.40.5.094).
   Formula source: [July 31, 2014 author copy](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf).
4. Bailey, D. H., Borwein, J. M., Lopez de Prado, M., and Zhu, Q. J. (2014). *Pseudo-Mathematics and Financial
   Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance*. Notices of the American
   Mathematical Society, 61(5), 458-471. [DOI](https://doi.org/10.1090/noti1105).
   Formula source: [April 1, 2014 author copy](https://www.davidhbailey.com/dhbpapers/backtest-pseudo.pdf).
5. Christie, S. (2005). *Is the Sharpe Ratio Useful in Asset Allocation?* MAFC Research Papers, 1-48,
   Macquarie Applied Finance Centre. [Institutional record](https://researchers.mq.edu.au/en/publications/is-the-sharpe-ratio-useful-in-asset-allocation/).
   SSRN 720801; cited Appendix B pagination refers to the locally checked preprint.
6. Opdyke, J. D. (2007). *Comparing Sharpe Ratios: So Where Are the p-values?* Journal of Asset Management,
   8(5), 308-336. [DOI](https://doi.org/10.1057/palgrave.jam.2250084).
   Local preprint page locators are not journal page numbers; its exact revision date is not verified here.
7. Ledoit, O., and Wolf, M. (2008). *Robust Performance Hypothesis Testing with the Sharpe Ratio*. Journal of
   Empirical Finance, 15(5), 850-859. [DOI](https://doi.org/10.1016/j.jempfin.2008.03.002).
   Checked source: [January 2008 Zurich Working Paper 320](https://www.econ.uzh.ch/apps/workingpapers/wp/iewwp320.pdf),
   especially printed pp.4-6. This is working-paper text inspection, not a journal-page audit.
8. Lo, A. W. (2002). *The Statistics of Sharpe Ratios*. Financial Analysts Journal, 58(4), 36-52.
   Checked source: [journal PDF hosted at Berkeley](https://traders.berkeley.edu/papers/The-Statistics-of-Sharpe-Ratios.pdf),
   text of printed pp.39-40 and Appendix A p.47. Earlier progress entries saying this paper was unavailable are historical.
9. Lopez de Prado, M., and Porcu, E. (2026). *The Deflated Sharpe Ratio: A Unified Framework for Search-Adjusted
   Performance Inference*. Journal of Portfolio Management, 53(1), 70-120, according to the
   [author publication record](https://www.quantresearch.org/Publications.htm).
   [SSRN 7198158](https://ssrn.com/abstract=7198158), revised August 30, 2026; the record gives a September 23,
   2025 writing date. Only metadata and the indexed abstract were consulted; full proofs were not assessed.
