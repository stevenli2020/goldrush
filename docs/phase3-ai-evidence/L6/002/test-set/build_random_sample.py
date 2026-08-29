"""Build the locked 50-event random sample from official archived OFAC delta files."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

ARCHIVE_API = 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/GetDeltaFileArchive'
DOWNLOAD_API = 'https://sanctionslistservice.ofac.treas.gov/api/download/delta'
USER_AGENT = 'GoldRush/0.3 Phase-3 research'


def load_parser():
    parser_path = Path(__file__).resolve().parents[4] / 'phase2-ingestion/L6/002/parser.py'
    spec = importlib.util.spec_from_file_location('l6_002_parser', parser_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def archive_entries(session, years):
    entries = []
    for year in years:
        response = session.post(f'{ARCHIVE_API}?year={year}', json={}, headers={'User-Agent': USER_AGENT}, timeout=60)
        response.raise_for_status()
        entries.extend(entry for entry in response.json() if entry.get('downloadLink') and entry.get('publishDisplayDate'))
    return entries


def build(output, years, seed=6002, session=None):
    if output.exists():
        raise FileExistsError(f'locked sample already exists: {output}')
    client = session or requests.Session()
    parser = load_parser()
    entries = sorted(archive_entries(client, years), key=lambda entry: entry['fileName'])
    selected = random.Random(seed).sample(entries, min(50, len(entries)))
    cases = []
    for entry in selected:
        url = f"{DOWNLOAD_API}?filename={quote(entry['downloadLink'], safe='')}"
        response = client.get(url, headers={'User-Agent': USER_AGENT}, timeout=120)
        response.raise_for_status()
        temp = output.parent / f".{entry['fileName']}"
        temp.write_bytes(response.content)
        try:
            rows = parser.parse_xml(temp, entry['publishDisplayDate'][:10])
        finally:
            temp.unlink(missing_ok=True)
        for row in rows:
            if row['target_name']:
                cases.append({'archive_filename': entry['fileName'], 'publication_date': row['event_date'], 'ofac_entity_id': row['ofac_entity_id'], 'target_name': row['target_name'], 'source_url': url, 'manual_review_required': True})
                break
    payload = {'locked_at': datetime.now(timezone.utc).isoformat(), 'seed': seed, 'years': years, 'purpose': 'Random source-backed sample for manual candidate false-positive review.', 'cases': cases}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, default=Path(__file__).with_name('random_sample.json'))
    ap.add_argument('--year', type=int, action='append', default=[2025, 2026])
    args = ap.parse_args()
    print(json.dumps(build(args.output, args.year), indent=2))


if __name__ == '__main__':
    main()
