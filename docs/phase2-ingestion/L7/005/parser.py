"""Parse preserved FRED SOFR and EFFR observations into a funding spread."""
from __future__ import annotations
import argparse
import csv
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
VARIABLE_ID = 'L7-005'
SOFR = 'SOFR'
EFFR = 'EFFR'
PARSER_VERSION = '0.1.0'
OUTPUT_FIELDS = ['variable_id', 'observation_date', 'sofr_percent', 'effr_percent', 'repo_funding_stress_bps', 'unit', 'observation_definition', 'source_name', 'source_release', 'source_attribution', 'sofr_series_id', 'effr_series_id', 'sofr_raw_file_path', 'effr_raw_file_path', 'sofr_manifest_file_path', 'effr_manifest_file_path', 'sofr_retrieved_at', 'effr_retrieved_at', 'validation_status', 'availability_status', 'parser_version']

def metadata_file(path: Path) -> str:
    return None

def load_series(raw_path: Path, manifest_path: Path, expected_series: str) -> tuple[dict[str, float], dict[str, Any], str]:
    payload = json.loads(raw_path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict) or not isinstance(payload.get('observations'), list):
        raise ValueError(f'{expected_series} raw FRED file lacks observations')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or manifest.get('series_id') != expected_series:
        raise ValueError(f'manifest series_id must be {expected_series}')
    metadata = None
    retrieved_at = manifest.get('retrieved_at')
    if not isinstance(retrieved_at, str) or not retrieved_at:
        raise ValueError(f'{expected_series} manifest retrieved_at is required')
    values: dict[str, float] = {}
    for item in payload['observations']:
        if not isinstance(item, dict):
            raise ValueError(f'{expected_series} observation must be an object')
        date_text = str(item.get('date', ''))
        value_text = item.get('value')
        if value_text in (None, '', '.'):
            continue
        try:
            date.fromisoformat(date_text)
            value = float(value_text)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'invalid {expected_series} observation: {item}') from exc
        if not math.isfinite(value):
            raise ValueError(f'non-finite {expected_series} value: {value_text}')
        if date_text in values and values[date_text] != value:
            raise ValueError(f'conflicting duplicate {expected_series} date: {date_text}')
        values[date_text] = value
    return (values, manifest)

def parse_observations(sofr_raw: Path, sofr_manifest: Path, effr_raw: Path, effr_manifest: Path, *, stale_after_days: int=5, today: date | None=None) -> list[dict[str, Any]]:
    sofr, sm = load_series(sofr_raw, sofr_manifest, SOFR)
    effr, em = load_series(effr_raw, effr_manifest, EFFR)
    overlap = sorted(set(sofr) & set(effr))
    if not overlap:
        raise ValueError('SOFR and EFFR contain no valid overlapping observations')
    as_of = today or datetime.now(timezone.utc).date()
    rows: list[dict[str, Any]] = []
    for date_text in overlap:
        spread = (sofr[date_text] - effr[date_text]) * 100.0
        validation = 'PASS' if -500.0 <= spread <= 2000.0 and -10.0 <= sofr[date_text] <= 50.0 and (-10.0 <= effr[date_text] <= 50.0) else 'FLAG'
        rows.append({'variable_id': VARIABLE_ID, 'observation_date': date_text, 'sofr_percent': sofr[date_text], 'effr_percent': effr[date_text], 'repo_funding_stress_bps': spread, 'unit': 'basis_points', 'observation_definition': 'SOFR minus EFFR, multiplied by 100; secured Treasury repo funding relative to effective federal funds', 'source_name': 'FRED', 'source_release': 'Federal Reserve Bank of New York Reference Rates', 'source_attribution': 'Federal Reserve Bank of New York via FRED', 'sofr_series_id': SOFR, 'effr_series_id': EFFR, 'sofr_raw_file_path': str(sofr_raw), 'effr_raw_file_path': str(effr_raw), 'sofr_manifest_file_path': str(sofr_manifest), 'effr_manifest_file_path': str(effr_manifest), 'sofr_retrieved_at': sm['retrieved_at'], 'effr_retrieved_at': em['retrieved_at'], 'validation_status': validation, 'availability_status': 'STALE' if (as_of - date.fromisoformat(date_text)).days > stale_after_days else 'AVAILABLE', 'parser_version': PARSER_VERSION})
    return rows

def carry_forward(prior_path: Path) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L7-005 observation is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    valid = [r for r in rows if r.get('validation_status') in {'PASS', 'FLAG'}]
    if not valid:
        raise ValueError('prior L7-005 output contains no valid observation')
    row = max(valid, key=lambda r: r['observation_date']).copy()
    for field in ('sofr_percent', 'effr_percent', 'repo_funding_stress_bps'):
        row[field] = float(row[field])
    row['availability_status'] = 'STALE'
    row['parser_version'] = PARSER_VERSION
    return [row]

def write_blocked_status(output_path: Path, reason: str) -> Path:
    path = output_path.with_suffix('.status.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'validation_status': 'FAIL', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')
    return path

def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    status = output_path.with_suffix('.status.json')
    if status.exists():
        status.unlink()
    with output_path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Parse FRED SOFR-EFFR repo funding stress')
    for name in ('sofr-raw', 'sofr-manifest', 'effr-raw', 'effr-manifest', 'prior'):
        cli.add_argument(f'--{name}', type=Path)
    cli.add_argument('--output', type=Path, default=Path('data/processed/L7_005_observations.csv'))
    cli.add_argument('--stale-after-days', type=int, default=5)
    args = cli.parse_args(argv)
    try:
        if all((getattr(args, n.replace('-', '_')) for n in ('sofr_raw', 'sofr_manifest', 'effr_raw', 'effr_manifest'))):
            rows = parse_observations(args.sofr_raw, args.sofr_manifest, args.effr_raw, args.effr_manifest, stale_after_days=args.stale_after_days)
        elif args.prior:
            rows = carry_forward(args.prior)
        else:
            raise ValueError('provide all SOFR/EFFR raw and manifest paths, or --prior')
    except (OSError, ValueError) as exc:
        if args.prior:
            try:
                rows = carry_forward(args.prior)
            except (OSError, ValueError) as fallback_exc:
                path = write_blocked_status(args.output, str(fallback_exc))
                print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
                return 0
        else:
            path = write_blocked_status(args.output, str(exc))
            print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
            return 0
    write_csv(rows, args.output)
    print(f'Wrote {len(rows)} observations to {args.output}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
