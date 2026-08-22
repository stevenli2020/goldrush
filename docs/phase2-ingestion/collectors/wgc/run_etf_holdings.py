"""Shared-extractor adapter for the existing L0-003 ETF holdings parser."""
import argparse
import sys
from pathlib import Path

import pandas as pd

PARSER_DIR = Path(__file__).resolve().parents[2] / "L0" / "003"
sys.path.insert(0, str(PARSER_DIR))
from parse_etf_holding import GoldETFHoldingsParser  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", default="docs/phase2-ingestion/L0/003/processed/L0_003_observations.csv")
    parser.add_argument("--log", default="docs/phase2-ingestion/L0/003/archive/ingest.log")
    parser.add_argument("--publication-date", required=True)
    parser.add_argument("--download-date", required=True)
    args = parser.parse_args(argv)
    output = Path(args.output); log = Path(args.log)
    output.parent.mkdir(parents=True, exist_ok=True); log.parent.mkdir(parents=True, exist_ok=True)
    parser_impl = GoldETFHoldingsParser(parser_version="1.0.0", log_path=str(log))
    records = parser_impl.parse_file(args.input, args.publication_date, args.download_date)
    pd.DataFrame(records).to_csv(output, index=False, encoding="utf-8")
    print(f"ETF holdings parsed: {len(records)} records; output={output}")
    return 1 if parser_impl.validation_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
