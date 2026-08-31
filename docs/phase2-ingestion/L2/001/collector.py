"""Collect and preserve OpenBB/yfinance DXY OHLC data."""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from openbb import obb
SYMBOL = 'DX-Y.NYB'
COLLECTOR_VERSION = '0.1.0'

def collect(start_date: str, end_date: str | None, raw_dir: Path, manifest_dir: Path, *, force: bool=False) -> dict:
    result = obb.equity.price.historical(symbol=SYMBOL, start_date=start_date, end_date=end_date, provider='yfinance')
    frame = result.to_df()
    if frame is None or frame.empty:
        raise ValueError('OpenBB returned no DXY observations')
    frame = frame.reset_index()
    if 'date' not in frame.columns:
        raise ValueError('OpenBB response does not contain a date column')
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    payload = frame.to_csv(index=False).encode('utf-8')
    metadata = hashlib.sha256(payload).hexdigest()
    retrieved_at = datetime.now(timezone.utc)
    stamp = retrieved_at.strftime('%Y%m%dT%H%M%SZ')
    raw_path = raw_dir / f'DX-Y.NYB-{stamp}.csv'
    if force or not raw_path.exists():
        raw_path.write_bytes(payload)
    manifest = {'symbol': SYMBOL, 'provider': 'yfinance', 'client': 'OpenBB', 'raw_path': str(raw_path), 'size_bytes': len(payload), 'sha256': metadata, 'observation_count': len(frame), 'retrieved_at': retrieved_at.isoformat(), 'start_date': start_date, 'end_date': end_date, 'changed': True, 'forced': force, 'collector_version': COLLECTOR_VERSION}
    manifest_path = manifest_dir / f'DX-Y.NYB-{stamp}.json'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest | {'manifest_path': str(manifest_path)}

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Collect DXY OHLC data through OpenBB/yfinance')
    cli.add_argument('--start-date', required=True)
    cli.add_argument('--end-date')
    cli.add_argument('--raw-dir', type=Path, default=Path('data/raw'))
    cli.add_argument('--manifest-dir', type=Path, default=Path('data/manifests'))
    cli.add_argument('--force', action='store_true')
    args = cli.parse_args(argv)
    print(json.dumps(collect(args.start_date, args.end_date, args.raw_dir, args.manifest_dir, force=args.force), indent=2))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
