# Internal adversarial review of research-paper.tex

Date: 2026-11-12. This is an internal, role-separated review carried out within the project after the first complete
draft. It is not an independent peer review, and the five perspectives below share the same author and errors.
No verdict is offered on behalf of any reviewer; the record lists concerns and what was done about them.

Severity: **Major** = could change a conclusion or mislead a reader; **Minor** = presentation or precision.

## Reviewer A: mathematical statistician

| # | Concern | Severity | Action |
|---|---|---|---|
| A1 | Proposition 1 needs a CLT for the sample mean and consistency of the sample SD; skew/kurtosis estimates enter the PSR denominator | Minor | Conditions stated; Appendix A shows the denominator tends to 1 at SR = 0 |
| A2 | Claim that Eq. 4 "overstates E[max] for small N" is false at N = 2 (0.519 vs exact 0.564) | Major (factual) | **Fixed**: restricted to N = 10 to 100; N = 2 case noted |
| A3 | "DSR spread is a single strategy's, the maximum's spread is smaller" needs justification | Minor | True for N >= 2 (Var(max of 2) = 1 - 1/pi); kept as stated |
| A4 | Romano-Wolf claim ("cannot reject") was stated as certain without computation | Major (unsupported) | **Fixed**: now "would be expected to stop ... not computed", with Hansen (2005) for the power ordering |
| A5 | Holm families and the evidence rule chosen post hoc | Major | Disclosed in Section 4.4 and Table 2; cannot be repaired retrospectively |
| A6 | Power calculation treats the HAC s.e. as known | Minor | Formula in Appendix A labelled; values are approximate |
| A7 | Implied-N "recovery" might be read as validating Eq. 9 | Major | Text states it checks the estimate of the formula, not the correction; exact equicorrelated E[max] given |

## Reviewer B: quantitative finance researcher

| # | Concern | Severity | Action |
|---|---|---|---|
| B1 | Research factors are not point-in-time; history is revised between releases | Major | **Added** "Data construction" limitation |
| B2 | Survivorship bias | Minor | **Added**: CRSP-based portfolios include delisted firms |
| B3 | Sharpe comparison of a lower-volatility long-biased rule with the market | Minor | Financial-interpretation paragraph explains it |
| B4 | Crisis-window returns of an in-sample-selected rule could be read as evidence of protection | Major | Placed only in an appendix table note and labelled in sample |
| B5 | Costs ignore impact, financing, taxes | Minor | Stated in Section 7 |
| B6 | Statement about Sullivan, Timmermann and White (1999) misrepresented their result (their best rule survived the Reality Check in sample) | Major (factual) | **Fixed** after reading p.37 of the article; Sections 2, 8 and Table 1 corrected |

## Reviewer C: empirical econometrician

| # | Concern | Severity | Action |
|---|---|---|---|
| C1 | Fixed block lengths, no data-driven choice | Minor | **Added** limitation citing Politis and White (2004) |
| C2 | "Full-window rate is a mixture" is heuristic | Minor | Worded "close to the average"; not a decomposition |
| C3 | Sub-period agreement presented as confirmation | Major | Text calls it a model check; prediction not blind |
| C4 | Fixed-b alternatives mentioned without citation | Minor | **Fixed**: Kiefer and Vogelsang (2005), DOI verified |
| C5 | Walk-forward is one realized path and was not recorded before running | Major | Labelled exploratory in Table 2, Section 7 and abstract wording softened from "underperforms" to "lower Sharpe ratio" |
| C6 | "Strategy-minus-market influence series inherits little serial correlation" not measured | Minor (unsupported) | **Removed** |
| C7 | Decimalization as a reason for the post-1999 change is speculative | Minor | Phrased as a candidate; mechanism explicitly untested |

## Reviewer D: research software engineer

| # | Concern | Severity | Action |
|---|---|---|---|
| D1 | Industry archive has no durable copy | Major | Investigated: rolling URL still matches; no matching Wayback capture; factor ZIP recovered from Wayback and verified. Remains open (limitations R1) |
| D2 | No full dependency lock | Minor | **Added** `environment-lock.txt` |
| D3 | Scripts overwrite `results/` | Minor | Reproduction done in an isolated copy; procedure in `reproducibility.md` |
| D4 | Figures must come from saved outputs | Major | `experiments/submission_figures.py` reads `results/` only, writes PDFs to `docs/submission/figures/`; curves are documented closed forms |
| D5 | Figure legends cited wrong equation numbers after renumbering | Minor | **Fixed** |
| D6 | One archived file differs from current code | Minor | Explained (partial-block correction); counts identical |
| D7 | TeX build needs network | Minor | Documented |

## Reviewer E: skeptical editor

| # | Concern | Severity | Action |
|---|---|---|---|
| E1 | "In practice these statistics are frequently read as hurdles" unsupported | Minor | **Fixed**: now cites the source papers' own hurdle readings (DSR p.10, PBO p.14) |
| E2 | Novelty relative to Ledoit-Wolf and the 2026 DSR framework | Major | Contribution paragraph, Table 1 and Section 8 disclaim priority; literature-review.md lists access levels |
| E3 | Title emphasizes serial dependence while the paper also covers DSR, PBO and a case study | Minor | Kept: dependence is the main stress test; subtitle covers the rest. Owner may prefer "... and Strategy Search" |
| E4 | Unverified affiliation | Minor | **Removed** "Independent research" |
| E5 | Abstract length about 230 words | Minor | **Trimmed** to about 200 |
| E6 | Floats drifting away from their sections | Minor | **Fixed** with section float barriers |
| E7 | Overfull lines in tables and appendix | Minor | **Fixed**; final build has no overfull boxes |

## Follow-up: follow-up review findings, 2026-11-12

| # | Finding | Action |
|---|---|---|
| X1 | Walk-forward stitched each rule's own costed returns, missing costs at rule switches | **Confirmed** by independent reconstruction (same 4 dates, 0.466781 -> 0.466419); fixed with tests first; original output preserved |
| X2 | "Every printed example" overstates replication coverage | **Fixed**: "selected numerical examples (Table 3)" |
| X3 | Contribution listed a stepwise test that was never run; text predicted the StepM outcome | **Fixed**: joint SPA only; StepM outcome not stated |
| X4 | Power and MDE read as measured power | **Fixed**: labelled Normal-shift approximations conditional on the estimated s.e. |
| X5 | Hansen recentring attributed to Sullivan et al.; omega undefined | **Fixed** |
| X6 | Industry start-date rationale wrong; averaging read as decomposition; seed description in pseudocode wrong | **Fixed** |
| X7 | GARCH paper retitled on SSRN; reference-status wording | **Fixed** in `references.bib` |

These were missed by the internal review above, which is one reason it should not be read as independent.

## Not fixed (and why)

- S1-S3 in `limitations-and-open-issues.md` need new experiments or full-text access; new experiments require a
  recorded owner prediction under the project's rules and were not run.
- No reviewer verdict is recorded. The manuscript has not been externally reviewed.
