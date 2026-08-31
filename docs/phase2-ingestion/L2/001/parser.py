"""Parse preserved DXY OHLC snapshots for L2-001."""
from __future__ import annotations
import argparse
import csv
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
VARIABLE_ID = 'L2-001'
SYMBOL = 'DX-Y.NYB'
PARSER_VERSION = '0.1.0'
OUTPUT_FIELDS = ['variable_id', 'observation_date', 'dxy_open', 'dxy_high', 'dxy_low', 'dxy_close', 'volume', 'canonical_field', 'unit', 'source_name', 'provider', 'symbol', 'raw_file_path', 'manifest_path', 'retrieved_at', 'validation_status', 'availability_status', 'is_revised', 'prior_dxy_close', 'revision_reason', 'parser_version']
OHLC_FIELDS = ('open', 'high', 'low', 'close', 'volume')

def metadata_file(path: Path) -> str:
    return None

def load_manifest(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    manifest = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(manifest, dict) or manifest.get('symbol') != SYMBOL:
        raise ValueError(f'manifest symbol must be {SYMBOL}')
    return manifest

def parse_raw(raw_path: Path, *, manifest_path: Path | None=None, stale_after_days: int=5, prior_path: Path | None=None) -> list[dict[str, Any]]:
    import pandas as pd
    manifest = load_manifest(manifest_path)
    raw_metadata = None
    frame = pd.read_csv(raw_path)
    required = {'date', 'close'}
    if not required.issubset(frame.columns):
        raise ValueError('DXY raw data must contain date and close columns')
    parsed_dates: list[date] = []
    for value in frame['date']:
        try:
            parsed_dates.append(date.fromisoformat(str(value)[:10]))
        except ValueError as exc:
            raise ValueError(f'invalid DXY date: {value}') from exc
    frame['_date'] = parsed_dates
    prior: dict[str, dict[str, str]] = {}
    if prior_path and prior_path.exists():
        with prior_path.open(newline='', encoding='utf-8') as handle:
            prior = {row['observation_date']: row for row in csv.DictReader(handle)}
    if frame['_date'].duplicated().any():
        for day, group in frame.groupby('_date'):
            for field in OHLC_FIELDS:
                if field not in group.columns:
                    continue
                normalized = []
                for value in group[field]:
                    if pd.isna(value) or value == '':
                        normalized.append(None)
                    else:
                        try:
                            normalized.append(float(value))
                        except (TypeError, ValueError) as exc:
                            raise ValueError(f'invalid DXY {field}: {value}') from exc
                if len(set(normalized)) > 1:
                    raise ValueError(f'conflicting duplicate {field} values: {day}')
        frame = frame.drop_duplicates(subset=['_date'], keep='first')
    rows = []
    today = datetime.now(timezone.utc).date()
    retrieved = manifest.get('retrieved_at') or datetime.now(timezone.utc).isoformat()
    for _, item in frame.sort_values('_date').iterrows():
        values: dict[str, float | None] = {}
        for field in OHLC_FIELDS:
            if field not in frame.columns or pd.isna(item[field]) or item[field] == '':
                values[field] = None
            else:
                try:
                    values[field] = float(item[field])
                except (TypeError, ValueError) as exc:
                    raise ValueError(f'invalid DXY {field}: {item[field]}') from exc
                if not math.isfinite(values[field]):
                    raise ValueError(f'non-finite DXY {field}: {item[field]}')
        if item['_date'] >= today:
            continue
        # Providers may return an in-progress or otherwise incomplete bar.
        # Exclude that row, but keep parsing later completed observations.
        if values['close'] is None:
            continue
        if values['close'] <= 0 or not 50 <= values['close'] <= 200:
            validation = 'FLAG'
        else:
            validation = 'PASS'
        date_text = item['_date'].isoformat()
        previous = prior.get(date_text)
        prior_fields = {'open': 'dxy_open', 'high': 'dxy_high', 'low': 'dxy_low', 'close': 'dxy_close', 'volume': 'volume'}
        changed_values = previous and any(((previous.get(prior_fields[field]) or '') != ('' if values[field] is None else str(values[field])) for field in ('open', 'high', 'low', 'close', 'volume')))
        rows.append({'variable_id': VARIABLE_ID, 'observation_date': date_text, 'dxy_open': values['open'], 'dxy_high': values['high'], 'dxy_low': values['low'], 'dxy_close': values['close'], 'volume': values['volume'], 'canonical_field': 'dxy_close', 'unit': 'index', 'source_name': 'Yahoo Finance via OpenBB', 'provider': 'yfinance', 'symbol': SYMBOL, 'raw_file_path': str(raw_path), 'manifest_path': str(manifest_path or ''), 'retrieved_at': retrieved, 'validation_status': validation, 'availability_status': 'STALE' if (today - item['_date']).days > stale_after_days else 'AVAILABLE', 'is_revised': bool(changed_values), 'prior_dxy_close': previous.get('dxy_close') if changed_values else None, 'revision_reason': 'historical OHLC value changed' if changed_values else None, 'parser_version': PARSER_VERSION})
    if not rows:
        raise ValueError('DXY raw data contains no observations')
    return rows

def carry_forward(prior_path: Path, *, retrieved_at: str | None=None) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L2-001 observation is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    valid = [row for row in rows if row.get('validation_status') == 'PASS']
    if not valid:
        raise ValueError('prior L2-001 output contains no valid observation')
    row = max(valid, key=lambda item: item['observation_date']).copy()
    row['availability_status'] = 'STALE'
    row['retrieved_at'] = retrieved_at or datetime.now(timezone.utc).isoformat()
    row['parser_version'] = PARSER_VERSION
    return [row]

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
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps({'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'validation_status': 'FAIL', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')
    return status_path

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Parse DXY OHLC data for L2-001')
    cli.add_argument('--raw', type=Path)
    cli.add_argument('--manifest', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--output', type=Path, default=Path('data/processed/L2_001_observations.csv'))
    cli.add_argument('--stale-after-days', type=int, default=5)
    args = cli.parse_args(argv)
    try:
        if args.raw:
            rows = parse_raw(args.raw, manifest_path=args.manifest, stale_after_days=args.stale_after_days, prior_path=args.prior)
        elif args.prior:
            rows = carry_forward(args.prior)
        else:
            cli.error('provide --raw or --prior')
    except (OSError, ValueError) as exc:
        if args.prior:
            try:
                rows = carry_forward(args.prior)
            except (OSError, ValueError) as fallback_exc:
                path = write_blocked_status(args.output, str(fallback_exc))
                print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
                return 0
            write_csv(rows, args.output)
            print(f'Carried forward {len(rows)} observation to {args.output}')
            return 0
        path = write_blocked_status(args.output, str(exc))
        print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
        return 0
    write_csv(rows, args.output)
    print(f'Wrote {len(rows)} observations to {args.output}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
