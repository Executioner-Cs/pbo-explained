# Evidence audit

Claim-by-claim provenance for `research-paper.tex`. Status labels:

- **REPRODUCED**: the producing script was rerun on 2026-11-12 in an isolated copy and its output matched the archived
  file byte for byte (or differed only as noted).
- **PAPER**: value printed in a source paper; checked against the rendered page in `docs/paper_check.md` and by a unit test.
- **ANALYTIC**: closed form evaluated in code or by hand in this audit.
- **POST HOC**: computed after the results it summarizes were known.
- **EXPLORATORY**: no recorded prediction.

## Replication

| Claim | Experiment | Source code | Output | Status |
|---|---|---|---|---|
| Selected numerical examples only (Table 3), not every printed illustration. PSR 0.982 / 0.913 / 0.953; MinTRL 2.73 / 2.83 / 3.24 / 4.99 | unit tests | `src/pbo/psr_dsr.py`, `tests/test_psr_dsr.py` | test suite (285 pass) | PAPER (SF pp.9-11); 0.953 checked over the rounded-input interval |
| DSR 0.9004 / 0.9505; SR0 0.1132 | unit tests | `psr_dsr.dsr`, `sr0` | test suite | PAPER (DSR p.10) |
| E[max of 10] = 1.57; MinBTL 45 configs in 5 years | unit tests | `src/pbo/minbtl.py`, `tests/test_minbtl.py` | test suite | PAPER (PSEUDO pp.9, 11) |
| C(16,8) = 12,870, paper prints 12,780 | unit test | `cscv.splits` | test suite | ANALYTIC; typo noted in `paper_values.py` |
| Best-of-N sim 0.688 / 0.984 / 1.119; SE 0.443 | D1 | `experiments/best_of_n.py` | `results/best_of_n.txt` | REPRODUCED |
| Exact E[max] 0.6882 / 0.9873 / 1.1214 (x 5^-1/2) | quadrature | `experiments/manuscript_numbers.py` | `results/manuscript_numbers.txt` | REPRODUCED; POST HOC |
| Eq. 2.4 understates at N = 2 | analytic | `experiments/submission_figures.py` (Figure 1 curves) | `figures/fig1_best_of_n.pdf` | ANALYTIC (0.519 vs exact 0.564) |

## Synthetic calibration (Table 4, Figures 2-3)

| Claim | Experiment | Source code | Output | Status |
|---|---|---|---|---|
| PSR(0) > 0.95: IID 4.95%, AR 0.1 6.35%, AR 0.3 11.85% [10.47, 13.35], others 4.35-5.45% | D3 | `experiments/calibration.py`, `src/pbo/scenarios.py` | `results/calibration.txt` | REPRODUCED |
| Newey-West PSR, AR 0.3: 7.10% [6.01, 8.31] | D3 | same | same | REPRODUCED |
| Analytic rates 6.84% / 11.37% (large T), 6.83% / 11.36% (T = 1248) | analytic | `psr_dsr.ar1_psr_false_positive` | `results/calibration.txt`, `results/psr_ar1_curve.txt` | REPRODUCED; ANALYTIC (re-derived by hand: F = 1.857, 1.645/sqrt(F) = 1.207) |
| Holm verdicts: phi 0.3 detected, phi 0.1 suggestive (p 0.0075, Holm 0.060) | binomial tests | `experiments/manuscript_numbers.py` | `results/manuscript_numbers.txt` | REPRODUCED; POST HOC rule |
| NW truncation-bias prediction 5.76% (factor 1.704 vs 1.857) | analytic | `manuscript_numbers.py` | same | REPRODUCED; POST HOC |
| DSR rates 0.00-0.70%, 2.60% at rho 0.7; 5.05% with implied N 30.7 | D3 | `calibration.py`, `psr_dsr.implied_n` | `results/calibration.txt` | REPRODUCED; implied-N lead row chosen post hoc |
| Equicorrelated E[max] = sqrt(1-rho) x IID: 1.373 vs implementation 1.141 | analytic | `docs/publication_audit.md` section 6 | audit record | ANALYTIC (quadrature in the audit; derivation in Appendix A) |
| Mean PBO 0.481-0.520; PBO <= 0.05 at most 1/200 | D3 | `calibration.py`, `src/pbo/cscv.py` | `results/calibration.txt` | REPRODUCED |
| GARCH shuffle controls -0.002, +0.009 | D3 | same | same | REPRODUCED |
| D2: PSR 99.15%, DSR 0.05%, mean DSR 0.488, V-known 0.15% | D2 | `experiments/dsr_false_positives.py` | `results/dsr_false_positives.txt` | REPRODUCED |
| D5: mean PBO table (Table 10) | D5 | `experiments/null_checks.py` | `results/null_checks.txt` | REPRODUCED; EXPLORATORY; original "power" reading withdrawn |
| SR_a = 2 at phi 0.3 has 250-day Sharpe 1.47 (factor 1.852) | analytic | `docs/publication_audit.md` section 5 | audit record | ANALYTIC (recomputed in audit) |

## Industry bootstrap (Table 5, Figure 4, Table 11)

| Claim | Experiment | Source code | Output | Status |
|---|---|---|---|---|
| Full window L = 1/5/20/60: 5.35 / 5.15 / 6.25 / 6.25% | D4 | `experiments/french_bootstrap.py` | `results/french_bootstrap.txt` | REPRODUCED |
| Replicate L = 20/60: 5.90 / 6.00%; NW 5.60 / 5.70%; AR(5) 5.30 / 5.35%; weekly 4.35% | D4 replicate | `experiments/french_followups.py` | `results/french_followups.txt` | REPRODUCED (counts identical; see reproducibility.md for 3 approximation digits) |
| Approximations 4.99 / 5.42 / 5.50 / 5.38% | analytic | `scenarios.block_bootstrap_factor`, `french_followups.py` | `results/french_followups.txt` (archived, pre-correction) | REPRODUCED with correction: current code gives 5.39 at L = 60 |
| Lag-1 autocorrelation +0.157 (1971-98), -0.026 (1999-2026) | descriptive | `french_followups.py` | `results/french_followups.txt` | REPRODUCED |
| Sub-periods 8.35% [7.17, 9.65] (167/2000), 3.85% [3.05, 4.79] (77/2000); approximations 8.37 / 3.94% | D4 corrected | `experiments/g6_corrected.py`, `pbo.french.demean_by_period` | `results/g6_corrected.txt` | REPRODUCED; design committed before run (d78d8e8); prediction not blind |
| Uncentred sub-period rates 10.45% / 3.30% | withdrawn run | `french_followups.py` | `results/french_followups.txt` | REPRODUCED but WITHDRAWN as a zero-edge rate |
| Industry means nonzero within periods (36/49, 13/49 positive) | audit | `docs/publication_audit.md` section 1 | audit record | Recomputed in the audit; not rerun here |
| DSR 3.05-3.55% (implied N 23.0-23.3), 1.25-1.90% (N = 49); PBO 0.505-0.520 | D4 | `french_bootstrap.py` | `results/french_bootstrap.txt` | REPRODUCED |
| L = 60 shuffle +0.017 did not replicate (+0.001, -0.001) | D4 replicate | `french_followups.py` | `results/french_followups.txt` | REPRODUCED |
| Holm verdicts for Table 5 | binomial tests | `manuscript_numbers.py` | `results/manuscript_numbers.txt` | REPRODUCED; POST HOC |

## Case study (Tables 6-7, 9; Figures 5-7)

| Claim | Experiment | Source code | Output | Status |
|---|---|---|---|---|
| 15/225 Sharpe 0.593 / 0.588 / 0.582; market 0.458; 55 / 50 / 45 of 93 above | D6 | `experiments/ma_crossover.py`, `src/pbo/strategies.py` | `results/ma_crossover.txt` | REPRODUCED; design committed (afd69c1) |
| DSR 0.9985 / 0.9980 / 0.9969; implied N 17.2; PBO 0.240 / 0.208 / 0.193 | D6 | same | same | REPRODUCED |
| Paired diff 0.130, se 0.099, p 0.0943; 0 of 93 pass Bonferroni at 0/11/44 lags | D6 follow-up | `experiments/market_comparison.py`, `psr_dsr.sharpe_diff` | `results/market_comparison.txt` | REPRODUCED; design committed (d944135) |
| 43 of 93 differences negative; largest z 1.31 | D6 | same | same | Counted from the 93-row table in this audit |
| CI [-0.064, 0.323]; MDE 0.246 / 0.406; power 0.37 / 0.025 | derived | `manuscript_numbers.py` | `results/manuscript_numbers.txt` | REPRODUCED; POST HOC |
| Extra lag: 0.578, PBO 0.216, DSR 0.9959, p 0.113, 48 of 93 | D7 | `experiments/case_study_checks.py` | `results/case_study_checks.txt` | REPRODUCED; EXPLORATORY |
| Turnover 1.32/yr, break-even 121 bps | D7 | same | same | REPRODUCED; EXPLORATORY |
| Sub-period diffs +0.068 (p 0.305), +0.167 (p 0.117) | D7 | same | same | REPRODUCED; EXPLORATORY |
| DSR < 0.95 at N about 7.4e5 | D7 | same | same, and `results/fig7_dsr_vs_n.txt` | REPRODUCED; EXPLORATORY |
| SPA statistic 1.265, p 0.504 | D7 | `psr_dsr.spa_sharpe`, `scenarios.stationary_bootstrap_indices` | `results/case_study_checks.txt` | REPRODUCED; EXPLORATORY; recentring checked against Hansen (2005) g_c in this audit |
| Walk-forward OOS 0.466 vs 0.536, diff -0.070 (se 0.107), p 0.743, 10 settings | D7 | `experiments/performance_checks.py`, `strategies.position_returns` | `results/performance_checks.txt` (corrected); original `results/performance_checks_v1_stitched_costs.txt` | CORRECTED 2026-11-12: costs now charged on the actual position path (4 switch days, 20 bps); independently reconstructed before the fix; EXPLORATORY |
| Descriptives (skew -0.50, kurtosis 17.7, lag-1 -0.001; long 76%), Table 9, crisis returns | D7 | same | same | REPRODUCED; EXPLORATORY; in-sample |

## Statements about the literature

| Claim | Basis | Status |
|---|---|---|
| SF p.4 and p.8 cite Opdyke for validity under stationary ergodic returns | page reading recorded in PROGRESS.md | Read on local PDF (`papers/sharpe-frontier.pdf`) by the project; not re-read in this session |
| Ledoit and Wolf (2008), Remark 3.1, call Opdyke's time-series formulas incorrect | working paper read by a project reviewer | Not re-read in this session |
| Lopez de Prado and Porcu (2026): DSR-L / DSR-LS / DSR-EO, calibration results | SSRN abstract via web search, 2026-11-12 | Abstract-level only |
| Lopez de Prado, Porcu, Zoonekynd, Engle (2026): GARCH Sharpe inference | Crossref record (doi 10.2139/ssrn.6568702), secondary descriptions | Metadata only |
| Sullivan, Timmermann and White (1999): best DJIA rule survives the Reality Check in 1897-1986, not repeated in 1987-1996 | text of the published article, p.37 (conclusion), hosted copy read 2026-11-12 | Verified; an earlier draft sentence that misstated this was corrected |
| All DOIs, volumes, pages | Crossref API, 2026-11-12 | Verified, except Politis-Romano 1992, Memmel 2003, Mertens 2002, Christie 2005 |
