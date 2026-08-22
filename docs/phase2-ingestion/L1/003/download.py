"""Download and preserve the Federal Reserve GS&W TIPS curve CSV."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
import requests

SOURCE_URL = "https://www.federalreserve.gov/data/yield-curve-tables/feds200805.csv"
VERSION = "0.1.0"

def download(output_dir: Path, *, url: str = SOURCE_URL, session=None) -> dict:
    client = session or requests.Session()
    response = client.get(url, headers={"User-Agent": "GoldRush research collector/0.1"}, timeout=60)
    if response.status_code != 200:
        raise RuntimeError(f"Federal Reserve CSV HTTP status {response.status_code}")
    content = response.content
    if not content or b"Date," not in content or b"TIPSY02" not in content:
        raise ValueError("response is not the expected GS&W TIPS CSV")
    now = datetime.now(timezone.utc); stamp = now.strftime("%Y%m%dT%H%M%SZ")
    digest = hashlib.sha256(content).hexdigest()
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / f"feds200805-{stamp}.csv"
    raw_path.write_bytes(content)
    record = {"source_url": url, "raw_path": str(raw_path), "sha256": digest, "size_bytes": len(content), "downloaded_at": now.isoformat(), "http_status": response.status_code, "parser_version": VERSION}
    (output_dir / f"feds200805-{stamp}.manifest.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--output-dir", type=Path, default=Path("data/raw")); args = ap.parse_args(); print(json.dumps(download(args.output_dir), indent=2))
