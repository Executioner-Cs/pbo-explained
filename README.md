# Backtest overfitting: when a good backtest meets a harder question

A computational replication and empirical stress test of the statistics used to screen backtests: the probabilistic
and deflated Sharpe ratios (PSR, DSR), minimum track record and backtest lengths (MinTRL, MinBTL), and the probability
of backtest overfitting (PBO) estimated by combinatorially symmetric cross-validation (CSCV).

**Question.** Are these statistics reliable decision rules when returns are serially dependent, heavy tailed or
correlated, and does a historically superior trading rule survive a selection-aware test against the market?

**Short answer (RECOMPUTED).** In the stated zero-mean industry bootstraps, uncorrected PSR passes
8.35% of early-period samples and 3.85% of late-period samples against a nominal 5%; only the early excess survives
the stated Holm adjustment. The operational 2014 DSR is strongly conservative under independent zero-skill search.
The best of 93 moving-average settings has zero-skill DSR 0.998, but its standalone Sharpe advantage is not established
(SPA p = 0.504). Baseline market-alpha evidence is exploratory and borderline; an extra day of execution delay gives
alpha SPA p = 0.084. DSR of active returns, standalone Sharpe differences and market alpha answer different questions.
No implementable trading edge or new statistic is claimed.

## Read first

[![Tests](https://github.com/Executioner-Cs/pbo-explained/actions/workflows/tests.yml/badge.svg)](https://github.com/Executioner-Cs/pbo-explained/actions/workflows/tests.yml)

**Working paper · 34 pages · one-page brief · Python 3.13 · MIT code licence**


1. [One-page research brief](docs/submission/research-brief.pdf)
2. [Working paper](docs/submission/final-research-paper.pdf) (LaTeX source and bibliography in the same folder)
3. [How to reproduce every number](docs/submission/reproducibility.md)

Supporting documents in [`docs/submission/`](docs/submission/): claim-by-claim [evidence audit](docs/submission/evidence-audit.md),
[literature review](docs/submission/literature-review.md), [limitations and open issues](docs/submission/limitations-and-open-issues.md),
and [release verification](docs/submission/release-verification.md). See the [documentation index](docs/README.md) for methods and provenance. The full internal review archive stays local; public methods, correction history, code and numerical outputs are included.

## Repository map

```text
src/pbo/        Library: Sharpe, PSR/MinTRL/DSR, CSCV/PBO, MinBTL, data loaders, scenarios, strategies
tests/          Unit tests; expectations come only from paper values or closed forms
experiments/    One script per analysis; each writes one file in results/
results/        Current reproducible outputs quoted in the paper
docs/submission The paper and its companion documents
docs/           Research records: methods supplement, data manifest, paper checks, audits, roadmap
PROGRESS.md     Current verified state and correction summary
```

## Setup and tests

Python 3.13, from the repository root. A Windows and a WSL virtual environment are not interchangeable.

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q          # 296 tests
```

On Windows use `py -3.13 -m venv .venv` and `.\.venv\Scripts\python.exe`.

## Data

The real-data analyses use two Kenneth R. French Data Library archives, identified by SHA-256 in `src/pbo/french.py`.
Both exact files are preserved by the Internet Archive; [reproducibility.md](docs/submission/reproducibility.md) gives the
download commands. The loader refuses any file with a different hash. Without the archives, the data-dependent tests
skip, so passing tests alone do not reproduce the real-data results.

## What is included

- Library implementations, paper-value provenance and deterministic tests.
- Fixed-seed synthetic studies, corrected industry bootstraps and a 93-rule market case study.
- Final saved results and a documented correction history; superseded files remain in Git history.
- LaTeX, bibliography, vector figures, the full paper and the one-page brief.
- [Added delayed-execution alpha experiment](experiments/delayed_alpha.py), its [design](docs/submission/evidence/delayed-alpha-design.md), [output](results/delayed_alpha.txt) and [raw bootstrap vectors](results/delayed_alpha_bootstrap.npz).

The local full suite passes 296 tests with the frozen archives present. Hosted CI skips the two archive-dependent checks when those inputs are absent; a green badge alone does not reproduce the empirical findings.

## Regenerating results

Each script overwrites its own result file, for example `.venv/bin/python experiments/calibration.py`. Run them in a copy
of the repository if you want to compare with the saved outputs; the procedure and expected run times are in
[reproducibility.md](docs/submission/reproducibility.md). `experiments/submission_figures.py` rebuilds the paper's figures
from the saved results.

## License

Code: [MIT](LICENSE). The data are not covered by this licence and are not redistributed here.
