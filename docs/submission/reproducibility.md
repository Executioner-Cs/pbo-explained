# Reproducibility

How to rebuild every number, table and figure in `research-paper.pdf`, what was actually re-executed for this
version, and what cannot yet be reproduced from a fresh copy.

## 1. Environment

| Item | Value used for this version |
|---|---|
| OS | Ubuntu 22.04 under WSL2 on Windows 11 (all runs); Windows-native `.venv` not used |
| Python | 3.13.18 |
| Packages | numpy 2.5.4, scipy 1.18.1, matplotlib 3.11.2, pytest 9.2.0; full list in [`environment-lock.txt`](environment-lock.txt) |
| TeX | Tectonic 0.15.0 (x86_64-unknown-linux-musl), fetches its TeX bundle over the network on first use |
| PDF inspection | PyMuPDF in a separate scratch virtual environment (not a project dependency) |

`requirements.txt` pins the top-level packages; `environment-lock.txt` is the full `pip freeze` of the environment that
produced the outputs. Setup from the repository root:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt     # installs pbo-explained in editable mode
```

## 2. Input data

| Archive (place unmodified in `data/`) | SHA-256 | Durable source |
|---|---|---|
| `49_Industry_Portfolios_daily_CSV.zip` | `b9d36d571e968d71f7b03207e7fed6398554f953719b8c1bf3ee3ad8d00e7520` | Internet Archive capture `20261113053423` (independent retrieval/hash verified) |
| `F-F_Research_Data_Factors_daily_CSV.zip` | `96c23b88e651cbfff3740a53f8225e59ee39893371e96385a1d8125ec2cd9c89` | Internet Archive capture `20261030074337` (verified) |

Checks performed on 2026-11-12:

- Local archives in `data/` hash to the values above.
- The rolling French Data Library URLs returned bytes with **both** hashes on 2026-11-12. The loader
  (`pbo.french.read_snapshot`) downloads the rolling URL when `data/` is empty and refuses any other bytes, so a fresh
  copy reproduces the inputs **only while the library still serves this release**.
- The Internet Archive CDX index lists four 2026 captures of the factor ZIP. The capture of 2026-10-30 has SHA-1
  digest `SKQU4RLWQKRR4JE5IGEHUQ7SPPKJOIT3`, identical to the local file; the downloaded capture has the frozen
  SHA-256. Retrieval:

  ```bash
  curl -L -o data/F-F_Research_Data_Factors_daily_CSV.zip \
    "https://web.archive.org/web/20261030074337id_/https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_daily_CSV.zip"
  sha256sum data/F-F_Research_Data_Factors_daily_CSV.zip
  ```

- A new capture of the original public industry URL was requested on 2026-11-13 UTC. The capture response
  pointed to timestamp `20261113053423`; an independent GET of its raw binary replay returned 4,177,116 bytes
  with the frozen industry SHA-256. No locally uploaded replacement was used.

  ```bash
  mkdir -p data
  curl --fail --location -o data/49_Industry_Portfolios_daily_CSV.zip \
    "https://web.archive.org/web/20261113053423id_/https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/49_Industry_Portfolios_daily_CSV.zip"
  sha256sum data/49_Industry_Portfolios_daily_CSV.zip
  ```

Both captures were retrieved independently and hashed; [data-recovery.json](data-recovery.json) records the exact
URLs, timestamps, byte lengths and digests. Data are not included in the software release or licensed by MIT.
A timestamped public recovery route does not guarantee perpetual availability or grant redistribution rights.

Validate both archives without running experiments:

```bash
.venv/bin/python -c "from pbo.french import load_returns, load_market; load_returns(); load_market(); print('Frozen snapshots validated')"
```

### Alternative reproduction (clearly not the published numbers)

If the frozen industry bytes become unavailable, the experiments can be rerun on a newer release only by
(1) downloading the new archives, (2) changing the expected hashes in `src/pbo/french.py`, which defines a new dataset,
and (3) writing outputs to new result files. Results will differ because the library revises history. Such a rerun
tests robustness to data vintage; it does not reproduce this paper. Keep the hash check enabled.

## 3. Tests

```bash
.venv/bin/python -m pytest -q
```

Recorded outcome for this version (2026-11-12, frozen archives present): **285 passed**, no skips (279 before the
walk-forward cost fix added six `position_returns` tests).
With `data/` empty, the frozen-data tests skip, so a green suite does not by itself establish real-data reproduction.

## 4. Experiments

Every script overwrites its own file in `results/`. To check reproduction without touching the archived outputs, copy
the repository (without `.venv`) to a scratch directory and run there with `PYTHONPATH` set to the copy's `src/`, as
done for this version:

```bash
mkdir ~/pbo_repro && tar --exclude=.venv --exclude=.git -cf - . | tar -xf - -C ~/pbo_repro
cd ~/pbo_repro && cp -r results results_orig
export PYTHONPATH=$PWD/src
for s in best_of_n dsr_false_positives null_checks calibration french_bootstrap french_followups g6_corrected \
         ma_crossover market_comparison case_study_checks performance_checks manuscript_numbers figure_psr_ar1 figures; do
  /path/to/repo/.venv/bin/python experiments/$s.py
done
for f in results_orig/*; do cmp -s "$f" "results/$(basename "$f")" && echo "same $f" || echo "DIFF $f"; done
```

Order matters: `manuscript_numbers.py` reads other saved results, and `figures.py` must run last.

### Outcome of the full rerun (2026-11-12, 12 cores)

| Script | Wall time | Output vs archived file |
|---|---|---|
| best_of_n | 20 s | identical |
| dsr_false_positives | 21 s | identical |
| null_checks | 43 s | identical |
| calibration | 350 s | identical |
| french_bootstrap | 72 s | identical |
| french_followups | 117 s | content differs in 3 approximation values (see below); archived file has CRLF line endings |
| g6_corrected | 16 s | identical |
| ma_crossover | 12 s | identical |
| market_comparison | 12 s | identical |
| case_study_checks | 31 s | identical |
| performance_checks | 11 s | identical at the time; **later corrected** (walk-forward switch costs). Original kept as `results/performance_checks_v1_stitched_costs.txt`; regenerated file differs in the walk-forward Sharpe (0.467 -> 0.466), Sortino (0.630 -> 0.629) and difference (-0.069 -> -0.070, p 0.7417 -> 0.7428). After the fix, `ma_crossover`, `market_comparison` and `case_study_checks` were rerun in the isolated copy and remain byte-identical |
| manuscript_numbers | 11 s | identical |
| figure_psr_ar1 | 17 s | identical text and PNG |
| figures | 28 s | identical text and all six PNGs |

`french_followups.txt` difference, all of it: predicted rate at L = 60 `0.0538 -> 0.0539` (z `+1.72 -> +1.71`);
early-period predicted rate `0.0838 -> 0.0837` (z `+3.34 -> +3.35`), printed twice. This is the documented effect of
the later partial-final-block correction to `block_bootstrap_factor` (PROGRESS.md, "Corrections after the publication
audit"); the archived file is deliberately kept as the original. Every simulated count is identical.

## 5. Submission figures and PDF

```bash
.venv/bin/python experiments/submission_figures.py          # writes docs/submission/figures/*.pdf; reads results/ only
cd docs/submission
tectonic research-paper.tex                                  # runs BibTeX automatically
tectonic research-summary.tex
```

`submission_figures.py` runs no simulation and writes nothing to `results/`. Its two analytic curves are the
expected-maximum approximation (PSEUDO Eq. 2.4) and exact Normal-maximum quadrature.

## 6. Seeds

| Seed | Used by |
|---|---|
| 20261109 | `best_of_n.py` |
| 20261110 | `dsr_false_positives.py`, `calibration.py`, `null_checks.py` (IID) |
| 20261112 | `french_bootstrap.py` |
| 20261113 | `french_followups.py`, `g6_corrected.py` (children 9 and 10 of `SeedSequence(20261113).spawn(11)`) |
| 20261114 | `null_checks.py` (AR(1) and GARCH noise) |
| 20261115 | `case_study_checks.py` (stationary bootstrap for SPA) |

## 7. Numerical tolerances

Test tolerances are half a unit in the last printed digit for paper values (`src/pbo/paper_values.py`). Domain checks
use a 1e-12 relative tolerance on Pearson's skew/kurtosis bound and accept correlation eigenvalues down to
-1e-10 times dimension. Byte-identical reruns above mean that no tolerance was needed to declare agreement.
