# Working-paper release verification

*Backtest Overfitting Statistics under Serial Dependence and Benchmark Choice: A Replication and Empirical Stress Test*, Mayank Khandelwal, 13 November 2026.

Status: working paper; no external peer review. Internal assessment: ready with disclosed limitations. This is a replication and empirical stress test, with no new statistic or implementable trading-edge claim.

## Delivered artifacts

- [Full working paper](working-paper.pdf), 34 pages; [LaTeX](source/working-paper.tex); [bibliography](source/references.bib).
- [Research brief](research-brief.pdf), one page; [source](source/research-brief.tex).
- [Reproduction instructions](reproducibility.md), [literature/access record](literature-review.md), [limitations](limitations.md).

PDF SHA-256:

```text
paper  153e898df04a58bd5f38c8faf60a13dbb7684c2b15f6c86dd18260fe51bab9ea
brief  3f07a409b0cfe5759e0fa48a1d721d450dcbf718f7583f8f3ba0fa0277866e30
```

## Verification actually performed

- Final local deterministic suite: 296 passed, no skips. A fresh-interpreter run also gave 296 passed.
- All 13 main experiment scripts ran in an isolated source copy with freshly installed dependencies; all regenerated text outputs matched the current saved files byte for byte.
- All seven reconstructed figures matched rendered pixels; the two analytic curve files matched bytes. Figure PDFs contain timestamps, so binary PDF equality is not claimed.
- The paper's 34 pages and one-page brief were visually inspected. After later repairs, unchanged pages were confirmed by exact rendered equality and every changed page reopened. No clipping, overlapping text, missing glyphs or unresolved citation placeholders were found.
- The delayed-alpha sensitivity used 93 original rules, 5 bps, execution delay 2, 2,000 stationary-bootstrap replicates, mean block 20 and seed 20261118. Independent reconstruction from its saved vectors gives 168/2000 = p 0.084, Monte Carlo s.e. 0.0062. [Design](methods/delayed-alpha-design.md); [script](../experiments/delayed_alpha.py); [full output](../results/delayed_alpha.txt); [raw vectors](../results/delayed_alpha_bootstrap.npz).

The isolated rerun was on the same machine, with copied, hash-checked input archives. Earlier exact-archive download verification is recorded in the project history; the final rerun is not claimed as independent hardware or a fresh independent download. CI without the archives skips two frozen-data checks and does not reproduce the empirical study.

## Scientific corrections retained

The globally centered G6 subperiod run is withdrawn; corrected runs center each period. The late-period PSR result is suggestive under the eight-row Holm family, not a multiplicity-adjusted discovery. Mean PBO is not decision power or future-failure probability. A noisy walk-forward shortfall is not an established failure of the rule family. Active-return DSR, standalone Sharpe differences and market alpha are distinct estimands. The baseline positive alpha evidence is post hoc and execution-sensitive. Superseded follow-up and walk-forward outputs are preserved in Git history at commit `f1f8a3e`; only current reproducible outputs remain in the live tree.

## Remaining limits

One vendor, market and rule family; retrospective choices; tablewise rather than research-wide error control; idealized execution on a nontraded research factor; unverified stationarity and bootstrap assumptions; modern 2026 procedures not experimentally compared; untagged PDF accessibility. Internal review is not independent human peer review. A public release does not strengthen these scientific claims.

Private internal review notes are kept outside the repository; they are not needed to reproduce any public result. Public-facing methods, correction history, numerical outputs and the added raw sensitivity evidence are provided here for inspection. Release tags identify the published source tree; the paper's original review baseline was commit 68882f58251dfa98adb0949c02f333d481ea2643 plus preserved working-tree revisions.

## Hosted portability check

The first hosted CI run exposed two failures in a bitwise CSCV oracle comparison: the reference used scalar `math.log`, while production used vectorized `numpy.log`. The reference now applies the same final vector log kernel after its independently computed two-pass Sharpe estimates and ranks. The strict array-equality assertion remains; no numerical tolerance or research threshold was relaxed, and production calculations are unchanged. The hosted CI status records the outcome for the current source revision.

## Canonical publication layout

The reader-facing files are now docs/working-paper.pdf and docs/research-brief.pdf. LaTeX, bibliography and the seven vector figures are under docs/source/; reproduction and evidence documentation are under docs/. Rebuilding after the move preserved all 34 paper pages: pages 1–33 are pixel-identical to the inspected artifact, and the revised documentation link on page 34 was visually inspected. The one-page brief is pixel-identical. Numerical research calculations are unchanged.

The files later moved from paper/ to docs/, and the figure script was renamed to experiments/build_paper_figures.py. Both PDFs were rebuilt with Tectonic 0.15.0 so that page 34 prints the new command. Compared with the previous artifacts at 150 dpi: pages 1–33 of the paper and the brief have identical extracted text and rendered pixels; page 34 differs only in that command and was visually inspected. Regenerated figures match the previous ones in text and rendered pixels; their bytes differ only in the embedded creation date. docs/checksums.sha256 identifies the current bytes.
