"""Shared-extractor adapter for the existing L0-006 recycling collector."""
import argparse
import json
import sys
from pathlib import Path
PARSER_DIR = Path(__file__).resolve().parents[2] / 'L0' / '006' / 'scripts'
sys.path.insert(0, str(PARSER_DIR))
from parse_gold_recycling import GoldRecyclingCollector

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--publication-date', required=True)
    ap.add_argument('--download-date', required=True)
    ap.add_argument('--source-manifest', required=True, type=Path)
    args = ap.parse_args(argv)
    manifest = json.loads(args.source_manifest.read_text(encoding='utf-8'))
    if Path(manifest.get('raw_path', '')).resolve() != args.input.resolve():
        raise ValueError('Source manifest raw_path does not match --input')
    if args.download_date != manifest.get('downloaded_at', '')[:10]:
        raise ValueError('Download date does not match source manifest')
    collector = GoldRecyclingCollector(output_path=args.output)
    payload = collector.run(publication_date=args.publication_date, source_file=args.input, is_live_source=True)
    payload['ingestion_metadata']['downloaded_at'] = manifest['downloaded_at']
    payload['ingestion_metadata']['source_manifest'] = str(args.source_manifest)
    args.output.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    print(f"Recycling observations parsed: {len(payload.get('observations', []))}")
    return 0 if payload.get('observations') else 1
if __name__ == '__main__':
    raise SystemExit(main())
