"""Preserve the public CME interest-rate bulletin and write a SHA-256 manifest."""
from __future__ import annotations
import argparse, hashlib, json, urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://www.cmegroup.com/daily_bulletin/current/Section10_Interest_Rate_Futures_Continued.pdf"
HEADERS = {"User-Agent": "Mozilla/5.0 GoldRush/0.1", "Referer": "https://www.cmegroup.com/market-data/daily-bulletin.html"}

def download(out_dir: Path, url: str = URL) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    retrieved = datetime.now(timezone.utc)
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        status = getattr(response, "status", response.getcode())
        content_type = (response.headers.get("Content-Type") or "").lower()
        data = response.read()
    if status != 200:
        raise RuntimeError(f"CME bulletin HTTP status {status}")
    if not data.startswith(b"%PDF"):
        raise ValueError(f"CME bulletin is not a PDF (content-type={content_type or 'unknown'})")
    stamp = retrieved.strftime("%Y%m%dT%H%M%SZ")
    raw = out_dir / f"section10-{stamp}.pdf"
    raw.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    manifest = {"variable_id":"L1-006", "source_url":url, "raw_path":str(raw), "sha256":sha,
                "size_bytes":len(data), "retrieved_at":retrieved.isoformat(), "http_status":status,
                "content_type":content_type}
    raw.with_suffix(".manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--out-dir", type=Path, default=Path(__file__).parent / "data/raw")
    print(json.dumps(download(p.parse_args().out_dir), indent=2))
