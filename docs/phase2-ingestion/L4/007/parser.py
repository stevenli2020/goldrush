"""Parse preserved FRED GFDEGDQ188S observations for L4-007."""
from __future__ import annotations
import argparse
import csv
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
VARIABLE_ID = 'L4-007'
SERIES_ID = 'GFDEGDQ188S'
PARSER_VERSION = '0.1.0'
STALE_AFTER_DAYS = 190
OUTPUT_FIELDS = ['variable_id', 'observation_date', 'observation_year', 'observation_quarter', 'federal_debt_pct_gdp', 'unit', 'series_definition', 'period_definition', 'seasonal_adjustment', 'source_name', 'source_series_id', 'source_release', 'raw_file_path', 'manifest_path', 'retrieved_at', 'validation_status', 'availability_status', 'parser_version']

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

def quarter_end(observation_date: date) -> date:
    ends = {1: date(observation_date.year, 3, 31), 4: date(observation_date.year, 6, 30), 7: date(observation_date.year, 9, 30), 10: date(observation_date.year, 12, 31)}
    try:
        return ends[observation_date.month]
    except KeyError as exc:
        raise ValueError(f'observation date is not a quarter start: {observation_date}') from exc

def operational_availability(latest_date: date, *, today: date, stale_after_days: int) -> str:
    return 'STALE' if (today - quarter_end(latest_date)).days > stale_after_days else 'AVAILABLE'

def parse_observations(raw_path: Path, manifest_path: Path, *, today: date | None=None, stale_after_days: int=STALE_AFTER_DAYS) -> list[dict[str, Any]]:
    observations, manifest = load_inputs(raw_path, manifest_path)
    by_date: dict[date, float] = {}
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
        if not math.isfinite(value) or observation_date.day != 1:
            raise ValueError(f'invalid FRED observation: {item}')
        quarter_end(observation_date)
        if observation_date in by_date and by_date[observation_date] != value:
            raise ValueError(f'conflicting duplicate observation date: {observation_date}')
        by_date.setdefault(observation_date, value)
    if not by_date:
        raise ValueError('raw FRED file contains no numeric observations')
    current_date = today or datetime.now(timezone.utc).date()
    availability = operational_availability(max(by_date), today=current_date, stale_after_days=stale_after_days)
    retrieved_at = manifest.get('retrieved_at')
    if not isinstance(retrieved_at, str) or not retrieved_at:
        raise ValueError('manifest retrieved_at is required')
    rows = []
    for observation_date in sorted(by_date):
        value = by_date[observation_date]
        rows.append({'variable_id': VARIABLE_ID, 'observation_date': observation_date.isoformat(), 'observation_year': observation_date.year, 'observation_quarter': (observation_date.month - 1) // 3 + 1, 'federal_debt_pct_gdp': value, 'unit': 'percent_of_gdp', 'series_definition': 'U.S. federal total public debt divided by GDP', 'period_definition': 'FRED quarterly observation date is the first day of the quarter', 'seasonal_adjustment': 'seasonally_adjusted', 'source_name': 'FRED', 'source_series_id': SERIES_ID, 'source_release': 'Debt to Gross Domestic Product Ratios', 'raw_file_path': str(raw_path), 'manifest_path': str(manifest_path), 'retrieved_at': retrieved_at, 'validation_status': 'PASS' if 0 <= value <= 250 else 'FLAG', 'availability_status': availability, 'parser_version': PARSER_VERSION})
    return rows

def carry_forward(prior_path: Path, *, retrieved_at: str | None=None) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L4-007 observation is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    valid = [row for row in rows if row.get('validation_status') == 'PASS']
    if not valid:
        raise ValueError('prior L4-007 output contains no valid observation')
    latest = max(valid, key=lambda row: row['observation_date']).copy()
    latest['observation_year'] = int(latest['observation_year'])
    latest['observation_quarter'] = int(latest['observation_quarter'])
    latest['federal_debt_pct_gdp'] = float(latest['federal_debt_pct_gdp'])
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
    cli = argparse.ArgumentParser(description='Parse FRED GFDEGDQ188S for L4-007')
    cli.add_argument('--raw', type=Path)
    cli.add_argument('--manifest', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--output', type=Path, default=Path('data/processed/L4_007_observations.csv'))
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
