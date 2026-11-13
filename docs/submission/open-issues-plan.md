# Recommended route to a defensible public working paper

Review date: 2026-11-12. This is a prioritized repair/release plan, not a new publication approval.
The current compiled PDFs have not been edited or rebuilt by this review. No result file was changed.

## 1. Repair existing evidence before expanding the study

A new deterministic check found a walk-forward accounting bug in experiments/performance_checks.py:69-73.
The code stitches rule returns whose costs were computed for separate hypothetical positions. At an annual
rule change, actual portfolio turnover depends on the previously held position, not on the newly selected
rule's hypothetical prior position. Keep training selection unchanged, form the actual selected-position path,
then charge costs from changes in that realized path. State the initial-entry convention.

RECOMPUTED independently, with the initial position flat (also flat in the actual first selected observation):

- Four mismatched cost dates: 1991-01-02, 1995-01-03, 1998-01-02 and 2016-01-04.
- Summed excess returns fall by 20 basis points after the missing costs are charged. This is an additive return
  difference, not a compounded wealth difference.
- Conventional annualized walk-forward Sharpe changes from 0.46678094 to 0.46641898, changing the three-decimal
  display from 0.467 to 0.466. The conclusion of insufficient superiority is not reversed by this diagnostic.

Required: add an independent transition-cost regression, fix accounting, preserve the old exploratory output,
and regenerate the affected output, tables, summary and PDFs with an explicit correction record. Reproduction
of the old bytes did not validate the original accounting.

Other manuscript corrections required before the next release:

- Replace 'every printed example in the four papers' with 'the selected numerical examples listed in Table ...'.
  The suite does not reproduce every empirical experiment and printed illustration in all four papers.
- Remove the contribution claim that a stepwise test was reported. The code reports a joint SPA-style maximum
  test, not the uncomputed Romano-Wolf stepwise procedure.
- Distinguish Sullivan-Timmermann-White's Sharpe-based Reality Check from Hansen's later SPA recentering.
  Define omega as sqrt(T) times the bootstrap SD of the estimated Sharpe difference, matching the code.
- Delete any prediction of what an uncomputed Romano-Wolf procedure would conclude. Its outcome is unmeasured.
- Identify the industry start date as the chosen first July after the final missing-value date, not the first day
  on which all 49 industries had data. No change in the data window is needed.
- Describe minimum detectable differences and illustrative power as Normal-shift approximations conditional on
  the estimated SE remaining fixed. They are not measured power of the complete search-and-selection procedure.
- Describe full-window/subperiod averaging as a descriptive observation, not a decomposition of bootstrap rates.
- The calibration-loop pseudocode should not claim an independent child seed per dataset: child streams are
  assigned by scenario/block/check and datasets are drawn sequentially from those streams.

## 2. Resolve data recovery without overclaiming permissions or permanence

The current exact industry bytes should be preserved before the rolling endpoint changes. Preferred end state:
a provider-supported immutable source or an authorized repository deposit with clear access/redistribution terms.
An Internet Archive capture of the existing public URL is a practical additional recovery route, not a guarantee
of perpetual availability and not a software/data licence.

Before describing capture as successful: retrieve the resulting binary capture independently, verify the frozen
SHA-256, record capture URL/time and digest, and exercise the documented acquisition route from an empty data
cache. Keep local untouched copies. Do not rehost the ZIP under the project's software licence without a clear
basis for data redistribution. A DOI for code/results does not itself archive the required data.

No public capture request or dataset upload was made in this review. Such an outward-facing action still needs
explicit owner authorization. The reported matching factor capture should also be tested through the final
fresh-copy reproduction procedure rather than treated as an unlimited durability guarantee.

## 3. Finish the literature assessment in order of relevance

Obtain lawful full text from a library, publisher entitlement or author-provided manuscript:

1. Lopez de Prado and Porcu's unified DSR framework: closest overlap with the DSR interpretation and novelty.
2. The 2026 Sharpe-inference/reporting paper: relevant to dependence, benchmarks and power.
3. The 2026 GARCH paper: essential if adding positive-benchmark/GARCH experiments, or making broad GARCH claims.

Direct full-text access failed in this review. Available abstract, metadata and companion code must not be
represented as inspected proofs. Build a short comparison table: formulation, null, assumptions, adjustment,
known operating characteristics, and what this study actually evaluates. Retain the explicit 2014-only scope
until a broader comparison is justified. No priority claim follows from absence of an example in the older paper.

Metadata correction: SSRN 6568702 currently identifies *Signal-to-Noise Ratio Inference under Volatility Clustering
and Heavy Tails*, revised 28 September 2026. If retaining the older GARCH title, identify that exact older version;
otherwise update the bibliography and access note to the current record.

## 4. Resolve reference status precisely

A DOI or Crossref entry is not required for a valid chapter or research note. Separate metadata verification,
full-text inspection and secondary attribution.

- Memmel (2003), *Performance Hypothesis Testing with the Sharpe Ratio*, Finance Letters 1, 21-23:
  metadata confirmed in the author's Deutsche Bundesbank bibliography. Full text was not inspected here.
  Say 'no DOI located', not 'no DOI'.
  https://www.bundesbank.de/en/christoph-memmel
- Politis and Romano (1992), *A Circular Block-Resampling Procedure for Stationary Data*, in LePage and Billard
  (eds.), *Exploring the Limits of Bootstrap*, Wiley, 263-270: metadata corroborated by author/institutional
  bibliographies. Distinguish the March 1991 Stanford precursor, EFS NSF 370, from the 1992 chapter.
  https://mathweb.ucsd.edu/~politis/DPpublication.html
  https://statistics.stanford.edu/technical-reports/circular-block-resampling-procedure-stationary-data
- Mertens: the author's working-papers page links *Correct variance for estimated Sharpe Ratios*, a comment on
  Lo (2002). The linked PDF was not successfully read. Exact document title/date/institution remain unverified.
  Until obtained, use 'Mertens, as cited by Bailey and Lopez de Prado (2012)' for the historical attribution;
  the inspected SF formula is sufficient for the actual implemented equation. Do not invent a registry record.
  https://www.elmarmertens.com/research/workingpapers

## 5. Freeze the scientific scope

The untested items are not all defects that need another experiment. For the present working paper:

- Keep PBO decision power, positive-benchmark PSR/MinTRL calibration, Romano-Wolf StepM and broader markets
  outside scope. Remove any result-like implication about them.
- State that block lengths and bandwidths are specified modeling choices. If one additional scientific study is
  justified by external review, prioritize a pre-recorded dependence/bandwidth sensitivity over adding many tests.
- A measured PBO power study would be a separate extension with an explicit decision rule, horizon-matched
  signal, uncertainty target and prediction; it should not be quietly appended to improve the story.

The evidence rule and walk-forward design cannot become prospective by owner approval after the fact.
Keep their chronology and exploratory status. A new validation requires a design fixed before genuinely unused
outcomes are inspected; re-labelling the existing full-history analysis is not prospective validation.

## 6. Make a version that a technical reviewer can inspect quickly

After the repairs above, produce a reviewed release with:

- One clear README entry path: research question, one-page summary, paper, reproduction instructions and limits.
- A source commit for computations, a named working-paper release/tag, and hashes of the released PDFs/results.
  The manuscript should cite the computation commit; do not attempt to embed a commit's own hash inside itself.
- An installation/reproduction check in a clean directory/environment. Distinguish absent-data skips from a
  completed data-backed test. Run fast deterministic tests in CI; keep long simulations separately invocable.
- A correction log and the original outputs. Present findings as verified under their assumptions, not as
  'peer-reviewed' or 'journal published' before either is true.
- An external technical read, if available, of the estimands, bootstrap/null construction, selection correction
  and executable-cost accounting. Internal review is not independent external peer review.

The useful professional signal is the ability to defend a clear question, reconstruct the evidence, detect a flaw,
repair it transparently and explain what the result does not establish. Extra page count or a larger test count
cannot substitute for that. No outcome with recruiters or employers is guaranteed by this package.
