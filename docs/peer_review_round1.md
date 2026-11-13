# Peer review, round 1: editorial decision and revision roadmap

Manuscript: docs/writeup.md (with docs/research_methods.md), as of commit d78d8e8 plus results/g6_corrected.txt.
Date: 2026-11-12. Calibration status: NOT_CALIBRATED. Venue: none confirmed (criteria_binding_unavailable).

## Internal review perspectives and scope
Five internal editorial perspectives were used: journal fit, methodology, domain interpretation, practice and
reproducibility, and adversarial critique. Earlier internal code, mathematical and claims checks informed this
worksheet. These are internal assessments, not reports from independent external referees. Role separation
does not establish independence of errors; no journal review or venue acceptance is claimed.

## Decision: Major Revision

| Seat | Recommendation |
|---|---|
| Journal-Fit | Major Revision |
| R1 Methodology | Major Revision |
| R2 Domain | Major Revision |
| R3 Practice | Major Revision |
| Devil's Advocate | no CRITICAL issues; 3 MAJOR |

Every number checked by any reviewer matches results/. No seat found a computational error that changes a
conclusion. The decision rests on inference, positioning, integration and packaging, all repairable mostly with
results already in hand.

## Consensus findings (raised by 3 or more seats)
1. Corrected G6 is not integrated (all five, plus statistics and code reviews). The manuscript, methods supplement
   and README still say "pending". With centring, 1971-98 over-rejects (8.35% [7.17, 9.65]) and 1999-2026
   under-rejects (3.85% [3.05, 4.79]); the full-window 6.25% is a mixture of the two (mean 6.1%). PSR distortion
   can go in either direction.
2. Section 3.5 reporting (R1, DA, statistics review, manual review): L = 5 (5.15%), the G1 replicate (5.90%,
   6.00%), the follow-up A analytic benchmark and the PBO paired controls (including the non-replicated +0.017) are
   omitted; the pooled z = 3.14 is post hoc. No evidence-rule verdict is given for the French rows (L = 20 and 60
   are suggestive, z = 2.57).
3. Power of the market test (R1, DA, manual review): se 0.099 gives a minimum detectable difference of about 0.41
   at the Bonferroni cutoff (0.25 unadjusted); power against 0.130 is 2.5%. 95% CI for the difference
   [-0.064, 0.324]. "Insufficient evidence" must be read with this.
4. Implied-N table cells mislabelled (all seats that checked): "implied N 5.05" is the DSR acceptance rate at
   implied N 30.7.
5. Literature (Journal-Fit, R2, R3, DA): missing White (2000), Hansen (2005), Romano-Wolf (2005),
   Sullivan-Timmermann-White (1999), Brock-Lakonishok-LeBaron (1992), Harvey-Liu(-Zhu), Jobson-Korkie, Memmel,
   Mertens, Newey-West (1987, 1994), Kunsch, Politis-Romano, Lo-MacKinlay (1988, 1990), and two 2026 papers in
   the same lineage (Lopez de Prado-Lipton-Zoonekynd, JPM 52(6), doi 10.3905/jpm.2026.1.837; Lopez de
   Prado-Porcu-Zoonekynd-Engle, GARCH Sharpe inference).
6. Submission form (Journal-Fit, R3, R2): internal workflow text (banner, TODO/step numbers, G-codes, PROGRESS.md
   pointers), no Introduction or Conclusion, no stated takeaways, missing statements, no license, no archive or
   durable data route.

## Disagreements adjudicated
- G6 prediction chronology. Journal-Fit said the numerical prediction predates both runs. R1, DA and the
  statistics review say the 8.38% / 3.94% values were printed by the same follow-up run that produced the
  uncentred G6 result, and the prediction was proposed after that. The record (results/french_followups.txt,
  PROGRESS.md) supports R1/DA. Ruling: the prediction is the approximation, not blind; judge only its direction;
  call the agreement a model check.
- DSR framing. R2 and DA: the 2014 DSR's near-zero null rate is a property of its design (location benchmark,
  single-strategy SE), not a calibration failure; Lopez de Prado-Porcu (2026) describe the versions as serving
  different objectives. No seat disagreed. Ruling: reframe "Neither is a calibrated 5% test" and explain why the
  rate rises with correlation (V measures only idiosyncratic dispersion).
- G4. DA: lower effective signal explains the mean-PBO shift (interpolation predicts about 0.32 vs 0.391 +/- 0.043);
  R1: Normal z on 20 skewed values is rough. Ruling: move G4 out of "what breaks"; label exploratory; optional
  matched-signal rerun.
- Interpretation of the period effect. DA, R2, R3, Journal-Fit: pre-1999 daily autocorrelation is plausibly
  nonsynchronous trading / stale prices (Lo-MacKinlay 1990). R1: it is still real dependence for PSR's inputs, but
  not exploitable. Ruling: report it as dependence in these portfolio return series and name the mechanism as a
  hypothesis.
- Attribution. Journal-Fit and R2: the (1 + phi)/(1 - phi) factor and the Newey-West Sharpe adjustment are
  standard (Lo 2002; Newey-West). Ruling: keep "our derivation" only for the rejection-rate approximation, if it
  is not printed elsewhere.

## Devil's Advocate issues (no CRITICAL)
- M1 period effect in both directions: accepted (consensus 1).
- M2 G4 signal rescaling: accepted (see above).
- M3 stale-price alternative: accepted as a hypothesis to state, not test.
Strongest counter-argument recorded: most calibration findings are known or follow from construction; the
contribution is a traceable replication plus quantified operating characteristics. The revision should state
which findings are confirmations and which are new evidence, rather than contest this.

## Revision roadmap (in order; no new theory needed)
A. Integrate results already in hand
1. Section 3.5: corrected G6 as the primary real-data result (counts, CIs, approximation, direction verdicts);
   full-window rate as a regime mixture; report every L and every rerun, the follow-up A benchmark and the PBO
   paired controls; drop or label the pooled z.
2. Section 3.6: CI for the difference, minimum detectable difference at both cutoffs, power at 0.130; print
   difference, se and raw p at 0, 11 and 44 lags; label the raw p as selection-biased.
3. Relabel the implied-N cells; give separate DSR ranges for N = 49 and implied N.
4. G6 prediction: judge direction only; disclose that the correction followed a failed check.
B. Inference framework
5. One primary criterion (exact binomial), declared families, exact and Holm-adjusted p for every cell; list all
   post hoc choices in Methods (evidence rule, implied-N lead row, pooling).
6. Best-of-N gap: attribute to the Eq. 2.4 approximation (quadrature 0.6882 / 0.9873 / 1.1214 matches simulation).
7. Newey-West at phi 0.3: report the bias-only prediction (5.76%) and the full Newey-West column.
8. Report PBO <= 0.05 acceptance rates under the null; state that exchangeable nulls do not stress PBO.
C. Framing and literature
9. Reframe the 2014 DSR results as design properties; explain the correlation effect.
10. Section 3.4 provenance chain: Jobson-Korkie, Memmel, Lo 2002, Mertens, Christie (HAC in practice, lag-0
    appendix), Opdyke, SF, Ledoit-Wolf; correct Lopez de Prado-Porcu description and add DOI 10.3905/jpm.2026.070.
11. Related-work paragraph: RC/SPA/StepM and Sullivan-Timmermann-White as the direct precedent for Section 3.6;
    state why Bonferroni (or add SPA/StepM with the existing bootstrap).
12. Position against the two 2026 same-lineage papers (read in full).
D. Practice
13. Decision table: decision, statistic and hurdle, what a pass does not imply, evidence still required.
14. Case study sensitivity: one-day extra lag, turnover and break-even cost, split at 1999; DSR break-even N.
E. Form and availability
15. Standard structure: Introduction, Related work, Methods (with the evidence rule), Results, Discussion,
    Conclusion; numbered, captioned tables; remove banner, TODO/step labels, G-codes; define acronyms.
16. Statements: data and code availability, license, author contributions, funding, conflicts, ethics (not
    applicable), and other venue-required disclosure statements (owner's decision).
17. Reproducibility package: license file, archive with DOI, tagged release, environment stamp (commit, versions)
    in each result file, CITATION.cff, durable data route or documented redistribution limit.

Code items (from the code review, not manuscript-blocking): hash the download before moving it into place, add a
timeout; stable variance merge in cscv; clip negative block factor; .gitattributes and utf-8/LF result writing;
consistent lag validation; compute the 11 lags from T.

## Attachments
- Acronym check (advisory): undefined at first use: PSR, PBO, AR, SF, DSR, PSEUDO, MinBTL, MinTRL,
  GARCH, IID, CRSP, SR, CSCV, HAC, SHA (and PAPER, TODO, which are labels).
- Suggested-reference check and reviewer claim check: not run (they call external bibliographic indexes and a
  separate judge; DOIs listed above were resolved by the domain seat via Crossref).
