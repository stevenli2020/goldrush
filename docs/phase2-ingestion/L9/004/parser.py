"""Parse canonical India demand and import components from WGC GDT."""
from __future__ import annotations
import argparse, calendar, csv, json, re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
VARIABLE_ID = 'L9-004'
PARSER_VERSION = '0.2.0'
MAX_PLAUSIBLE_TONNES = 10000.0
FIELDS = ['variable_id', 'observation_period', 'observation_period_type', 'observation_date', 'component', 'value', 'unit', 'value_definition', 'source_workbook', 'raw_file_path', 'manifest_path', 'retrieved_at', 'publication_date', 'download_date', 'validation_status', 'availability_status', 'parser_version']

def normalize_period(period):
    if re.fullmatch('20\\d{2}\\.0', period):
        period = period[:-2]
    if re.fullmatch('20\\d{2}', period):
        return (period, 'annual')
    match = re.fullmatch("Q([1-4])'(\\d{2})", period)
    if not match:
        return (None, None)
    return (period, 'quarterly')

def period_date(period):
    normalized, period_type = normalize_period(period)
    if not normalized:
        return None
    if period_type == 'annual':
        return f'{normalized}-12-31'
    q = int(normalized[1])
    year = 2000 + int(normalized[3:])
    month = q * 3
    return f'{year:04d}-{month:02d}-{calendar.monthrange(year, month)[1]:02d}'

def _extract(book, sheet, label, component, definition, metadata, retrieved, manifest, publication, download, stale, source_name, raw_path):
    data = pd.read_excel(book, sheet_name=sheet, header=None)
    matches = data[data.apply(lambda r: r.astype(str).str.strip().eq(label).any(), axis=1)]
    if matches.empty:
        raise ValueError(f'{label} not found in {sheet}')
    if len(matches) > 1:
        raise ValueError(f'conflicting duplicate row for {label} in {sheet}')
    row = matches.iloc[0]
    header = next((i for i in range(min(10, len(data))) if any((period_date(str(v).strip()) for v in data.iloc[i]))), None)
    if header is None:
        raise ValueError(f'period header not found in {sheet}')
    now = datetime.now(timezone.utc).date()
    out = []
    seen = {}
    for col, raw_period in enumerate(data.iloc[header]):
        period = str(raw_period).strip()
        period, period_type = normalize_period(period)
        obs = period_date(period) if period else None
        if not obs:
            continue
        cell = row.iloc[col]
        if pd.isna(cell) or str(cell).strip() == '':
            continue
        try:
            value = float(cell)
        except (TypeError, ValueError) as exc:
            raise ValueError(f'malformed numeric value for {component} {period}: {cell}') from exc
        if value != value or value in (float('inf'), float('-inf')):
            raise ValueError(f'non-finite numeric value for {component} {period}')
        key = (component, period_type, period)
        if key in seen and seen[key] != value:
            raise ValueError(f'conflicting duplicate observation: {key}')
        seen[key] = value
        out.append({'variable_id': VARIABLE_ID, 'observation_period': period, 'observation_period_type': period_type, 'observation_date': obs, 'component': component, 'value': value, 'unit': 'metric_tonnes', 'value_definition': definition, 'source_workbook': source_name, 'raw_file_path': raw_path, 'manifest_path': str(manifest or ''), 'retrieved_at': retrieved, 'publication_date': publication, 'download_date': download, 'validation_status': 'FLAG' if value < 0 or value > MAX_PLAUSIBLE_TONNES else 'PASS', 'availability_status': 'STALE' if (now - datetime.fromisoformat(obs).date()).days > stale else 'AVAILABLE', 'parser_version': PARSER_VERSION})
    return out

def parse_workbook(workbook, manifest_path=None, publication_date='', download_date='', stale_after_days=450, prior_path=None):
    book = Path(workbook)
    metadata = None
    retrieved = datetime.now(timezone.utc).isoformat()
    source_name = book.name
    raw_path = str(book)
    if manifest_path:
        m = json.loads(Path(manifest_path).read_text())
        retrieved = m.get('downloaded_at', retrieved)
        source_name = m.get('filename', source_name)
        raw_path = m.get('raw_path', raw_path)
    out = []
    for sheet, label, component, definition in [('Jewellery', 'India', 'jewellery_demand_tonnes', 'India jewellery demand'), ('Bar and Coin', 'India', 'bar_and_coin_demand_tonnes', 'India bar-and-coin demand'), ('India Supply', 'Gross Bullion Imports', 'gross_bullion_imports_tonnes', 'India gross bullion imports'), ('India Supply', 'Net Bullion Imports', 'net_bullion_imports_tonnes', 'India net bullion imports')]:
        out += _extract(book, sheet, label, component, definition, metadata, retrieved, manifest_path, publication_date, download_date, stale_after_days, source_name, raw_path)
    if not out:
        raise ValueError('no India observations')
    return sorted(out, key=lambda x: (x['observation_date'], x['component']))

def carry_forward(prior):
    p = Path(prior)
    if not p.exists():
        raise FileNotFoundError('no prior L9-004 observation is available')
    with p.open(newline='', encoding='utf-8') as h:
        rows = list(csv.DictReader(h))
    valid = [r for r in rows if r.get('validation_status') in {'PASS', 'FLAG'}]
    if not valid:
        raise ValueError('prior L9-004 output contains no valid observations')
    latest = max((r['observation_date'] for r in valid))
    kept = [r.copy() for r in valid if r['observation_date'] == latest]
    for row in kept:
        row['availability_status'] = 'STALE'
        row['retrieved_at'] = datetime.now(timezone.utc).isoformat()
        row['parser_version'] = PARSER_VERSION
    return kept

def write_blocked(output, reason):
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.status.json').write_text(json.dumps({'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'validation_status': 'FAIL', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n')

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path)
    ap.add_argument('--manifest', type=Path)
    ap.add_argument('--output', type=Path, default=Path('data/processed/L9_004_observations.csv'))
    ap.add_argument('--publication-date', default='')
    ap.add_argument('--download-date', default='')
    ap.add_argument('--prior', type=Path)
    a = ap.parse_args(argv)
    try:
        rows = parse_workbook(a.input, a.manifest, a.publication_date, a.download_date) if a.input else carry_forward(a.prior)
    except Exception as exc:
        if a.prior:
            try:
                rows = carry_forward(a.prior)
            except Exception as fallback:
                write_blocked(a.output, str(fallback))
                print(json.dumps({'status': 'BLOCKED'}))
                return 0
        else:
            write_blocked(a.output, str(exc))
            print(json.dumps({'status': 'BLOCKED'}))
            return 0
    a.output.parent.mkdir(parents=True, exist_ok=True)
    with a.output.open('w', newline='', encoding='utf-8') as h:
        w = csv.DictWriter(h, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    if a.output.with_suffix('.status.json').exists():
        a.output.with_suffix('.status.json').unlink()
    print(f'Wrote {len(rows)} observations to {a.output}')
if __name__ == '__main__':
    main()
