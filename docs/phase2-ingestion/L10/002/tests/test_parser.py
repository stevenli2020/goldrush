import importlib.util
import json
from pathlib import Path

import pytest


SPEC = importlib.util.spec_from_file_location("l10_002_parser", Path(__file__).parents[1] / "parser.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


PDF_TEXT = """PG02B BULLETIN # 166@  Fri, Aug 28, 2026 PG02B
GC COMEX GOLD FUTURES                          324775                       3250     328025           423793    -       5205          207110           478014
"""


def test_extracts_current_gold_futures_open_interest():
    assert module.observation_date_from_text(PDF_TEXT) == "2026-08-28"
    assert module.open_interest_from_text(PDF_TEXT) == 423793


def test_rejects_missing_or_duplicate_gold_futures_rows():
    with pytest.raises(ValueError, match="exactly one"):
        module.open_interest_from_text("no gold row")
    with pytest.raises(ValueError, match="exactly one"):
        module.open_interest_from_text(PDF_TEXT + PDF_TEXT)


def test_rejects_a_malformed_open_interest_field():
    malformed = PDF_TEXT.replace("423793", "broken")
    with pytest.raises(ValueError, match="malformed"):
        module.open_interest_from_text(malformed)


def test_rejects_manifest_for_a_different_pdf(tmp_path):
    pdf = tmp_path / "section02b.pdf"
    pdf.write_bytes(b"%PDF")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"target": "section02b", "raw_path": str(tmp_path / "other.pdf")}))
    with pytest.raises(ValueError, match="does not identify"):
        module.validate_manifest(pdf, manifest)


def test_source_reference_is_project_relative(tmp_path, monkeypatch):
    manifest = tmp_path / "docs" / "phase2-ingestion" / "data" / "cme" / "manifests" / "section02b.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text("{}")
    monkeypatch.setattr(module, "PROJECT_ROOT", tmp_path)
    assert module.source_reference(manifest) == "docs/phase2-ingestion/data/cme/manifests/section02b.json"
