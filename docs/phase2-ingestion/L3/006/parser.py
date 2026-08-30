"""L3-006 Phase 2 source extractor; it never assigns a policy signal."""
from __future__ import annotations
import argparse
import csv
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from bs4 import BeautifulSoup
VARIABLE_ID = 'L3-006'
PARSER_VERSION = '0.2.0'
FIELDS = ['variable_id', 'meeting_date', 'statement_release_date', 'publication_timestamp', 'retrieval_timestamp', 'target_range_lower_percent', 'target_range_upper_percent', 'guidance_signal', 'rationale', 'supporting_evidence', 'counter_evidence', 'reviewer', 'review_timestamp', 'statement_text', 'source_url', 'html_raw_path', 'pdf_raw_path', 'html_manifest_path', 'pdf_manifest_path', 'validation_status', 'availability_status', 'parser_version']

def normalize(text: str) -> str:
    return ' '.join(text.replace('\xa0', ' ').split())

def load_manifest(path: Path, expected_type: str) -> dict[str, Any]:
    record = json.loads(path.read_text(encoding='utf-8'))
    if record.get('document_type') != expected_type:
        raise ValueError(f'expected {expected_type} manifest')
    for field in ('release_date', 'meeting_date', 'retrieved_at', 'source_url', 'raw_path'):
        if not record.get(field):
            raise ValueError(f'{expected_type} manifest missing {field}')
    if not Path(record['raw_path']).is_file():
        raise ValueError(f'{expected_type} raw file does not exist')
    return record

def mixed_number(text: str) -> float:
    match = re.fullmatch('(\\d+)(?:-(\\d+)/(\\d+))?', text)
    if not match:
        raise ValueError(f'invalid target rate: {text}')
    value = float(match.group(1))
    if match.group(2):
        value += int(match.group(2)) / int(match.group(3))
    return value

def extract_statement(html_path: Path) -> tuple[str, float | None, float | None, str]:
    soup = BeautifulSoup(html_path.read_bytes(), 'html.parser')
    article = soup.select_one('#article')
    if article is None:
        raise ValueError('official statement article not found')
    paragraphs = []
    for paragraph in article.find_all('p'):
        text = normalize(paragraph.get_text(' ', strip=True))
        if not text or 'For release at' in text or 'For media inquiries' in text or (text == 'Share'):
            continue
        paragraphs.append(text)
    statement = normalize(' '.join(paragraphs))
    if 'Federal Open Market Committee' not in statement or 'Committee' not in statement:
        raise ValueError('official FOMC statement markers are missing')
    target = re.search('target range for the federal funds rate at\\s+(\\d+(?:-\\d+/\\d+)?)\\s+to\\s+(\\d+(?:-\\d+/\\d+)?)\\s+percent', statement, re.I)
    lower = mixed_number(target.group(1)) if target else None
    upper = mixed_number(target.group(2)) if target else None
    release = re.search('For release at\\s+(\\d{1,2}):(\\d{2})\\s+([ap])\\.m\\.\\s+(EDT|EST)', soup.get_text(' ', strip=True), re.I)
    timestamp = ''
    if release:
        hour = int(release.group(1)) % 12 + (12 if release.group(3).lower() == 'p' else 0)
        offset = '-04:00' if release.group(4).upper() == 'EDT' else '-05:00'
        timestamp = f'{hour:02d}:{release.group(2)}:00{offset}'
    return (statement, lower, upper, timestamp)

def parse_statement(html_manifest: Path, pdf_manifest: Path, *, stale_after_days: int=60) -> list[dict[str, Any]]:
    html = load_manifest(html_manifest, 'statement_html')
    pdf = load_manifest(pdf_manifest, 'statement_pdf')
    if html['release_date'] != pdf['release_date']:
        raise ValueError('statement HTML and PDF release dates differ')
    if html['meeting_date'] != pdf['meeting_date']:
        raise ValueError('statement HTML and PDF meeting dates differ')
    html_path = Path(html['raw_path'])
    statement, lower, upper, time_part = extract_statement(html_path)
    age = (datetime.now(timezone.utc).date() - date.fromisoformat(html['release_date'])).days
    availability = 'STALE' if age > stale_after_days else 'AVAILABLE'
    publication = f"{html['release_date']}T{time_part or '14:00:00-04:00'}"
    return [{
        'variable_id': VARIABLE_ID,
        'meeting_date': html['meeting_date'],
        'statement_release_date': html['release_date'],
        'publication_timestamp': publication,
        'retrieval_timestamp': html['retrieved_at'],
        'target_range_lower_percent': lower,
        'target_range_upper_percent': upper,
        'guidance_signal': 'UNCLASSIFIED',
        'rationale': 'No independently reproducible classification method is configured',
        'supporting_evidence': '',
        'counter_evidence': '',
        'reviewer': '',
        'review_timestamp': '',
        'statement_text': statement,
        'source_url': html['source_url'],
        'html_raw_path': str(html_path),
        'pdf_raw_path': str(Path(pdf['raw_path'])),
        'html_manifest_path': str(html_manifest),
        'pdf_manifest_path': str(pdf_manifest),
        'validation_status': 'PASS',
        'availability_status': availability,
        'parser_version': PARSER_VERSION,
    }]

def write_csv(rows: list[dict[str, Any]], output: Path) -> None:
    releases = [row['statement_release_date'] for row in rows]
    if len(releases) != len(set(releases)):
        raise ValueError('duplicate statement release')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.status.json').unlink(missing_ok=True)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def carry_forward(prior: Path) -> list[dict[str, Any]]:
    if not prior.exists():
        raise FileNotFoundError('no prior valid statement exists')
    with prior.open(newline='', encoding='utf-8') as handle:
        valid = [row for row in csv.DictReader(handle) if row.get('validation_status') == 'PASS']
    if not valid:
        raise ValueError('no prior valid statement exists')
    latest = max(valid, key=lambda row: row['statement_release_date']).copy()
    latest['availability_status'] = 'STALE'
    latest['parser_version'] = PARSER_VERSION
    return [latest]

def blocked(output: Path, reason: str, fallback_reason: str) -> None:
    path = output.with_suffix('.status.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'variable_id': VARIABLE_ID, 'availability_status': 'BLOCKED', 'reason': reason, 'fallback_reason': fallback_reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Parse an official FOMC statement')
    cli.add_argument('--html-manifest', type=Path)
    cli.add_argument('--pdf-manifest', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--stale-after-days', type=int, default=60)
    cli.add_argument('--output', type=Path, default=Path('data/processed/L3_006_statements.csv'))
    args = cli.parse_args(argv)
    try:
        if not args.html_manifest or not args.pdf_manifest:
            raise ValueError('both statement manifests are required')
        rows = parse_statement(args.html_manifest, args.pdf_manifest, stale_after_days=args.stale_after_days)
    except (OSError, ValueError) as exc:
        try:
            rows = carry_forward(args.prior) if args.prior else []
            if not rows:
                raise ValueError('no prior valid statement exists')
        except (OSError, ValueError) as fallback_exc:
            blocked(args.output, str(exc), str(fallback_exc))
            return 0
    write_csv(rows, args.output)
    print(f'Wrote {len(rows)} statement row to {args.output}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
