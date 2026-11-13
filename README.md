# Backtest-overfitting statistics: replication and extensions

This repository reproduces published Sharpe-ratio, PSR, DSR, MinTRL, MinBTL and CSCV/PBO calculations,
then examines their behavior in controlled simulations and an idealized market-factor strategy search.
It accompanies the [working manuscript](docs/writeup.md), revised after a
[publication audit](docs/publication_audit.md) and a [panel review](docs/peer_review_round1.md). It does not
establish an executable trading strategy or certify future performance.

## Start here

- [One-page research summary](docs/submission/research-summary.pdf).
- [Working paper](docs/submission/research-paper.pdf), [source](docs/submission/research-paper.tex), and [reproduction instructions](docs/submission/reproducibility.md).
- [Earlier manuscript](docs/writeup.md): project-level questions, methods, results and correction history.
- [Progress and corrections](PROGRESS.md): recorded designs, predictions, results and withdrawn claims.
- [Roadmap](docs/TODO.md): review and sign-off state.
- [Methods supplement](docs/research_methods.md): estimands, assumptions, generators, nulls and inference conventions.
- [Data manifest](docs/data_manifest.md): required snapshots, hashes, transformations and reproduction limits.
- [Paper checks](docs/paper_check.md): page-level verification record; constants live in `src/pbo/paper_values.py`.

The original G6 period comparison did not impose zero means within each period. Its calibration interpretation
is withdrawn. `experiments/g6_corrected.py` centers each period separately (design committed before the run,
d78d8e8) and wrote `results/g6_corrected.txt`; the original output is retained in `results/french_followups.txt`.

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

**Both frozen inputs now have independently hash-verified timestamped recovery URLs.** Use the capture URLs
in the [data manifest](docs/data_manifest.md) and [machine-readable recovery record](docs/submission/data-recovery.json)
before running the loaders. The default loader still downloads the rolling provider URL if a ZIP is absent and
refuses a mismatching hash; do not disable that check. Data remain outside Git and are not licensed under MIT.
Archival availability is not a guarantee of perpetual access or permission to redistribute the data.

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
| `g6_corrected.py` | `g6_corrected.txt` | Frozen industry archive; uses `french_bootstrap.py` and `french_followups.py` settings |
| `manuscript_numbers.py` | `manuscript_numbers.txt` | Saved results and frozen factor archive; derived statistics only |
| `ma_crossover.py` | `ma_crossover.txt` | Frozen factor archive |
| `market_comparison.py` | `market_comparison.txt` | Frozen factor archive |
| `figure_psr_ar1.py` | `psr_ar1_curve.txt`, `figure1_psr_ar1.png` | Saved calibration output and analytic approximation |

Calibration and bootstrap scripts perform many simulations and can take minutes. Settings, fixed seeds and
process-pool entry points are defined in the scripts. Monte Carlo intervals quantify simulation uncertainty
conditional on each specified data-generating process; they do not remove model or historical-sample uncertainty.

The code is released under the [MIT License](LICENSE). Data access and redistribution conditions are separate
from the software license and are not granted by it.
