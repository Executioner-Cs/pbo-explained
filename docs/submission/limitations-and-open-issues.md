# Limitations and open issues

Ordered by how much each would change a reader's assessment. "Fixable" means fixable without new theory.

## Scientific

| # | Issue | Effect on conclusions | Fixable? |
|---|---|---|---|
| S1 | PBO decision power never measured (only mean PBO with a planted edge, 20 datasets per cell) | No statement about PBO's ability to pass real edges under dependence | Yes: pre-record a design reporting P(PBO <= 0.05) and P(planted strategy selected), with matched annual-horizon signal; owner prediction required first |
| S2 | PSR tested only at SR* = 0; MinTRL never stress-tested | GARCH and Student-t cells say nothing about PSR at positive benchmarks, where kurtosis and clustering enter | Yes: new simulation design |
| S3 | Three 2026 papers in the same lineage read only at abstract or metadata level | DSR findings may be anticipated or generalized by Lopez de Prado and Porcu (2026) | Yes: obtain and read full texts |
| S4 | Evidence rule (exact binomial + Holm) fixed after results were seen | Changes one verdict (1999-2026 sub-period: suggestive to detected) | No: disclosed; cannot be undone retrospectively |
| S5 | Corrected sub-period prediction equals the approximation and was proposed after the uncentred run | The 8.35% / 3.85% agreement is a model check, not an independent test | Partly: a fresh period split or another dataset with a recorded prediction |
| S6 | Bootstrap block lengths fixed by design; circular fixed blocks remove dependence beyond L | Real-data rates are conditional on L | Yes: Politis-White automatic length or stationary bootstrap sensitivity |
| S7 | One data vendor, one market, one rule family | External validity limited | Yes, with more data |
| S8 | Newey-West variant tried only with the rule-of-thumb lag | Does not show whether any HAC choice restores 5% under AR(1) 0.3 | Yes |
| S9 | Walk-forward and descriptive checks not recorded before running | Exploratory only | No |
| S10 | Case-study execution idealized (same-close fill, research portfolio, flat costs) | Not an implementable strategy; affects only the economic reading, not the statistical contrast | Yes, with an executable proxy (e.g., an index ETF or futures) and a recorded design |
| S11 | Romano-Wolf StepM not computed | Out of scope for this working paper; its outcome is not stated | Yes, with the existing bootstrap |

## Reproducibility

| # | Issue | Status |
|---|---|---|
| R1 | Frozen industry ZIP recovery | **Verified:** capture `20261113053423`, independently retrieved with the frozen SHA-256; see data-recovery.json. Future availability is external, not guaranteed. |
| R2 | Frozen factor ZIP | **Resolved** for durability: Internet Archive capture 20261030074337 matches the SHA-256 |
| R3 | Data licence for redistribution not stated by the French Data Library | Open; archives are not committed |
| R4 | Full transitive lock | Resolved for this machine: `environment-lock.txt`. Not tested on a clean machine or on native Windows |
| R5 | `results/french_followups.txt` predates the partial-block fix (3 printed approximations differ by 0.0001 from current code) | Documented, intentionally kept as the original |
| R6 | LaTeX build depends on Tectonic downloading its bundle from the network | Open; a pinned TeX Live image would remove this |
| R7 | No CI; experiments not run by the test suite | Open |
| R8 | Version of record not committed or tagged; remote not updated | Owner decision; nothing was committed or pushed |
| R9 | Walk-forward cost stitching (found by follow-up review) | **Fixed** 2026-11-12: `strategies.position_returns`, regression tests, regenerated output, original preserved, correction in Appendix D |
| R10 | Clean-environment reproduction (fresh clone, empty `data/`, new venv) not yet exercised | Open; required before a tagged release |

## Publication

| # | Issue |
|---|---|
| P1 | No external peer review. The internal review in `internal-review.md` is role-separated work within the project and is not independent |
| P2 | Contribution is incremental relative to Ledoit and Wolf (2008) and the 2026 DSR framework; suitable venues are practitioner or replication outlets rather than top methods journals |
| P3 | Author contributions, funding and tool-use disclosure statements must be completed by the author for a specific venue |
| P4 | Mertens (2002) document not inspected; cited only as attributed by Bailey and Lopez de Prado (2012). Memmel (2003) and Politis-Romano (1992) metadata corroborated by author bibliographies verified against the authors' institutional records |
