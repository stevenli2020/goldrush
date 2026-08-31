"""Download and preserve the official BIS private-credit aggregate CSV."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import requests
SOURCE_URL = 'https://stats.bis.org/api/v1/data/WS_TC/Q.5A.P.A.M.USD.A?startPeriod=1970-Q1'
SERIES_KEY = 'Q.5A.P.A.M.USD.A'
DATASET_ID = 'BIS:WS_TC(2.0)'
COLLECTOR_VERSION = '0.1.0'

def metadata_bytes(data: bytes) -> str:
    return None

def validate_csv(data: bytes) -> None:
    header = data.decode('utf-8-sig', errors='strict').splitlines()[0].split(',')
    required = {'STRUCTURE_ID', 'FREQ', 'BORROWERS_CTY', 'TC_BORROWERS', 'TC_LENDERS', 'VALUATION', 'UNIT_TYPE', 'UNIT_MULT', 'TC_ADJUST', 'TIME_PERIOD', 'OBS_VALUE'}
    if not required.issubset(header):
        raise ValueError('BIS response does not contain the expected WS_TC columns')

def _write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise FileExistsError(f'refusing to overwrite different file: {path}')
        return
    path.write_bytes(data)

def collect(raw_dir: Path, manifest_dir: Path, *, url: str=SOURCE_URL, session=None) -> dict:
    client = session or requests.Session()
    response = client.get(url, headers={'Accept': 'application/vnd.sdmx.data+csv;version=2.0.0', 'User-Agent': 'GoldRush/0.1'}, timeout=60)
    if response.status_code != 200:
        raise RuntimeError(f'BIS HTTP status {response.status_code}')
    data = response.content
    if not data:
        raise ValueError('BIS download was empty')
    validate_csv(data)
    retrieved_at = datetime.now(timezone.utc)
    stamp = retrieved_at.strftime('%Y%m%dT%H%M%SZ')
    metadata = None
    raw_path = raw_dir / f'ws-tc-{stamp}-.csv'
    _write_new(raw_path, data)
    manifest = {'dataset_id': DATASET_ID, 'series_key': SERIES_KEY, 'source_url': url, 'retrieved_at': retrieved_at.isoformat(), 'raw_path': str(raw_path), 'size_bytes': len(data), 'http_status': response.status_code, 'collector_version': COLLECTOR_VERSION}
    manifest_path = manifest_dir / f'ws-tc-{stamp}-.manifest.json'
    _write_new(manifest_path, (json.dumps(manifest, indent=2) + '\n').encode())
    manifest['manifest_path'] = str(manifest_path)
    return manifest

def main() -> None:
    root = Path(__file__).resolve().parent
    cli = argparse.ArgumentParser(description='Download BIS WS_TC private-credit aggregate')
    cli.add_argument('--raw-dir', type=Path, default=root / 'data/raw')
    cli.add_argument('--manifest-dir', type=Path, default=root / 'data/manifests')
    args = cli.parse_args()
    print(json.dumps(collect(args.raw_dir, args.manifest_dir), indent=2))
if __name__ == '__main__':
    main()
