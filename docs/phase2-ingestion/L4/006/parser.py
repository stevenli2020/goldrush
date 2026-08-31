"""Parse preserved FRED FYFSGDA188S observations for L4-006."""
from __future__ import annotations
import argparse
import csv
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
VARIABLE_ID = 'L4-006'
SERIES_ID = 'FYFSGDA188S'
PARSER_VERSION = '0.1.0'
STALE_AFTER_DAYS = 550
OUTPUT_FIELDS = ['variable_id', 'observation_date', 'observation_year', 'fiscal_balance_pct_gdp', 'unit', 'sign_convention', 'period_definition', 'source_name', 'source_series_id', 'source_release', 'raw_file_path', 'manifest_path', 'retrieved_at', 'validation_status', 'availability_status', 'parser_version']

def metadata_file(path: Path) -> str:
    return None

def load_inputs(raw_path: Path, manifest_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any], str]:
    payload = json.loads(raw_path.read_text(encoding='utf-8'))
    observations = payload.get('observations') if isinstance(payload, dict) else None
    if not isinstance(observations, list):
        raise ValueError('raw FRED file does not contain an observations list')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or manifest.get('series_id') != SERIES_ID:
        raise ValueError(f'manifest series_id must be {SERIES_ID}')
    metadata = None
    return (observations, manifest)

def operational_availability(latest_year: int, *, today: date, stale_after_days: int) -> str:
    fiscal_year_end = date(latest_year, 9, 30)
    return 'STALE' if (today - fiscal_year_end).days > stale_after_days else 'AVAILABLE'

def parse_observations(raw_path: Path, manifest_path: Path, *, today: date | None=None, stale_after_days: int=STALE_AFTER_DAYS) -> list[dict[str, Any]]:
    observations, manifest = load_inputs(raw_path, manifest_path)
    by_year: dict[int, tuple[str, float]] = {}
    for item in observations:
        if not isinstance(item, dict):
            raise ValueError('FRED observation must be an object')
        value_text = item.get('value')
        if value_text in (None, '', '.'):
            continue
        try:
            observation_date = date.fromisoformat(str(item.get('date', '')))
            value = float(value_text)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'invalid FRED observation: {item}') from exc
        if not math.isfinite(value):
            raise ValueError(f'invalid FRED observation: {item}')
        prior = by_year.get(observation_date.year)
        if prior and prior[1] != value:
            raise ValueError(f'conflicting duplicate observation year: {observation_date.year}')
        by_year.setdefault(observation_date.year, (observation_date.isoformat(), value))
    if not by_year:
        raise ValueError('raw FRED file contains no numeric observations')
    current_date = today or datetime.now(timezone.utc).date()
    availability = operational_availability(max(by_year), today=current_date, stale_after_days=stale_after_days)
    retrieved_at = manifest.get('retrieved_at')
    if not isinstance(retrieved_at, str) or not retrieved_at:
        raise ValueError('manifest retrieved_at is required')
    rows = []
    for year in sorted(by_year):
        observation_date, value = by_year[year]
        rows.append({'variable_id': VARIABLE_ID, 'observation_date': observation_date, 'observation_year': year, 'fiscal_balance_pct_gdp': value, 'unit': 'percent_of_gdp', 'sign_convention': 'negative=deficit; positive=surplus', 'period_definition': "federal fiscal-year balance divided by annual calendar-year GDP, using FRED's published year label", 'source_name': 'FRED', 'source_series_id': SERIES_ID, 'source_release': 'Debt to Gross Domestic Product Ratios', 'raw_file_path': str(raw_path), 'manifest_path': str(manifest_path), 'retrieved_at': retrieved_at, 'validation_status': 'PASS' if -30 <= value <= 10 else 'FLAG', 'availability_status': availability, 'parser_version': PARSER_VERSION})
    return rows

def carry_forward(prior_path: Path, *, retrieved_at: str | None=None) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L4-006 observation is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    valid = [row for row in rows if row.get('validation_status') == 'PASS']
    if not valid:
        raise ValueError('prior L4-006 output contains no valid observation')
    latest = max(valid, key=lambda row: int(row['observation_year'])).copy()
    latest['observation_year'] = int(latest['observation_year'])
    latest['fiscal_balance_pct_gdp'] = float(latest['fiscal_balance_pct_gdp'])
    latest['availability_status'] = 'STALE'
    latest['retrieved_at'] = retrieved_at or datetime.now(timezone.utc).isoformat()
    latest['parser_version'] = PARSER_VERSION
    return [latest]

def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    blocked_path = output_path.with_suffix('.status.json')
    if blocked_path.exists():
        blocked_path.unlink()
    with output_path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def write_blocked_status(output_path: Path, reason: str) -> Path:
    blocked_path = output_path.with_suffix('.status.json')
    blocked_path.parent.mkdir(parents=True, exist_ok=True)
    blocked_path.write_text(json.dumps({'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'validation_status': 'FAIL', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')
    return blocked_path

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Parse FRED FYFSGDA188S for L4-006')
    cli.add_argument('--raw', type=Path)
    cli.add_argument('--manifest', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--output', type=Path, default=Path('data/processed/L4_006_observations.csv'))
    cli.add_argument('--stale-after-days', type=int, default=STALE_AFTER_DAYS)
    args = cli.parse_args(argv)
    try:
        if args.raw and args.manifest:
            rows = parse_observations(args.raw, args.manifest, stale_after_days=args.stale_after_days)
        elif args.prior and (not args.raw):
            rows = carry_forward(args.prior)
        else:
            raise ValueError('provide --raw and --manifest, or --prior')
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
