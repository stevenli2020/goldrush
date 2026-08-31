"""Parse monthly official-sector gold purchase changes from the WGC workbook."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

def parse_file(path: Path, publication_date: str, download_date: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name='Monthly', header=None)
    header = next((i for i in range(len(raw)) if str(raw.iloc[i, 1]).strip().lower() == 'country'), None)
    if header is None:
        raise ValueError('Monthly country header not found')
    dates = pd.to_datetime(raw.iloc[header], errors='coerce', format='mixed')
    date_cols = [i for i in range(3, len(raw.columns)) if pd.notna(dates.iloc[i])]
    if not date_cols:
        raise ValueError('No monthly date columns found')
    metadata = None
    records = []
    population = raw.iloc[header + 1:].copy()
    labels = population.iloc[:, 1].astype(str).str.strip()
    population = population[labels.ne('nan') & ~labels.str.endswith('*')]
    for col in date_cols:
        values = pd.to_numeric(population.iloc[:, col], errors='coerce')
        total = float(values.sum(min_count=1)) if values.notna().any() else None
        if total is None:
            continue
        records.append({'variable_id': 'L5-001', 'observation_date': dates.iloc[col].strftime('%Y-%m-%d'), 'official_purchase_change_tonnes': total, 'unit': 'metric_tonnes', 'source_file': path.name, 'source_publication_date': publication_date, 'download_date': download_date, 'ingested_at': datetime.now(timezone.utc).isoformat(), 'validation_status': 'PASS', 'availability_status': 'AVAILABLE', 'parser_version': '1.1.0'})
    if not records:
        raise ValueError('No official purchase records found')
    return pd.DataFrame(records).drop_duplicates('observation_date')

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--publication-date', required=True)
    ap.add_argument('--download-date', required=True)
    a = ap.parse_args(argv)
    df = parse_file(a.input, a.publication_date, a.download_date)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.output, index=False)
    print(f'Official purchase records parsed: {len(df)}')
if __name__ == '__main__':
    main()
