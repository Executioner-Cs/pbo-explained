# Working-paper release verification

*Backtest Overfitting Statistics under Serial Dependence and Benchmark Choice: A Replication and Empirical Stress Test*, Mayank Khandelwal, 13 November 2026.

Status: working paper; no external peer review. Internal assessment: ready with disclosed limitations. This is a replication and empirical stress test, with no new statistic or implementable trading-edge claim.

## Delivered artifacts

- [Full working paper](final-research-paper.pdf), 34 pages; [LaTeX](final-research-paper.tex); [bibliography](final-references.bib).
- [Research brief](research-brief.pdf), one page; [source](research-brief.tex).
- [Reproduction instructions](reproducibility.md), [literature/access record](literature-review.md), [limitations](limitations-and-open-issues.md).

PDF SHA-256:

```text
paper  a448d6401bd0d5cb981f9e66186c3659ed725ebd0b88c992a668e51aa182b7c4
brief  3cdb7532cf412e96fe7d1e0926d1908f560529a63f8d76e561aee72abf139620
```

## Verification actually performed

- Final local deterministic suite: 296 passed, no skips. A fresh-interpreter run also gave 296 passed.
- All 13 main experiment scripts ran in an isolated source copy with freshly installed dependencies; all regenerated text outputs matched the current saved files byte for byte.
- All seven reconstructed figures matched rendered pixels; the two analytic curve files matched bytes. Figure PDFs contain timestamps, so binary PDF equality is not claimed.
- The paper's 34 pages and one-page brief were visually inspected. After later repairs, unchanged pages were confirmed by exact rendered equality and every changed page reopened. No clipping, overlapping text, missing glyphs or unresolved citation placeholders were found.
- The delayed-alpha sensitivity used 93 original rules, 5 bps, execution delay 2, 2,000 stationary-bootstrap replicates, mean block 20 and seed 20261118. Independent reconstruction from its saved vectors gives 168/2000 = p 0.084, Monte Carlo s.e. 0.0062. [Design](evidence/delayed-alpha-design.md); [script](../../experiments/delayed_alpha.py); [full output](../../results/delayed_alpha.txt); [raw vectors](../../results/delayed_alpha_bootstrap.npz).

The isolated rerun was on the same machine, with copied, hash-checked input archives. Earlier exact-archive download verification is recorded in the project history; the final rerun is not claimed as independent hardware or a fresh independent download. CI without the archives skips two frozen-data checks and does not reproduce the empirical study.

## Scientific corrections retained

The globally centered G6 subperiod run is withdrawn; corrected runs center each period. The late-period PSR result is suggestive under the eight-row Holm family, not a multiplicity-adjusted discovery. Mean PBO is not decision power or future-failure probability. A noisy walk-forward shortfall is not an established failure of the rule family. Active-return DSR, standalone Sharpe differences and market alpha are distinct estimands. The baseline positive alpha evidence is post hoc and execution-sensitive. The original follow-up and walk-forward outputs are retained in versioned result files.

## Remaining limits

One vendor, market and rule family; retrospective choices; tablewise rather than research-wide error control; idealized execution on a nontraded research factor; unverified stationarity and bootstrap assumptions; modern 2026 procedures not experimentally compared; untagged PDF accessibility. Internal review is not independent human peer review. A public release does not strengthen these scientific claims.

The complete internal review archive remains preserved locally. Public-facing methods, correction history, numerical outputs and the added raw sensitivity evidence are provided here for inspection. Release tags identify the published source tree; the paper's original review baseline was commit 68882f58251dfa98adb0949c02f333d481ea2643 plus preserved working-tree revisions.
