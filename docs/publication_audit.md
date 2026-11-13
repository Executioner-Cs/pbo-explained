# Adversarial publication audit

Date: 2026-11-12. Verdict: not ready for publication without substantive corrections.
Scope: statistical estimands, simulation nulls, implementation boundaries, manuscript claims, source provenance,
execution assumptions and independent reproduction. Existing outputs were preserved. No production code was changed.

RECOMPUTED: the existing suite passes all 224 tests. A separate audit file, tmp/test_publication_probes.py,
contains nine independently specified invariant/domain checks; all nine fail on the reviewed tree. That file is
intentionally outside tests/ and is not part of the ordinary suite. A green existing suite did not establish that
all simulated populations satisfied their stated null hypotheses.

## 1. High: G6 does not test the stated zero-edge null

Locations: experiments/french_followups.py:108,137,164-167; docs/writeup.md:114-115,139-140.

The loader demeans each industry over the full history. Slicing this history into early/late periods does not
preserve zero means in either period. G6 resamples those slices unchanged, whereas its predicted rejection rate
uses centered autocorrelations and assumes zero Sharpe. The simulated and predicted populations differ in mean.

RECOMPUTED on the frozen snapshot, using the actual 1999-01-01 split:

- Early: 36 of 49 industry means positive; average conventional annualized Sharpe across industries +0.04543;
  individual values range from -0.23947 to +0.37655.
- Late: 13 of 49 means positive; average -0.04041; range -0.29985 to +0.15054.
- Every subperiod industry mean is nonzero; full-window means are approximately zero.

The saved 10.45% versus 3.30% rates are observed rejection rates under mixed nonzero means, not clean estimates
of false-positive rates under two zero-edge populations. They cannot isolate a dependence/period effect.
This does not invalidate the full-window demeaned bootstrap or the synthetic AR(1) counterexample.

Required: preserve the original G6 output, withdraw its zero-edge attribution, and prepare a separate corrected
G6 run that demeans each industry separately within each period. Record the prediction/design before running.
The current step 4 completion and manuscript review records need an explicit correction, not silent rewriting
of the experiment's history.

## 2. High: statistical power was not measured

Locations: experiments/null_checks.py:69-77; docs/writeup.md:87-90,142; PROGRESS.md G4 section.

G4 records mean PBO, its Monte Carlo SE, minimum and maximum. It does not record the probability of accepting
at PBO <= 0.05 with a real edge, or the probability of selecting the planted strategy. An increase in mean PBO
alone does not imply lower decision power.

Independent counterexample: a constant PBO of 0.1 has acceptance probability zero at threshold 0.05. PBO zero
with probability 0.8 and one otherwise has a higher mean, 0.2, but acceptance probability 0.8.

Required: report the measured mean-PBO response without calling it power. Alternatively prerecord a decision-power
metric and report its rate/uncertainty. No additional experiment is required merely to narrow the existing claim.

## 3. High for durable reproducibility: hashes do not supply the frozen inputs

Locations: src/pbo/french.py:51-64; .gitignore; tests/test_french_loader.py:65.

The code downloads a rolling current ZIP and demands the frozen hash. The snapshot itself is ignored and there
is no immutable acquisition/provisioning route. Once upstream bytes change, the hash correctly detects a mismatch
but cannot recover the original dataset. The real-data integration check skips when that ignored file is absent.
No claim is made here that the current upstream ZIP already mismatches.

Source: the official French Data Library describes source-format changes, data revisions and historical archives:
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

Required: a durable permitted snapshot location or exact immutable provisioning procedure, a data manifest, and
fresh-clone reproduction instructions/checks. Keep hash enforcement. The repository also lacks a tracked README,
software license and CI configuration; these are dissemination gaps rather than proof of incorrect calculations.

## 4. Medium: the manuscript does not apply its own evidence rule

Locations: PROGRESS.md:37-39; docs/writeup.md:81.

The recorded rule distinguishes suggestive evidence (absolute z between 2 and 3) from detected effects (z at least
3 or within-table Bonferroni significance). The manuscript calls both AR(1) cases detected.

RECOMPUTED for the phi=0.1 PSR cell, 127/2000 versus 0.05:
null z=2.77014; exact two-sided binomial p=0.00753529; Bonferroni over nine scenarios p=0.06781765.
This is suggestive under the recorded rule. The phi=0.3 finding is much stronger.

Required: reconcile the language with that rule and disclose that the decision rule was completed after the run.
An unadjusted confidence interval excluding 5% is not the same decision as the declared table-wise rule.

## 5. Medium: annual-horizon signal strength changes in G4

Locations: experiments/null_checks.py:28,59,65,73; docs/writeup.md:89-90.

G4 holds the marginal daily mean/SD ratio fixed, scaled by sqrt(250), while changing autocorrelation. That is a
conventional annualized marginal Sharpe, not the Sharpe of 250-day summed returns under dependence.

RECOMPUTED: at phi=0.3, the finite 250-day variance inflation is 1.8522449. A setting labeled annual SR=2 then
has summed-return Sharpe 1.46954, versus 2 under IID. Both marginal signal and dependence are defined correctly,
but this is not a comparison holding annual-horizon signal-to-noise fixed.

Required: label the convention and the unintended horizon effect. Do not use this comparison alone to claim that
PBO fails at detecting an otherwise identical annual-horizon edge.

## 6. Medium: effective trial count is a heuristic, not known ground truth

Locations: PROGRESS.md:70; src/pbo/psr_dsr.py:103-120; experiments/calibration.py implied-N interpretation.

PAPER: DSR Appendix 3, printed p.14 Eq.9, interpolates between endpoint correlations; p.15 discusses limitations.
The implementation faithfully reproduces that interpolation. Recovering 30.715 when its input-correlation formula
gives 30.7 validates estimation of that formula, not a true independent-trial count or maximum correction.
Source: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf

DERIVATION: for X_i=sqrt(rho)Z_0+sqrt(1-rho)Z_i, the expected maximum is sqrt(1-rho) times the IID expected maximum.
RECOMPUTED by independent Normal-density quadrature: with 100 trials and rho=0.7 that expectation is 1.37347;
using cross-sectional variance 0.3 and interpolated N=30.7 in the implemented approximation gives 1.14084.
These are standardized Normal-max quantities, not newly simulated trading Sharpe results.

Required: replace 'true 30.7' with 'the Eq.9 interpolation evaluated at the generating correlation'. Do not infer
that the heuristic correction is validated by recovering its own formula. This is not an assertion that DSR must
have an exact simultaneous 5% error rate; the repository already correctly notes the absence of such a theorem.

## 7. Medium: probability saturation defeats the Newey-West correction

Location: src/pbo/psr_dsr.py:96-100.

RECOMPUTED synthetic counterexample:

    psr_long_run(psr(0.1, 0, 10000), 100) -> 1.0

The original CDF rounds to one; its inverse is infinite. Correcting the original finite z-statistic gives
0.840729 instead. Passing through a rounded probability discards information the correction needs.

Required: preserve the z-statistic or original inputs through the variance correction. Add a regression test.
UNVERIFIED: whether this changes any saved acceptance flags; no such effect has been established in this audit.

## 8. Medium: finite-mean-variance corrections are not exact PSR probabilities

Locations: src/pbo/psr_dsr.py:60-78; results/calibration.txt analytic-rate labels.

The finite-T branch uses an exact sample-mean variance factor inside an asymptotic Normal approximation.
It does not integrate over the random sample standard deviation or estimated skewness/kurtosis.

Independent counterexample for supplied Normal moments: at T=2, the PSR z-statistic is
SR/sqrt(1+SR^2/2), bounded by sqrt(2), below the 95% Normal cutoff. Its rejection probability is zero.
RECOMPUTED: the helper instead returns 0.0100046 at phi=0,T=2.
The actual plug-in-moment implementation at two observations is a different statistic, not this supplied-moment case.

Required: label the finite branch an approximation using finite-sample mean variance. The figure's large-sample
label is already appropriate. Do not test this approximation as an exact finite-sample Sharpe law.

## 9. Medium: the predicted bootstrap variance ignores the partial final block

Locations: src/pbo/scenarios.py:92-105; experiments/french_followups.py:59-61.

The documented factor is exact only for complete blocks. T=1248 is not divisible by L=5,20,60.
If T=qL+r, the correct factor for the mean is (qL F_L + r F_r)/T, since independently sampled blocks add variances.
For source [+1,-1], L=2, T=3, F_L=0 but the full block plus one final observation has factor 1/3, not zero.

RECOMPUTED for the actual full-window panel: correcting the partial-block mean variance changes the predicted
rate by -0.0000745, -0.0009264 and +0.0056389 percentage points at L=5,20,60 respectively. This error is small
here; it is not evidence that the main observed rejection rates are invalid.

Required: implement the remainder weighting or explicitly label the full-block approximation at the caller.
The subsequent Normal approximation remains an approximation after this variance correction.

## 10. Medium: controls change more than their attribution claims

G2, src/pbo/french.py:40-51 and experiments/french_followups.py:129,136:
per-industry fitted AR filters change marginal moments and cross-industry relationships. OLS orthogonality to
lagged regressors does not guarantee residual autocorrelations vanish at every fitted lag. The docstring's
'keeps everything else' claim is false. Describe G2 as a residual-series robustness check, not an isolated intervention.

Weekly B, experiments/french_followups.py:7,109-111,133:
keeping 1248 observations changes represented horizon from 1248 days to 6240 days, also changes marginal moments,
and uses arithmetic five-day sums rather than compounded holding returns. Describe these simultaneous changes;
'only frequency changed' is false. Changing the weekly definition would require a documented new result.

## 11. Medium: lagged indexing does not establish executable timing performance

Locations: src/pbo/strategies.py:21-33; docs/writeup.md:119-134.

The signal from close t earns the entire close-t to close-t+1 return, assuming execution at the same close just
observed. The no-lookahead test checks array causality, not a feasible closing fill or real-time data availability.
The underlying French market is a CRSP research portfolio, not an identified executable instrument:
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html

Required: explicitly call this an idealized factor-index experiment with same-close fills and simplified costs.
Do not silently add a trading lag, change the return series or imply the old statistics would remain the same.
An implementable strategy claim needs a separate execution/proxy design.

## 12. Medium/low: validated boundaries and exact-replication wording overstate coverage

RECOMPUTED API counterexamples, also captured in the separate audit probes:

- sharpe(np.array([1,2,3])*1e200,250) returns zero; at scale 1e-200 it returns infinity. The exact invariant value is sqrt(1500).
- implied_n accepts off-diagonal correlations above one and asymmetric matrices; one impossible input returns zero.
- newey_west_factor([1,NaN,3],1) returns NaN instead of a domain error.
- psr accepts a negative raw kurtosis when its computed denominator happens to stay positive.
- cscv on an empty (0,2) matrix raises IndexError instead of a specific ValueError.
- The older french_followups module still has a bare sibling import, so package import fails although its documented
  direct-script command works. Reporting helpers also accept nonboolean rate inputs without rejecting them.

Location docs/writeup.md:42: 'All printed examples ... to printed precision' is too strong. The three-year SF
example requires the input-rounding interval explicitly used by tests/test_psr_dsr.py:18-48; the direct central
printed-input plug-in rounds differently. Say 'consistent after accounting for rounded inputs'.

Required: tests first, consistent domain checks, stable Sharpe computation, precise wording. Not every bad-input
case affects the frozen valid-input experiments; distinguish library reliability from scientific conclusions.

## Repair order and correction design

1. Reopen the scientific review of G6 and affected manuscript claims. Preserve old outputs and their provenance.
2. Correct claims that need no rerun: measured PBO versus power, significance-rule verdicts, interpolation truth,
   annualization convention, execution idealization, control scope and rounded-input replication.
3. Add the failing invariant/domain tests to the ordinary suite as the corresponding bugs are fixed. Keep statistical
   corrections on z/raw inputs, and test block-remainder covariance against a hand-worked finite population.
4. Prepare a corrected G6-only experiment: same frozen dates, split, T=1248, L=20, 2000 datasets, random target
   selection, and the original two G6 child seeds. Independently demean all columns within each period before
   resampling. Compare to the appropriately labeled zero-mean approximation; retain raw counts and exact CIs.
   Unit-test each intended bootstrap population's mean before any simulation. Use a new result file with a clear
   correction link to the original; do not overwrite french_followups.txt. Record the owner's prediction first.
5. Audit any saved outputs affected by numerical fixes before changing their claims. Regenerate only affected
   analyses, with fixed settings and explicit reasons, preserving the original evidence.
6. Provide immutable input acquisition and fresh-clone instructions, then repeat the manuscript review. Revisit
   completed roadmap/sign-off entries transparently. No commit, push, or fresh publication approval is implied here.
