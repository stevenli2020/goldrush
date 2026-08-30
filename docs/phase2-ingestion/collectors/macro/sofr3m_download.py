"""Download and normalize FRED's 90-day average SOFR series for L0-009."""
from __future__ import annotations
import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
SERIES_ID = 'SOFR90DAYAVG'
URL = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}'
PHASE2_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PHASE2_ROOT / 'L0/009/data/raw/sofr3m.csv'
DEFAULT_MANIFEST = PHASE2_ROOT / 'L0/009/data/raw/sofr3m.manifest.json'

def download(output: Path, manifest: Path, url: str=URL) -> dict:
    try:
        result = subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error', '--max-time', '30', url], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError('FRED curl download failed') from exc
    content = result.stdout
    rows = list(csv.DictReader(content.decode('utf-8-sig').splitlines()))
    if not rows or 'observation_date' not in rows[0] or SERIES_ID not in rows[0]:
        raise ValueError(f'FRED response is missing the expected {SERIES_ID} CSV columns')
    normalized = [{'observation_date': row['observation_date'], 'sofr3m_percent': row[SERIES_ID]} for row in rows if row.get(SERIES_ID, '').strip() not in {'', '.'}]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['observation_date', 'sofr3m_percent'])
        writer.writeheader()
        writer.writerows(normalized)
    record = {'source_url': url, 'source_series': SERIES_ID, 'output_path': str(output), 'rows': len(normalized), 'retrieved_at': datetime.now(timezone.utc).isoformat()}
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    return record

def main(argv: list[str] | None=None) -> int:
    parser = argparse.ArgumentParser(description='Download FRED SOFR90DAYAVG for L0-009')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args(argv)
    print(json.dumps(download(args.output, args.manifest), indent=2))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
