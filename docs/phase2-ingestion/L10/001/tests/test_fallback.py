import csv
import importlib.util
import subprocess
from pathlib import Path

MODULE = Path(__file__).parents[1] / "collector.py"
spec = importlib.util.spec_from_file_location("l10_001_collector_fallback", MODULE)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


def prior_file(tmp_path, report_date="2026-08-18"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "processed.csv"
    row = {"report_date": report_date, "validation_status": "PASS", "availability_status": "AVAILABLE", "value": "141648"}
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row)); writer.writeheader(); writer.writerow(row)
    return path


def test_failed_download_uses_prior_as_available(tmp_path):
    result = collector.fallback_current(prior_file(tmp_path), as_of="2026-08-23")
    assert result["collection_status"] == "FALLBACK"
    assert result["availability_status"] == "AVAILABLE"
    assert result["observation"]["report_date"] == "2026-08-18"


def test_failed_download_without_prior_is_blocked(tmp_path):
    result = collector.fallback_current(tmp_path / "missing.csv", as_of="2026-08-23")
    assert result["collection_status"] == "BLOCKED"
    assert result["availability_status"] == "BLOCKED"


def test_prior_crossing_stale_threshold(tmp_path):
    result = collector.fallback_current(prior_file(tmp_path, report_date="2026-08-01"), as_of="2026-08-23")
    assert result["availability_status"] == "STALE"


def test_failed_download_path_uses_prior(monkeypatch, tmp_path):
    def fail(_url):
        raise RuntimeError("network unavailable")
    monkeypatch.setattr(collector, "download_bytes", fail)
    result = collector.collect_or_fallback(tmp_path / "raw", tmp_path / "manifests", tmp_path / "extract.csv", prior_path=prior_file(tmp_path / "prior"), as_of="2026-08-23")
    assert result["collection_status"] == "FALLBACK"
    assert result["availability_status"] == "AVAILABLE"


def test_failed_download_path_without_prior_is_blocked(monkeypatch, tmp_path):
    monkeypatch.setattr(collector, "download_bytes", lambda _url: (_ for _ in ()).throw(RuntimeError("network unavailable")))
    result = collector.collect_or_fallback(tmp_path / "raw", tmp_path / "manifests", tmp_path / "extract.csv", as_of="2026-08-23")
    assert result["collection_status"] == "BLOCKED"
    assert result["availability_status"] == "BLOCKED"


def test_curl_called_process_error_invokes_fallback(monkeypatch, tmp_path):
    def fail(_url):
        raise subprocess.CalledProcessError(7, ["curl"])
    monkeypatch.setattr(collector, "download_bytes", fail)
    result = collector.collect_or_fallback(tmp_path / "raw", tmp_path / "manifests", tmp_path / "extract.csv", prior_path=prior_file(tmp_path / "prior"), as_of="2026-08-23")
    assert result["collection_status"] == "FALLBACK"
    assert result["availability_status"] == "AVAILABLE"
