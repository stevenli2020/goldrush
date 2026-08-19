"""
test_parse_etf_holding.py — L0-003 test suite

Run:
    cd /mnt/d/Projects/GoldRush/docs/phase2-ingestion/L0/003
    python -m pytest tests/test_parse_etf_holding.py -v
"""

import sys
from pathlib import Path

# Add parent directory (L0/003) to sys.path so parse_etf_holding can be found
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from parse_etf_holding import GoldETFHoldingsParser


@pytest.fixture
def parser():
    return GoldETFHoldingsParser()


@pytest.fixture
def sample_csv(tmp_path):
    csv_file = tmp_path / "raw_etf_data.csv"
    content = (
        "observation_date,region,holdings_tonnes\n"
        "2026-08-01,GLOBAL,3100.50\n"
        "2026-08-02,GLOBAL,3102.10\n"
        "2026-08-02,GLOBAL,3102.10\n"  # Duplicate
        "2026-08-03,GLOBAL,-500.00\n"  # Negative value
        "2026-08-04,GLOBAL,invalid\n"  # Malformed value
        "2026-08-05,GLOBAL,3400.00\n"  # Abnormal change (>5%)
        "INVALID-DATE,GLOBAL,3100.0\n"  # Invalid date
    )
    csv_file.write_text(content, encoding="utf-8")
    return csv_file


def test_parse_normal_and_anomalies(parser, sample_csv):
    records = parser.parse_csv(sample_csv, "2026-08-18", "2026-08-19")

    # Should yield 2026-08-01, 2026-08-02, and 2026-08-05 (3 valid rows parsed)
    assert len(records) == 3

    # Check normal record
    rec1 = records[0]
    assert rec1["observation_date"] == "2026-08-01"
    assert rec1["holdings_tonnes"] == 3100.50
    assert rec1["validation_status"] == "PASS"
    assert rec1["availability_status"] == "AVAILABLE"

    # Check abnormal jump
    rec3 = records[2]
    assert rec3["observation_date"] == "2026-08-05"
    assert rec3["validation_status"] == "FLAG"


def test_revision_detection(parser, tmp_path):
    csv_file = tmp_path / "revised_data.csv"
    csv_file.write_text("observation_date,region,holdings_tonnes\n2026-08-01,GLOBAL,3150.00\n")

    prior = {("2026-08-01", "GLOBAL"): 3100.50}
    records = parser.parse_csv(csv_file, "2026-08-18", "2026-08-19", prior_records=prior)

    assert len(records) == 1
    rec = records[0]
    assert rec["revision_metadata"]["is_revision"] is True
    assert rec["revision_metadata"]["prior_value"] == 3100.50


def test_stale_fallback(parser):
    base_record = {
        "observation_date": "2026-08-01",
        "holdings_tonnes": 3100.50,
        "unit": "metric_tonnes",
        "region": "GLOBAL",
        "source_citation": "World Gold Council",
        "source_file": "data.csv",
        "publication_date": "2026-08-01",
        "download_date": "2026-08-01",
        "file_sha256": "a" * 64,
        "ingestion_timestamp": "2026-08-01T00:00:00Z",
        "parser_version": "1.0.0",
        "revision_metadata": {"is_revision": False, "prior_value": None, "revision_reason": None},
        "validation_status": "PASS",
        "availability_status": "AVAILABLE",
    }

    fallback = parser.generate_stale_fallback(base_record, "2026-08-02")
    assert fallback["observation_date"] == "2026-08-02"
    assert fallback["holdings_tonnes"] == 3100.50
    assert fallback["availability_status"] == "STALE"