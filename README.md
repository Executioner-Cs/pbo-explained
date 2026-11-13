# Backtest-overfitting statistics: replication and extensions

This repository reproduces published Sharpe-ratio, PSR, DSR, MinTRL, MinBTL and CSCV/PBO calculations,
then examines their behavior in controlled simulations and an idealized market-factor strategy search.
It accompanies the [working manuscript](docs/writeup.md), which is **under correction** following a
[publication audit](docs/publication_audit.md). It does not establish an executable trading strategy or
certify future performance.

## Start here

- [Manuscript](docs/writeup.md): questions, methods, results, limitations and references.
- [Progress and corrections](PROGRESS.md): recorded designs, predictions, results and withdrawn claims.
- [Roadmap](docs/TODO.md): review and sign-off state.
- [Methods supplement](docs/research_methods.md): estimands, assumptions, generators, nulls and inference conventions.
- [Data manifest](docs/data_manifest.md): required snapshots, hashes, transformations and reproduction limits.
- [Paper checks](docs/paper_check.md): page-level verification record; constants live in `src/pbo/paper_values.py`.

The original G6 period comparison did not impose zero means within each period. Its calibration interpretation
is withdrawn. `experiments/g6_corrected.py` centers each period separately; its design and prediction are
recorded, but its simulation remains pending the pre-run commit and review workflow. The original output is
retained in `results/french_followups.txt`; a corrected run writes only `results/g6_corrected.txt`.

## Environment and tests

Use Python 3.13 and run commands from the repository root. Create a virtual environment for the platform
you are using; a Windows environment and a WSL environment are not interchangeable.

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

WSL/Linux:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q
```

`requirements.txt` pins the recorded top-level package versions and installs this package in editable mode.
It is not a complete transitive dependency lock. For a development install using the declared version ranges,
use the same virtual-environment interpreter with `-m pip install -e ".[dev,figure]"`; the `figure` extra installs
matplotlib for the plot script.

The normal test command does not run the experiment scripts. Most tests use synthetic inputs. Frozen-data
tests are skipped when their ignored snapshots are absent, so passing tests alone do not establish that the
real-data experiments can be reproduced.

## Data and reproduction

**A fresh clone does not currently supply a durable route to the exact frozen input bytes.** The loader
downloads a rolling French Data Library URL if a local ZIP is absent, then rejects bytes with a different
hash. SHA-256 detects a revised snapshot; it cannot recover the original. Obtain the exact archives listed in
the [manifest](docs/data_manifest.md), put them in `data/` without extracting or modifying them, and retain
the hash checks. An immutable provisioning location is still a publication requirement.

After provisioning both archives, this check reads and validates them without writing any experiment result:

```bash
.venv/bin/python -c "from pbo.french import load_returns, load_market; load_returns(); load_market(); print('Frozen snapshots validated')"
```

On Windows, replace `.venv/bin/python` with `.\.venv\Scripts\python.exe`. If an archive is absent, the loader
attempts a download; the check is not an offline acquisition procedure.

## Experiment entry points

Saved outputs are in `results/`. The following scripts are regeneration commands, not part of the test suite.
Except for the separately named corrected G6 output, **each script overwrites its named result files**.
Preserve the published originals and follow the recorded correction design before rerunning an affected analysis.
Run scripts directly, for example `.venv/bin/python experiments/best_of_n.py`; some older scripts use sibling
imports and are not supported through `python -m experiments...`.

| Script in `experiments/` | Output in `results/` | Inputs |
|---|---|---|
| `best_of_n.py` | `best_of_n.txt` | Seeded synthetic returns |
| `dsr_false_positives.py` | `dsr_false_positives.txt` | Seeded synthetic returns |
| `null_checks.py` | `null_checks.txt` | Seeded synthetic returns |
| `calibration.py` | `calibration.txt` | Seeded synthetic scenarios |
| `french_bootstrap.py` | `french_bootstrap.txt` | Frozen industry archive |
| `french_followups.py` | `french_followups.txt` | Frozen industry archive and bootstrap output; includes historical, uncentered G6 |
| `g6_corrected.py` | `g6_corrected.txt` | Frozen industry archive; corrected run pending |
| `ma_crossover.py` | `ma_crossover.txt` | Frozen factor archive |
| `market_comparison.py` | `market_comparison.txt` | Frozen factor archive |
| `figure_psr_ar1.py` | `psr_ar1_curve.txt`, `figure1_psr_ar1.png` | Saved calibration output and analytic approximation |

Calibration and bootstrap scripts perform many simulations and can take minutes. Settings, fixed seeds and
process-pool entry points are defined in the scripts. Monte Carlo intervals quantify simulation uncertainty
conditional on each specified data-generating process; they do not remove model or historical-sample uncertainty.

No software license is supplied yet. The project owner must select one before permission to reuse the code
can be stated. Data access and redistribution conditions are separate from the software license.
