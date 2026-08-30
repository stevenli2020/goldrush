import importlib.util
from pathlib import Path

import pytest


spec = importlib.util.spec_from_file_location(
    "l6_001_score", Path(__file__).parents[1] / "score.py"
)
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)


def test_flat_line():
    result = score.compute_l6_001([10.0] * 60, False, None, 0)
    assert result == (0.0, 0, None)


def test_short_history_is_rejected():
    with pytest.raises(ValueError, match="exactly 60"):
        score.compute_l6_001([10.0] * 59, False, None, 0)


def test_sudden_spike():
    result = score.compute_l6_001([1.0] * 55 + [10.0] * 5, False, None, 0)
    assert result[0] == pytest.approx(1.0)
    assert result[1] == 0
    assert result[2] == "elevated"


def test_missing_data_decay_and_reset():
    day1 = score.compute_l6_001([], True, 0.8, 0)
    day2 = score.compute_l6_001([], True, day1[0], day1[1])
    day3 = score.compute_l6_001([], True, day2[0], day2[1])
    assert day1 == (pytest.approx(0.76), 1, None)
    assert day2 == (pytest.approx(0.722), 2, None)
    assert day3 == (0.0, 3, None)
