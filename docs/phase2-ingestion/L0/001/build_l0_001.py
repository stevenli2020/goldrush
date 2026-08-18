from pathlib import Path


def create_config_file(output_path: str = "data/config.yaml") -> None:
    """Generates the YAML configuration file for L0-001 WGC Above-Ground Stocks collector."""
    config_content = """# L0-001 Configuration: World Gold Council Above-Ground Gold Stocks

source:
  url: "https://www.gold.org/goldhub/data/above-ground-stocks"
  worksheet_name: "Above-ground stocks"
  source_citation: "Metals Focus, Refinitiv GFMS, World Gold Council"

parser:
  script_path: "scripts/parse_above_ground.py"
  version: "1.0.0"

paths:
  raw_dir: "data/raw"
  processed_dir: "data/processed"
  samples_dir: "data/samples"
  archive_dir: "data/archive"
  filename_pattern: "raw_wgc_above_ground_stock_{date}.xlsx"

outputs:
  csv_filename: "above_ground_stocks.csv"
  parquet_filename: "above_ground_stocks.parquet"
  warnings_filename: "validation_warnings.log"
  revision_filename: "revision_log.json"

freshness:
  max_age_days: 365
  fallback_to_prior: true

validation:
  sum_tolerance_tonnes: 1.5
  yoy_warning_threshold_pct: 25.0
  allow_negative_values: false
"""

    target_file = Path(output_path)
    target_file.parent.mkdir(parents=True, exist_ok=True)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(config_content.strip() + "\n")

    print(f"Successfully generated {target_file.resolve()}")


if __name__ == "__main__":
    create_config_file()