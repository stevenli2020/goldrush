"""Collect newest official OFAC XML delta."""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import requests
import re
ARCHIVE_API = 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/GetDeltaFileArchive'
DOWNLOAD_API = 'https://sanctionslistservice.ofac.treas.gov/api/download/delta'
VERSION = '0.2.0'

def metadata(b):
    return None

def select_latest(entries):
    valid = [e for e in entries if re.search('_delta(?:_\\d+)?\\.xml$', e.get('fileName', '')) and e.get('publishDisplayDate') and e.get('downloadLink')]
    if not valid:
        raise ValueError('OFAC archive returned no XML delta entries')

    def sort_key(entry):
        match = re.search('_delta(?:_(\\d+))?\\.xml$', entry['fileName'])
        sequence = int(match.group(1) or 0) if match else 0
        return (entry['publishDisplayDate'], sequence)
    return max(valid, key=sort_key)

def archive_sequence(filename):
    match = re.search(r'_delta(?:_(\d+))?\.xml$', filename)
    if not match:
        raise ValueError('OFAC archive filename has no delta sequence')
    return int(match.group(1) or 1)

def collect(raw_dir, manifest_dir, *, year=None, session=None):
    year = year or datetime.now(timezone.utc).year
    s = session or requests.Session()
    h = {'User-Agent': 'GoldRush/0.2 personal research', 'Accept': 'application/json'}
    a = s.post(f'{ARCHIVE_API}?year={year}', json={}, headers=h, timeout=60)
    if a.status_code != 200:
        raise RuntimeError(f'OFAC archive HTTP status {a.status_code}')
    try:
        entry = select_latest(a.json())
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError('invalid OFAC archive response') from exc
    filename = entry['downloadLink']
    url = f"{DOWNLOAD_API}?filename={quote(filename, safe='')}"
    r = s.get(url, headers=h, timeout=120, allow_redirects=True)
    if r.status_code != 200 or not r.content:
        raise RuntimeError(f'OFAC delta HTTP status {r.status_code}')
    if b'<sanctionsData' not in r.content[:2000]:
        raise ValueError('OFAC download is not XML sanctionsData')
    pub = entry['publishDisplayDate']
    try:
        publication_date = datetime.fromisoformat(pub.replace('Z', '+00:00')).date().isoformat()
    except ValueError as exc:
        raise ValueError('OFAC archive entry has an invalid publication date') from exc
    sequence = archive_sequence(entry['fileName'])
    suffix = '' if sequence == 1 else f'_{sequence}'
    now = datetime.now(timezone.utc)
    stamp = now.strftime('%Y%m%dT%H%M%SZ')
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw = raw_dir / f'L6-002_{publication_date}{suffix}.xml'
    if raw.exists() and raw.read_bytes() != r.content:
        raise FileExistsError('immutable OFAC raw collision')
    if not raw.exists():
        raw.write_bytes(r.content)
    manifest = {'variable_id': 'L6-002', 'source_url': url, 'archive_api': f'{ARCHIVE_API}?year={year}', 'retrieved_at': now.isoformat(), 'publication_date': publication_date, 'publication_datetime': pub, 'archive_sequence': sequence, 'raw_path': str(raw), 'size_bytes': len(r.content), 'content_type': r.headers.get('content-type', ''), 'http_status': r.status_code, 'collector_version': VERSION, 'archive_entry': entry}
    manifest_dir.mkdir(parents=True, exist_ok=True)
    mp = manifest_dir / f'L6-002_{publication_date}{suffix}_{stamp}.manifest.json'
    payload = json.dumps(manifest, indent=2) + '\n'
    if mp.exists() and mp.read_text(encoding='utf-8') != payload:
        raise FileExistsError('immutable OFAC manifest collision')
    if not mp.exists():
        mp.write_text(payload, encoding='utf-8')
    manifest['manifest_path'] = str(mp)
    return manifest

def main():
    root = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int)
    ap.add_argument('--raw-dir', type=Path, default=root / 'data/raw')
    ap.add_argument('--manifest-dir', type=Path, default=root / 'data/manifests')
    a = ap.parse_args()
    print(json.dumps(collect(a.raw_dir, a.manifest_dir, year=a.year), indent=2))
if __name__ == '__main__':
    main()
