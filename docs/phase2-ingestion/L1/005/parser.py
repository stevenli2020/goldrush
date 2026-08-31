"""Parse preserved FRED THREEFYTP10 observations for L1-005."""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path
VARIABLE_ID, SERIES_ID, UNIT, VERSION = ('L1-005', 'THREEFYTP10', 'percent', '0.1.0')
FIELDS = ['variable_id', 'observation_date', 'value', 'unit', 'source_name', 'source_series_id', 'raw_file_path', 'retrieved_at', 'validation_status', 'availability_status', 'parser_version']

def parse_observations(raw_path: Path, *, retrieved_at=None, stale_after_days=7):
    payload = json.loads(raw_path.read_text(encoding='utf-8'))
    items = payload.get('observations') if isinstance(payload, dict) else None
    if not isinstance(items, list):
        raise ValueError('raw FRED file does not contain observations')
    metadata = None
    now = datetime.now(timezone.utc)
    retrieved_at = retrieved_at or now.isoformat()
    rows = []
    for item in items:
        if item.get('value') in (None, '', '.'):
            continue
        try:
            date = datetime.strptime(str(item['date']), '%Y-%m-%d').date()
            value = float(item['value'])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'invalid FRED observation: {item}') from exc
        rows.append({'variable_id': VARIABLE_ID, 'observation_date': date.isoformat(), 'value': value, 'unit': UNIT, 'source_name': 'FRED', 'source_series_id': SERIES_ID, 'raw_file_path': str(raw_path), 'retrieved_at': retrieved_at, 'validation_status': 'PASS' if -10 <= value <= 10 else 'FLAG', 'availability_status': 'STALE' if (now.date() - date).days > stale_after_days else 'AVAILABLE', 'parser_version': VERSION})
    if not rows:
        raise ValueError('raw FRED file contains no usable observations')
    return rows

def write_csv(rows, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def main(argv=None):
    ap = argparse.ArgumentParser(description='Parse FRED THREEFYTP10 observations for L1-005')
    ap.add_argument('--raw', type=Path, required=True)
    ap.add_argument('--output', type=Path, default=Path('data/processed/L1_005_observations.csv'))
    ap.add_argument('--retrieved-at')
    ap.add_argument('--stale-after-days', type=int, default=7)
    args = ap.parse_args(argv)
    rows = parse_observations(args.raw, retrieved_at=args.retrieved_at, stale_after_days=args.stale_after_days)
    write_csv(rows, args.output)
    print(f'Wrote {len(rows)} observations to {args.output}')
if __name__ == '__main__':
    raise SystemExit(main())
