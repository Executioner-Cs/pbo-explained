# Submission readiness

Date: 2026-11-12. Scope: `docs/submission/` built from the working tree at commit d78d8e8 plus uncommitted changes
present before this package was assembled. Nothing was committed, pushed or published.

## Acceptance criteria

| Criterion | Status | Evidence |
|---|---|---|
| Repository thoroughly inspected | Done | README, PROGRESS, TODO, writeup, paper, methods, data manifest, publication audit, panel review, all `src/` modules, experiment scripts and result files read |
| Existing papers and notes examined | Done within limits | Project page checks (`docs/paper_check.md`) relied on; source PDFs not re-read page by page in this session |
| Contribution accurately classified | Done | Paper Section 1, Table 1; `literature-review.md` section 3 |
| Mathematics checked | Done | PSR, delta-method influence, block-bootstrap factor, AR(1) factor, equicorrelated maximum, SPA recentring, power formula re-derived (Appendix A); code read against them |
| Main empirical results verified | Done | Every experiment rerun in an isolated copy; 13 of 14 result text files and all 7 PNGs byte-identical; the 14th differs only by a documented 0.0001 correction |
| Withdrawn claims excluded or accurately discussed | Done | Uncentred sub-period rates, "power" reading of D5, implied-N "true count", pooled rate, phi 0.1 "detected": Appendix D |
| Failed or negative tests reported | Done | No setting beats the market; SPA p 0.50; walk-forward shortfall; Newey-West does not restore 5%; L = 60 PBO effect did not replicate; prediction 3 not judged |
| Literature review complete within documented limits | Partial | Three 2026 papers abstract/metadata only; no systematic database search |
| Bibliographic metadata verified | Done except 3 | Crossref for all DOIs; Politis-Romano 1992, Memmel 2003, Mertens 2002 unconfirmed and flagged in `references.bib` |
| Figures correspond to actual calculations | Done | `experiments/submission_figures.py` reads `results/` only; analytic curves documented |
| Manuscript complete | Done | 28 pages: main text pp.1-23, references, appendices A-E |
| PDF compiles and renders | Done | Tectonic 0.15.0; no undefined references; no overfull boxes; every page rendered to an image and inspected |
| Reproducibility workflow documented and tested | Done, with open data issue | `reproducibility.md`; tests 279 passed; full rerun completed |
| Unresolved dependencies and data problems disclosed | Done | Industry archive durability open; factor archive resolved via Internet Archive |
| Internal adversarial review completed | Done | `internal-review.md`; 3 factual errors found and fixed (Eq 2.4 direction, StepM claim, Sullivan et al. reading) |
| Internal consistency checked | Done | Every decimal in the TeX source matched against `results/*.txt`; the 12 non-matches are paper values, Normal quantiles or audit quadrature values |

## Outstanding blockers before external submission

1. **Industry data durability (R1).** The exact industry archive is retrievable today only from a rolling URL. Owner
   action: request an Internet Archive capture while the bytes still match, or archive privately under the data terms.
2. **Full text of Lopez de Prado and Porcu (2026).** Needed to state precisely whether the DSR findings are already in
   the literature.
3. **Version of record.** Commit, tag and (if desired) archive the release; record the commit in the paper's code
   availability statement. Owner decision.
4. **Venue-specific statements.** Author contributions, funding and disclosure wording.

## Recommended but not blocking

- PBO decision-power experiment (limitation S1) with a recorded prediction.
- PSR at SR* > 0 under GARCH and Student-t (S2).
- Block-length sensitivity with an automatic rule (S6).
- Romano-Wolf StepM (S11), a few lines with the existing bootstrap.

## Assessment

The statistical content is internally consistent, reproduces from code, and is honest about chronology and
withdrawn claims. The contribution is a careful replication plus conditional operating characteristics, not a
methodological advance. It is ready for technical scrutiny by a quantitative reader as a working paper. It is not yet
ready for journal submission because of blockers 1-3 above.

## Follow-up review, 2026-11-12

The assessment above describes the assembled draft, not unconditional approval for public distribution.
A subsequent review identified incorrect walk-forward transition-cost stitching and remaining overstatements
about example coverage and stepwise testing. See [open-issues-plan.md](open-issues-plan.md) for the reproduced
accounting discrepancy and prioritized repairs. The current PDFs have not yet incorporated those repairs.
No new publication, archive capture, commit or push was performed in this follow-up review.

## Status after the follow-up repairs, 2026-11-12

Done: walk-forward cost accounting fixed (confirmed independently, tests first, original output preserved,
PROGRESS.md entry); manuscript, summary, bibliography and companion documents corrected for example coverage,
stepwise-test claims, power wording, SPA attribution, omega definition, start-date rationale, averaging wording,
seed description and reference status; both PDFs rebuilt (28 pages and 1 page, no undefined references or
overfull boxes); suite 285 passed.

Still open before a public release: an authorized immutable copy of the industry archive; full texts of the
2026 papers; a clean-environment reproduction from a fresh clone; owner decision on commit, tag and release.
No archive request, commit or push has been made.

## Current release-candidate verification, 2026-11-13 UTC

This update supersedes the open-data status above while preserving the earlier review chronology.
Both exact ZIPs were independently retrieved from timestamped captures and SHA-256 checked; the newly created
industry capture is 20261113053423. See data-recovery.json. Clean-environment reproduction is being checked
separately and will be recorded in a release receipt. The three 2026 full texts remain inaccessible through
ordinary public links and were not found in the repository; full-text-access.json records that limitation.
The release decision is a draft working-paper candidate, not final journal-publication approval.
