# Current research state

Authoritative paper: [final-research-paper.pdf](docs/submission/final-research-paper.pdf), with [source](docs/submission/final-research-paper.tex), [brief](docs/submission/research-brief.pdf) and [release verification](docs/submission/release-verification.md).

The full chronological design, prediction, correction and owner-sign-off log is preserved in commit `f1f8a3e` and its ancestors. This current-state summary replaces duplicated drafts and old result copies in the live tree; it does not erase that history.

## Verified evidence

- RECOMPUTED: 296 deterministic tests pass with both frozen input archives present. Hosted CI without the archives skips two frozen-data checks; it does not reproduce the empirical experiments.
- RECOMPUTED: all 13 principal experiment scripts ran in an isolated source copy with fresh dependencies on the same machine; their text outputs matched the current results byte for byte.
- RECOMPUTED: seven reconstructed figures match rendered pixels; the two analytic curves match saved text bytes. PDF timestamps prevent a general binary-identity claim.
- The 34-page paper and one-page brief were rendered and inspected, with exact rendered equality used for unchanged pages after repairs. No clipping, missing glyphs, overlap or unresolved citation placeholders was found. PDFs remain untagged.
- Exact input digests and acquisition commands are in [data_manifest.md](docs/data_manifest.md) and [reproducibility.md](docs/submission/reproducibility.md). Source PDFs and data archives are not distributed.

## Principal findings and scope

- RECOMPUTED: under the stated zero-mean industry bootstrap, uncorrected PSR passes 8.35% of early-period samples and 3.85% of late-period samples against nominal 5%. Only the early excess survives the stated eight-row Holm adjustment. Intervals are conditional Monte Carlo uncertainty.
- RECOMPUTED: the best of 93 moving-average rules has Sharpe 0.588 versus market 0.458 and zero-skill DSR 0.998. Its standalone Sharpe advantage is not statistically established; Sharpe SPA p = 0.504.
- RECOMPUTED: baseline market-alpha evidence is exploratory and borderline. With one extra execution day, alpha SPA p = 0.084, 168/2000 exceedances, Monte Carlo s.e. 0.0062. The public script, pre-run sensitivity design, full table and raw bootstrap vectors are supplied.
- Active-return DSR, standalone Sharpe differences and constant-beta alpha are distinct estimands. No implementable trading edge, future-performance claim or new statistic is established.

## Material corrections retained

1. The original G6 subperiod run resampled globally centered data whose subperiod means were nonzero. It is withdrawn; corrected runs center each period using the original seed streams. The failed original check is disclosed.
2. Eight real-data PSR rows form one Holm family. The late-period result is suggestive (adjusted p about 0.096), not a multiplicity-adjusted discovery.
3. Mean PBO is not statistical power or a future-failure probability. Bootstrap variance agreement checks a Normal approximation, not independent prediction or new theory.
4. Walk-forward costs now follow actual held positions at rule switches. Its noisy shortfall does not establish failure of the rule family.
5. Alpha was added after the first benchmark comparisons; its endpoint and SPA selection are post hoc. The delayed-execution negative sensitivity is reported, without changing the 5% threshold.
6. Public SPA boundaries now reject nonfinite/undefined input. Tests demonstrated the defect before the guard; valid finite-input arithmetic is unchanged.
7. Current French follow-up approximations include the partial-final-block correction. Superseded raw outputs and drafts remain recoverable in Git history; the live results correspond to current code.

## Current limitations

Retrospective choices and limited multiplicity families; one vendor, market and rule family; idealized execution; unverified stationarity/bootstrap assumptions; modern 2026 procedures not experimentally compared; no measured PBO decision power; untagged accessibility. The paper is a replication and conditional empirical stress test. Internal review is not external peer review.

## Public-release preparation

The owner authorized public GitHub preparation and requested a final-only live tree. Common credential/machine-path patterns were absent in the screened tracked history and release files. Internal review archives are preserved locally and excluded from publication. Current release artifacts have SHA-256 checksums, reproduction instructions and CI. Earlier files are preserved through Git history rather than duplicate live filenames. LinkedIn copy is prepared separately; no social post or tagging notification has been sent.
