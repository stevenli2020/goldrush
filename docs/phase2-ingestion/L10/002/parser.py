"""Extract the COMEX Gold futures open-interest total from CME Section 02B."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path


ROW_PREFIX = "GC COMEX GOLD FUTURES"
OPEN_INTEREST_START = 102
OPEN_INTEREST_END = 112
PROJECT_ROOT = Path(__file__).resolve().parents[4]


def extract_pdf_text(pdf_path: Path) -> str:
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    if not result.stdout.strip():
        raise ValueError("Section 02B PDF produced no text")
    return result.stdout


def observation_date_from_text(text: str) -> str:
    match = re.search(r"\b[A-Z][a-z]{2},\s+[A-Z][a-z]{2}\s+\d{1,2},\s+\d{4}\s+PG02B\b", text)
    if not match:
        raise ValueError("Section 02B bulletin date was not found")
    date_text = match.group().removesuffix(" PG02B")
    return datetime.strptime(date_text, "%a, %b %d, %Y").date().isoformat()


def open_interest_from_text(text: str) -> int:
    rows = [line for line in text.splitlines() if line.startswith(ROW_PREFIX)]
    if len(rows) != 1:
        raise ValueError(f"expected exactly one {ROW_PREFIX!r} row; found {len(rows)}")
    value_text = rows[0][OPEN_INTEREST_START:OPEN_INTEREST_END].strip().replace(",", "")
    if not value_text.isdigit():
        raise ValueError("current COMEX Gold open-interest field is malformed")
    return int(value_text)


def validate_manifest(pdf_path: Path, manifest_path: Path) -> None:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read source manifest: {exc}") from exc
    if manifest.get("target") != "section02b":
        raise ValueError("source manifest is not for CME Section 02B")
    if Path(manifest.get("raw_path", "")).resolve() != pdf_path.resolve():
        raise ValueError("source manifest does not identify the supplied PDF")


def source_reference(manifest_path: Path) -> str:
    try:
        return manifest_path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError as exc:
        raise ValueError("source manifest must be inside the project") from exc


def parse(pdf_path: Path, manifest_path: Path) -> list[dict[str, object]]:
    validate_manifest(pdf_path, manifest_path)
    text = extract_pdf_text(pdf_path)
    return [{
        "variable_id": "L10-002",
        "observation_date": observation_date_from_text(text),
        "product": "COMEX GOLD",
        "open_interest_contracts": open_interest_from_text(text),
        "unit": "contracts",
        "source_series_id": "COMEX_GOLD",
        "source_manifest": source_reference(manifest_path),
        "validation_status": "PASS",
        "availability_status": "AVAILABLE",
    }]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = parse(args.pdf, args.source_manifest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=output[0])
        writer.writeheader()
        writer.writerows(output)
    print(f"Wrote {len(output)} observations to {args.output}")


if __name__ == "__main__":
    main()
