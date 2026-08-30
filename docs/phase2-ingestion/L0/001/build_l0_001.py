from pathlib import Path

def create_config_file(output_path: str='data/config.yaml') -> None:
    """Generates the YAML configuration file for L0-001 WGC Above-Ground Stocks collector."""
    config_content = '# L0-001 Configuration: World Gold Council Above-Ground Gold Stocks\n\nsource:\n  url: "https://www.gold.org/goldhub/data/above-ground-stocks"\n  worksheet_name: "Above-ground stocks"\n  source_citation: "Metals Focus, Refinitiv GFMS, World Gold Council"\n\nparser:\n  script_path: "scripts/parse_above_ground.py"\n  version: "1.0.0"\n\npaths:\n  raw_dir: "data/raw"\n  processed_dir: "data/processed"\n  samples_dir: "data/samples"\n  archive_dir: "data/archive"\n  filename_pattern: "raw_wgc_above_ground_stock_{date}.xlsx"\n\noutputs:\n  csv_filename: "above_ground_stocks.csv"\n  parquet_filename: "above_ground_stocks.parquet"\n  warnings_filename: "validation_warnings.log"\n  revision_filename: "revision_log.json"\n\nfreshness:\n  max_age_days: 365\n  fallback_to_prior: true\n\nvalidation:\n  sum_tolerance_tonnes: 1.5\n  yoy_warning_threshold_pct: 25.0\n  allow_negative_values: false\n'
    target_file = Path(output_path)
    target_file.parent.mkdir(parents=True, exist_ok=True)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(config_content.strip() + '\n')
    print(f'Successfully generated {target_file.resolve()}')
if __name__ == '__main__':
    create_config_file()
