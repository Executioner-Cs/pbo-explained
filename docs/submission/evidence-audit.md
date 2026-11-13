# Claim-to-evidence map

All empirical values below are **RECOMPUTED** from the supplied code and saved outputs. Printed source-paper values are **PAPER**, with page-level provenance in [paper_check.md](../paper_check.md) and `src/pbo/paper_values.py`. No claim below is an external peer-review certification.

| Final claim | Producing script | Saved evidence | Interpretation |
|---|---|---|---|
| Selected PSR, MinTRL, DSR and MinBTL numerical examples reproduce | Library tests; `src/pbo/paper_values.py` | `tests/test_psr_dsr.py`, `tests/test_minbtl.py`; final paper replication table | PAPER values, with stated rounding caveat for the three-year PSR example |
| Best of 100 zero-skill five-year trials averages annualized Sharpe about 1.12 | `experiments/best_of_n.py` | `results/best_of_n.txt` | Fixed-seed simulation; Normal-maximum approximation distinguished from exact quadrature |
| Uncorrected PSR passes 11.85% under AR(1), phi 0.3 | `experiments/calibration.py` | `results/calibration.txt` | Zero-mean null; conditional Monte Carlo intervals; existing dependence theory |
| Seven-lag Newey–West leaves 7.10% in that cell | `experiments/french_followups.py` | `results/french_followups.txt` | Leading correction is incomplete at this bandwidth/sample size |
| Operational 2014 DSR is strongly conservative under independent zero-skill search | `experiments/dsr_false_positives.py`, `calibration.py` | Corresponding result files | Not a calibrated 5% familywise test merely because its score exceeds 0.95 |
| Corrected industry subperiod passes are 8.35% and 3.85% | `experiments/g6_corrected.py` | `results/g6_corrected.txt` | Each period centered separately; original uncentered run withdrawn |
| Late-period finding is suggestive, Holm p about 0.096 | `experiments/review_checks.py` | `results/review_checks.txt`, item 4 | One eight-row family; evidence rule/post hoc chronology disclosed |
| Removing dependence gives 5.05% and 4.67% | `experiments/review_checks.py` | Item 1 | Conditional post hoc controls; causal market mechanism not identified |
| Mean PBO remains near its reference in the studied nulls | `calibration.py`, `french_bootstrap.py`, `null_checks.py` | Corresponding result files | Does not measure decision power or a future failure probability |
| 93-rule winner has Sharpe 0.588 versus 0.458, DSR 0.998, PBO 0.208 | `experiments/ma_crossover.py` | `results/ma_crossover.txt` | Selected in sample at 5 bps; idealized execution on a research factor |
| Standalone Sharpe difference is +0.130, HAC s.e. 0.099, p 0.0943 | `experiments/market_comparison.py` | `results/market_comparison.txt` | Single selected-rule p is selection-biased; no rule passes Bonferroni |
| Sharpe SPA p = 0.504 | `experiments/case_study_checks.py` | `results/case_study_checks.txt` | No established Sharpe superiority under the conditional bootstrap |
| Active-return DSR is 0.0296 | `experiments/review_checks.py` | Item 6 | Sharpe of strategy-minus-market returns, not difference of standalone Sharpes |
| Baseline alpha is 3.16% a year, HAC t 2.71; alpha SPA is borderline | `experiments/review_checks.py` | Items 5, 10–11 | Post hoc; p spans 0.035–0.065 across bootstrap choices; not a confirmatory discovery |
| One extra execution day gives alpha SPA p = 0.084 | `experiments/delayed_alpha.py` | `results/delayed_alpha.txt`, `results/delayed_alpha_bootstrap.npz` | 168/2000 exceedances; Monte Carlo s.e. 0.0062; execution-sensitive evidence |
| Walk-forward Sharpe 0.466 versus 0.536, difference -0.070 with s.e. 0.107 | `experiments/performance_checks.py` | `results/performance_checks.txt` | Selector diagnostic on reused history; no established deterioration |
| All seven figures reconstruct | `experiments/submission_figures.py` | `docs/submission/figures/`; saved analytic curves | Rendered pixel equality checked; PDF binary identity not claimed |

The [reproduction instructions](reproducibility.md) give commands, data hashes, ordering and seeds. The [release verification](release-verification.md) records actual execution scope. The final paper's correction appendix and Git history retain withdrawn analyses and earlier interpretations, without duplicate result copies in the live tree.
