"""Parse the verified Chinese WGC premium/discount workbook layout."""
from __future__ import annotations
import argparse
import csv
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
import pandas as pd
VARIABLE_ID = 'L9-001'
TARGET = 'gold_premiums'
PARSER_VERSION = '0.2.0'
SHEET_NAME = 'Chinese premiums-discounts'
TITLE_MARKER = 'Chinese Premium/Discount'
UNIT_MARKER = 'US$/oz'
SMOOTHING_METHOD = '5-day moving average as published by WGC'
OUTPUT_FIELDS = ['variable_id', 'observation_date', 'premium_discount_usd_per_oz', 'unit', 'value_definition', 'smoothing_method', 'source_name', 'source_workbook', 'raw_file_path', 'manifest_path', 'retrieved_at', 'collection_target', 'page_url', 'download_url', 'source_filename', 'raw_size_bytes', 'http_status', 'content_type', 'validation_status', 'availability_status', 'is_revised', 'prior_value', 'revision_reason', 'parser_version']

def metadata_file(path: Path) -> str:
    return None

def load_manifest(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    try:
        manifest = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError('invalid WGC manifest') from exc
    if not isinstance(manifest, dict):
        raise ValueError('WGC manifest must be an object')
    if manifest.get('target') != TARGET:
        raise ValueError(f'manifest target must be {TARGET}')
    filename = str(manifest.get('filename', ''))
    raw_path = str(manifest.get('raw_path', ''))
    if filename != 'gold-premiums.xlsx' or not raw_path.endswith(filename):
        raise ValueError('manifest does not identify gold-premiums.xlsx')
    for field in ('page_url', 'download_url', 'size_bytes', 'downloaded_at'):
        if field not in manifest:
            raise ValueError(f'manifest missing {field}')
    return manifest

def parse_date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if hasattr(value, 'date') and (not isinstance(value, str)):
        return value.date()
    text = str(value).strip()
    for fmt in ('%Y%m%d', '%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y'):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    raise ValueError(f'invalid observation date: {value}')

def find_china_rows(workbook: Path) -> pd.DataFrame:
    book = pd.ExcelFile(workbook)
    if SHEET_NAME not in book.sheet_names:
        raise ValueError(f'required sheet missing: {SHEET_NAME}')
    raw = pd.read_excel(workbook, sheet_name=SHEET_NAME, header=None)
    title_cells = [str(value).strip() for value in raw.iloc[:5].to_numpy().ravel() if not pd.isna(value)]
    title = ' '.join(title_cells)
    if TITLE_MARKER.lower() not in title.lower() or UNIT_MARKER.lower() not in title.lower() or '5 day moving average' not in title.lower():
        raise ValueError('Chinese sheet title does not verify series, unit, and moving-average definition')
    return raw.iloc[5:, :2].reindex(columns=[0, 1]).copy()

def parse_workbook(workbook: Path, *, manifest_path: Path | None=None, stale_after_days: int=10, prior_path: Path | None=None) -> list[dict[str, Any]]:
    manifest = load_manifest(manifest_path)
    raw_metadata = None
    if manifest:
        if int(manifest['size_bytes']) != workbook.stat().st_size:
            raise ValueError('workbook size does not match manifest')
    data = find_china_rows(workbook)
    prior: dict[str, dict[str, str]] = {}
    if prior_path and prior_path.exists():
        with prior_path.open(newline='', encoding='utf-8') as handle:
            prior = {row['observation_date']: row for row in csv.DictReader(handle)}
    observations: dict[str, float] = {}
    started = False
    for _, item in data.iterrows():
        raw_date, raw_value = (item.iloc[0], item.iloc[1])
        if pd.isna(raw_date) and pd.isna(raw_value):
            continue
        if pd.isna(raw_date):
            raise ValueError('missing Chinese premium/discount date')
        try:
            day = parse_date(raw_date)
        except ValueError:
            if not started and isinstance(raw_date, str) and (not str(raw_date).strip()):
                continue
            raise
        started = True
        if pd.isna(raw_value) or str(raw_value).strip() == '':
            raise ValueError(f'missing Chinese premium/discount value for {day}')
        try:
            value = float(raw_value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'invalid Chinese premium/discount value: {raw_value}') from exc
        if not math.isfinite(value):
            raise ValueError(f'non-finite Chinese premium/discount value: {raw_value}')
        key = day.isoformat()
        if key in observations and observations[key] != value:
            raise ValueError(f'conflicting duplicate observation date: {key}')
        observations[key] = value
    if not observations:
        raise ValueError('workbook contains no Chinese premium/discount observations')
    now = datetime.now(timezone.utc)
    retrieved = manifest.get('downloaded_at') or now.isoformat()
    rows = []
    for key in sorted(observations):
        value = observations[key]
        previous = prior.get(key)
        revised = previous is not None and float(previous['premium_discount_usd_per_oz']) != value
        rows.append({'variable_id': VARIABLE_ID, 'observation_date': key, 'premium_discount_usd_per_oz': value, 'unit': 'usd_per_troy_ounce', 'value_definition': 'WGC theoretical local-vs-international gold price difference', 'smoothing_method': SMOOTHING_METHOD, 'source_name': 'World Gold Council', 'source_workbook': workbook.name, 'raw_file_path': str(workbook), 'manifest_path': str(manifest_path or ''), 'retrieved_at': retrieved, 'collection_target': manifest.get('target', TARGET), 'page_url': manifest.get('page_url', ''), 'download_url': manifest.get('download_url', ''), 'source_filename': manifest.get('filename', workbook.name), 'raw_size_bytes': manifest.get('size_bytes', workbook.stat().st_size), 'http_status': manifest.get('http_status'), 'content_type': manifest.get('content_type', ''), 'validation_status': 'PASS', 'availability_status': 'STALE' if (now.date() - date.fromisoformat(key)).days > stale_after_days else 'AVAILABLE', 'is_revised': revised, 'prior_value': previous['premium_discount_usd_per_oz'] if revised else None, 'revision_reason': 'WGC historical source revision' if revised else None, 'parser_version': PARSER_VERSION})
    return rows

def carry_forward(prior_path: Path, *, retrieved_at: str | None=None) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L9-001 observation is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    valid = [row for row in rows if row.get('validation_status') == 'PASS']
    if not valid:
        raise ValueError('prior L9-001 output contains no valid observation')
    row = max(valid, key=lambda item: item['observation_date']).copy()
    row['availability_status'] = 'STALE'
    row['retrieved_at'] = retrieved_at or datetime.now(timezone.utc).isoformat()
    row['parser_version'] = PARSER_VERSION
    return [row]

def write_csv(rows: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    status = output.with_suffix('.status.json')
    if status.exists():
        status.unlink()
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def refresh_availability(prior_path: Path, *, stale_after_days: int=10) -> list[dict[str, Any]]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L9-001 output is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = list(csv.DictReader(handle))
    today = datetime.now(timezone.utc).date()
    for row in rows:
        age = (today - date.fromisoformat(row['observation_date'])).days
        row['availability_status'] = 'STALE' if age > stale_after_days else 'AVAILABLE'
        row['parser_version'] = PARSER_VERSION
    if not rows:
        raise ValueError('prior L9-001 output contains no observations')
    return rows

def write_blocked(output: Path, reason: str) -> Path:
    status = output.with_suffix('.status.json')
    status.parent.mkdir(parents=True, exist_ok=True)
    status.write_text(json.dumps({'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'validation_status': 'FAIL', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')
    return status

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Parse WGC Chinese gold premium/discount workbook')
    cli.add_argument('--workbook', type=Path)
    cli.add_argument('--manifest', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--refresh-status', action='store_true')
    cli.add_argument('--output', type=Path, default=Path('data/processed/L9_001_observations.csv'))
    cli.add_argument('--stale-after-days', type=int, default=10)
    args = cli.parse_args(argv)
    try:
        if args.refresh_status:
            rows = refresh_availability(args.prior or args.output, stale_after_days=args.stale_after_days)
        elif args.workbook:
            rows = parse_workbook(args.workbook, manifest_path=args.manifest, stale_after_days=args.stale_after_days, prior_path=args.prior)
        elif args.prior:
            rows = carry_forward(args.prior)
        else:
            cli.error('provide --workbook or --prior')
    except (OSError, ValueError) as exc:
        if args.prior:
            try:
                rows = carry_forward(args.prior)
            except (OSError, ValueError) as fallback_exc:
                path = write_blocked(args.output, str(fallback_exc))
                print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
                return 0
            write_csv(rows, args.output)
            print(f'Carried forward {len(rows)} observation to {args.output}')
            return 0
        path = write_blocked(args.output, str(exc))
        print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
        return 0
    write_csv(rows, args.output)
    print(f'Wrote {len(rows)} observations to {args.output}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
