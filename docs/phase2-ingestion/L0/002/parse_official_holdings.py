"""Parse the WGC latest official gold holdings workbook for L0-002."""
from __future__ import annotations
import argparse, re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

def parse_file(path: Path, publication_date: str, download_date: str) -> pd.DataFrame:
    metadata = None
    sheets = pd.read_excel(path, sheet_name=None, header=None)
    rows = []
    for sheet, raw in sheets.items():
        header_row = None
        value_col = None
        for i in range(len(raw)):
            values = [str(v).lower() for v in raw.iloc[i].tolist()]
            if any(('tonnes' in v for v in values)):
                header_row = i
                for j, v in enumerate(values):
                    if 'tonnes' in v or 'holdings' in v:
                        value_col = j
                        break
                break
        if header_row is None or value_col is None:
            continue
        for _, row in raw.iloc[header_row + 1:].iterrows():
            text_values = [v for v in row.tolist() if isinstance(v, str) and v.strip()]
            country = text_values[0] if text_values else None
            value = row.iloc[value_col] if value_col < len(row) else None
            if not isinstance(country, str) or not country.strip() or (not pd.notna(value)):
                continue
            try:
                tonnes = float(value)
            except (TypeError, ValueError):
                continue
            if tonnes < 0:
                raise ValueError(f'Negative holdings for {country}')
            rows.append({'variable_id': 'L0-002', 'country': country.strip(), 'holdings_tonnes': tonnes, 'unit': 'metric_tonnes', 'source_file': path.name, 'source_publication_date': publication_date, 'download_date': download_date, 'ingested_at': datetime.now(timezone.utc).isoformat(), 'validation_status': 'PASS', 'availability_status': 'AVAILABLE', 'parser_version': '1.0.0'})
    if not rows:
        raise ValueError('No official holdings rows found')
    return pd.DataFrame(rows).drop_duplicates(subset=['country'])

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
    print(f'Parsed {len(df)} holdings records')
if __name__ == '__main__':
    main()
