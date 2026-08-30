import importlib.util
import json
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("cme_extract", Path(__file__).parents[1] / "cme_extract.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_l10_002_is_blocked_when_no_section02b_manifest_exists(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "MANIFESTS", tmp_path)
    results = []
    module.dispatch_l10_002(results, False)
    assert results == [{
        "target": "l10_002",
        "status": "BLOCKED",
        "reason": "Section 02B manifest not present",
    }]


def test_l10_002_is_blocked_after_a_failed_section02b_download(tmp_path, monkeypatch):
    manifest_dir = tmp_path / "manifests"
    log_dir = tmp_path / "logs"
    manifest_dir.mkdir()
    log_dir.mkdir()
    raw = tmp_path / "section02b.pdf"
    raw.write_bytes(b"%PDF")
    (manifest_dir / "section02b-20260829T000000Z.json").write_text(json.dumps({
        "target": "section02b",
        "raw_path": str(raw),
    }))
    (log_dir / "cme-download-20260829T000001Z.json").write_text(json.dumps({
        "results": [{"target": "section02b", "status": "FAIL"}],
    }))
    monkeypatch.setattr(module, "MANIFESTS", manifest_dir)
    monkeypatch.setattr(module, "LOGS", log_dir)
    results = []
    module.dispatch_l10_002(results, False)
    assert results == [{
        "target": "l10_002",
        "status": "BLOCKED",
        "stage": "download",
        "error": "latest Section 02B download status: FAIL",
    }]
