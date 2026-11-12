# Step 5 implementation review, 2026-11-12

Scope: paired Sharpe inference, crossover matrix preparation, experiment imports/reporting, called library
boundaries, and the recorded design. The real market-comparison follow-up has not run. The existing step 5
prediction, 11-lag primary analysis, 0/44-lag sensitivities, 93-setting family, and costs are unchanged.

## Mathematical and source check

PAPER: Ledoit and Wolf (2008), *Robust performance hypothesis testing with the Sharpe ratio*, Journal of
Empirical Finance 15(5), 850-859, DOI 10.1016/j.jempfin.2008.03.002. Read the online January working paper,
printed p.4 Eqs.1-5 and Section 3.1 pp.4-5:
https://www.econ.uzh.ch/apps/workingpapers/wp/iewwp320.pdf
This was text inspection, not a new visual audit of every local source PDF.

DERIVATION (not a formula quoted from the paper): for standardized return z=(r-mu)/sigma and S=mu/sigma,
projecting the paper's mean/mean-square gradient gives influence h=z-S*(z^2-1)/2. For paired returns,
q=h_x-h_y. Centering q and applying Bartlett lag weights gives

    SE^2 = [sum(q_t^2) + 2 sum_h (1-h/(L+1)) sum_t q_t q_(t-h)] / T^2.

This scalar projection retains all cross-covariances and replaces the four-dimensional matrix calculation.
Computing variance from centered observations and normalizing columns by powers of two avoids raw
second-moment cancellation and raw-scale fourth-power overflow. Identical influences cancel before HAC.
Our choices remain Bartlett weights, no T/(T-4) adjustment, and rule-derived lag count at this sample size.
HAC inference still requires suitable stationarity, moments, dependence, and bandwidth assumptions.

RECOMPUTED (deterministic tests, independently derived expectations): a four-observation paired fixture gives SE=sqrt(1/2) at L=0 and SE=1/2 at L=1.
A 36-observation equal-weight Cartesian quadrature has Normal moments through degree four exactly; it
replaces two sampled 200,000-observation Normal tests. The nonzero-Sharpe correlated case includes all
cross terms. Additional regressions cover large means, extreme return scaling, and proportional returns.

## Changes and checks

- Shared crossover-panel preparation owns common warm-up/block trimming. Positions and trading costs are
  formed before trimming; entry costs are not spuriously restarted at the retained sample boundary.
- Both experiment modules import independently. No experiment imports another experiment for configuration.
  Small explicit grid declarations are retained as design settings, not outcome-dependent constants.
- Synthetic reporting checks exercise 93 settings, primary/sensitivity order, independent p=1/2 expectations,
  captured persistence, and refusal to save invalid zero-SE inference. No real follow-up observations are used.
- Sharpe and MinBTL public boundaries reject malformed/nonfinite inputs. Normal survival quantiles avoid
  cancellation in the expected-maximum approximation for very large finite trial counts.
- Market loading rejects an empty/incomplete frozen calendar and missing columns before indexing.
- Statements that intervals containing 5% prove calibration is corrected were weakened. PSR over-rejection
  is distinguished from changes in DSR acceptance rates, which remained below 5% in the reported AR cells.
- No fitted outcome constants, response-dependent grids, or copied result expectations were found in the
  step 5 implementation. Hashes, sample schema, seeds, and parameter settings are documented design inputs.

Historical calibration experiments were not rerun or structurally rewritten. This review does not establish
future performance, exact finite-sample HAC calibration, or a new visual verification of all paper constants.

## Verification

RECOMPUTED: 151 focused tests and 224 full-suite tests passed. Both experiment imports are covered by tests.
The original MA experiment reproduced its saved text exactly with saving disabled; no raw result was changed.
The market-comparison follow-up was exercised only with synthetic data and a stubbed statistic, never with
its real data/statistic combination. Its result file remains absent. No staging or commits were performed.
