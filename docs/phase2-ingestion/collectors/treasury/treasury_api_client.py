"""Minimal raw-preserving client for the U.S. Treasury Fiscal Data API."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

CLIENT_VERSION = "0.1.0"
USER_AGENT = "GoldRush/0.1 personal-trade-advisor"
PHASE2_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_DIR = PHASE2_ROOT / "data/treasury/raw"
DEFAULT_MANIFEST_DIR = PHASE2_ROOT / "data/treasury/manifests"


def _validate_response(response: Any) -> dict[str, Any]:
    if response.status_code != 200:
        raise RuntimeError(f"Treasury Fiscal Data HTTP status {response.status_code}")
    content_type = response.headers.get("content-type", "").lower()
    if "json" not in content_type:
        raise ValueError("Treasury Fiscal Data response is not JSON content")
    try:
        payload = response.json()
    except ValueError as exc:
        raise ValueError("Treasury Fiscal Data response is malformed JSON") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        raise ValueError("Treasury Fiscal Data response does not contain a data list")
    meta = payload.get("meta")
    if not isinstance(meta, dict):
        raise ValueError("Treasury Fiscal Data response does not contain metadata")
    return payload


def fetch_dataset(
    endpoint: str,
    query: dict[str, Any],
    raw_dir: Path,
    manifest_dir: Path,
    *,
    session: Any | None = None,
    timeout: int = 30,
    max_retries: int = 2,
) -> dict[str, Any]:
    client = session or requests.Session()
    retrieved_at = datetime.now(timezone.utc)
    stamp = retrieved_at.strftime("%Y%m%dT%H%M%SZ")
    base_query = dict(query)
    base_query.setdefault("page[size]", 1000)
    page_number = 1
    raw_paths: list[str] = []
    page_hashes: list[str] = []
    contents: list[bytes] = []
    record_count = 0
    total_pages = 1
    while page_number <= total_pages:
        params = {**base_query, "page[number]": page_number}
        response = None
        for attempt in range(max_retries + 1):
            try:
                response = client.get(endpoint, params=params, timeout=timeout,
                                      headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
            except (requests.Timeout, requests.ConnectionError) as exc:
                if attempt == max_retries:
                    raise RuntimeError("Treasury Fiscal Data request failed after retries") from exc
                time.sleep(0.25 * (attempt + 1))
                continue
            if response.status_code not in {429, 500, 502, 503, 504} or attempt == max_retries:
                break
            time.sleep(0.25 * (attempt + 1))
        payload = _validate_response(response)
        try:
            total_pages = int(payload["meta"].get("total-pages", 1))
        except (TypeError, ValueError) as exc:
            raise ValueError("Treasury Fiscal Data total-pages is invalid") from exc
        if total_pages < 1:
            raise ValueError("Treasury Fiscal Data total-pages must be positive")
        content = response.content
        digest = hashlib.sha256(content).hexdigest()
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path = raw_dir / f"treasury-{stamp}-page{page_number:03d}.json"
        raw_path.write_bytes(content)
        raw_paths.append(str(raw_path))
        page_hashes.append(digest)
        contents.append(content)
        record_count += len(payload["data"])
        page_number += 1
    source_sha256 = hashlib.sha256(b"".join(contents)).hexdigest()
    manifest = {
        "endpoint": endpoint,
        "query": base_query,
        "retrieved_at": retrieved_at.isoformat(),
        "raw_paths": raw_paths,
        "page_sha256": page_hashes,
        "source_sha256": source_sha256,
        "page_count": len(raw_paths),
        "record_count": record_count,
        "byte_size": sum(len(content) for content in contents),
        "client_version": CLIENT_VERSION,
    }
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"treasury-{stamp}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return {**manifest, "manifest_path": str(manifest_path)}


def main(argv: list[str] | None = None) -> int:
    cli = argparse.ArgumentParser(description="Fetch and preserve Treasury Fiscal Data JSON")
    cli.add_argument("endpoint")
    cli.add_argument("--filter", required=True)
    cli.add_argument("--sort", default="record_date")
    cli.add_argument("--fields")
    cli.add_argument("--page-size", type=int, default=1000)
    cli.add_argument("--raw-dir", type=Path, default=DEFAULT_RAW_DIR)
    cli.add_argument("--manifest-dir", type=Path, default=DEFAULT_MANIFEST_DIR)
    args = cli.parse_args(argv)
    query = {"filter": args.filter, "sort": args.sort, "page[size]": args.page_size}
    if args.fields:
        query["fields"] = args.fields
    manifest = fetch_dataset(args.endpoint, query, args.raw_dir, args.manifest_dir)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
