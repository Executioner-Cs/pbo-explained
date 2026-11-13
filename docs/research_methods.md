# Methods and estimands supplement

Status: working-paper methods specification, 2026-11-12. Corrected G6 has run (results/g6_corrected.txt). Paper formulas are distinguished from numerical implementation choices and
extensions performed in this repository. This document does not establish priority over the literature.

## 1. Observation unit and Sharpe estimand

Returns are decimal excess returns over the risk-free rate at their original observation frequency. For each
series, the point estimate is sample mean divided by sample standard deviation, with ddof=0 (our convention).
Skewness and raw kurtosis use SciPy's default biased standardized central-moment estimators, with
kurtosis(fisher=False). Raw Normal kurtosis is 3. These are distributional moments, not annualized inputs.

For display only, daily marginal Sharpes are multiplied by sqrt(250), using DSR working paper p.10's calendar
convention (PAPER). This is not generally the Sharpe of an annual-horizon return sum under serial dependence.
For stationary daily returns, the variance of the q-day sum contains lagged covariance terms. Holding daily
mean/SD fixed while changing those terms changes the horizon-level signal-to-noise ratio. No comparison here
is claimed to hold both quantities constant. Compounded holding-return Sharpe is a further distinct estimand.

## 2. PSR, MinTRL and the original DSR construction

PAPER: Bailey and Lopez de Prado, *The Sharpe Ratio Efficient Frontier*, July 2012 working copy, p.9 Eq.11:

    z = (SR_hat - SR_star) sqrt(T-1) / sqrt(A),
    A = 1 - skew_hat SR_hat + (kurt_hat-1) SR_hat^2 / 4,
    PSR = Phi(z).

This is an asymptotic Normal inference score. It is not, without a Bayesian model and prior, a posterior
probability that a strategy has skill. In the calibration study the fixed strategy is chosen independently
of its observed performance, SR_star=0, and the reported decision is PSR>0.95.

PAPER: MinTRL is the inversion in SF p.11 Eq.13. No dependent-return calibration of MinTRL is claimed.
PAPER: the DSR calculation replicates Bailey and Lopez de Prado's July 2014 working copy, p.8 Eq.2:

    SR0 = sqrt(V) expected_max_normal(N),
    DSR = PSR evaluated at SR_star=SR0.

The selected series maximizes full-sample marginal Sharpe. V is estimated as the cross-sectional sample
variance of per-period candidate Sharpes (ddof=1, our choice). Expected maximum uses the published Normal-max
approximation, not exact integration. DSR is evaluated both with the enumerated candidate count and, where
reported, the Eq.9 interpolation N=rho+(1-rho)M. Here rho is mean off-diagonal return correlation; negative
estimates are clamped to zero (our choice). Recovering that interpolation's generating-correlation value is
not validation of a true independent-trial count. The approximation does not support N<2 in this implementation.
Numerical domain checks use a relative 1e-12 tolerance at the Pearson skew/kurtosis bound and allow correlation
matrix eigenvalues down to -1e-10 times matrix dimension for roundoff (our numerical choices). Singular valid
correlations are accepted even though applying the expected-maximum approximation at N=1 remains unsupported.

Only this original location-benchmark construction is implemented. The later DSR framework of Lopez de Prado
and Porcu (2026) distinguishes location, location-scale and full-search-distribution approaches; its indexed
abstract and publication metadata have been consulted, not its full proofs. No result in this study establishes
the operating characteristics of those later alternatives.

## 3. CSCV/PBO and what is not measured

PAPER: PBO working copy dated February 27, 2015, Algorithm 2.3 pp.11-12 and Section 3.1 p.13. Partition the
chronological T-by-N return matrix into S equally sized contiguous blocks; enumerate all halves of the blocks.
For each split, select the highest in-sample Sharpe and rank it on the complementary observations. For rank r
with 1 worst, use omega=r/(N+1), then logit log(omega/(1-omega)).

Our implementation counts logits<=0 and uses average OOS ranks for ties; IS argmax ties select the first column.
The paper's strict-rank definition and integral endpoint differ, so this convention is explicit. With continuous,
exchangeable strategies and independent IS/OOS halves, the expected fraction is 1/2 for even N. The odd-N
25/49 quantity used for industries is a reference; the heterogeneous industries need not be exchangeable.

PBO is a conditional fraction of overlapping splits, not a future-failure probability. Individual splits do
not form independent Bernoulli trials. Monte Carlo SEs in this study are computed across separately generated
datasets, not across overlapping splits. G4 reports changes in mean PBO under a planted signal. Neither
threshold-decision power nor the probability of identifying the planted strategy was measured there.

## 4. Controlled synthetic designs

RECOMPUTED settings and modeling choices: experiments/calibration.py and results/calibration.txt. N=100,
T=1248, S=16; 2000 datasets per scenario for PSR/DSR and 200 for PBO; root seed 20261110. Candidate columns have
zero unconditional means. Independent spawned streams separate scenarios and shuffled controls.

- IID baseline: independent standard Normal returns.
- AR(1): stationary Normal marginals with unit variance, phi in {0.1,0.3}; initial state drawn from the stationary
  Normal law, innovations scaled by sqrt(1-phi^2). Serial predictability remains even though each fixed column's
  unconditional mean is zero.
- Gaussian GARCH(1,1): (alpha,beta) in {(0.05,0.90),(0.10,0.85)}, intercept 1-alpha-beta. A 500-step burn-in from
  unit variance is an approximation to stationary initialization (our choice). Volatility clustering and
  unconditional fat tails change together; the comparison is not an isolated clustering intervention.
- Student-t: degrees of freedom in {8,5}, scaled to unit variance, independent across time and candidates.
- Equicorrelated Normal columns: rho in {0.3,0.7}, implemented as a common factor plus independent residuals.
- Paired shuffle controls use one common row permutation, preserving contemporaneous cross-sections and
  empirical marginal distributions while altering time order. PSR/DSR are permutation invariant; PBO can change.

G4 uses the separate settings in experiments/null_checks.py: T=992, N=100, S=16 and 20 datasets per signal cell.
Its marginal daily signal is fixed across noise conditions. Its q-scaled labels do not fix annual-horizon Sharpe.
The limited number of datasets and mean-only output do not justify a general power comparison.

## 5. Real-data conditional nulls and correction history

The exact ZIP identities, dates, source URLs and transformations are listed in [data_manifest.md](data_manifest.md).
For the full-window bootstrap, each industry is demeaned once over the observed window. Conditional on that
empirical source distribution, circular row resampling has zero expected mean per industry. This is a constructed
null; it does not establish that the original economic population had zero expected returns.

Whole-day rows preserve contemporaneous relationships. Fixed-length circular blocks preserve within-block
sequences, attenuate dependence at boundaries, and destroy long regimes. The resampled process is not strictly
stationary across fixed block positions. Block lengths {1,5,20,60}, primary 20, are modeling choices. Bootstrap
Monte Carlo CIs are conditional on this source history and construction; they do not quantify uncertainty over
alternative histories, model selection or regime specification.

Original G6 sliced the globally demeaned history without centering each slice. Its simulated populations did
not satisfy the zero-mean null. The old rates are retained as historical outputs and their calibration attribution
is withdrawn. Corrected G6 centers each industry independently within each date-defined period, keeps the
original child seeds 9 and 10 from SeedSequence(20261113).spawn(11), and writes a new result file. The design
were committed before that run (d78d8e8); the prediction equals the analytic approximation and was proposed
after the uncentred result was known. Result: 1971-98 8.35% [7.17, 9.65], 1999-2026 3.85% [3.05, 4.79].

AR residuals (G2) and arithmetic five-day aggregation (B) are robustness checks with multiple simultaneous
changes. Their results do not isolate an autocorrelation intervention.

## 6. Analytic approximation and variance correction

DERIVATION, independently worked out from the Gaussian AR(1) mean variance and the delta method:
at zero true Sharpe, the limiting variance inflation is F=(1+phi)/(1-phi). The corresponding large-sample
rejection-rate approximation is 1-Phi(Phi_inverse(0.95)/sqrt(F)). This is the dashed curve in Figure 1.
Ledoit-Wolf (2008), Remark 3.1, already identifies the underlying omitted-dependence problem in Opdyke's
stationary-time-series formulas; this study does not claim discovery of that problem.

For finite sample-mean variance use F_T=1+2 sum_(h=1)^(T-1) (1-h/T)phi^h. Substitution into a Normal law remains
an approximation to PSR rejection, because estimated variance and higher moments are random. Similarly, for
bootstrap length T=qL+r, independent block sums give the exact conditional mean-variance factor
(q L F_L+r F_r)/T, with circular autocovariances. Exact mean variance does not make the later PSR tail calculation exact.

The Newey-West diagnostic estimates a Bartlett long-run variance factor for the return mean. At the tested
zero-Sharpe null this supplies the leading asymptotic variance term. It is not asserted to be a general nonzero-
Sharpe correction. The finite z-statistic is retained before dividing by sqrt(F), avoiding probability saturation.
The bandwidth rule int(4*(T/100)^(2/9)) is a modeling choice; its finite-sample adequacy is not guaranteed.

## 7. Idealized factor-index case study and paired inference

The signal index compounds market excess return plus RF. Each setting holds the market or RF, uses the preceding
close's MA signal, and pays cost times absolute position change. Earning the entire next close-to-close return
assumes a fill at the close just observed. No real-time executable instrument, auction-fill mechanism or point-in-
time availability of the revised research factor has been established. The case study is a statistical illustration.

For strategy-minus-market Sharpe, the paired HAC implementation derives the influence of each series from
Ledoit-Wolf (2008), January working paper p.4 Eqs.1-5. With z_t=(r_t-mean)/sd and S=mean/sd, its influence is
h_t=z_t-S*(z_t^2-1)/2. Center q_t=h_strategy,t-h_market,t; estimate its long-run covariance with Bartlett weights.
The variance of the estimated Sharpe difference is the weighted covariance sum divided by T. This retains all
mean/variance cross-covariances. Our choices differ from the paper's simulated implementation: Bartlett kernel,
fixed finite bandwidth and no T/(T-4) scaling. The annual display factor multiplies both difference and SE.

The primary comparison uses 11 lags and all 93 settings at 5 bps; 0 and 44 lags are sensitivities only. One-sided
p-values use the Normal tail; adjusted p=min(1,93*p). Bonferroni requires no independence between candidate tests,
but cannot repair invalid marginal p-values. HAC validity requires suitable stationarity, mixing, finite moments
and bandwidth growth. These conditions have not been established for the long market history.

## 8. Uncertainty, decisions and scope of contribution

Rate CIs use Clopper-Pearson intervals across independent Monte Carlo datasets. Mean SEs use the sample SD divided
by sqrt(dataset count). These intervals do not include data-source or structural uncertainty. The evidence rule
in PROGRESS.md was completed after the calibration run; the study must not be described as preregistered.
Predictions and recorded designs provide a chronology, not a registry-backed preregistration claim.

The contribution is a source-traceable implementation, a specified calibration grid, conditional dependence
experiments, and an explicit comparison between search-adjusted zero-skill inference and market-benchmark inference.
No new PBO/PSR/DSR statistic, first serial-correlation correction, general calibration theorem, or profitable
executable strategy is claimed. A complete assessment of later Sharpe/DSR formulations and immutable data
provisioning remain publication tasks.
