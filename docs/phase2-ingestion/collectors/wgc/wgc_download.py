"""Download and preserve WGC workbooks; variable parsers do extraction."""
from __future__ import annotations
import argparse, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urljoin
import yaml
from curl_cffi import requests
USER_AGENT = 'Mozilla/5.0 GoldRush WGC downloader'

def load_config(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8'))

def metadata_bytes(content: bytes) -> str:
    return None

def load_cookies(path: Path):
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding='utf-8'))
    return value if isinstance(value, list) else []

def filename_from_response(response, url: str) -> str:
    header = response.headers.get('Content-Disposition', '')
    match = re.search('filename\\*=UTF-8\'\'([^;]+)|filename=\\"?([^;\\"]+)', header, re.I)
    return unquote((match.group(1) or match.group(2)).strip()) if match else unquote(url.split('/')[-1].split('?')[0])

def find_download_url(html: str, pattern: str, page_url: str) -> str:
    match = re.search(pattern, html, re.I)
    if not match:
        raise RuntimeError('no matching workbook link found')
    return urljoin(page_url, unquote(match.group(1).strip()))

def validate_xlsx(response):
    if response.status_code != 200:
        raise RuntimeError(f'HTTP status {response.status_code}')
    content_type = response.headers.get('Content-Type', '').lower()
    if not response.content or 'text/html' in content_type or (not response.content.startswith(b'PK\x03\x04')):
        raise RuntimeError('response is not a non-empty XLSX file')

def latest_manifest(root: Path, target: str):
    records = []
    for path in root.glob(f'{target}-*.json'):
        try:
            records.append(json.loads(path.read_text(encoding='utf-8')))
        except (OSError, json.JSONDecodeError):
            pass
    return max(records, key=lambda x: x.get('downloaded_at', ''), default=None)

def download_target(session, name, target, roots):
    now = datetime.now(timezone.utc)
    page = session.get(target['page_url'], headers={'User-Agent': USER_AGENT}, impersonate='chrome', timeout=30)
    if page.status_code != 200:
        raise RuntimeError(f'page HTTP status {page.status_code}')
    url = find_download_url(page.text, target['link_pattern'], target['page_url'])
    response = session.get(url, headers={'User-Agent': USER_AGENT, 'Referer': target['page_url']}, impersonate='chrome', timeout=60)
    validate_xlsx(response)
    filename, content = (filename_from_response(response, url), response.content)
    metadata = None
    previous = latest_manifest(roots['manifests'], name)
    changed = not previous or previous.get('') != metadata
    raw_path = roots['raw'] / target['directory'] / filename
    if changed:
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(content)
    record = {'target': name, 'page_url': target['page_url'], 'download_url': url, 'filename': filename, 'raw_path': str(raw_path), 'size_bytes': len(content), 'downloaded_at': now.isoformat(), 'http_status': response.status_code, 'content_type': response.headers.get('Content-Type', ''), 'changed': changed}
    roots['manifests'].mkdir(parents=True, exist_ok=True)
    stamp = now.strftime('%Y%m%dT%H%M%SZ')
    manifest_path = roots['manifests'] / f'{name}-{stamp}.json'
    record['manifest_path'] = str(manifest_path)
    manifest_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    return record

def main(argv=None):
    cli = argparse.ArgumentParser()
    cli.add_argument('--config', type=Path, default=Path(__file__).with_name('config.yaml'))
    cli.add_argument('--target', help='download one configured target')
    args = cli.parse_args(argv)
    config_path, config = (args.config.resolve(), load_config(args.config.resolve()))
    base = config_path.parent
    roots = {k: (base / config['collector'][v]).resolve() for k, v in {'raw': 'raw_root', 'manifests': 'manifest_root', 'logs': 'log_root'}.items()}
    session = requests.Session()
    cookie_path = (base / config['collector']['cookie_jar']).resolve()
    for cookie in load_cookies(cookie_path):
        if cookie.get('name') and cookie.get('value'):
            session.cookies.set(cookie['name'], cookie['value'], domain=cookie.get('domain', '.gold.org'))
    results = []
    targets = config['targets']
    if args.target:
        if args.target not in targets:
            cli.error(f'unknown target: {args.target}')
        targets = {args.target: targets[args.target]}
    for name, target in targets.items():
        try:
            result = download_target(session, name, target, roots)
            results.append(result)
            print(f"OK {name}: {result['filename']} ({('changed' if result['changed'] else 'unchanged')})")
        except Exception as exc:
            results.append({'target': name, 'error': str(exc)})
            print(f'ERROR {name}: {exc}', file=sys.stderr)
    roots['logs'].mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    (roots['logs'] / f'wgc-download-{stamp}.json').write_text(json.dumps({'results': results}, indent=2) + '\n', encoding='utf-8')
    return int(any(('error' in item for item in results)))
if __name__ == '__main__':
    raise SystemExit(main())
