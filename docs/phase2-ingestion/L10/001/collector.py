"""Download and extract the CFTC disaggregated futures-only COT file."""
from __future__ import annotations
import argparse
import csv
import io
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
SOURCE_URL = 'https://www.cftc.gov/dea/newcot/f_disagg.txt'
CLIENT_VERSION = '0.1.0'
EXPECTED_FIELDS = 191
GOLD_CODE = '088691'
GOLD_NAME = 'GOLD - COMMODITY EXCHANGE INC.'
FUTURES_ONLY = 'FutOnly'
STALE_DAYS = 10

def metadata_bytes(data: bytes) -> str:
    return None

def _int_field(value: str, field: str) -> int:
    value = value.strip()
    if value in {'', '.'}:
        raise ValueError(f'required CFTC field is missing: {field}')
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f'invalid integer in {field}: {value!r}') from exc

def extract_gold_rows(text: str, *, raw_metadata: str, raw_path: str, retrieved_at: str) -> list[dict]:
    rows: list[dict] = []
    for line_number, fields in enumerate(csv.reader(io.StringIO(text)), start=1):
        if not fields or all((not field.strip() for field in fields)):
            continue
        if len(fields) != EXPECTED_FIELDS:
            raise ValueError(f'line {line_number}: expected {EXPECTED_FIELDS} fields, got {len(fields)}')
        fields = [field.strip() for field in fields]
        if fields[3] != GOLD_CODE or fields[190] != FUTURES_ONLY:
            continue
        if fields[0] != GOLD_NAME:
            raise ValueError(f'line {line_number}: contract {GOLD_CODE} has unexpected market name {fields[0]!r}')
        report_date = fields[2]
        for value in (fields[7], fields[13], fields[14], fields[15], fields[185]):
            if value in {'', '.'}:
                raise ValueError(f'line {line_number}: missing required gold field for {report_date}')
        rows.append({'report_date': report_date, 'market_name': fields[0], 'cftc_contract_market_code': fields[3], 'open_interest': _int_field(fields[7], 'open_interest'), 'managed_money_long': _int_field(fields[13], 'managed_money_long'), 'managed_money_short': _int_field(fields[14], 'managed_money_short'), 'managed_money_spreading': _int_field(fields[15], 'managed_money_spreading'), 'contract_units': fields[185], 'fut_only_or_combined': fields[190], 'raw_path': raw_path, 'retrieved_at': retrieved_at})
    if not rows:
        raise ValueError(f'no {GOLD_NAME} futures-only row found')
    unique: dict[str, dict] = {}
    for row in rows:
        previous = unique.get(row['report_date'])
        if previous is None:
            unique[row['report_date']] = row
        elif any((previous[name] != row[name] for name in ('open_interest', 'managed_money_long', 'managed_money_short', 'managed_money_spreading'))):
            raise ValueError(f"conflicting duplicate CFTC observation for {row['report_date']}")
    return list(unique.values())

def download_bytes(url: str=SOURCE_URL) -> tuple[bytes, int]:
    completed = subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error', '--user-agent', 'GoldRush/0.1', '--write-out', '\\n%{http_code}', url], check=True, capture_output=True)
    try:
        payload, status_text = completed.stdout.rsplit(b'\n', 1)
        status = int(status_text)
    except (ValueError, IndexError) as exc:
        raise ValueError('CFTC download did not return an HTTP status') from exc
    if status < 200 or status >= 300:
        raise RuntimeError(f'CFTC download returned HTTP {status}')
    if not payload:
        raise ValueError('CFTC download was empty')
    return (payload, status)

def _write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != data:
            raise FileExistsError(f'refusing to overwrite different file: {path}')
        return
    path.write_bytes(data)

def collect(raw_dir: Path, manifest_dir: Path, extracted_path: Path, *, url: str=SOURCE_URL) -> dict:
    data, http_status = download_bytes(url)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    retrieval_stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    metadata = None
    rows = extract_gold_rows(data.decode('utf-8-sig'), raw_metadata=metadata, raw_path='', retrieved_at=retrieved_at)
    report_date = max((row['report_date'] for row in rows))
    raw_path = raw_dir / f'f_disagg_{report_date}_.txt'
    for row in rows:
        row['raw_path'] = str(raw_path)
    _write_new(raw_path, data)
    manifest = {'source_url': url, 'retrieved_at': retrieved_at, 'raw_path': str(raw_path), 'size_bytes': len(data), 'report_date_latest': report_date, 'gold_row_count': len(rows), 'http_status': http_status, 'client_version': CLIENT_VERSION}
    manifest_path = manifest_dir / f'f_disagg_{report_date}__{retrieval_stamp}.manifest.json'
    _write_new(manifest_path, json.dumps(manifest, indent=2).encode('utf-8'))
    write_extracted(extracted_path, rows)
    manifest['manifest_path'] = str(manifest_path)
    return manifest

def write_extracted(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = list(rows)
    if not rows:
        raise ValueError('cannot write an empty extraction')
    columns = list(rows[0].keys())
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

def fallback_current(prior_path: Path | None, *, as_of: str | None=None) -> dict:
    """Expose the latest valid prior observation without creating a new row."""
    if prior_path is None or not prior_path.exists():
        return {'collection_status': 'BLOCKED', 'availability_status': 'BLOCKED', 'observation': None}
    import datetime as _datetime
    today = _datetime.date.fromisoformat(as_of) if as_of else _datetime.datetime.now(timezone.utc).date()
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = [row for row in csv.DictReader(handle) if row.get('validation_status') == 'PASS']
    if not rows:
        return {'collection_status': 'BLOCKED', 'availability_status': 'BLOCKED', 'observation': None}
    latest = dict(max(rows, key=lambda row: row['report_date']))
    age = (today - _datetime.date.fromisoformat(latest['report_date'])).days
    latest['availability_status'] = 'AVAILABLE' if age <= STALE_DAYS else 'STALE'
    return {'collection_status': 'FALLBACK', 'availability_status': latest['availability_status'], 'observation': latest}

def collect_or_fallback(raw_dir: Path, manifest_dir: Path, extracted_path: Path, *, prior_path: Path | None=None, as_of: str | None=None, url: str=SOURCE_URL) -> dict:
    try:
        return {'collection_status': 'COLLECTED', 'manifest': collect(raw_dir, manifest_dir, extracted_path, url=url)}
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        result = fallback_current(prior_path, as_of=as_of)
        result['error'] = str(exc)
        return result

def main() -> None:
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description='Download and extract CFTC COT COMEX gold positioning')
    parser.add_argument('--raw-dir', type=Path, default=root / 'data/raw')
    parser.add_argument('--manifest-dir', type=Path, default=root / 'data/manifests')
    parser.add_argument('--extracted', type=Path, default=root / 'data/extracted/L10_001_source.csv')
    parser.add_argument('--prior', type=Path, help='processed output used only when download fails')
    parser.add_argument('--as-of', help='ISO date used for fallback freshness')
    args = parser.parse_args()
    print(json.dumps(collect_or_fallback(args.raw_dir, args.manifest_dir, args.extracted, prior_path=args.prior, as_of=args.as_of), indent=2))
if __name__ == '__main__':
    main()
