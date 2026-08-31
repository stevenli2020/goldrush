"""Parse monthly gold ETF demand from per-fund holdings changes in the WGC workbook."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

def parse_file(path: Path, publication_date: str, download_date: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name='Demand by month', header=None)
    header = next((i for i in range(len(raw)) if str(raw.iloc[i, 0]).lower() == 'date'), None)
    if header is None:
        raise ValueError('Demand by month date header not found')
    columns = [str(v).strip() for v in raw.iloc[header].tolist()]
    date_col = next((i for i, v in enumerate(columns) if v.lower() == 'date'), None)
    if date_col is None:
        raise ValueError('Demand by month date column not found')
    fund_start = next((i for i, v in enumerate(columns) if v.lower() == 'value (usd)'), None)
    if fund_start is None:
        raise ValueError('Demand by month fund columns not found')
    fund_start += 1
    records = []
    for _, row in raw.iloc[header + 1:].iterrows():
        if not pd.notna(row.iloc[date_col]):
            continue
        date = pd.to_datetime(row.iloc[date_col], errors='coerce')
        fund_values = pd.to_numeric(row.iloc[fund_start:], errors='coerce').dropna()
        if pd.isna(date) or fund_values.empty:
            continue
        value = fund_values.sum()
        records.append({'variable_id': 'L8-001', 'observation_date': date.strftime('%Y-%m-%d'), 'etf_flow_tonnes': float(value), 'unit': 'metric_tonnes', 'source_file': path.name, 'source_publication_date': publication_date, 'download_date': download_date, 'ingested_at': datetime.now(timezone.utc).isoformat(), 'validation_status': 'PASS', 'availability_status': 'AVAILABLE', 'parser_version': '1.1.0'})
    if not records:
        raise ValueError('No ETF flow records found')
    return pd.DataFrame(records).drop_duplicates('observation_date').sort_values('observation_date').reset_index(drop=True)

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
