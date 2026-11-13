"""Synthetic checks of the correction pipeline; no Monte Carlo runs or result-file writes."""
from pathlib import Path
import runpy

import numpy as np
from scipy.stats import beta


def test_g6_centers_periods_preserves_seeds_and_saves_only_correction(monkeypatch, capsys):
    directory = Path(__file__).resolve().parents[1] / "experiments"
    monkeypatch.syspath_prepend(str(directory))  # Documented direct-script sibling imports.
    main = runpy.run_path(directory / "g6_corrected.py", run_name="synthetic_check")["main"]
    dates = np.array([19980101, 19980102, 19990101, 19990102])
    panel = np.array([[1., 5.], [3., 7.], [10., 0.], [20., 2.]])
    expected = (np.array([[-1., -1.], [1., 1.]]), np.array([[-5., -1.], [5., 1.]]))
    saved, jobs = [], []

    class SyntheticPool:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def map(self, function, periods, blocks, seeds):
            assert function is main.__globals__["psr_flags"]
            references = np.random.SeedSequence(20261113).spawn(11)[9:11]
            for period, block, seed, reference, target in zip(periods, blocks, seeds, references, expected):
                np.testing.assert_array_equal(period, target)
                assert block == 20 and seed.spawn_key == reference.spawn_key
                np.testing.assert_array_equal(seed.generate_state(8), reference.generate_state(8))
                jobs.append(seed.spawn_key)
            # A known count suffices to test reporting; no sampler or statistic is called.
            return [([True, False] * 1000, []), ([True, False] * 1000, [])]

    monkeypatch.setitem(main.__globals__, "load_returns", lambda: (dates, panel, ["synthetic panel"]))
    monkeypatch.setitem(main.__globals__, "ProcessPoolExecutor", SyntheticPool)
    monkeypatch.setitem(main.__globals__, "predicted_rate", lambda period, block: 0.5)
    monkeypatch.setitem(main.__globals__, "save_results", lambda name, lines: saved.append((name, lines)))
    main()
    assert jobs == [(9,), (10,)]
    assert len(saved) == 1 and saved[0][0] == "g6_corrected"
    lines = saved[0][1]
    assert capsys.readouterr().out == "\n".join(lines) + "\n"
    rows = [line for line in lines if line.startswith(("1971-1998:", "1999-2026:"))]
    assert len(rows) == 2
    low, high = beta.ppf(0.025, 1000, 1001), beta.ppf(0.975, 1001, 1000)  # Exact binomial interval.
    for row in rows:
        assert "simulated 0.5000" in row and "(1000/2000)" in row
        assert f"[{low:.4f}, {high:.4f}]" in row
        assert "approximation 0.5000" in row and "simulated minus approximation +0.0000" in row
        assert "approximation inside the 95% CI: yes" in row
