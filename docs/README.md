# Documentation

## Read the research

| Document | Use it for |
|---|---|
| **[Working paper](working-paper.pdf)** | The complete argument, methods, results, references and correction history (34 pages). |
| **[Research brief](research-brief.pdf)** | A one-page overview of the question, principal findings and caveats. |

Both describe the same study; the brief is a summary, not another manuscript version. This is a working paper; external peer review has not been completed. LaTeX, bibliography and figure sources are in [`source/`](source/). File digests are in [`checksums.sha256`](checksums.sha256).

## Check the research

| Your question | Read this |
|---|---|
| How do I reproduce the results? | [Reproduction guide](reproducibility.md) |
| What was actually checked? | [Verification record](verification.md) |
| Which code and output support each claim? | [Evidence map](evidence.md) |
| What are the estimands and design choices? | [Research design](methods/research-design.md) |
| How do implementation conventions work? | [CSCV](methods/cscv.md), [PSR/MinTRL/DSR](methods/psr-dsr.md), [delayed-execution sensitivity design](methods/delayed-alpha-design.md) |
| Which exact data do I need? | [Data manifest](data-manifest.md) |
| Which source papers were used, in which versions? | [Source manifest](source-manifest.md) |
| Where did the printed paper constants come from? | [Paper checks](paper-checks.md) |
| How does this relate to prior work? | [Literature review](literature-review.md) |
| What remains uncertain? | [Limitations](limitations.md), [roadmap](TODO.md) |

Earlier drafts and superseded outputs remain in Git history. Rebuild the PDFs from the repository root with `python scripts/build_paper.py` (requires Tectonic).
