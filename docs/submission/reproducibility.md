# Reproducibility

How to rebuild every number, table and figure in `final-research-paper.pdf`, and what was verified for this version.

## 1. Environment

All runs used Ubuntu 22.04 under WSL2, Python 3.13.18, and this exact package set (`pip freeze` of the project
virtual environment):

```text
colorama==0.4.6      contourpy==1.4.0     cycler==0.12.1       fonttools==4.68.0
iniconfig==2.3.1     kiwisolver==1.5.1    matplotlib==3.11.2   numpy==2.5.4
packaging==26.3      pillow==13.0.0       pluggy==1.7.0        Pygments==2.21.0
pyparsing==3.3.3     pytest==9.2.0        python-dateutil==4.0.0
scipy==1.18.1        tzdata==2026.6       pbo-explained==0.1.0 (editable)
```

Setup from the repository root:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt     # pins numpy, scipy, matplotlib, pytest; installs pbo
```

On Windows use `.venv\Scripts\python.exe`. A Windows and a WSL virtual environment are not interchangeable.

## 2. Input data

| Archive (place unmodified in `data/`) | SHA-256 | Bytes | Permanent copy |
|---|---|---|---|
| `49_Industry_Portfolios_daily_CSV.zip` | `b9d36d571e968d71f7b03207e7fed6398554f953719b8c1bf3ee3ad8d00e7520` | 4,177,116 | Internet Archive capture `20261113053423` |
| `F-F_Research_Data_Factors_daily_CSV.zip` | `96c23b88e651cbfff3740a53f8225e59ee39893371e96385a1d8125ec2cd9c89` | 178,326 | Internet Archive capture `20261030074337` |

Both captures were downloaded independently and match the SHA-256 above (factor archive verified 2026-11-12,
industry archive 2026-11-13). Retrieve them with:

```bash
mkdir -p data
curl -L -o data/49_Industry_Portfolios_daily_CSV.zip \
  "https://web.archive.org/web/20261113053423id_/https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_daily_CSV.zip"
curl -L -o data/F-F_Research_Data_Factors_daily_CSV.zip \
  "https://web.archive.org/web/20261030074337id_/https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"
sha256sum data/*.zip
```

If `data/` is empty, the loader (`pbo.french.read_snapshot`) downloads the rolling French Data Library URL and refuses
any bytes whose hash differs; on 2026-11-12 the rolling URLs still served both frozen files. Validate without running
any experiment:

```bash
.venv/bin/python -c "from pbo.french import load_returns, load_market; load_returns(); load_market(); print('ok')"
```

The data belong to the Kenneth R. French Data Library. They are not committed to this repository and are not covered
by its MIT licence; an archived copy does not grant redistribution rights.

**Other data vintages.** To test robustness to a newer release, download it, change the expected hashes in
`src/pbo/french.py` (this defines a new dataset), and write outputs to new result files. The numbers will differ; such a
run does not reproduce this paper.

## 3. Tests

```bash
.venv/bin/python -m pytest -q
```

Outcome for this version (2026-11-13, archives present): **296 passed**, no skips. With `data/` empty the frozen-data
tests skip, so a passing suite alone does not show that the real-data experiments reproduce.

## 4. Experiments

Each script writes its own file in `results/` and overwrites it. To check reproduction without touching the archived
outputs, run in a copy:

```bash
mkdir ~/pbo_repro && tar --exclude=.venv --exclude=.git -cf - . | tar -xf - -C ~/pbo_repro
cd ~/pbo_repro && cp -r results results_orig && export PYTHONPATH=$PWD/src
for s in best_of_n dsr_false_positives null_checks calibration french_bootstrap french_followups g6_corrected \
         ma_crossover market_comparison case_study_checks performance_checks manuscript_numbers review_checks submission_figures; do
  /path/to/repo/.venv/bin/python experiments/$s.py
done
for f in results_orig/*.txt; do cmp -s "$f" "results/$(basename "$f")" && echo "same $f" || echo "DIFF $f"; done
```

`manuscript_numbers.py` reads other saved results, so run it after them; `submission_figures.py` runs last.

| Script | Output in `results/` | Wall time (12 cores) | Verified |
|---|---|---|---|
| `best_of_n.py` | `best_of_n.txt` | 20 s | identical |
| `dsr_false_positives.py` | `dsr_false_positives.txt` | 21 s | identical |
| `null_checks.py` | `null_checks.txt` | 43 s | identical |
| `calibration.py` | `calibration.txt` | 350 s | identical |
| `french_bootstrap.py` | `french_bootstrap.txt` | 72 s | identical |
| `french_followups.py` | `french_followups.txt` | 117 s | see note 1 |
| `g6_corrected.py` | `g6_corrected.txt` | 16 s | identical |
| `ma_crossover.py` | `ma_crossover.txt` | 12 s | identical, also after the cost fix |
| `market_comparison.py` | `market_comparison.txt` | 12 s | identical, also after the cost fix |
| `case_study_checks.py` | `case_study_checks.txt` | 31 s | identical, also after the cost fix |
| `performance_checks.py` | `performance_checks.txt` | 11 s | see note 2 |
| `manuscript_numbers.py` | `manuscript_numbers.txt` | 11 s | identical |
| `review_checks.py` | `review_checks.txt` | see final execution log | final continuation rerun recorded separately |
| `submission_figures.py` | `psr_ar1_curve.txt`, `fig7_dsr_vs_n.txt`; PDFs in `docs/submission/figures/` | 30 s | both text files identical |

1. `french_followups.txt` was regenerated with the current partial-final-block correction. The original is preserved in
   the historical results tree at commit `f1f8a3e`. L = 60 changes 0.0538 to 0.0539 (z +1.72 to +1.71); the early-period
   approximation changes 0.0838 to 0.0837 in two places (early z +3.34 to +3.35). Every simulated count is identical.
   The correction appendix records the reconciliation; the superseded output is recoverable from Git history at `f1f8a3e`.
2. `performance_checks.txt` was regenerated after the walk-forward cost correction (Sharpe 0.467 to 0.466, Sortino 0.630
   to 0.629, difference -0.069 to -0.070, p 0.7417 to 0.7428). The original is preserved in
   the historical results tree at commit `f1f8a3e`.

## 5. Paper and summary

```bash
cd docs/submission
tectonic final-research-paper.tex        # Tectonic 0.15.0; runs BibTeX itself; downloads its TeX bundle on first use
tectonic research-brief.tex
```

The final page count, actual visual inspection and PDF hashes are recorded in `release-verification.md` and the public release checksums. Tectonic can emit underfull bibliography-box and repeated-BibTeX consistency warnings; those are not a warning-free build. Undefined citations and overfull boxes are checked separately, followed by visual inspection.

## 6. Seeds

| Seed | Used by |
|---|---|
| 20261109 | `best_of_n.py` |
| 20261110 | `dsr_false_positives.py`, `calibration.py`, `null_checks.py` (IID) |
| 20261112 | `french_bootstrap.py` |
| 20261113 | `french_followups.py`; `g6_corrected.py` uses children 9 and 10 of `SeedSequence(20261113).spawn(11)` |
| 20261114 | `null_checks.py` (AR(1) and GARCH noise) |
| 20261115 | `case_study_checks.py` (stationary bootstrap for SPA) |

## 7. Tolerances

Tests compare paper values to half a unit in the last printed digit (`src/pbo/paper_values.py`). Domain checks use a
1e-12 relative tolerance on Pearson's skewness-kurtosis bound and accept correlation eigenvalues down to -1e-10 times the
dimension. The reruns above matched byte for byte, so no tolerance was needed to declare agreement.


## 8. Added delayed-execution alpha check

From the repository root:

```bash
.venv/bin/python experiments/delayed_alpha.py
```

The [pre-run design](evidence/delayed-alpha-design.md) is exploratory and post hoc. The script writes `results/delayed_alpha.txt` and `results/delayed_alpha_bootstrap.npz`, including all 93 observed alphas and 2,000 joint bootstrap vectors. Fixed seed 20261118, execution delay 2 and mean block 20 are modeling choices. Expected result: SPA p = 0.084, with Monte Carlo s.e. 0.0062. This weakens the baseline borderline alpha inference; it does not prove alpha is absent.

## 9. Release verification and scope

See [release-verification.md](release-verification.md) for the actual tests, principal reruns, figure comparisons, page inspection and PDF digests. The final suite passed 296 tests with the frozen archives. A fresh dependency environment also passed 296 tests; the isolated main experiments used copied, hash-checked archives on the same machine. The full internal review archive is preserved locally and is not required to execute these public reproduction commands.

Tectonic 0.15.0 builds both documents from this folder. It downloads a TeX bundle on first use; the toolchain is not hermetically locked. Underfull bibliography lines and a repeated-BibTeX consistency/rerun warning were observed; no undefined citations or overfull boxes were found, followed by actual page inspection. Figure PDFs contain timestamps, so numerical and rendered equality are distinguished from binary equality. The PDFs have searchable text and embedded fonts but are untagged.

Public release tags identify immutable source revisions. The original reviewed baseline was commit `68882f58251dfa98adb0949c02f333d481ea2643` plus the preserved working tree. The final paper does not embed a later commit hash, avoiding a self-referential commit; release metadata and SHA-256 identify the exact artifact.
