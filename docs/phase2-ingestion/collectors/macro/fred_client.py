"""Transport client for preserving FRED series responses.

Variable-specific parsers remain responsible for transformations and validation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import requests
FRED_OBSERVATIONS_URL = 'https://api.stlouisfed.org/fred/series/observations'
CLIENT_VERSION = '0.1.0'
PHASE2_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_DIR = PHASE2_ROOT / 'data/macro/raw/fred'
DEFAULT_MANIFEST_DIR = PHASE2_ROOT / 'data/macro/manifests'
DEFAULT_API_KEY_FILE = PHASE2_ROOT / 'data/macro/secrets/fred_api_key'

def metadata_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def read_api_key_file(path: Path) -> str:
    """Read a local-only key file containing one FRED API key."""
    try:
        key = path.read_text(encoding='utf-8').strip()
    except FileNotFoundError:
        return ''
    if not key:
        raise ValueError(f'FRED API key file is empty: {path}')
    return key

def validate_payload(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or not isinstance(payload.get('observations'), list):
        raise ValueError('FRED response does not contain an observations list')
    observations = payload['observations']
    for item in observations:
        if not isinstance(item, dict) or 'date' not in item or 'value' not in item:
            raise ValueError('FRED observation is missing date or value')
    return observations

def latest_manifest(manifest_dir: Path, series_id: str) -> dict[str, Any] | None:
    records = []
    for path in manifest_dir.glob(f'{series_id}-*.json'):
        try:
            records.append(json.loads(path.read_text(encoding='utf-8')))
        except (OSError, json.JSONDecodeError):
            continue
    return max(records, key=lambda record: record.get('retrieved_at', ''), default=None)

def fetch_series(series_id: str, api_key: str, raw_dir: Path, manifest_dir: Path, *, observation_start: str | None=None, observation_end: str | None=None, session: requests.Session | Any | None=None, force: bool=False) -> dict[str, Any]:
    if not api_key:
        raise ValueError('FRED API key is required')
    params = {'series_id': series_id, 'api_key': api_key, 'file_type': 'json'}
    if observation_start:
        params['observation_start'] = observation_start
    if observation_end:
        params['observation_end'] = observation_end
    client = session or requests.Session()
    response = client.get(FRED_OBSERVATIONS_URL, params=params, timeout=30)
    if response.status_code != 200:
        raise RuntimeError(f'FRED HTTP status {response.status_code}')
    content = response.content
    try:
        payload = response.json()
    except (ValueError, json.JSONDecodeError) as exc:
        raise ValueError('FRED response is not valid JSON') from exc
    observations = validate_payload(payload)
    metadata = metadata_bytes(content)
    previous = latest_manifest(manifest_dir, series_id)
    changed = force or not previous or previous.get('sha256') != metadata
    retrieved_at = datetime.now(timezone.utc)
    stamp = retrieved_at.strftime('%Y%m%dT%H%M%SZ')
    raw_path = raw_dir / f'{series_id}-{stamp}.json'
    if changed:
        raw_dir.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(content)
    elif previous and previous.get('raw_path'):
        raw_path = Path(previous['raw_path'])
    record = {'series_id': series_id, 'request_url': FRED_OBSERVATIONS_URL, 'request_params': {key: value for key, value in params.items() if key != 'api_key'}, 'raw_path': str(raw_path), 'size_bytes': len(content), 'sha256': metadata, 'observation_count': len(observations), 'retrieved_at': retrieved_at.isoformat(), 'http_status': response.status_code, 'changed': changed, 'forced': force, 'client_version': CLIENT_VERSION}
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / f'{series_id}-{stamp}.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    return record

def main(argv: list[str] | None=None) -> int:
    parser = argparse.ArgumentParser(description='Fetch and preserve a FRED series')
    parser.add_argument('series_id')
    parser.add_argument('--raw-dir', type=Path, default=DEFAULT_RAW_DIR)
    parser.add_argument('--manifest-dir', type=Path, default=DEFAULT_MANIFEST_DIR)
    parser.add_argument('--start-date')
    parser.add_argument('--end-date')
    parser.add_argument('--api-key-file', type=Path, default=DEFAULT_API_KEY_FILE)
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args(argv)
    api_key = os.environ.get('FRED_API_KEY', '') or read_api_key_file(args.api_key_file)
    record = fetch_series(args.series_id, api_key, args.raw_dir, args.manifest_dir, observation_start=args.start_date, observation_end=args.end_date, force=args.force)
    print(json.dumps(record, indent=2))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
