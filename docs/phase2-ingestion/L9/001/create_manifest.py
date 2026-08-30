"""Create a shared-WGC-compatible manifest for a manual workbook download."""
from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
PAGE_URL = 'https://www.gold.org/goldhub/data/gold-premium'
DOWNLOAD_URL = 'https://www.gold.org/download/file/11657/gold-premiums.xlsx'

def main() -> int:
    cli = argparse.ArgumentParser()
    cli.add_argument('workbook', type=Path)
    cli.add_argument('manifest', type=Path)
    cli.add_argument('--page-url', default=PAGE_URL)
    cli.add_argument('--download-url', default=DOWNLOAD_URL)
    args = cli.parse_args()
    metadata = None
    payload = {'target': 'gold_premiums', 'page_url': args.page_url, 'download_url': args.download_url, 'filename': 'gold-premiums.xlsx', 'raw_path': str(args.workbook), 'size_bytes': args.workbook.stat().st_size, 'downloaded_at': datetime.now(timezone.utc).isoformat(), 'http_status': None, 'content_type': None, 'download_method': 'manual_authenticated_download'}
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    payload['manifest_path'] = str(args.manifest)
    args.manifest.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in payload.items() if k not in {'raw_path', 'manifest_path'}}))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
