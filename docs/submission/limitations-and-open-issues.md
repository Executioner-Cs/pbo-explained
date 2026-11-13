# Limitations and open issues

Ordered by how much each would change a reader's assessment. "Fixable" means fixable without new theory.

## Scientific

| # | Issue | Effect on conclusions | Fixable? |
|---|---|---|---|
| S1 | PBO decision power never measured (only mean PBO with a planted edge, 20 datasets per cell) | No statement about PBO's ability to pass real edges under dependence | Yes: a pre-recorded design reporting P(PBO <= 0.05) and P(planted strategy selected), with a horizon-matched signal |
| S2 | PSR tested only at SR* = 0; MinTRL not stress-tested | GARCH and Student-t cells say nothing about PSR at positive benchmarks, where kurtosis and clustering enter | Yes: new simulation design |
| S3 | The 2026 procedures (DSR-LS, DSR-EO, AR(1)-corrected variance, clustered effective trials) not tested | They may remove the distortions documented here | Yes: implement and rerun the same designs |
| S4 | Evidence rule (exact binomial + Holm) fixed after results were seen | Earlier family splitting changed the late-period verdict; final eight-row family restores suggestive (Holm p=0.096) | No: disclosed |
| S5 | Corrected sub-period prediction equals the approximation and was proposed after the uncentred run | The 8.35% / 3.85% agreement is a model check, not an independent test | Partly: a fresh split or dataset with a recorded prediction |
| S6 | Bootstrap block lengths fixed by design; fixed blocks remove dependence beyond L | Real-data rates are conditional on L | Yes: Politis-White automatic length or stationary-bootstrap sensitivity |
| S7 | One data vendor, one market, one rule family | External validity limited | Yes, with more data |
| S8 | Newey-West tried only with the rule-of-thumb lag | Does not show whether any HAC choice restores 5% under AR(1) 0.3 | Yes |
| S9 | Walk-forward and descriptive checks not logged before running | Exploratory only | No |
| S10 | Case-study execution idealized (same-close fill, research portfolio, flat costs) | Affects inference too: delayed alpha SPA p=0.084, weakening the baseline borderline evidence | Yes, with a traded proxy and a recorded design |
| S11 | Romano-Wolf StepM not computed | Out of scope; its outcome is not stated | Yes, with the existing bootstrap |
| S12 | Supplementary proofs of the 2026 papers not checked | Their published results are relied on as stated | Yes |

## Reproducibility

| # | Issue | Status |
|---|---|---|
| R1 | Durable copies of the frozen inputs | Resolved: both ZIPs have Internet Archive captures whose downloads match the frozen SHA-256 (`reproducibility.md`). Future availability is outside the project's control |
| R2 | Data redistribution terms not stated by the French Data Library | Open; archives are not committed |
| R3 | `results/french_followups.txt` predates the partial-block fix (three printed approximations differ by 0.0001) | Documented, kept as the original |
| R4 | TeX build downloads the Tectonic bundle on first use | Open; a pinned TeX image would remove this |
| R5 | Automated deterministic CI; Monte Carlo experiments are separate from the test suite | CI is provided; full empirical reruns remain separate |
| R6 | Fresh-clone reproduction on a second machine | Not done by this review |
| R7 | Version of record | Public release tag identifies the delivered source tree |

## Publication

| # | Issue |
|---|---|
| P1 | No external peer review. The internal review in `submission-readiness.md` is not independent |
| P2 | Contribution is incremental relative to Ledoit and Wolf (2008) and the 2026 papers; a practitioner or replication venue fits it better than a methods journal |
| P3 | Author contributions and any disclosure wording must be completed for a specific venue |
| P4 | Mertens (2002) and Memmel (2003) not examined directly; Mertens is cited as attributed by Bailey and Lopez de Prado (2012) |

## Final continuation

Current public issue dispositions are consolidated in `release-verification.md`. Assistance and author responsibility are now
disclosed in the paper; venue-specific wording remains the author's responsibility. The final PDF is untagged. Modern-method
comparisons, broader calibration and prospective/tradable validation remain future studies rather than demonstrated defects
that can be repaired by editing this manuscript.
