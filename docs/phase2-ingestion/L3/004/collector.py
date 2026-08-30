"""Preserve raw inputs for the L3-004 cumulative policy probability tree."""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from datetime import date, datetime, timedelta, timezone
from importlib.metadata import version
from pathlib import Path
from cme_fedwatch import FOMC_MEETINGS, schedule_status
from curl_cffi import requests as curl_requests
VARIABLE_ID = 'L3-004'
COLLECTOR_VERSION = '0.1.0'
CME_URL = 'https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/305/FUT'
ROOT = Path(__file__).resolve().parents[2]
FRED_CLIENT_PATH = ROOT / 'collectors' / 'macro' / 'fred_client.py'

def _fred_client():
    spec = importlib.util.spec_from_file_location('l3_004_fred_client', FRED_CLIENT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def metadata_bytes(content: bytes) -> str:
    return None

def previous_business_day(value: date) -> date:
    value -= timedelta(days=1)
    while value.weekday() >= 5:
        value -= timedelta(days=1)
    return value

def fetch_cme(requested_date: date, session=None) -> tuple[bytes, dict, date, str]:
    client = session or curl_requests.Session(impersonate='chrome')
    candidate = requested_date
    for _ in range(5):
        url = f"{CME_URL}?tradeDate={candidate.strftime('%m/%d/%Y')}"
        response = client.get(url)
        response.raise_for_status()
        content = response.content
        payload = json.loads(content)
        if not payload.get('empty'):
            actual = datetime.strptime(payload['tradeDate'], '%m/%d/%Y').date()
            return (content, payload, actual, url)
        candidate = previous_business_day(candidate)
    raise ValueError('CME returned no settlement data for the requested date or prior business days')

def collect(requested_date: date, raw_dir: Path, manifest_dir: Path, api_key: str, *, cme_session=None) -> Path:
    retrieved = datetime.now(timezone.utc)
    stamp = retrieved.strftime('%Y%m%dT%H%M%SZ')
    content, cme_payload, actual_date, cme_url = fetch_cme(requested_date, cme_session)
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    cme_path = raw_dir / f'cme-zq-{actual_date.isoformat()}-{stamp}.json'
    cme_path.write_bytes(content)
    fred = _fred_client()
    fred_raw_dir = raw_dir / 'fred'
    fred_manifest_dir = manifest_dir / 'fred'
    start = (actual_date - timedelta(days=14)).isoformat()
    fred_records = {}
    for series_id in ('EFFR', 'DFEDTARL', 'DFEDTARU'):
        record = fred.fetch_series(series_id, api_key, fred_raw_dir, fred_manifest_dir, observation_start=start, observation_end=actual_date.isoformat(), force=True)
        fred_records[series_id] = record
    package_version = version('cme-fedwatch')
    schedule_record = {'package_name': 'cme-fedwatch', 'package_version': package_version, 'snapshot_for': actual_date.isoformat(), 'schedule_status': schedule_status(actual_date), 'meetings': [meeting.isoformat() for meeting in FOMC_MEETINGS], 'source_url': 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm', 'retrieved_at': retrieved.isoformat()}
    schedule_path = raw_dir / f'fomc-schedule-{stamp}.json'
    schedule_path.write_text(json.dumps(schedule_record, indent=2) + '\n', encoding='utf-8')
    manifest = {'variable_id': VARIABLE_ID, 'collector_version': COLLECTOR_VERSION, 'requested_trade_date': requested_date.isoformat(), 'observation_date': actual_date.isoformat(), 'retrieved_at': retrieved.isoformat(), 'cme': {'source_url': cme_url, 'product_id': '305/FUT', 'raw_path': str(cme_path), 'trade_date': actual_date.isoformat(), 'report_type': cme_payload.get('reportType'), 'update_time': cme_payload.get('updateTime')}, 'fred': fred_records, 'schedule': {'raw_path': str(schedule_path), 'schedule_status': schedule_record['schedule_status'], 'source_url': schedule_record['source_url']}, 'package_name': 'cme-fedwatch', 'package_version': package_version}
    manifest_path = manifest_dir / f'L3-004-{actual_date.isoformat()}-{stamp}.json'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest_path

def main(argv: list[str] | None=None) -> int:
    parser = argparse.ArgumentParser(description='Collect raw L3-004 inputs')
    parser.add_argument('--trade-date', type=date.fromisoformat)
    parser.add_argument('--raw-dir', type=Path, default=Path('docs/phase2-ingestion/L3/004/data/raw'))
    parser.add_argument('--manifest-dir', type=Path, default=Path('docs/phase2-ingestion/L3/004/data/manifests'))
    parser.add_argument('--api-key-file', type=Path, default=ROOT / 'data/macro/secrets/fred_api_key')
    args = parser.parse_args(argv)
    requested = args.trade_date or previous_business_day(date.today())
    fred = _fred_client()
    api_key = os.environ.get('FRED_API_KEY', '') or fred.read_api_key_file(args.api_key_file)
    path = collect(requested, args.raw_dir, args.manifest_dir, api_key)
    print(json.dumps({'manifest': str(path)}))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
