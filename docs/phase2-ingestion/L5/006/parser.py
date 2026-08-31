"""Parse canonical negative official-sector reserve changes from WGC."""
from __future__ import annotations
import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
VARIABLE_ID = 'L5-006'
PARSER_VERSION = '0.2.0'
DE_MINIMIS_TONNES = 0.0001
MAX_PLAUSIBLE_TONNES = 10000.0
FIELDS = ['variable_id', 'country_entity', 'observation_date', 'signed_change_tonnes', 'official_sector_net_reduction_tonnes', 'unit', 'value_definition', 'source_workbook', 'raw_file_path', 'manifest_path', 'retrieved_at', 'publication_date', 'download_date', 'validation_status', 'availability_status', 'parser_version']

def parse_workbook(workbook: Path, *, manifest_path: Path | None=None, publication_date='', download_date='', stale_after_days=120, prior_path=None):
    raw = pd.read_excel(workbook, sheet_name='Monthly', header=None)
    header = next((i for i in range(len(raw)) if str(raw.iloc[i, 1]).strip().lower() == 'country'), None)
    if header is None:
        raise ValueError('Monthly country header not found')
    dates = pd.to_datetime(raw.iloc[header], errors='coerce', format='mixed')
    date_cols = [i for i in range(3, len(raw.columns)) if pd.notna(dates.iloc[i])]
    if not date_cols:
        raise ValueError('no monthly date columns')
    labels = raw.iloc[header + 1:, 1].astype(str).str.strip()
    rows = raw.iloc[header + 1:].copy()
    rows = rows[labels.ne('nan') & ~labels.str.endswith('*')]
    metadata = None
    now = datetime.now(timezone.utc)
    retrieved = now.isoformat()
    if manifest_path:
        m = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
        retrieved = m.get('downloaded_at', retrieved)
    out = []
    seen = {}
    for _, row in rows.iterrows():
        country = str(row.iloc[1]).strip()
        if not country or country.lower() == 'nan':
            continue
        for col in date_cols:
            cell = row.iloc[col]
            if pd.isna(cell) or str(cell).strip() == '':
                continue
            try:
                value = float(cell)
            except (TypeError, ValueError) as exc:
                raise ValueError(f'malformed numeric value for {country} {dates.iloc[col].date()}: {cell}') from exc
            if value != value or value in (float('inf'), float('-inf')):
                raise ValueError('non-finite official change')
            if value >= 0 or abs(value) < DE_MINIMIS_TONNES:
                continue
            obs = dates.iloc[col].date()
            key = (country, obs.isoformat())
            if key in seen and seen[key] != value:
                raise ValueError(f'conflicting duplicate observation: {key}')
            seen[key] = value
            reduction = abs(value)
            out.append({'variable_id': VARIABLE_ID, 'country_entity': country, 'observation_date': obs.isoformat(), 'signed_change_tonnes': value, 'official_sector_net_reduction_tonnes': reduction, 'unit': 'metric_tonnes', 'value_definition': 'negative canonical official reserve change expressed as a positive reduction; not an identified lending flow', 'source_workbook': Path(workbook).name, 'raw_file_path': str(workbook), 'manifest_path': str(manifest_path or ''), 'retrieved_at': retrieved, 'publication_date': publication_date, 'download_date': download_date, 'validation_status': 'FLAG' if reduction > MAX_PLAUSIBLE_TONNES else 'PASS', 'availability_status': 'STALE' if (now.date() - obs).days > stale_after_days else 'AVAILABLE', 'parser_version': PARSER_VERSION})
    if not out:
        raise ValueError('no negative canonical official changes found')
    return sorted(out, key=lambda r: (r['observation_date'], r['country_entity']))

def carry_forward(prior: Path):
    if not prior.exists():
        raise FileNotFoundError('no prior L5-006 observation is available')
    with prior.open(newline='', encoding='utf-8') as h:
        rows = list(csv.DictReader(h))
    valid = [r for r in rows if r.get('validation_status') in {'PASS', 'FLAG'}]
    if not valid:
        raise ValueError('prior L5-006 output contains no valid observations')
    latest = max((r['observation_date'] for r in valid))
    kept = [r.copy() for r in valid if r['observation_date'] == latest]
    for row in kept:
        row['availability_status'] = 'STALE'
        row['retrieved_at'] = datetime.now(timezone.utc).isoformat()
        row['parser_version'] = PARSER_VERSION
    return kept

def write_blocked(output: Path, reason: str):
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.status.json').write_text(json.dumps({'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'validation_status': 'FAIL', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', type=Path)
    ap.add_argument('--manifest', type=Path)
    ap.add_argument('--output', type=Path, default=Path('data/processed/L5_006_observations.csv'))
    ap.add_argument('--publication-date', default='')
    ap.add_argument('--download-date', default='')
    ap.add_argument('--prior', type=Path)
    a = ap.parse_args(argv)
    try:
        rows = parse_workbook(a.input, manifest_path=a.manifest, publication_date=a.publication_date, download_date=a.download_date) if a.input else carry_forward(a.prior)
    except (OSError, ValueError) as exc:
        if a.prior:
            try:
                rows = carry_forward(a.prior)
            except (OSError, ValueError) as fallback:
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
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
