# PBO, PSR and the 2014 Deflated Sharpe Ratio: a replication and conditional calibration study

Mayank Khandelwal. Working paper, revised 2026-11-12.

**Keywords:** backtest overfitting; probabilistic Sharpe ratio; deflated Sharpe ratio; combinatorially symmetric
cross-validation; serial correlation; replication. **JEL:** C12, C15, C58, G11.

Provenance labels used throughout: PAPER = printed in a cited paper (page given); RECOMPUTED = produced by the
accompanying code (result file given); UNVERIFIED = not checked by code or against a page. Modelling choices that
are ours, not the source papers', are marked "(our choice)".

## Abstract
We reimplement the probability of backtest overfitting (PBO, estimated by combinatorially symmetric
cross-validation, CSCV), the probabilistic Sharpe ratio (PSR), the minimum track record length (MinTRL), the
minimum backtest length (MinBTL) and the 2014 deflated Sharpe ratio (DSR), reproduce every printed example, and
measure how the three statistics behave when one assumption of independent and identically distributed (IID)
Normal returns is relaxed, under a block bootstrap of
daily US industry returns, and in an idealized moving-average search on the US market factor. Four findings.
(1) Confirming known theory (Lo 2002; Ledoit and Wolf 2008): with zero true Sharpe, uncorrected PSR(0) rejects
11.85% of the time at 95% under Gaussian first-order autoregressive, AR(1), dependence with phi = 0.3, matching the large-sample value 11.37%.
(2) On real industry returns the distortion follows the data's dependence in both directions: after centering each
period, PSR(0) rejects 8.35% [7.17, 9.65] when resampling 1971-1998 and 3.85% [3.05, 4.79] for 1999-2026; the
full-window rate is a mixture of the two. (3) By construction the 2014 DSR compares the selected Sharpe with the
expected noise maximum, so its null acceptance rate is far below 5% (0.05% in an IID search of 100) and rises with
cross-strategy correlation. (4) In the market case study the best of 93 settings has DSR 0.998, yet a paired test
against buy-and-hold does not reject (raw one-sided p 0.094; Hansen's SPA test over all 93 settings, p 0.50); the
paired test could only have detected an annual Sharpe advantage of about 0.41, and the result is insensitive to an
extra day of execution lag and to trading costs. The statistics answer different questions; none certifies an edge.

## 1. Introduction
Backtests are searches, and the best of many noisy strategies looks good by construction. Bailey, Borwein, Lopez de
Prado and Zhu proposed PBO and MinBTL to measure that selection effect (Bailey et al. 2014, 2017), and Bailey and
Lopez de Prado proposed PSR, MinTRL and DSR to attach confidence to a Sharpe ratio after allowing for
non-normality and the number of trials (Bailey and Lopez de Prado 2012, 2014). These tools are widely used as
screening thresholds: "DSR above 0.95" or "PBO at most 0.05".

This paper asks what these statistics measure, and what limitations appear when their assumptions are relaxed in
controlled and empirical designs. It is a replication and conditional calibration study: the formulas, the
selection problem and the serial-dependence caveat come from the cited literature.

| Statistic | Source | Question it answers |
|---|---|---|
| PBO via CSCV | Bailey et al. (2017), Algorithm 2.3 | How often does the in-sample winner of a strategy set rank at or below the out-of-sample median? |
| PSR | Bailey and Lopez de Prado (2012), Eq. 11 | How confident are we that one strategy's Sharpe exceeds a benchmark SR*, allowing for skew and kurtosis? |
| DSR (2014) | Bailey and Lopez de Prado (2014), Eq. 2 | PSR for the best of N trials, against SR0, the Sharpe the best of N zero-skill trials is expected to reach. |
| MinTRL | Bailey and Lopez de Prado (2012), Eq. 13 | How long a track record PSR needs for a given confidence. |
| MinBTL | Bailey et al. (2014), Eq. 3.2 | How the number of trials, sample length and expected best noise Sharpe are related. |

**Contribution.** Confirmations of known results: the replication of every printed example, and the AR(1) PSR
distortion. New quantitative evidence, conditional on the designs studied: (a) the operating characteristics of
the 2014 DSR under IID and correlated searches and its sensitivity to the trial-count convention; (b) the
period-dependent, two-directional PSR distortion on daily industry returns; (c) a single case study contrasting
DSR's zero-skill benchmark with a market benchmark, with the power of the market test made explicit. We claim no
new statistic and no calibration theorem.

## 2. Related work
**Sharpe-ratio inference.** Jobson and Korkie (1981) and Memmel (2003) give the IID Normal variance of a Sharpe
ratio and of differences of Sharpe ratios. Lo (2002) derives standard errors for IID returns and, by GMM with a
heteroskedasticity- and autocorrelation-consistent (HAC) estimator, for serially dependent returns. Mertens (2002)
gives the IID non-Normal variance that PSR uses. Christie (2005) estimates by GMM with a HAC matrix in practice,
while his analytical closed form (Appendix B) is contemporaneous only. Opdyke (2007) equates that closed form with
Mertens' and extends its validity to stationary ergodic returns; Bailey and Lopez de Prado (2012, p.4) inherit
the claim. Ledoit and Wolf (2008, Remark 3.1) point out that Opdyke's time-series formulas reduce to the IID ones
and are therefore incorrect, and propose HAC and studentized bootstrap tests of Sharpe differences. Pav (2021)
surveys the field.

**Data snooping and multiple testing.** White's (2000) Reality Check, Hansen's (2005) test for superior predictive
ability (SPA) and the stepwise procedure of Romano and Wolf (2005) test whether the best of many rules beats a
benchmark while accounting for the search. Sullivan, Timmermann and White (1999) applied the Reality Check to
moving-average and other technical rules on US index data, building on Brock, Lakonishok and LeBaron (1992). Our
case study is a small instance of that design. Harvey and Liu (2014, 2015) and Harvey, Liu and Zhu (2016) discuss
multiple-testing haircuts for Sharpe ratios and factors. Lopez de Prado and Lewis (2018) estimate the effective
number of trials by clustering, an alternative to the DSR interpolation we use.

**Later formulations.** Lopez de Prado and Porcu (2026) present the 2014 DSR as a location benchmark and a newer
implementation that adds dispersion, describing them as serving different inferential objectives; Lopez de Prado,
Lipton and Zoonekynd (2026) revisit PSR, MinTRL and DSR. We evaluate only the 2012/2014 formulas; these later
papers were consulted through abstracts and metadata only (UNVERIFIED for content), and how their procedures behave
in our designs is not established here.

**Return data.** Daily portfolio returns show positive autocorrelation partly induced by nonsynchronous trading
(Lo and MacKinlay 1988, 1990). This is relevant to the period effect in Section 4.5.

## 3. Methods
Full specifications are in the methods supplement (docs/research_methods.md) and the input manifest
(docs/data_manifest.md). Equation and page references are to the author copies listed in the references.

### 3.1 Statistics and implementation
- Formulas follow the source papers; every constant is stored with its page (src/pbo/paper_values.py), and a
  page-by-page check of all 52 constants found 45 matches, 0 mismatches and 7 derived values (docs/paper_check.md).
- Test expectations come only from paper examples or independently derived closed forms; 279 tests pass
  (RECOMPUTED, 2026-11-12).
- Modelling choices (ours): PBO counts logit <= 0 (our reading of Sec. 3.1, p.13; Def. 2.2 on p.10 uses rank <
  N/2), so the exchangeable-null reference is 0.5 for N = 100 and 25/49 for N = 49; ties take average ranks;
  Sharpe ratios use ddof 0 and the variance V of trial Sharpes in DSR uses ddof 1; implied N (DSR Eq. 8-9) clamps a
  negative average correlation at 0; the Newey and West (1987) long-run variance uses the Newey and West (1994)
  lag rule int(4 (T/100)^(2/9)), giving 7 lags at T = 1248 and 11 at T = 13,664.

### 3.2 Designs
- **Synthetic (Section 4.3).** N = 100 zero-edge strategies, T = 1248 days (DSR p.9's 1250 trimmed so 16 blocks
  divide it), seed 20261110. Scenarios (our choice): IID Normal; AR(1) phi 0.1, 0.3; generalized autoregressive conditional heteroskedasticity, GARCH(1,1) (0.05, 0.90),
  (0.10, 0.85); Student-t nu 8, 5; one-factor correlation rho 0.3, 0.7. PSR on a fixed, unselected strategy; DSR on
  the best of 100. 2000 datasets for PSR and DSR, 200 for PBO.
- **Real dependence (Section 4.5).** Kenneth French 49 industry portfolios, daily, value weighted, 1971-07-01 to
  2026-09-30 (frozen snapshot, SHA-256 in the manifest), each industry demeaned so the true edge is zero; circular
  block bootstrap (Kunsch 1989; Politis and Romano 1992) of whole days, block length L = 1, 5, 20 (primary), 60;
  T = 1248; PSR on a uniformly drawn industry. Sub-period run: split at 1999-01-01, each industry demeaned within
  its own period, L = 20.
- **Case study (Section 4.6).** Fama-French daily market factor (Mkt-RF, RF); 93 moving-average crossover settings
  (fast 5-50, slow 25-250 days, our choice); long the market when the fast average is above the slow one, otherwise
  flat; costs 0, 5 (main) or 10 basis points per change in position (our choice); 1972-07-18 to 2026-09-30, T =
  13,664. Paired Sharpe-difference test against buy-and-hold on the same days: delta method with a Bartlett HAC
  covariance (Ledoit and Wolf 2008, Eqs. 1-5, with a Bartlett kernel, fixed bandwidth and no T/(T-4) scaling as our
  choices), one-sided, Bonferroni over 93 settings. Robustness checks (Section 4.7): one extra day of execution
  lag; turnover and break-even cost; the paired test by sub-period (split 1999-01-01); the trial count at which
  DSR falls below 0.95; and Hansen's (2005) consistent SPA test applied to Sharpe differences of all 93 settings
  against the market, as Sullivan, Timmermann and White (1999) apply the Reality Check, with a stationary bootstrap
  (Politis and Romano 1994; mean block 20 days, 2000 resamples, seed 20261115; our choices).

### 3.3 Inference and the evidence rule
Rejection counts are tested against the nominal 5% with an exact two-sided binomial test; p-values are
Holm-adjusted within one family per table (synthetic scenarios; French first run; French replicate; sub-periods).
An effect is **detected** if the Holm-adjusted p < 0.05 and **suggestive** if only the unadjusted p < 0.05
(RECOMPUTED, results/manuscript_numbers.txt). Rates carry exact (Clopper-Pearson) 95% intervals; means carry one
Monte Carlo standard error. With 2000 datasets the standard error of a 5% rate is 0.49 percentage points.

### 3.4 What was fixed in advance, and what was not
Designs and predictions were recorded before each run; from the case study on, they were committed to version
control before running. The following choices were made after results were seen and are disclosed as such: the
original evidence rule (|z| bands) and its replacement by the rule above, which changes one verdict (Section 4.5);
the choice of implied N as the lead DSR row; pooling over block lengths (dropped in this revision); the
prediction for the corrected sub-period run, which equals the analytic approximation and was proposed after the
uncorrected result was known (Appendix A). The robustness checks of Section 4.7 were designed before they were run
but have no recorded predictions; they are exploratory.

## 4. Results

### 4.1 Replication
All printed examples are reproduced, consistent with the printed values after accounting for rounded inputs
(RECOMPUTED, tests/; the SF three-year example is checked over the interval of inputs that round to the printed
ones).

**Table 1. Printed examples reproduced.**

| Example | Paper value |
|---|---|
| PSR(0), hedge fund: Normal / with skew and kurtosis / 3 years | 0.982 / 0.913 / 0.953 (PAPER, SF pp.9-10) |
| MinTRL, SR 2 vs SR* 1: daily / weekly / monthly / monthly HFR | 2.73 / 2.83 / 3.24 / 4.99 years (PAPER, SF p.11) |
| DSR, SR 2.5: N = 100 / N = 46; SR0 | 0.9004 / 0.9505; 0.1132 (PAPER, DSR p.10) |
| Expected maximum of N = 10 standard Normals | 1.57 (PAPER, PSEUDO p.9) |
| MinBTL, target Sharpe 1, 5 years | at most 45 configurations (PAPER, PSEUDO p.11) |

The PBO paper prints 12,780 splits for 16 blocks (pp.11, 22); Eq. 2.3 gives C(16, 8) = 12,870. The expected
maximum of five-year annual Sharpe estimates in simulation is 0.688 +/- 0.006, 0.984 +/- 0.005 and 1.119 +/- 0.004
for N = 10, 45, 100 (RECOMPUTED, results/best_of_n.txt), below the PSEUDO Eq. 2.4 values 0.704, 1.000 and 1.132.
The gap is the error of the Eq. 2.4 approximation: exact quadrature gives 0.6882, 0.9873 and 1.1214 (RECOMPUTED,
results/manuscript_numbers.txt), within one Monte Carlo standard error of the simulation.

### 4.2 Selection: PSR versus DSR in an IID search
With 100 zero-edge strategies over five years of daily data (2000 searches; RECOMPUTED,
results/dsr_false_positives.txt), PSR(0) > 0.95 on the best strategy occurs 99.15% [98.64, 99.50] of the time,
because PSR ignores the search. DSR > 0.95 occurs 0.05% [0.00, 0.28] of the time (a closed-form approximation with
V known gives 0.15%), and the mean DSR of the best strategy is 0.488. This is what the 2014 construction implies:
the selected Sharpe is centred near SR0, the expected noise maximum, and DSR measures its distance from SR0 in units
of a single strategy's standard error, which is wider than the spread of the maximum. DSR is therefore a
conservative screen under this null, not a 5% test.

### 4.3 Relaxing one assumption, zero true edge
**Table 2. Rejection rates in % with exact 95% intervals (2000 datasets per cell) and mean PBO +/- one Monte Carlo
standard error (200 datasets). RECOMPUTED, results/calibration.txt.**

| Scenario | PSR(0) > 0.95 | PSR, Newey-West variance | DSR > 0.95, N = 100 | DSR > 0.95, implied N (mean N) | Mean PBO |
|---|---|---|---|---|---|
| IID Normal | 4.95 [4.04, 5.99] | 5.10 | 0.00 [0.00, 0.18] | | 0.520 +/- 0.010 |
| AR(1) phi 0.1 | 6.35 [5.32, 7.51] | 5.30 | 0.10 [0.01, 0.36] | | 0.495 +/- 0.010 |
| AR(1) phi 0.3 | 11.85 [10.47, 13.35] | 7.10 [6.01, 8.31] | 0.70 [0.38, 1.17] | | 0.482 +/- 0.011 |
| GARCH (0.05, 0.90) | 4.70 [3.81, 5.72] | 4.60 | 0.15 [0.03, 0.44] | | 0.481 +/- 0.011 |
| GARCH (0.10, 0.85) | 5.45 [4.50, 6.54] | 5.80 | 0.10 [0.01, 0.36] | | 0.501 +/- 0.011 |
| Student-t nu 8 | 4.35 [3.50, 5.34] | 4.65 | 0.15 [0.03, 0.44] | | 0.511 +/- 0.011 |
| Student-t nu 5 | 4.85 [3.95, 5.88] | 5.20 | 0.05 [0.00, 0.28] | | 0.504 +/- 0.011 |
| Correlated rho 0.3 | 5.35 [4.40, 6.43] | 5.55 | 0.70 [0.38, 1.17] | 1.05 [0.65, 1.60] (70.3) | 0.512 +/- 0.011 |
| Correlated rho 0.7 | 4.95 [4.04, 5.99] | 5.20 | 2.60 [1.95, 3.40] | 5.05 [4.13, 6.10] (30.7) | 0.504 +/- 0.011 |

- **PSR.** Under the rule of Section 3.3, AR(1) phi 0.3 is detected (exact p < 0.0001) and phi 0.1 is suggestive
  (exact p = 0.0075, Holm p = 0.060); no other scenario differs from 5%. For a stationary Gaussian AR(1) at zero
  Sharpe, the sample mean's variance is inflated by F = (1 + phi)/(1 - phi) in large samples (the standard
  long-run variance; cf. Lo 2002), so the rejection rate is 1 - Phi(Phi^-1(0.95)/sqrt(F)): 6.84% at phi 0.1 and
  11.37% at phi 0.3, both inside the simulated intervals (Figure 1).
- **Newey-West.** The HAC variance cuts the phi 0.3 rate to 7.10%, not to 5%. Truncation bias alone, an expected
  Bartlett factor of 1.704 against the true 1.857 at 7 lags, predicts 5.76% (RECOMPUTED,
  results/manuscript_numbers.txt), below the simulated interval; the remainder is consistent with sampling noise in
  the estimated factor. A longer bandwidth, prewhitening or fixed-b critical values were not tried.
- **DSR.** The rate rises with correlation because V is the cross-sectional variance of the trial Sharpes: it
  measures only idiosyncratic dispersion, so SR0 shrinks as correlation rises while the selected strategy still
  carries the common component. Implied N (30.7 at rho 0.7) is the DSR Eq. 9 interpolation evaluated at the
  generating correlation (an interpolation, DSR p.14), not a known true number of independent trials; using it
  raises the rate to 5.05%. Neither row is meant as a 5% test (Section 4.2).
- **PBO.** Mean PBO stays within about 2 standard errors of 0.5 in every scenario, and PBO <= 0.05 accepted a
  zero-edge set at most once in 200 (Student-t nu 8). Because the strategies are exchangeable and no scenario
  creates dependence between in-sample and out-of-sample halves, a mean near 0.5 is guaranteed here; these nulls
  do not stress PBO's mechanism. Time-shuffle controls under GARCH give paired differences of -0.002 +/- 0.004 and
  +0.009 +/- 0.004.
- **PBO with one real edge (exploratory).** In a separate design (T = 992, 20 datasets per cell; RECOMPUTED,
  results/null_checks.txt), one strategy has a fixed daily mean/SD ratio scaled by sqrt(250). Mean PBO is higher
  under AR(1) phi 0.3 than under IID noise (0.391 +/- 0.043 vs 0.189 +/- 0.037 at label 2; 0.098 +/- 0.019 vs
  0.026 +/- 0.007 at label 3), and no change was detected under GARCH. Under AR(1) the same daily ratio is a weaker
  signal at longer horizons (label 2 corresponds to a 250-day summed-return Sharpe of about 1.47), which can account
  for the shift; only mean PBO was measured, not decision power, and 20 skewed values per cell make the
  normal-theory comparison rough.

**Figure 1.** Uncorrected PSR(0) > 0.95 rate under AR(1) with zero true Sharpe, T = 1248. Points: simulation (2000
datasets each) with exact 95% intervals (RECOMPUTED, results/calibration.txt). Dashed line: large-sample rate
1 - Phi(Phi^-1(0.95)/sqrt(F)), an asymptotic approximation (RECOMPUTED, results/psr_ar1_curve.txt). Dotted line:
nominal 5%.

![Figure 1](../results/figure1_psr_ar1.png)

### 4.4 The serial-correlation claim in its literature
Bailey and Lopez de Prado (2012, p.4; also p.8) state, citing Opdyke (2007), that their results hold for
stationary and ergodic returns. Section 4.3 shows that the unchanged Eq. 11 variance over-rejects under stationary
AR(1) dependence at zero Sharpe, and the discrepancy persists as the sample grows. This confirms Ledoit and Wolf
(2008, Remark 3.1) and follows from Lo's (2002) treatment of dependent returns; the chain of the claim is set out in
Section 2. The 2012 paper's IID results, examples and formulas stand.

### 4.5 Real dependence: daily industry returns
**Table 3. PSR(0) > 0.95 on bootstrapped industry returns, zero true edge, T = 1248, 2000 datasets per row.
RECOMPUTED (files given); verdicts by the rule of Section 3.3.**

| Run | Rate, % [exact 95% CI] | Analytic approximation | Exact p | Holm p | Verdict |
|---|---|---|---|---|---|
| Full window, L = 1 (french_bootstrap.txt) | 5.35 [4.40, 6.43] | 4.99 | 0.47 | 0.94 | none |
| Full window, L = 5 | 5.15 [4.22, 6.21] | 5.42 | 0.76 | 0.94 | none |
| Full window, L = 20 | 6.25 [5.23, 7.40] | 5.50 | 0.014 | 0.055 | suggestive |
| Full window, L = 60 | 6.25 [5.23, 7.40] | 5.38 | 0.014 | 0.055 | suggestive |
| Replicate, L = 20 (french_followups.txt) | 5.90 [4.91, 7.02] | 5.50 | 0.072 | 0.090 | none |
| Replicate, L = 60 | 6.00 [5.00, 7.13] | 5.38 | 0.045 | 0.090 | suggestive |
| 1971-1998, centred, L = 20 (g6_corrected.txt) | 8.35 [7.17, 9.65] | 8.37 | < 0.0001 | < 0.0001 | detected |
| 1999-2026, centred, L = 20 | 3.85 [3.05, 4.79] | 3.94 | 0.018 | 0.018 | detected (below 5%) |

- The analytic approximation is our derivation from each industry's circular autocorrelations, averaged over
  industries. Sub-period values include the partial final block; full-window values are as saved before that
  correction, which changes them by at most 0.01 points (L = 60: 5.38 to 5.39).
- On the full 1971-2026 history the excess is at most suggestive. Splitting the history shows why: resampling
  1971-1998, when mean daily lag-1 autocorrelation across industries was +0.157, PSR over-rejects; resampling
  1999-2026 (mean -0.026), it under-rejects. The full-window rate is close to the average of the two (6.1%), so it
  describes a mixture, not either period. In both periods the approximation is within 0.1 percentage points of the
  simulation.
- Removing linear autocorrelation by AR(5) residuals gives 5.30% and 5.35% at L = 20 and 60, and a Newey-West
  variance gives 5.60% and 5.70% (results/french_followups.txt); these change marginal moments and cross-industry
  relationships as well, so they are robustness checks, not isolated interventions. Weekly sums give 4.35%
  [3.50, 5.34], but also change horizon and moments.
- DSR acceptance stays below 5% throughout: 3.05-3.55% with implied N (23.0 to 23.3 for 49 industries) and
  1.25-1.90% with N = 49. Mean PBO is 0.505-0.520 (standard errors 0.012-0.014; reference 25/49 = 0.510), and PBO
  <= 0.05 accepted at most 1 of 200 zero-edge sets. A time-shuffle control gave +0.017 +/- 0.005 at L = 60 in the
  first run but did not replicate (+0.001 +/- 0.004 fixed blocks, -0.001 +/- 0.004 random blocks).
- The pre-1999 autocorrelation is plausibly in part a nonsynchronous-trading effect in portfolio returns (Lo and
  MacKinlay 1990). It is real dependence in the series PSR is applied to, but not necessarily exploitable
  predictability; we did not test the mechanism.

### 4.6 Case study: moving-average timing on the US market
This is an idealized research-factor experiment, not an executable strategy: the market factor is a Center for Research in Security
Prices (CRSP) research portfolio, the signal at the close of day t earns the close-t to close-(t+1) return (a fill at the same close), and
costs are a flat charge per change in position.

**Table 4. Best of 93 settings at 5 bps (RECOMPUTED, results/ma_crossover.txt, results/market_comparison.txt,
results/manuscript_numbers.txt).**

| Measure | Value | What it says |
|---|---|---|
| Best setting (fast 15, slow 225): annual Sharpe vs market | 0.588 vs 0.458 | In-sample advantage of +0.130, selected from 93 |
| PBO (16 blocks) | 0.208 | 20.8% of CSCV splits put the in-sample winner at or below the out-of-sample median; fails the "customary" 0.05 cut-off (PAPER, PBO p.14) |
| DSR, N = 93 / implied N 17.2 | 0.9980 / 0.9994 | Best Sharpe is far above SR0, the zero-skill selection benchmark; not a comparison with the market |
| Paired HAC test vs market, 11 lags | difference 0.130, se 0.099, 95% CI [-0.064, 0.323], raw one-sided p 0.094 | No setting passes Bonferroni over 93; the raw p of a setting chosen as best is itself selection-biased |
| Power of that test | 80% power needs a difference of 0.246 (single test) or 0.406 (Bonferroni); power at 0.130 is 0.37 and 0.025 | The test could not have detected a plausible timing advantage |
| Bandwidth sensitivity | se 0.104 (0 lags), 0.101 (44 lags); raw p 0.105, 0.100 | Same decision |

At 0 and 10 bps the best setting is the same, with PBO 0.240 and 0.193. The DSR near 1 mostly reflects the length
of the sample (54 years of daily data) and the closeness of the 93 settings (small V), which put SR0 near zero; it
says nothing about the market. PBO 0.208 has no reference distribution for this correlated family; in the
exploratory real-edge design of Section 4.3 a planted edge also had mean PBO well above 0.05, so the 0.05 cut-off
rejects real edges too.

### 4.7 Robustness of the case study (exploratory)
**Table 5. Case-study checks at 5 bps, paired tests with 11 lags, annualized (RECOMPUTED,
results/case_study_checks.txt).**

| Check | Result |
|---|---|
| Baseline (signal acts next day) | 15/225: Sharpe 0.588 vs market 0.458; PBO 0.208; DSR 0.9980; difference +0.130, one-sided p 0.094 |
| One extra day of lag | 15/225 still best: Sharpe 0.578; PBO 0.216; DSR 0.9959; difference +0.120, p 0.113; 48 of 93 settings above the market (50 at baseline) |
| Turnover of 15/225 | 72 changes in position in 54.7 years, 1.32 per year |
| Break-even cost | 121 bps per change before its Sharpe falls to the market's |
| 1972-1998 (6,686 days) | Sharpe 0.568 vs 0.500; difference +0.068 (se 0.134), p 0.305 |
| 1999-2026 (6,978 days) | Sharpe 0.606 vs 0.439; difference +0.167 (se 0.140), p 0.117 |
| DSR break-even trial count | DSR falls below 0.95 only near N = 740,000 (V held at its observed value) |
| Hansen SPA, all 93 settings vs market | statistic 1.265, p 0.504 |

The selected rule trades about once a year, so neither costs nor one day of execution delay change the picture,
and its in-sample advantage is larger after 1999 than before, so the stale-price effect of Section 4.5 does not
explain it. DSR would need about 740,000 trials to fall below 0.95: with 54 years of daily data, almost any
positive-Sharpe rule clears the zero-skill benchmark. A test that accounts for the dependence among the 93
settings, rather than Bonferroni, gives the same answer (SPA p 0.50).

Conclusion: the selected rule had a higher historical Sharpe than the market, but the evidence neither
establishes that any of the 93 settings beats it nor that timing skill is absent.

## 5. Discussion
**Table 6. Which statistic for which decision.**

| Decision | Statistic and hurdle | A pass does not imply | Evidence still needed |
|---|---|---|---|
| Is one pre-specified strategy's Sharpe above a hurdle? | PSR(SR*) | Robustness to serial dependence (Sections 4.3, 4.5) | A dependence-robust variance (HAC) or lower-frequency data, checked for the period |
| Is a search winner better than the best of N noise trials? | DSR (2014) | Skill relative to a benchmark; a 5% error rate (Section 4.2) | A defensible N; a benchmark-relative test |
| Do the search's rankings persist out of sample? | PBO | A probability of future failure | A reference distribution for the strategy family |
| Should capital move from the benchmark to the strategy? | None of the above | | A benchmark-relative test with search control (Reality Check, SPA, StepM), power analysis, out-of-sample or walk-forward evidence, costs and capacity |

The case study makes the last row concrete: high selection-adjusted confidence (DSR 0.998) coexists with no
evidence of beating the market, because the two statistics answer different questions. The real-data results
add a practical point for PSR: its error depends on the period's dependence, so one fixed correction factor does
not fit all histories.

## 6. Limitations
- PSR was tested only at SR* = 0; MinTRL under GARCH is untested. Synthetic levels are our choices, not a survey.
- Real-data intervals are Monte Carlo error given one 1971-2026 history; the circular block bootstrap with fixed L
  attenuates dependence at lags below L and removes it beyond L.
- The evidence rule was set after results were seen (Section 3.4); the Monte Carlo design resolves effects of
  about 1 percentage point or more.
- DSR results concern the 2014 construction and the Eq. 9 interpolation; later formulations were not evaluated.
- PBO is a share of overlapping CSCV splits, not a future failure probability, and has no binomial standard error.
  CSCV, like any double-precision implementation, cannot rank strategies whose Sharpe ratios differ below machine
  precision.
- The case study is one market, one strategy family and one grid, with same-close fills. The HAC test is
  asymptotic and requires stationarity, mixing and finite moments that the sub-period results call into question;
  the SPA bootstrap uses one mean block length. The robustness checks of Section 4.7 had no recorded predictions.
- All results are historical; none says how a strategy will perform in the future.

## 7. Conclusion
The replication reproduces every printed example of the source papers. The extensions show that the three
statistics answer different questions and should not be read as interchangeable thresholds. Uncorrected PSR is
reliable only when the returns it is applied to are close to serially uncorrelated; on daily industry returns its
error moves with the period's dependence, in both directions. The 2014 DSR is a conservative screen against a
noise benchmark whose acceptance depends on cross-strategy correlation and on the trial count, not a test against
any investable alternative. PBO behaves as designed under exchangeable nulls, which therefore say little about its
power. A benchmark-relative question needs a benchmark-relative test, and that test should report its power.

## Statements
**Data availability.** Kenneth French Data Library: daily 49 Industry Portfolios and Fama/French research factors,
downloaded 2026-11-12 (202609 CRSP release), identified by SHA-256 in docs/data_manifest.md. The archives are not
redistributed; exact reproduction requires obtaining these snapshots, and the loaders reject any other bytes.
**Code availability.** github.com/Executioner-Cs/pbo-explained, MIT license; results in this version come from
the commit recorded with the release. **Author contributions, funding, conflicts of interest, tool-use
disclosure.** To be completed by the author. **Ethics.** Not applicable: public aggregate data, no human subjects.

## References
Equation and page locators refer to the versions named here. DOIs were resolved through Crossref on 2026-11-12.

1. Bailey, D. H., Borwein, J. M., Lopez de Prado, M., and Zhu, Q. J. (2014). Pseudo-mathematics and financial
   charlatanism: the effects of backtest overfitting on out-of-sample performance. *Notices of the American
   Mathematical Society* 61(5), 458-471. doi:10.1090/noti1105. Author copy of April 1, 2014.
2. Bailey, D. H., Borwein, J. M., Lopez de Prado, M., and Zhu, Q. J. (2017). The probability of backtest
   overfitting. *Journal of Computational Finance* 20(4). doi:10.21314/JCF.2016.322. Author copy of February 27, 2015.
3. Bailey, D. H., and Lopez de Prado, M. (2012). The Sharpe ratio efficient frontier. *Journal of Risk* 15(2),
   3-44. doi:10.21314/JOR.2012.255. Author copy of July 2012.
4. Bailey, D. H., and Lopez de Prado, M. (2014). The deflated Sharpe ratio: correcting for selection bias,
   backtest overfitting, and non-normality. *Journal of Portfolio Management* 40(5), 94-107.
   doi:10.3905/jpm.2014.40.5.094. Author copy of July 31, 2014.
5. Brock, W., Lakonishok, J., and LeBaron, B. (1992). Simple technical trading rules and the stochastic properties
   of stock returns. *Journal of Finance* 47(5). doi:10.1111/j.1540-6261.1992.tb04681.x.
6. Christie, S. (2005). Is the Sharpe ratio useful in asset allocation? MAFC Research Paper, Macquarie Applied
   Finance Centre. SSRN 720801.
7. Hansen, P. R. (2005). A test for superior predictive ability. *Journal of Business and Economic Statistics*.
   doi:10.1198/073500105000000063.
8. Harvey, C. R., and Liu, Y. (2014). Evaluating trading strategies. *Journal of Portfolio Management* 40(5).
   doi:10.3905/jpm.2014.40.5.108.
9. Harvey, C. R., and Liu, Y. (2015). Backtesting. *Journal of Portfolio Management* 42(1).
   doi:10.3905/jpm.2015.42.1.013.
10. Harvey, C. R., Liu, Y., and Zhu, H. (2016). ... and the cross-section of expected returns. *Review of Financial
    Studies* 29(1). doi:10.1093/rfs/hhv059.
11. Jobson, J. D., and Korkie, B. M. (1981). Performance hypothesis testing with the Sharpe and Treynor measures.
    *Journal of Finance* 36(4). doi:10.1111/j.1540-6261.1981.tb04891.x.
12. Kunsch, H. R. (1989). The jackknife and the bootstrap for general stationary observations. *Annals of
    Statistics* 17(3). doi:10.1214/aos/1176347265.
13. Ledoit, O., and Wolf, M. (2008). Robust performance hypothesis testing with the Sharpe ratio. *Journal of
    Empirical Finance* 15(5), 850-859. doi:10.1016/j.jempfin.2008.03.002. Locators from University of Zurich
    Working Paper 320 (January 2008), checked by text inspection.
14. Lo, A. W. (2002). The statistics of Sharpe ratios. *Financial Analysts Journal* 58(4), 36-52.
    doi:10.2469/faj.v58.n4.2453.
15. Lo, A. W., and MacKinlay, A. C. (1988). Stock market prices do not follow random walks: evidence from a simple
    specification test. *Review of Financial Studies* 1(1). doi:10.1093/rfs/1.1.41.
16. Lo, A. W., and MacKinlay, A. C. (1990). An econometric analysis of nonsynchronous trading. *Journal of
    Econometrics* 45. doi:10.1016/0304-4076(90)90098-E.
17. Lopez de Prado, M., and Lewis, M. J. (2018). Detection of false investment strategies using unsupervised
    learning methods. SSRN. doi:10.2139/ssrn.3167017.
18. Lopez de Prado, M., Lipton, A., and Zoonekynd, V. (2026). Sharpe ratio inference: a new standard for decision
    making and reporting. *Journal of Portfolio Management* 52(6). doi:10.3905/jpm.2026.1.837. Abstract only.
19. Lopez de Prado, M., and Porcu, E. (2026). The deflated Sharpe ratio: a unified framework for search-adjusted
    performance inference. *Journal of Portfolio Management* 53(1), 70-120. doi:10.3905/jpm.2026.070. Abstract
    only.
20. Memmel, C. (2003). Performance hypothesis testing with the Sharpe ratio. *Finance Letters* 1, 21-23.
21. Mertens, E. (2002). Variance of the IID estimator in Lo (2002). Working paper, University of Basel.
22. Newey, W. K., and West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation
    consistent covariance matrix. *Econometrica* 55(3). doi:10.2307/1913610.
23. Newey, W. K., and West, K. D. (1994). Automatic lag selection in covariance matrix estimation. *Review of
    Economic Studies* 61(4). doi:10.2307/2297912.
24. Opdyke, J. D. (2007). Comparing Sharpe ratios: so where are the p-values? *Journal of Asset Management* 8(5),
    308-336. doi:10.1057/palgrave.jam.2250084. Locators from the preprint.
25. Pav, S. E. (2021). *The Sharpe Ratio: Statistics and Applications*. CRC Press. doi:10.1201/9781003181057.
26. Politis, D. N., and Romano, J. P. (1994). The stationary bootstrap. *Journal of the American Statistical
    Association* 89(428). doi:10.1080/01621459.1994.10476870.
27. Politis, D. N., and Romano, J. P. (1992). A circular block-resampling procedure for stationary data. In
    *Exploring the Limits of Bootstrap*, Wiley. (UNVERIFIED: page range and DOI not checked.)
27. Romano, J. P., and Wolf, M. (2005). Stepwise multiple testing as formalized data snooping. *Econometrica*
    73(4). doi:10.1111/j.1468-0262.2005.00615.x.
28. Sullivan, R., Timmermann, A., and White, H. (1999). Data-snooping, technical trading rule performance, and the
    bootstrap. *Journal of Finance* 54(5). doi:10.1111/0022-1082.00163.
29. White, H. (2000). A reality check for data snooping. *Econometrica* 68(5). doi:10.1111/1468-0262.00152.

## Appendix A. Correction history
The repository keeps every original result file. Corrections made after an internal audit and review:
- **Sub-period comparison.** The first sub-period run resampled each period without re-centring it; industry
  means were then not zero (36 of 49 positive in 1971-1998, 13 of 49 in 1999-2026), and its rates (10.45%, 3.30%)
  mixed mean differences with dependence. It was withdrawn and rerun with each period centred, with the same
  random streams (Table 3). The prediction recorded for the rerun equals the analytic approximation and was
  proposed after the uncorrected result was known; only its direction is a test, and the close agreement is a
  model check. The audit was triggered by the failed check of the first run.
- **AR(1) phi 0.1.** First reported as detected; under the recorded rule it is suggestive.
- **PBO with a real edge.** First described as reduced power; only mean PBO was measured, and the edge convention
  explains part of the shift (Section 4.3).
- **Implied N.** First described as a true number of trials; it is the Eq. 9 interpolation.
- **Pooling.** A pooled rate over block lengths (5.88%, z = 3.14), chosen after the run, was dropped.
