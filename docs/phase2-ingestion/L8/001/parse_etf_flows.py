"""Parse monthly aggregate gold ETF flows from the WGC ETF workbook."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

def parse_file(path: Path, publication_date: str, download_date: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name='Fund flows by month', header=None)
    header = next((i for i in range(len(raw)) if str(raw.iloc[i, 0]).lower() == 'date'), None)
    if header is None:
        raise ValueError('Fund flows by month date header not found')
    columns = [str(v).strip() for v in raw.iloc[header].tolist()]
    date_col, tonnes_col = (0, next((i for i, v in enumerate(columns) if v.lower() == 'tonnes'), None))
    if tonnes_col is None:
        raise ValueError('Aggregate tonnes column not found')
    metadata = None
    records = []
    for _, row in raw.iloc[header + 1:].iterrows():
        if not pd.notna(row.iloc[date_col]) or not pd.notna(row.iloc[tonnes_col]):
            continue
        date = pd.to_datetime(row.iloc[date_col], errors='coerce')
        value = pd.to_numeric(row.iloc[tonnes_col], errors='coerce')
        if pd.isna(date) or pd.isna(value):
            continue
        records.append({'variable_id': 'L8-001', 'observation_date': date.strftime('%Y-%m-%d'), 'etf_flow_tonnes': float(value), 'unit': 'metric_tonnes', 'source_file': path.name, 'source_publication_date': publication_date, 'download_date': download_date, 'ingested_at': datetime.now(timezone.utc).isoformat(), 'validation_status': 'PASS', 'availability_status': 'AVAILABLE', 'parser_version': '1.0.0'})
    if not records:
        raise ValueError('No ETF flow records found')
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
    print(f'ETF flow records parsed: {len(df)}')
if __name__ == '__main__':
    main()
