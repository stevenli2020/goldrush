"""Download and preserve FOMC calendar, statement, and SEP documents."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.federalreserve.gov"
CALENDAR_URL = f"{BASE_URL}/monetarypolicy/fomccalendars.htm"
USER_AGENT = "GoldRush personal trade-advisor research collector/1.0"
VERSION = "0.1.0"
PHASE2_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PHASE2_ROOT / "data/fomc/raw"
MANIFEST_DIR = PHASE2_ROOT / "data/fomc/manifests"

PATTERNS = {
    "statement_html": re.compile(r"/newsevents/pressreleases/monetary(\d{8})a\.htm$"),
    "statement_pdf": re.compile(r"/monetarypolicy/files/monetary(\d{8})a1\.pdf$"),
    "sep_html": re.compile(r"/monetarypolicy/fomcprojtabl(\d{8})\.htm$"),
    "sep_pdf": re.compile(r"/monetarypolicy/files/fomcprojtabl(\d{8})\.pdf$"),
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "www.federalreserve.gov":
        raise ValueError(f"unexpected Federal Reserve URL: {url}")


def classify_url(url: str) -> tuple[str, str] | None:
    validate_url(url)
    for document_type, pattern in PATTERNS.items():
        match = pattern.search(urlparse(url).path)
        if match:
            stamp = match.group(1)
            return document_type, f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:]}"
    return None


def discover_documents(calendar_html: bytes, start_date: date, end_date: date) -> list[dict[str, str]]:
    soup = BeautifulSoup(calendar_html, "html.parser")
    if "FOMC Meetings" not in soup.get_text(" ", strip=True):
        raise ValueError("calendar does not contain expected FOMC marker")
    found: dict[tuple[str, str], dict[str, str]] = {}
    for anchor in soup.find_all("a", href=True):
        url = urljoin(BASE_URL, anchor["href"])
        if urlparse(url).hostname != "www.federalreserve.gov":
            continue
        classified = classify_url(url)
        if not classified:
            continue
        document_type, release_date = classified
        release = date.fromisoformat(release_date)
        if start_date <= release <= end_date:
            found[(document_type, release_date)] = {
                "document_type": document_type,
                "release_date": release_date,
                "meeting_date": release_date,
                "source_url": url,
            }
    return sorted(found.values(), key=lambda item: (item["release_date"], item["document_type"]))


def validate_content(document_type: str, content: bytes, content_type: str) -> None:
    if not content:
        raise ValueError("empty Federal Reserve response")
    if document_type.endswith("_pdf"):
        if "pdf" not in content_type.lower() or not content.startswith(b"%PDF"):
            raise ValueError("unexpected PDF content")
        return
    if "html" not in content_type.lower():
        raise ValueError("unexpected HTML content type")
    text = BeautifulSoup(content, "html.parser").get_text(" ", strip=True)
    markers = {
        "calendar_html": ("FOMC Meetings", "Meeting calendars"),
        "statement_html": ("Federal Open Market Committee", "statement"),
        "sep_html": ("Summary of Economic Projections", "Midpoint of target range"),
    }
    if not all(marker.lower() in text.lower() for marker in markers[document_type]):
        raise ValueError(f"{document_type} is missing expected document markers")


def preserve_document(
    *, document_type: str, release_date: str, meeting_date: str, source_url: str,
    content: bytes, content_type: str, raw_dir: Path = RAW_DIR,
    manifest_dir: Path = MANIFEST_DIR, retrieved_at: str | None = None,
) -> dict[str, Any]:
    validate_url(source_url)
    validate_content(document_type, content, content_type)
    digest = sha256_bytes(content)
    extension = ".pdf" if document_type.endswith("_pdf") else ".html"
    raw_path = raw_dir / f"{release_date}-{document_type}-{digest[:12]}{extension}"
    manifest_path = manifest_dir / f"{release_date}-{document_type}-{digest[:12]}.json"
    changed = not raw_path.exists()
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    if changed:
        raw_path.write_bytes(content)
    retrieval = retrieved_at or datetime.now(timezone.utc).isoformat()
    record = {
        "source_url": source_url,
        "document_type": document_type,
        "release_date": release_date,
        "meeting_date": meeting_date,
        "retrieved_at": retrieval,
        "size_bytes": len(content),
        "content_type": content_type,
        "raw_path": str(raw_path),
        "sha256": digest,
        "changed": changed,
        "collector_version": VERSION,
    }
    if changed or not manifest_path.exists():
        manifest_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    record["manifest_path"] = str(manifest_path)
    return record


def download_document(document: dict[str, str], *, session: Any | None = None,
                      raw_dir: Path = RAW_DIR, manifest_dir: Path = MANIFEST_DIR) -> dict[str, Any]:
    validate_url(document["source_url"])
    client = session or requests.Session()
    response = client.get(document["source_url"], headers={"User-Agent": USER_AGENT}, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f"Federal Reserve HTTP status {response.status_code}")
    return preserve_document(
        **document, content=response.content,
        content_type=response.headers.get("content-type", ""),
        raw_dir=raw_dir, manifest_dir=manifest_dir,
    )


def preserve_manual(path: Path, *, source_url: str, document_type: str, release_date: str,
                    meeting_date: str | None = None, raw_dir: Path = RAW_DIR,
                    manifest_dir: Path = MANIFEST_DIR) -> dict[str, Any]:
    content_type = "application/pdf" if path.suffix.lower() == ".pdf" else "text/html"
    return preserve_document(
        document_type=document_type, release_date=release_date,
        meeting_date=meeting_date or release_date, source_url=source_url,
        content=path.read_bytes(), content_type=content_type,
        raw_dir=raw_dir, manifest_dir=manifest_dir,
    )


def collect(start_date: date, end_date: date, *, session: Any | None = None,
            raw_dir: Path = RAW_DIR, manifest_dir: Path = MANIFEST_DIR) -> list[dict[str, Any]]:
    client = session or requests.Session()
    response = client.get(CALENDAR_URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f"Federal Reserve calendar HTTP status {response.status_code}")
    calendar = preserve_document(
        document_type="calendar_html", release_date=end_date.isoformat(),
        meeting_date=end_date.isoformat(), source_url=CALENDAR_URL,
        content=response.content, content_type=response.headers.get("content-type", ""),
        raw_dir=raw_dir, manifest_dir=manifest_dir,
    )
    documents = discover_documents(response.content, start_date, end_date)
    return [calendar] + [download_document(item, session=client, raw_dir=raw_dir,
                                           manifest_dir=manifest_dir) for item in documents]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preserve official FOMC statements and SEP materials")
    parser.add_argument("--start-date", type=date.fromisoformat, required=True)
    parser.add_argument("--end-date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--raw-dir", type=Path, default=RAW_DIR)
    parser.add_argument("--manifest-dir", type=Path, default=MANIFEST_DIR)
    args = parser.parse_args(argv)
    records = collect(args.start_date, args.end_date, raw_dir=args.raw_dir,
                      manifest_dir=args.manifest_dir)
    print(json.dumps(records, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
