#!/usr/bin/env python3
"""
World Gold Council (WGC) Above-Ground Stocks Parser & Collector
Module ID: L0-001

Ingests, validates, normalizes, and tracks revisions for historical above-ground
gold stock datasets published by the World Gold Council.
"""

import argparse
import datetime
import hashlib
import json
import logging
import os
import re
import sys
from typing import Dict, List, Optional, Tuple

import pandas as pd

PARSER_VERSION = "1.0.0"
DEFAULT_SHEET_NAME = "Above-ground stocks"
DEFAULT_SOURCE_CITATION = "Metals Focus, Refinitiv GFMS, World Gold Council"

# Standard label mapping for raw cell values to canonical field names
LABEL_MAP = {
    "jewellery": "jewellery_tonnes",
    "private investment": "private_investment_tonnes",
    "bars & coins": "bars_and_coins_tonnes",
    "bars and coins": "bars_and_coins_tonnes",
    "etfs": "etfs_tonnes",
    "central banks": "central_banks_tonnes",
    "other": "other_tonnes",
    "total": "total_above_ground_tonnes",
}

REQUIRED_METRICS = [
    "jewellery_tonnes",
    "private_investment_tonnes",
    "bars_and_coins_tonnes",
    "etfs_tonnes",
    "central_banks_tonnes",
    "other_tonnes",
    "total_above_ground_tonnes",
]

OUTPUT_COLUMNS = [
    "observation_year",
    "observation_date",
    "jewellery_tonnes",
    "private_investment_tonnes",
    "bars_and_coins_tonnes",
    "etfs_tonnes",
    "central_banks_tonnes",
    "other_tonnes",
    "total_above_ground_tonnes",
    "source_citation",
    "workbook_sha256",
    "ingested_at",
    "download_date",
    "source_publication_date",
    "validation_status",
    "availability_status",
    "parser_version",
]
SCHEMA_COLUMNS = OUTPUT_COLUMNS


def calculate_sha256(file_path: str) -> str:
    """Computes SHA-256 hash of input file for data provenance tracking."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def normalize_label(label: str) -> Optional[str]:
    """Normalizes raw cell string to standard schema metric field name."""
    if not isinstance(label, str):
        return None
    clean = re.sub(r"\s+", " ", label).strip().lower()
    for key, mapped in LABEL_MAP.items():
        if key == clean or key in clean:
            return mapped
    return None


def extract_source_citation(df_raw: pd.DataFrame) -> str:
    """Extracts source citation string from raw worksheet footer if present."""
    for idx, row in df_raw.iterrows():
        for cell in row:
            if pd.notna(cell):
                cell_str = str(cell).strip()
                if cell_str.lower().startswith("source:"):
                    return cell_str.split(":", 1)[1].strip()
    return DEFAULT_SOURCE_CITATION


def parse_above_ground_data(
    excel_path: str,
    sheet_name: str = DEFAULT_SHEET_NAME,
    download_date: Optional[str] = None,
    source_publication_date: Optional[str] = None,
) -> pd.DataFrame:
    """Reads WGC Excel workbook and extracts wide normalized data."""
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Workbook not found at path: {excel_path}")

    file_hash = calculate_sha256(excel_path)
    retrieved_at = datetime.datetime.now(datetime.timezone.utc).isoformat()

    df_raw = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)

    # Search for year header row dynamically (row containing consecutive 4-digit years)
    year_row_idx = None
    year_cols: Dict[int, int] = {}

    for idx, row in df_raw.iterrows():
        matches = {}
        for c_idx, val in enumerate(row):
            if pd.notna(val):
                val_str = str(val).strip().split(".")[0]
                if re.match(r"^(19|20)\d{2}$", val_str):
                    matches[c_idx] = int(val_str)
        if len(matches) >= 3:
            year_row_idx = idx
            year_cols = matches
            break

    if year_row_idx is None or not year_cols:
        raise ValueError(f"Could not locate valid year headers in sheet '{sheet_name}'.")

    extracted_citation = extract_source_citation(df_raw)
    extracted_data: Dict[int, Dict[str, float]] = {year: {} for year in year_cols.values()}

    for idx in range(year_row_idx + 1, len(df_raw)):
        row = df_raw.iloc[idx]
        first_cell = str(row.iloc[0]) if pd.notna(row.iloc[0]) else str(row.iloc[1])
        field_name = normalize_label(first_cell)

        if field_name:
            for c_idx, year in year_cols.items():
                val = row.iloc[c_idx]
                if pd.isna(val):
                    raise ValueError(f"Missing required numeric value for field '{field_name}' in year {year}.")
                
                try:
                    clean_val = float(re.sub(r"[^\d.-]", "", str(val)))
                except ValueError:
                    raise ValueError(f"Malformed value '{val}' for field '{field_name}' in year {year}.")

                if not pd.notna(clean_val) or clean_val < 0:
                    raise ValueError(f"Invalid non-positive or non-finite value '{clean_val}' for field '{field_name}' in year {year}.")

                extracted_data[year][field_name] = clean_val

    rows = []
    for year in sorted(extracted_data.keys()):
        metrics = extracted_data[year]
        for req_field in REQUIRED_METRICS:
            if req_field not in metrics:
                raise ValueError(f"Required metric '{req_field}' missing for year {year}.")

        record = {
            "observation_year": int(year),
            "observation_date": f"{year}-12-31",
            "jewellery_tonnes": metrics["jewellery_tonnes"],
            "private_investment_tonnes": metrics["private_investment_tonnes"],
            "bars_and_coins_tonnes": metrics["bars_and_coins_tonnes"],
            "etfs_tonnes": metrics["etfs_tonnes"],
            "central_banks_tonnes": metrics["central_banks_tonnes"],
            "other_tonnes": metrics["other_tonnes"],
            "total_above_ground_tonnes": metrics["total_above_ground_tonnes"],
            "source_citation": extracted_citation,
            "workbook_sha256": file_hash,
            "ingested_at": retrieved_at,
            "download_date": download_date,
            "source_publication_date": source_publication_date,
            "validation_status": "PASS",
            "availability_status": "AVAILABLE",
            "parser_version": PARSER_VERSION,
        }
        rows.append(record)

    return pd.DataFrame(rows)[OUTPUT_COLUMNS]


def run_validations_and_log(
    df: pd.DataFrame,
    warnings_path: str,
    sum_tolerance: float = 1e-4,
    yoy_threshold_pct: float = 25.0,
) -> List[str]:
    """Validates structural sum equality and logs YoY variance warnings."""
    warnings = []

    for idx, row in df.iterrows():
        year = int(row["observation_year"])
        components_sum = (
            row["jewellery_tonnes"]
            + row["private_investment_tonnes"]
            + row["central_banks_tonnes"]
            + row["other_tonnes"]
        )
        total = row["total_above_ground_tonnes"]
        diff = abs(components_sum - total)

        if diff > sum_tolerance:
            raise ValueError(
                f"Validation Failure in Year {year}: Sum of components ({components_sum:.2f}) "
                f"differs from declared total ({total:.2f}) by {diff:.2f} tonnes (tolerance: {sum_tolerance})."
            )

        sub_diff = abs(row["bars_and_coins_tonnes"] + row["etfs_tonnes"] - row["private_investment_tonnes"])
        if sub_diff > sum_tolerance:
            raise ValueError(f"Validation Failure in Year {year}: investment subcategories differ by {sub_diff:.6f} tonnes.")

    df_sorted = df.sort_values("observation_year").reset_index(drop=True)
    for i in range(1, len(df_sorted)):
        prev_row = df_sorted.iloc[i - 1]
        curr_row = df_sorted.iloc[i]
        year = int(curr_row["observation_year"])

        for metric in REQUIRED_METRICS:
            prev_val = prev_row[metric]
            curr_val = curr_row[metric]

            if prev_val > 0:
                pct_change = ((curr_val - prev_val) / prev_val) * 100.0
                if abs(pct_change) > yoy_threshold_pct:
                    warnings.append(
                        f"[YoY WARNING] Year {year}, Field '{metric}': Large shift of {pct_change:.2f}% ({prev_val} -> {curr_val})."
                    )
                if curr_val < prev_val:
                    warnings.append(
                        f"[YoY DECREASE WARNING] Year {year}, Field '{metric}': Unexpected YoY decrease ({prev_val} -> {curr_val})."
                    )

    os.makedirs(os.path.dirname(warnings_path), exist_ok=True)
    with open(warnings_path, "w", encoding="utf-8") as f:
        if warnings:
            f.write("\n".join(warnings) + "\n")
        else:
            f.write("No validation warnings identified.\n")

    return warnings

validate_and_log = run_validations_and_log


def compare_and_log_revisions(
    current_df: pd.DataFrame,
    previous_filepath: Optional[str],
    revision_log_path: str,
) -> List[Dict]:
    """Compares current run against prior execution dataset to track source revisions."""
    revisions = []

    if previous_filepath and os.path.exists(previous_filepath):
        if previous_filepath.endswith(".parquet"):
            prev_df = pd.read_parquet(previous_filepath)
        else:
            prev_df = pd.read_csv(previous_filepath)

        curr_indexed = current_df.set_index("observation_year")
        prev_indexed = prev_df.set_index("observation_year")

        common_years = curr_indexed.index.intersection(prev_indexed.index)

        for year in common_years:
            for metric in REQUIRED_METRICS:
                if metric in prev_indexed.columns:
                    curr_val = float(curr_indexed.loc[year, metric])
                    prev_val = float(prev_indexed.loc[year, metric])

                    if abs(curr_val - prev_val) > 1e-4:
                        revisions.append({
                            "observation_year": int(year),
                            "field": metric,
                            "previous_value": prev_val,
                            "new_value": curr_val,
                            "difference": curr_val - prev_val,
                            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        })

    os.makedirs(os.path.dirname(revision_log_path), exist_ok=True)
    with open(revision_log_path, "w", encoding="utf-8") as f:
        json.dump(revisions, f, indent=2)

    return revisions


def main():
    parser = argparse.ArgumentParser(description="Parse WGC Above-Ground Gold Stocks Workbook")
    parser.add_argument("--input", "-i", required=True, help="Path to raw WGC excel file")
    parser.add_argument("--output-dir", "-o", default="data/processed", help="Output directory")
    parser.add_argument("--sheet", default=DEFAULT_SHEET_NAME, help="Worksheet name")
    parser.add_argument("--previous", help="Path to previous processed CSV or Parquet file")
    parser.add_argument("--download-date", help="Manual download date (YYYY-MM-DD)")
    parser.add_argument("--publication-date", help="WGC publication date (YYYY-MM-DD)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df_processed = parse_above_ground_data(
        args.input,
        sheet_name=args.sheet,
        download_date=args.download_date,
        source_publication_date=args.publication_date,
    )

    warnings_path = os.path.join(args.output_dir, "validation_warnings.log")
    validate_and_log(df_processed, warnings_path)

    revision_path = os.path.join(args.output_dir, "revision_log.json")
    compare_and_log_revisions(df_processed, args.previous, revision_path)

    csv_path = os.path.join(args.output_dir, "above_ground_stocks.csv")
    df_processed.to_csv(csv_path, index=False)

    parquet_path = os.path.join(args.output_dir, "above_ground_stocks.parquet")
    try:
        df_processed.to_parquet(parquet_path, index=False)
    except ImportError:
        pass

    print(f"Processing complete. Output written to '{args.output_dir}'.")

compare_revisions = compare_and_log_revisions


if __name__ == "__main__":
    main()
