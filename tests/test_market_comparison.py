"""Follow-up orchestration on synthetic data only; never load or write real experiment results."""
import importlib
from pathlib import Path
import runpy
import sys

import numpy as np
import pytest

from pbo import french, reporting

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "market_comparison.py"


def test_experiment_imports_do_not_load_data_or_write_results(monkeypatch, capsys):
    def unexpected(*args, **kwargs):
        raise AssertionError("import triggered an experiment side effect")

    monkeypatch.setattr(french, "load_market", unexpected)
    monkeypatch.setattr(reporting, "save_results", unexpected)
    monkeypatch.syspath_prepend(str(ROOT))
    for name in ("ma_crossover", "market_comparison"):
        module = f"experiments.{name}"
        monkeypatch.delitem(sys.modules, module, raising=False)
        importlib.import_module(module)
        runpy.run_path(ROOT / "experiments" / f"{name}.py", run_name="import_check")
        sys.modules.pop(module)  # Do not retain aliases to the patched I/O functions.
    assert capsys.readouterr().out == ""


def synthetic_script(monkeypatch):
    main = runpy.run_path(SCRIPT, run_name="synthetic_check")["main"]
    market = 0.001 + 0.0001 * np.sin(np.arange(400))
    saved = []
    monkeypatch.setitem(main.__globals__, "load_market", lambda: (np.arange(400), market, np.zeros(400)))
    monkeypatch.setitem(main.__globals__, "save_results", lambda name, lines: saved.append((name, lines)))
    return main, saved


def test_synthetic_pipeline_reports_every_setting_and_primary_first(monkeypatch, capsys):
    main, saved = synthetic_script(monkeypatch)
    calls = []

    def comparison(x, y, lags):
        assert x.shape == y.shape == (144,)  # 400 rows minus 250 warm-up and 6 leading remainder rows
        calls.append(lags)
        return 0.0, 1.0  # z=0 has exactly one-sided p=1/2, Bonferroni-adjusted p=1

    monkeypatch.setitem(main.__globals__, "sharpe_diff", comparison)
    main()
    # Lag rule int(4 (T/100)^(2/9)) at the synthetic T = 144 gives 4; sensitivities 0 and 4 x 4 (11 and 44 at T = 13664).
    assert calls == [4] * 93 + [0] * 93 + [16] * 93
    assert len(saved) == 1 and saved[0][0] == "market_comparison"
    lines = saved[0][1]
    assert capsys.readouterr().out == "\n".join(lines) + "\n"
    summaries = [line for line in lines if line.startswith("Bartlett")]
    assert [line.split(":")[0] for line in summaries] == [
        "Bartlett lags = 4 (primary)", "Bartlett lags = 0 (sensitivity)", "Bartlett lags = 16 (sensitivity)",
    ]
    rows = [line.split() for line in lines if len(line.split()) == 8 and line.split()[0].isdigit()]
    assert len(rows) == len({tuple(row[:2]) for row in rows}) == 93
    assert rows[0][:2] == ["5", "25"] and rows[-1][:2] == ["50", "250"]
    for row in rows:
        assert float(row[2]) == 0
        assert float(row[3]) == pytest.approx(np.sqrt(250), abs=0.0005)
        assert [float(value) for value in row[4:]] == [0.5, 1.0, 1.0, 1.0]


def test_zero_standard_error_stops_before_saving(monkeypatch):
    main, saved = synthetic_script(monkeypatch)
    monkeypatch.setitem(main.__globals__, "sharpe_diff", lambda *args: (0.0, 0.0))
    with pytest.raises(ValueError, match="positive finite standard errors"):
        main()
    assert saved == []
