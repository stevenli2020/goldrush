"""Extract a simple COMEX Gold front/far settlement pair from CME Section 62."""
from __future__ import annotations
import argparse
import csv
import re
import subprocess
from calendar import monthrange
from datetime import date
from pathlib import Path
MONTHS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
DELIVERY_MONTHS = {2, 4, 6, 8, 10, 12}

def month_end(year: int, month: int) -> date:
    return date(year, month, monthrange(year, month)[1])

def extract_rows_from_text(text: str, observation_date: date) -> list[dict]:
    marker = re.search('GC FUT\\s+COMEX GOLD FUTURES', text)
    if marker is None:
        raise ValueError('GC FUT COMEX GOLD FUTURES section not found')
    start = marker.start()
    end = text.find('TOTAL GC FUT', start)
    block = text[start:] if end < 0 else text[start:end]
    pattern = re.compile('^([A-Z]{3})(\\d{2})\\s+(?:----|\\d+\\.\\d{2})\\s+\\d+\\.\\d{2}[A-Z]?\\s*/\\s*\\d+\\.\\d{2}[A-Z]?\\s+(\\d+\\.\\d{2})', re.MULTILINE)
    contracts = []
    for match in pattern.finditer(block):
        month, year = (MONTHS.get(match.group(1)), 2000 + int(match.group(2)))
        if month not in DELIVERY_MONTHS:
            continue
        contracts.append({'label': f'{match.group(1)}{match.group(2)}', 'settlement': float(match.group(3)), 'expiry': month_end(year, month)})
    eligible = [row for row in contracts if row['settlement'] > 0 and row['expiry'] > observation_date]
    if len(eligible) < 2:
        raise ValueError('fewer than two eligible COMEX Gold contracts found')
    front = eligible[0]
    far = next((row for row in eligible[1:] if 60 <= (row['expiry'] - front['expiry']).days <= 120), None)
    if far is None:
        raise ValueError('no eligible front/far pair with 60-120 day span')
    return [{'observation_date': observation_date.isoformat(), 'near_settlement': front['settlement'], 'far_settlement': far['settlement'], 'days': (far['expiry'] - front['expiry']).days}]

def extract_pdf(pdf_path: Path, observation_date: date, output: Path) -> int:
    try:
        result = subprocess.run(['pdftotext', '-layout', str(pdf_path), '-'], check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise RuntimeError('pdftotext extraction failed') from exc
    text = result.stdout
    rows = extract_rows_from_text(text, observation_date)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--pdf', type=Path, required=True)
    p.add_argument('--observation-date', required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    print(f'Wrote {extract_pdf(args.pdf, date.fromisoformat(args.observation_date), args.output)} row(s)')
