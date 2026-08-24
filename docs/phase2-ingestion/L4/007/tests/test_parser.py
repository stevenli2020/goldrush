import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest
from jsonschema import FormatChecker, validate

PACKAGE = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("l4_007_parser", PACKAGE / "parser.py")
parser = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parser)
SCHEMA = json.loads((PACKAGE / "schema.json").read_text(encoding="utf-8"))


def write_inputs(tmp_path, observations, *, series_id="GFDEGDQ188S", bad_hash=False):
    raw = tmp_path / "raw.json"
    raw.write_text(json.dumps({"observations": observations}), encoding="utf-8")
    digest = hashlib.sha256(raw.read_bytes()).hexdigest()
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({
        "series_id": series_id,
        "sha256": "0" * 64 if bad_hash else digest,
        "retrieved_at": "2026-08-24T00:00:00+00:00",
    }), encoding="utf-8")
    return raw, manifest


def test_valid_quarterly_parsing_and_semantics(tmp_path):
    raw, manifest = write_inputs(tmp_path, [
        {"date": "2025-10-01", "value": "122.56815"},
        {"date": "2026-01-01", "value": "122.59387"},
    ])
    rows = parser.parse_observations(raw, manifest, today=date(2026, 8, 24))
    assert [row["observation_quarter"] for row in rows] == [4, 1]
    assert rows[-1]["federal_debt_pct_gdp"] == 122.59387
    assert rows[-1]["unit"] == "percent_of_gdp"
    assert rows[-1]["source_series_id"] == "GFDEGDQ188S"
    assert rows[-1]["availability_status"] == "AVAILABLE"


def test_missing_marker_and_chronological_order(tmp_path):
    raw, manifest = write_inputs(tmp_path, [
        {"date": "2026-01-01", "value": "122.5"},
        {"date": "2025-07-01", "value": "."},
        {"date": "2025-10-01", "value": "121.4"},
    ])
    rows = parser.parse_observations(raw, manifest)
    assert [row["observation_date"] for row in rows] == ["2025-10-01", "2026-01-01"]


def test_wrong_series_id_and_hash_mismatch(tmp_path):
    raw, wrong = write_inputs(tmp_path, [{"date": "2026-01-01", "value": "122"}], series_id="GDP")
    with pytest.raises(ValueError, match="series_id"):
        parser.parse_observations(raw, wrong)
    raw, bad_hash = write_inputs(tmp_path, [{"date": "2026-01-01", "value": "122"}], bad_hash=True)
    with pytest.raises(ValueError, match="hash"):
        parser.parse_observations(raw, bad_hash)


@pytest.mark.parametrize("observation_date,value", [
    ("bad", "122"), ("2026-02-01", "122"), ("2026-01-02", "122"),
    ("2026-01-01", "bad"), ("2026-01-01", "nan"), ("2026-01-01", "inf"),
])
def test_invalid_date_or_numeric_value(tmp_path, observation_date, value):
    raw, manifest = write_inputs(tmp_path, [{"date": observation_date, "value": value}])
    with pytest.raises(ValueError):
        parser.parse_observations(raw, manifest)


def test_duplicate_date_behavior(tmp_path):
    raw, manifest = write_inputs(tmp_path, [
        {"date": "2026-01-01", "value": "122"},
        {"date": "2026-01-01", "value": "122"},
    ])
    assert len(parser.parse_observations(raw, manifest)) == 1
    raw, manifest = write_inputs(tmp_path, [
        {"date": "2026-01-01", "value": "122"},
        {"date": "2026-01-01", "value": "123"},
    ])
    with pytest.raises(ValueError, match="conflicting duplicate"):
        parser.parse_observations(raw, manifest)


def test_validation_bounds_and_freshness(tmp_path):
    raw, manifest = write_inputs(tmp_path, [{"date": "2026-01-01", "value": "251"}])
    current = parser.parse_observations(raw, manifest, today=date(2026, 8, 24))
    assert current[0]["validation_status"] == "FLAG"
    assert current[0]["availability_status"] == "AVAILABLE"
    stale = parser.parse_observations(raw, manifest, today=date(2026, 10, 8))
    assert stale[0]["availability_status"] == "STALE"


def test_prior_fallback_is_one_schema_valid_stale_row(tmp_path):
    raw, manifest = write_inputs(tmp_path, [
        {"date": "2025-10-01", "value": "122.5"},
        {"date": "2026-01-01", "value": "122.6"},
    ])
    prior = tmp_path / "prior.csv"
    parser.write_csv(parser.parse_observations(raw, manifest), prior)
    rows = parser.carry_forward(prior, retrieved_at="2026-08-24T01:00:00+00:00")
    assert len(rows) == 1
    assert rows[0]["observation_date"] == "2026-01-01"
    assert rows[0]["availability_status"] == "STALE"
    validate(rows[0], SCHEMA, format_checker=FormatChecker())


def test_blocked_then_successful_recovery(tmp_path):
    output = tmp_path / "processed" / "L4_007_observations.csv"
    bad_raw, bad_manifest = write_inputs(tmp_path, [{"date": "bad", "value": "122"}])
    blocked = subprocess.run(
        [sys.executable, str(PACKAGE / "parser.py"), "--raw", str(bad_raw),
         "--manifest", str(bad_manifest), "--output", str(output)],
        capture_output=True, text=True, check=False,
    )
    status_path = output.with_suffix(".status.json")
    assert blocked.returncode == 0
    assert json.loads(status_path.read_text())["availability_status"] == "BLOCKED"

    good_raw, good_manifest = write_inputs(tmp_path, [{"date": "2026-01-01", "value": "122.6"}])
    recovered = subprocess.run(
        [sys.executable, str(PACKAGE / "parser.py"), "--raw", str(good_raw),
         "--manifest", str(good_manifest), "--output", str(output)],
        capture_output=True, text=True, check=False,
    )
    assert recovered.returncode == 0
    assert output.exists()
    assert not status_path.exists()


def test_cli_failure_with_prior_writes_one_stale_row(tmp_path):
    good_raw, good_manifest = write_inputs(tmp_path, [{"date": "2026-01-01", "value": "122.6"}])
    prior = tmp_path / "prior.csv"
    parser.write_csv(parser.parse_observations(good_raw, good_manifest), prior)
    bad_raw, bad_manifest = write_inputs(tmp_path, [{"date": "bad", "value": "122"}])
    output = tmp_path / "fallback.csv"
    result = subprocess.run(
        [sys.executable, str(PACKAGE / "parser.py"), "--raw", str(bad_raw),
         "--manifest", str(bad_manifest), "--prior", str(prior), "--output", str(output)],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 1
    assert rows[0]["availability_status"] == "STALE"
    assert not output.with_suffix(".status.json").exists()


def test_all_parsed_rows_validate_against_schema(tmp_path):
    raw, manifest = write_inputs(tmp_path, [
        {"date": "2025-10-01", "value": "122.5"},
        {"date": "2026-01-01", "value": "122.6"},
    ])
    for row in parser.parse_observations(raw, manifest):
        validate(row, SCHEMA, format_checker=FormatChecker())
