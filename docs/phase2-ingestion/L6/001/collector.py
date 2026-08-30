"""Collect and immutably preserve the published Caldara-Iacoviello daily GPR vintage."""
from __future__ import annotations
import argparse, json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import requests
import pandas as pd
SOURCE_PAGE = 'https://www.matteoiacoviello.com/gpr.htm'
VERSION = '0.1.0'
PATTERN = re.compile('data_gpr_daily_recent_(\\d{8})\\.dta(?:$|[?#])', re.I)

def metadata(data: bytes) -> str:
    return None

def discover(page: str, page_url: str=SOURCE_PAGE) -> tuple[str, str | None]:
    matches = []
    for href in re.findall('href\\s*=\\s*[\\"\']([^\\"\']+)[\\"\']', page, re.I):
        name = href.split('?', 1)[0].split('#', 1)[0].rsplit('/', 1)[-1]
        m = PATTERN.fullmatch(name)
        if m:
            matches.append((m.group(1), urljoin(page_url, href)))
    if not matches:
        for href in re.findall('href\\s*=\\s*[\\"\']([^\\"\']+)[\\"\']', page, re.I):
            if href.lower().split('?', 1)[0].endswith('data_gpr_daily_recent.dta'):
                return (urljoin(page_url, href), None)
        raise ValueError('no GPR daily Stata link found')
    vintage, url = max(matches)
    return (url, vintage)

def validate_stata(path: Path) -> None:
    try:
        df = pd.read_stata(path, convert_categoricals=False)
    except Exception as exc:
        raise ValueError('download is not a readable Stata file') from exc
    required = {'date', 'GPRD', 'GPRD_THREAT', 'GPRD_ACT'}
    if not required.issubset(df.columns):
        raise ValueError('GPR Stata file missing required columns')
    if df.empty:
        raise ValueError('GPR Stata file is empty')

def collect(raw_dir: Path, manifest_dir: Path, *, page_url=SOURCE_PAGE, session=None) -> dict:
    s = session or requests.Session()
    headers = {'User-Agent': 'GoldRush/0.1 personal research'}
    page = s.get(page_url, headers=headers, timeout=60)
    if page.status_code != 200:
        raise RuntimeError(f'GPR page HTTP status {page.status_code}')
    url, vintage = discover(page.text, page_url)
    response = s.get(url, headers=headers, timeout=120)
    if response.status_code != 200 or not response.content:
        raise RuntimeError(f'GPR download HTTP status {response.status_code}')
    if vintage is None:
        modified = response.headers.get('Last-Modified', '')
        try:
            vintage = datetime.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y%m%d')
        except ValueError as exc:
            raise ValueError('undated GPR link has no usable Last-Modified vintage') from exc
    metadata = None
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw = raw_dir / f'gpr-daily-{vintage}-.dta'
    if raw.exists() and raw.read_bytes() != response.content:
        raise FileExistsError('immutable raw path collision')
    if not raw.exists():
        raw.write_bytes(response.content)
    validate_stata(raw)
    manifest = {'variable_id': 'L6-001', 'source_url': url, 'source_page': page_url, 'retrieved_at': datetime.now(timezone.utc).isoformat(), 'source_vintage_date': f'{vintage[:4]}-{vintage[4:6]}-{vintage[6:]}', 'raw_path': str(raw), 'size_bytes': len(response.content), 'content_type': response.headers.get('content-type', ''), 'http_status': response.status_code, 'collector_version': VERSION, 'authors': 'Dario Caldara and Matteo Iacoviello'}
    manifest_dir.mkdir(parents=True, exist_ok=True)
    mp = manifest_dir / f'gpr-{vintage}--{stamp}.manifest.json'
    payload = json.dumps(manifest, indent=2) + '\n'
    if mp.exists() and mp.read_text(encoding='utf-8') != payload:
        raise FileExistsError('immutable GPR manifest collision')
    if not mp.exists():
        mp.write_text(payload, encoding='utf-8')
    manifest['manifest_path'] = str(mp)
    return manifest

def main() -> None:
    root = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw-dir', type=Path, default=root / 'data/raw')
    ap.add_argument('--manifest-dir', type=Path, default=root / 'data/manifests')
    args = ap.parse_args()
    print(json.dumps(collect(args.raw_dir, args.manifest_dir), indent=2))
if __name__ == '__main__':
    main()
