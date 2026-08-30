"""Parse preserved FRED WALCL observations for L7-001."""
from __future__ import annotations
import argparse
import csv
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
VARIABLE_ID = 'L7-001'
SERIES_ID = 'WALCL'
PARSER_VERSION = '0.1.0'
OUTPUT_FIELDS = ['variable_id', 'observation_date', 'fed_total_assets_millions_usd', 'unit', 'observation_definition', 'source_name', 'source_series_id', 'source_release', 'raw_file_path', 'manifest_file_path', 'retrieved_at', 'validation_status', 'availability_status', 'parser_version']

def metadata_file(path: Path) -> str:
    return None

def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict) or not isinstance(payload.get('observations'), list):
        raise ValueError('raw FRED file does not contain an observations list')
    return payload

def load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or manifest.get('series_id') != SERIES_ID:
        raise ValueError(f'manifest series_id must be {SERIES_ID}')
    return manifest

def parse_observations(raw_path: Path, manifest_path: Path, *, stale_after_days: int=10, today: date | None=None) -> list[dict[str, Any]]:
    payload = load_json(raw_path)
    manifest = load_manifest(manifest_path)
    raw_metadata = None
    observed: dict[str, float] = {}
    for item in payload['observations']:
        if not isinstance(item, dict):
            raise ValueError('FRED observation must be an object')
        date_text = str(item.get('date', ''))
        value_text = item.get('value')
        if value_text in (None, '', '.'):
            continue
        try:
            observation_date = date.fromisoformat(date_text)
            value = float(value_text)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'invalid FRED observation: {item}') from exc
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f'invalid WALCL value: {value_text}')
        if date_text in observed and observed[date_text] != value:
            raise ValueError(f'conflicting duplicate observation date: {date_text}')
        observed[date_text] = value
    if not observed:
        raise ValueError('raw FRED file contains no numeric observations')
    as_of = today or datetime.now(timezone.utc).date()
    retrieved_at = manifest.get('retrieved_at')
    if not isinstance(retrieved_at, str) or not retrieved_at:
        raise ValueError('manifest retrieved_at is required')
    rows = []
    for date_text in sorted(observed):
        value = observed[date_text]
        rows.append({'variable_id': VARIABLE_ID, 'observation_date': date_text, 'fed_total_assets_millions_usd': value, 'unit': 'millions_usd', 'observation_definition': 'Federal Reserve total assets, Wednesday level', 'source_name': 'FRED', 'source_series_id': SERIES_ID, 'source_release': 'H.4.1 Factors Affecting Reserve Balances', 'raw_file_path': str(raw_path), 'manifest_file_path': str(manifest_path), 'retrieved_at': retrieved_at, 'validation_status': 'PASS' if 100000 <= value <= 50000000 else 'FLAG', 'availability_status': 'STALE' if (as_of - date.fromisoformat(date_text)).days > stale_after_days else 'AVAILABLE', 'parser_version': PARSER_VERSION})
    return rows

def carry_forward(prior_path: Path, *, retrieved_at: str | None=None) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L7-001 observation is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    valid = [row for row in rows if row.get('validation_status') == 'PASS']
    if not valid:
        raise ValueError('prior L7-001 output contains no valid observation')
    latest = max(valid, key=lambda row: row['observation_date']).copy()
    latest['fed_total_assets_millions_usd'] = float(latest['fed_total_assets_millions_usd'])
    latest['availability_status'] = 'STALE'
    latest['retrieved_at'] = retrieved_at or datetime.now(timezone.utc).isoformat()
    latest['parser_version'] = PARSER_VERSION
    return [latest]

def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    status_path = output_path.with_suffix('.status.json')
    if status_path.exists():
        status_path.unlink()
    with output_path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def write_blocked_status(output_path: Path, reason: str) -> Path:
    status_path = output_path.with_suffix('.status.json')
    status = {'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'validation_status': 'FAIL', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2) + '\n', encoding='utf-8')
    return status_path

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Parse FRED WALCL observations for L7-001')
    cli.add_argument('--raw', type=Path)
    cli.add_argument('--manifest', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--output', type=Path, default=Path('data/processed/L7_001_observations.csv'))
    cli.add_argument('--stale-after-days', type=int, default=10)
    args = cli.parse_args(argv)
    try:
        if args.raw and args.manifest:
            rows = parse_observations(args.raw, args.manifest, stale_after_days=args.stale_after_days)
        elif args.prior and (not args.raw):
            rows = carry_forward(args.prior)
        else:
            raise ValueError('provide --raw with --manifest, or --prior')
    except (OSError, ValueError) as exc:
        if args.prior:
            try:
                rows = carry_forward(args.prior)
            except (OSError, ValueError) as fallback_exc:
                status_path = write_blocked_status(args.output, str(fallback_exc))
                print(json.dumps({'status': 'BLOCKED', 'status_path': str(status_path)}))
                return 0
        else:
            status_path = write_blocked_status(args.output, str(exc))
            print(json.dumps({'status': 'BLOCKED', 'status_path': str(status_path)}))
            return 0
    write_csv(rows, args.output)
    print(f'Wrote {len(rows)} observations to {args.output}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
