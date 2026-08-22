"""Shared-extractor adapter for the existing L0-006 recycling collector."""
import argparse
import sys
from pathlib import Path

PARSER_DIR = Path(__file__).resolve().parents[2] / "L0" / "006" / "scripts"
sys.path.insert(0, str(PARSER_DIR))
from parse_gold_recycling import GoldRecyclingCollector  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--publication-date", required=True)
    ap.add_argument("--download-date", required=True)
    args = ap.parse_args(argv)
    collector = GoldRecyclingCollector(output_path=args.output)
    payload = collector.run(publication_date=args.publication_date, source_file=args.input, is_live_source=True)
    print(f"Recycling observations parsed: {len(payload.get('observations', []))}")
    return 0 if payload.get("observations") else 1


if __name__ == "__main__":
    raise SystemExit(main())
