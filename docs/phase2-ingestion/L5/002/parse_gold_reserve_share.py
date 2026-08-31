"""Parse WGC official gold reserve shares for L5-002."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

def parse_file(path: Path, publication_date: str, download_date: str) -> pd.DataFrame:
    raw = pd.read_excel(path, sheet_name='PDF', header=None)
    header = next((i for i in range(len(raw)) if 'Tonnes' in raw.iloc[i].astype(str).tolist() and '% of reserves**' in raw.iloc[i].astype(str).tolist()), None)
    if header is None:
        raise ValueError('Official reserve-share header not found')
    metadata = None
    records = []
    panel_specs = [('left', 1, 2, 3, 4), ('right', 6, 7, 8, 9)]
    for panel, name_col, tonnes_col, share_col, asof_col in panel_specs:
        for _, row in raw.iloc[header + 1:].iterrows():
            name = row.iloc[name_col] if len(row) > name_col else None
            if pd.isna(name) or not str(name).strip():
                break
            tonnes = pd.to_numeric(row.iloc[tonnes_col], errors='coerce')
            share_text = str(row.iloc[share_col]).strip()
            share = pd.to_numeric(share_text.replace('1)', '').replace('2)', '').replace('3)', '').replace('4)', ''), errors='coerce')
            if pd.isna(share):
                continue
            if share < 0 or share > 1:
                raise ValueError(f'Reserve share out of bounds for {name}: {share}')
            if pd.notna(tonnes) and tonnes < 0:
                raise ValueError(f'Negative holdings for {name}')
            asof = row.iloc[asof_col]
            records.append({'variable_id': 'L5-002', 'country': str(name).strip(), 'panel': panel, 'gold_share_of_reserves': float(share), 'holdings_tonnes': float(tonnes) if pd.notna(tonnes) else None, 'holdings_as_of': str(asof).strip() if pd.notna(asof) else None, 'unit': 'fraction', 'source_file': path.name, 'source_publication_date': publication_date, 'download_date': download_date, 'ingested_at': datetime.now(timezone.utc).isoformat(), 'validation_status': 'PASS', 'availability_status': 'AVAILABLE', 'parser_version': '1.1.0'})
    if not records:
        raise ValueError('No reserve-share records found')
    return pd.DataFrame(records).drop_duplicates(['panel', 'country'])

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
    print(f'Reserve-share records parsed: {len(df)}')
if __name__ == '__main__':
    main()
