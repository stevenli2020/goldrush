"""Extract 30-Day Fed Funds (ZQ) settlements from a preserved CME PDF."""
from __future__ import annotations
import argparse, csv, io, re
from calendar import monthrange
from datetime import date
from pathlib import Path
CONTRACT_RE = re.compile('\\b([A-Z]{3})(\\d{2})\\b')
SETTLE_RE = re.compile('([0-9]{2,3}\\.[0-9]{4})\\s*\\(')
MONTHS = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
MONTH_CODES = {1: 'F', 2: 'G', 3: 'H', 4: 'J', 5: 'K', 6: 'M', 7: 'N', 8: 'Q', 9: 'U', 10: 'V', 11: 'X', 12: 'Z'}

def month_end_business_day(year: int, month: int) -> date:
    day = monthrange(year, month)[1]
    while date(year, month, day).weekday() >= 5:
        day -= 1
    return date(year, month, day)

def extract_rows_from_text(text: str, observation_date: date) -> list[dict]:
    start = text.find('30D FED FD FUT')
    if start < 0:
        raise ValueError('30D FED FD FUT section not found')
    end = text.find('TOTAL', start)
    block = text[start:] if end < 0 else text[start:end]
    rows = []
    matches = list(CONTRACT_RE.finditer(block))
    for index, match in enumerate(matches):
        month, yy = (match.group(1), int(match.group(2)))
        if month not in MONTHS:
            continue
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(block)
        tail = block[match.end():next_start]
        settle = SETTLE_RE.search(tail)
        if not settle:
            continue
        year = 2000 + yy
        rows.append({'observation_date': observation_date.isoformat(), 'contract': f'ZQ{MONTH_CODES[MONTHS[month]]}{yy:02d}', 'settlement_price': settle.group(1), 'expiry_date': month_end_business_day(year, MONTHS[month]).isoformat()})
    if not rows:
        raise ValueError('no 30-Day Fed Funds settlement rows found')
    return rows

def extract_pdf(pdf_path: Path, observation_date: date, output: Path) -> int:
    data = pdf_path.read_bytes()
    if not data.startswith(b'%PDF'):
        raise ValueError('input is not a PDF')
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ImportError('pypdf is required for PDF extraction') from exc
    text = '\n'.join((page.extract_text() or '' for page in PdfReader(io.BytesIO(data)).pages))
    rows = extract_rows_from_text(text, observation_date)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('pdf_path', type=Path)
    p.add_argument('--observation-date', required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    print({'rows': extract_pdf(a.pdf_path, date.fromisoformat(a.observation_date), a.output), 'output': str(a.output)})
