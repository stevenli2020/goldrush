"""Compare cme-fedwatch output with preserved official CME FedWatch CSVs."""
from __future__ import annotations
import argparse
import csv
import importlib.util
import json
import re
from datetime import date, datetime
from pathlib import Path
PACKAGE_VERSION = '0.1.3'
SUM_TOLERANCE = 0.001
MAX_BUCKET_ERROR = 0.1
MAX_TVD = 0.1
MATERIAL_PROBABILITY = 0.001
OFFICIAL_NAME = re.compile('^FedMeeting_(\\d{8})_downloaded_\\d{4}-\\d{2}-\\d{2}\\.csv$')
OFFICIAL_BUCKET = re.compile('^\\((\\d+)-(\\d+)\\)$')
PACKAGE_BUCKET = re.compile('^(\\d+(?:\\.\\d+)?)%-(\\d+(?:\\.\\d+)?)%$')

def metadata_file(path: Path) -> str:
    return None

def meeting_date_from_filename(path: Path) -> date:
    match = OFFICIAL_NAME.fullmatch(path.name)
    if not match:
        raise ValueError(f'invalid official comparison filename: {path.name}')
    return datetime.strptime(match.group(1), '%Y%m%d').date()

def official_bucket(label: str) -> tuple[float, float]:
    match = OFFICIAL_BUCKET.fullmatch(label)
    if not match:
        raise ValueError(f'invalid official outcome bucket: {label}')
    lower, upper = map(int, match.groups())
    if lower >= upper:
        raise ValueError(f'unordered official outcome bucket: {label}')
    return (lower / 100.0, upper / 100.0)

def bucket_key(lower: float, upper: float) -> str:
    return f'({round(lower * 100)}-{round(upper * 100)})'

def load_official(path: Path, trade_date: date) -> dict[str, float]:
    with path.open(newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or 'Date' not in reader.fieldnames:
            raise ValueError(f'official CSV missing Date header: {path}')
        bucket_headers = [header for header in reader.fieldnames if header != 'Date']
        for header in bucket_headers:
            official_bucket(header)
        target = None
        for row in reader:
            try:
                row_date = datetime.strptime(row['Date'], '%m/%d/%Y').date()
            except (TypeError, ValueError) as exc:
                raise ValueError(f"invalid official Date value: {row.get('Date')}") from exc
            if row_date == trade_date:
                target = row
                break
    if target is None:
        raise ValueError(f'official CSV has no row for {trade_date}: {path}')
    distribution: dict[str, float] = {}
    for header in bucket_headers:
        value = (target.get(header) or '').strip()
        if value == '':
            continue
        probability = float(value)
        if not 0.0 <= probability <= 1.0:
            raise ValueError(f'official probability outside 0..1: {header}={value}')
        lower, upper = official_bucket(header)
        distribution[bucket_key(lower, upper)] = probability
    return distribution

def compare_distributions(official: dict[str, float], calculated: dict[str, float]) -> dict:
    buckets = sorted(set(official) | set(calculated))
    errors = {bucket: abs(calculated.get(bucket, 0.0) - official.get(bucket, 0.0)) for bucket in buckets}
    official_sum = sum(official.values())
    calculated_sum = sum(calculated.values())
    official_modal = max(official, key=official.get)
    calculated_modal = max(calculated, key=calculated.get)
    missing_material = sorted((bucket for bucket, probability in official.items() if probability >= MATERIAL_PROBABILITY and bucket not in calculated))
    maximum_error = max(errors.values(), default=0.0)
    tvd = 0.5 * sum(errors.values())
    checks = {'official_sum_within_tolerance': abs(official_sum - 1.0) <= SUM_TOLERANCE, 'calculated_sum_within_tolerance': abs(calculated_sum - 1.0) <= SUM_TOLERANCE, 'modal_outcome_agrees': official_modal == calculated_modal, 'maximum_error_within_threshold': maximum_error <= MAX_BUCKET_ERROR, 'tvd_within_threshold': tvd <= MAX_TVD, 'no_material_official_bucket_missing': not missing_material}
    return {'official_probability_sum': official_sum, 'calculated_probability_sum': calculated_sum, 'official_modal_outcome': official_modal, 'calculated_modal_outcome': calculated_modal, 'official_bucket_coverage': sorted(official), 'calculated_bucket_coverage': sorted(calculated), 'missing_material_official_buckets': missing_material, 'maximum_absolute_bucket_error': maximum_error, 'total_variation_distance': tvd, 'checks': checks, 'pass': all(checks.values())}

def _production_parser():
    path = Path(__file__).with_name('parser.py')
    spec = importlib.util.spec_from_file_location('l3_004_production_parser', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def build_report(official_dir: Path, manifests: list[Path]) -> dict:
    production = _production_parser()
    official_files = {meeting_date_from_filename(path): path for path in official_dir.glob('FedMeeting_*_downloaded_*.csv')}
    if len(official_files) != 3:
        raise ValueError(f'expected three official comparison files, found {len(official_files)}')
    comparisons = []
    for manifest_path in manifests:
        inputs = production.source_inputs(manifest_path)
        tree = production.calculate_tree(inputs)
        if len(tree) < 3:
            raise ValueError('cumulative tree has fewer than three meetings')
        for sequence, meeting in enumerate(tree[:3], start=1):
            meeting_date = meeting['meeting_date']
            official_path = official_files.get(meeting_date)
            if official_path is None:
                raise ValueError(f'no official file for {meeting_date}')
            official = load_official(official_path, inputs['observation_date'])
            calculated = {bucket_key(inputs['target_lower'] + moves * 0.25, inputs['target_upper'] + moves * 0.25): probability for moves, probability in meeting['distribution'].items()}
            metrics = compare_distributions(official, calculated)
            buckets = sorted(set(official) | set(calculated))
            comparisons.append({'observation_date': inputs['observation_date'].isoformat(), 'meeting_date': meeting_date.isoformat(), 'meeting_sequence': sequence, 'production_scope': sequence <= 2, 'contract': meeting['contract'], 'conditional_transition': {str(key): value for key, value in meeting['conditional_transition'].items()}, 'official_file_path': str(official_path), 'source_manifest_path': str(manifest_path), 'official_distribution': official, 'calculated_distribution': calculated, 'bucket_differences': {bucket: calculated.get(bucket, 0.0) - official.get(bucket, 0.0) for bucket in buckets}, **metrics})
    expected_dates = {date(2026, 8, 19), date(2026, 8, 20), date(2026, 8, 21)}
    actual_dates = {date.fromisoformat(item['observation_date']) for item in comparisons}
    if actual_dates != expected_dates:
        raise ValueError(f'comparison dates mismatch: {sorted(actual_dates)}')
    production_gate = all((item['pass'] for item in comparisons if item['production_scope']))
    recursive_gate = all((item['pass'] for item in comparisons if not item['production_scope']))
    return {'comparison': 'L3-004 cumulative probability tree validation', 'package_name': 'cme-fedwatch', 'package_version': PACKAGE_VERSION, 'calculation_method': production.METHOD, 'thresholds': {'probability_sum_tolerance': SUM_TOLERANCE, 'maximum_absolute_bucket_error': MAX_BUCKET_ERROR, 'maximum_total_variation_distance': MAX_TVD, 'material_official_probability': MATERIAL_PROBABILITY}, 'comparisons': sorted(comparisons, key=lambda item: (item['observation_date'], item['meeting_date'])), 'production_scope_gate_pass': production_gate, 'recursive_validation_pass': recursive_gate, 'full_validation_pass': production_gate and recursive_gate}

def main(argv: list[str] | None=None) -> int:
    parser = argparse.ArgumentParser(description='Validate L3-004 Alternative 1')
    parser.add_argument('--official-dir', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, action='append', required=True)
    args = parser.parse_args(argv)
    report = build_report(args.official_dir, args.manifest)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'production_scope_gate_pass': report['production_scope_gate_pass'], 'recursive_validation_pass': report['recursive_validation_pass'], 'report': str(args.report)}))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
