"""Parse the current federal-funds-rate dot distribution from accessible SEP HTML."""
from __future__ import annotations
import argparse
import csv
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from bs4 import BeautifulSoup
VARIABLE_ID = 'L3-005'
PARSER_VERSION = '0.1.0'
FIELDS = ['variable_id', 'sep_release_date', 'meeting_date', 'projection_horizon', 'rate_bin_midpoint', 'participant_count', 'median_projected_rate', 'unit', 'publication_timestamp', 'retrieved_at', 'html_source_url', 'pdf_source_url', 'html_raw_path', 'pdf_raw_path', 'html_manifest_path', 'pdf_manifest_path', 'validation_status', 'availability_status', 'parser_version']

def metadata_file(path: Path) -> str:
    return None

def load_manifest(path: Path, expected_type: str) -> dict[str, Any]:
    record = json.loads(path.read_text(encoding='utf-8'))
    if record.get('document_type') != expected_type:
        raise ValueError(f'expected {expected_type} manifest')
    raw_path = Path(record['raw_path'])
    record['manifest_path'] = str(path)
    return record

def publication_timestamp(text: str, release_date: str) -> str:
    match = re.search('For release at\\s+(\\d{1,2}):(\\d{2})\\s+([ap])\\.m\\.,\\s+(EDT|EST)', text, re.I)
    if not match:
        return f'{release_date}T14:00:00-04:00'
    hour = int(match.group(1)) % 12 + (12 if match.group(3).lower() == 'p' else 0)
    offset = '-04:00' if match.group(4).upper() == 'EDT' else '-05:00'
    return f'{release_date}T{hour:02d}:{match.group(2)}:00{offset}'

def weighted_median(values: list[tuple[float, int]]) -> float:
    expanded = [value for value, count in sorted(values) for _ in range(count)]
    if not expanded:
        raise ValueError('empty SEP horizon distribution')
    middle = len(expanded) // 2
    return expanded[middle] if len(expanded) % 2 else (expanded[middle - 1] + expanded[middle]) / 2

def parse_sep(html_manifest: Path, pdf_manifest: Path, *, stale_after_days: int=120) -> list[dict[str, Any]]:
    html_meta = load_manifest(html_manifest, 'sep_html')
    pdf_meta = load_manifest(pdf_manifest, 'sep_pdf')
    if html_meta['release_date'] != pdf_meta['release_date']:
        raise ValueError('SEP HTML and PDF release dates differ')
    html_path = Path(html_meta['raw_path'])
    soup = BeautifulSoup(html_path.read_bytes(), 'html.parser')
    text = soup.get_text(' ', strip=True)
    if 'Summary of Economic Projections' not in text or 'Midpoint of target range' not in text:
        raise ValueError('SEP document markers are missing')
    distribution = next((table for table in soup.find_all('table') if 'Midpoint of target range or target level' in table.get_text(' ', strip=True)), None)
    if distribution is None:
        raise ValueError('SEP federal-funds-rate distribution table not found')
    table_rows = distribution.find_all('tr')
    headers = [cell.get_text(' ', strip=True) for cell in table_rows[0].find_all(['th', 'td'])][1:]
    if not headers or len(set(headers)) != len(headers):
        raise ValueError('invalid SEP projection horizons')
    by_horizon: dict[str, list[tuple[float, int]]] = {header: [] for header in headers}
    seen: set[tuple[str, float]] = set()
    for tr in table_rows[1:]:
        cells = [cell.get_text(' ', strip=True) for cell in tr.find_all(['th', 'td'])]
        if len(cells) != len(headers) + 1:
            raise ValueError('malformed SEP distribution row')
        try:
            rate = float(cells[0])
        except ValueError as exc:
            raise ValueError('invalid SEP rate bin') from exc
        if not 0 <= rate <= 20:
            raise ValueError('SEP rate bin outside plausible range')
        for horizon, count_text in zip(headers, cells[1:]):
            if not count_text:
                continue
            if not count_text.isdigit():
                raise ValueError('SEP participant count must be an integer')
            count = int(count_text)
            key = (horizon, rate)
            if key in seen:
                raise ValueError('duplicate SEP horizon/rate-bin record')
            seen.add(key)
            if count:
                by_horizon[horizon].append((rate, count))
    median_table = soup.find_all('table')[0]
    median_row = next(([cell.get_text(' ', strip=True) for cell in tr.find_all(['th', 'td'])] for tr in median_table.find_all('tr') if tr.find_all(['th', 'td']) and tr.find_all(['th', 'td'])[0].get_text(' ', strip=True) == 'Federal funds rate'), None)
    if median_row is None or len(median_row) < len(headers) + 1:
        raise ValueError('published federal-funds-rate medians not found')
    medians = {header: float(value) for header, value in zip(headers, median_row[1:1 + len(headers)])}
    totals = {horizon: sum((count for _, count in values)) for horizon, values in by_horizon.items()}
    maximum = max(totals.values())
    if any((total <= 0 or maximum - total > 1 for total in totals.values())):
        raise ValueError(f'SEP participant totals do not reconcile: {totals}')
    for horizon, values in by_horizon.items():
        if abs(weighted_median(values) - medians[horizon]) > 0.13:
            raise ValueError(f'SEP distribution does not match published median for {horizon}')
    release_date = html_meta['release_date']
    age = (datetime.now(timezone.utc).date() - date.fromisoformat(release_date)).days
    availability = 'STALE' if age > stale_after_days else 'AVAILABLE'
    published = publication_timestamp(text, release_date)
    rows = []
    for horizon in headers:
        for rate, count in sorted(by_horizon[horizon]):
            rows.append({'variable_id': VARIABLE_ID, 'sep_release_date': release_date, 'meeting_date': html_meta['meeting_date'], 'projection_horizon': horizon, 'rate_bin_midpoint': rate, 'participant_count': count, 'median_projected_rate': medians[horizon], 'unit': 'percent', 'publication_timestamp': published, 'retrieved_at': html_meta['retrieved_at'], 'html_source_url': html_meta['source_url'], 'pdf_source_url': pdf_meta['source_url'], 'html_raw_path': str(html_path), 'pdf_raw_path': pdf_meta['raw_path'], 'html_manifest_path': str(html_manifest), 'pdf_manifest_path': str(pdf_manifest), 'validation_status': 'PASS', 'availability_status': availability, 'parser_version': PARSER_VERSION})
    return rows

def write_csv(rows: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.status.json').unlink(missing_ok=True)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def carry_forward(prior: Path) -> list[dict[str, Any]]:
    if not prior.exists():
        raise FileNotFoundError('no prior valid SEP output exists')
    with prior.open(newline='', encoding='utf-8') as handle:
        rows = [row for row in csv.DictReader(handle) if row.get('validation_status') == 'PASS']
    if not rows:
        raise ValueError('no prior valid SEP output exists')
    latest = max((row['sep_release_date'] for row in rows))
    selected = [row.copy() for row in rows if row['sep_release_date'] == latest]
    for row in selected:
        row['availability_status'] = 'STALE'
        row['parser_version'] = PARSER_VERSION
    return selected

def blocked(output: Path, reason: str) -> None:
    path = output.with_suffix('.status.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'variable_id': VARIABLE_ID, 'availability_status': 'BLOCKED', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Parse current SEP federal-funds-rate dots')
    cli.add_argument('--html-manifest', type=Path)
    cli.add_argument('--pdf-manifest', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--stale-after-days', type=int, default=120)
    cli.add_argument('--output', type=Path, default=Path('data/processed/L3_005_dot_distribution.csv'))
    args = cli.parse_args(argv)
    try:
        if args.html_manifest and args.pdf_manifest:
            rows = parse_sep(args.html_manifest, args.pdf_manifest, stale_after_days=args.stale_after_days)
        else:
            raise ValueError('both SEP HTML and PDF manifests are required')
    except (OSError, ValueError) as exc:
        try:
            rows = carry_forward(args.prior) if args.prior else []
            if not rows:
                raise ValueError('no prior valid SEP output exists')
        except (OSError, ValueError) as fallback_exc:
            blocked(args.output, str(fallback_exc))
            return 0
    write_csv(rows, args.output)
    print(f'Wrote {len(rows)} SEP distribution rows to {args.output}')
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
