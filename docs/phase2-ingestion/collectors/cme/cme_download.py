"""Download CME daily bulletin PDFs (Sections 09,10,62,02b) with robust idempotency."""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

from curl_cffi import requests

# ---------------------------- Configuration ----------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data' / 'cme'
RAW_DIRS = {
    'section09': DATA / 'raw' / 'interest-rates',
    'section10': DATA / 'raw' / 'interest-rates',
    'section62': DATA / 'raw' / 'metals',
    'section02b': DATA / 'raw' / 'metals',
}
MANIFESTS = DATA / 'manifests'
LOGS = DATA / 'logs'
COOKIES = DATA / 'cookies' / 'cookies.json'

PAGE_URL = 'https://www.cmegroup.com/market-data/daily-bulletin.html'
TARGETS = {
    'section09': 'Section09_Interest_Rate_Futures.pdf',
    'section10': 'Section10_Interest_Rate_Futures_Continued.pdf',
    'section62': 'Section62_Metals_Futures_Products.pdf',
    'section02b': 'Section02B_Summary_Volume_And_Open_Interest_Metals_Futures_And_Options.pdf'
}
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/151.0 Safari/537.36'
REQUEST_TIMEOUT = 30
MAX_ATTEMPTS = 3

# ---------------------------- Cookie Handling ----------------------------
def load_cookies(path: Path) -> list[dict]:
    """Load cookies from JSON file; return empty list if file missing or corrupted."""
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        print(f'[warning] Cookie file {path} is corrupted, ignoring.', file=sys.stderr)
        return []

def save_cookies(path: Path, session) -> None:
    """Save session cookies to JSON file (merge with existing)."""
    rotated = session.cookies.get_dict()
    if not rotated:
        return
    existing = load_cookies(path)
    by_name = {item.get('name'): item for item in existing if item.get('name')}
    for name, value in rotated.items():
        item = by_name.setdefault(name, {
            'domain': '.cmegroup.com',
            'path': '/',
            'secure': True,
            'name': name
        })
        item['value'] = value
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(list(by_name.values()), indent=2) + '\n', encoding='utf-8')

def get_with_retries(session, url: str, **kwargs):
    """Retry transport errors and transient HTTP responses a bounded number of times."""
    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = session.get(url, timeout=REQUEST_TIMEOUT, **kwargs)
            if response.status_code == 429 or response.status_code >= 500:
                raise RuntimeError(f'HTTP {response.status_code}')
            return response
        except Exception as exc:
            last_error = exc
            if attempt < MAX_ATTEMPTS:
                time.sleep(attempt)
    raise RuntimeError(f'request failed after {MAX_ATTEMPTS} attempts: {last_error}') from last_error

def validate_cme_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != 'https' or parsed.hostname not in {'www.cmegroup.com', 'cmegroup.com'}:
        raise ValueError(f'unexpected CME URL: {url}')
    return url

# ---------------------------- Discovery ----------------------------
def discover(session, verbose=False) -> dict[str, str]:
    """Extract download URLs for target PDFs from the bulletin page."""
    response = get_with_retries(session, PAGE_URL, headers={'User-Agent': UA}, impersonate='chrome')
    response.raise_for_status()

    found = {}
    for section, filename in TARGETS.items():
        # Robust regex: look for href containing the filename (any path)
        pattern = r'href=[\'"]([^\'"]*?' + re.escape(filename) + r')[\'"]'
        match = re.search(pattern, response.text, re.I)
        if match:
            found[section] = validate_cme_url(urljoin(PAGE_URL, match.group(1)))
        elif verbose:
            print(f'[debug] {filename}: link not found')
    return found

# ---------------------------- Download One ----------------------------
def download_one(session, section: str, url: str, force: bool, verbose: bool) -> dict:
    """Download a single PDF, save it only if content changed."""
    validate_cme_url(url)
    response = get_with_retries(
        session,
        url,
        headers={'User-Agent': UA, 'Accept': 'application/pdf,*/*', 'Referer': PAGE_URL},
        impersonate='chrome'
    )
    content = response.content
    content_type = response.headers.get('Content-Type', '')

    if response.status_code != 200:
        raise RuntimeError(f'{section}: HTTP {response.status_code}')

    # Robust PDF detection (look for %PDF within first 1KB)
    if b'%PDF' not in content[:1024] or 'html' in content_type.lower():
        raise ValueError(f"{section}: response is not a PDF (content-type={content_type or 'unknown'})")

    retrieved = datetime.now(timezone.utc)
    # Find previous manifest (if any)
    previous_manifests = sorted(MANIFESTS.glob(f'{section}-*.json'))
    prior = None
    if previous_manifests:
        try:
            prior = json.loads(previous_manifests[-1].read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            prior = None   # ignore corrupted manifest

    # Determine if we need to save a new file
    prior_raw = Path(prior['raw_path']) if prior and prior.get('raw_path') else None
    if prior_raw and not prior_raw.is_absolute():
        prior_raw = (ROOT / prior_raw).resolve()
    changed = force or not prior_raw or not prior_raw.exists() or prior_raw.read_bytes() != content

    if changed:
        raw_dir = RAW_DIRS[section]
        raw_dir.mkdir(parents=True, exist_ok=True)
        final_path = raw_dir / f"{section}-{retrieved.strftime('%Y%m%dT%H%M%SZ')}.pdf"

        # Write to temporary file first to avoid orphaned files on interruption
        with tempfile.NamedTemporaryFile(dir=raw_dir, prefix='tmp_', suffix='.pdf', delete=False) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)

        # Atomically replace (safer than rename on Windows if destination somehow exists)
        tmp_path.replace(final_path)
        raw_path = final_path
    else:
        raw_path = prior_raw

    # Build record and save manifest
    record = {
        'target': section,
        'source_url': url,
        'raw_path': str(raw_path),
        'size_bytes': len(content),
        'retrieved_at': retrieved.isoformat(),
        'http_status': response.status_code,
        'content_type': content_type,
        'changed': changed,
        'forced': force
    }
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    manifest_path = MANIFESTS / f"{section}-{retrieved.strftime('%Y%m%dT%H%M%SZ')}.json"
    manifest_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')

    if verbose:
        print(f'[debug] {section}: changed={changed}')

    return record

# ---------------------------- Main ----------------------------
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Download CME daily bulletin PDFs')
    parser.add_argument('--cookies', type=Path, default=COOKIES, help='Path to cookies.json')
    parser.add_argument('--force', action='store_true', help='Force re-download even if unchanged')
    parser.add_argument('--verbose', '--debug', action='store_true', help='Print debug info')
    args = parser.parse_args(argv)

    session = requests.Session()

    # Load and inject cookies
    for cookie in load_cookies(args.cookies):
        if cookie.get('name') and cookie.get('value'):
            session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain=cookie.get('domain', '.cmegroup.com')
            )

    try:
        links = discover(session, args.verbose)
        results = []

        for section in TARGETS:
            if section not in links:
                results.append({'target': section, 'status': 'NOT_FOUND'})
                continue

            try:
                record = download_one(session, section, links[section], args.force, args.verbose)
                results.append({'target': section, 'status': 'PASS', **record})
            except Exception as exc:
                results.append({'target': section, 'status': 'FAIL', 'error': str(exc)})

        # Save updated cookies
        save_cookies(args.cookies, session)

        # Write run log
        LOGS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        log_path = LOGS / f'cme-download-{stamp}.json'
        log_path.write_text(
            json.dumps({
                'run_at': datetime.now(timezone.utc).isoformat(),
                'results': results
            }, indent=2) + '\n',
            encoding='utf-8'
        )

        # Print summary
        for result in results:
            print(f"{result['status']} {result['target']}")

        return int(any(r['status'] != 'PASS' for r in results))

    except Exception as exc:
        LOGS.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        (LOGS / f'cme-download-{stamp}.json').write_text(
            json.dumps({
                'run_at': datetime.now(timezone.utc).isoformat(),
                'results': [
                    {'target': section, 'status': 'FAIL', 'error': str(exc)}
                    for section in TARGETS
                ],
            }, indent=2) + '\n',
            encoding='utf-8',
        )
        print(f'FAIL collector: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
