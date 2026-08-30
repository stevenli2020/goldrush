"""Run one silent L6-002 live-feed snapshot through retrieval and scoring."""
from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COLLECTOR_PATH = ROOT / 'phase2-ingestion/L6/002/collector.py'
PARSER_PATH = ROOT / 'phase2-ingestion/L6/002/parser.py'
RETRIEVAL_PATH = Path(__file__).with_name('retrieval.py')
SCORER_PATH = Path(__file__).with_name('scorer.py')


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(monitor_dir: Path, year: int | None = None) -> dict:
    collector = load(COLLECTOR_PATH, 'l6_002_collector')
    parser = load(PARSER_PATH, 'l6_002_parser')
    retrieval = load(RETRIEVAL_PATH, 'l6_002_retrieval')
    scorer = load(SCORER_PATH, 'l6_002_scorer')
    raw_dir = monitor_dir / 'raw'
    manifest_dir = monitor_dir / 'manifests'
    phase2_csv = monitor_dir / 'phase2.csv'
    run_at = datetime.now(timezone.utc)
    manifest = collector.collect(raw_dir, manifest_dir, year=year)
    raw_path = Path(manifest['raw_path'])
    manifest_path = next(manifest_dir.glob(f"L6-002_{manifest['publication_date']}*.manifest.json"))
    events = parser.parse(raw_path, manifest_path)
    parser.write(events, phase2_csv)
    candidate_events = [event for event in events if event['is_candidate']]
    records = []
    for event in candidate_events:
        evidence = retrieval.retrieve_event(event)
        records.append({**event, **evidence, **scorer.score_record(evidence)})
    result = {
        'variable_id': 'L6-002',
        'run_status': 'SILENT_COMPLETE',
        'notifications_sent': False,
        'run_at': run_at.isoformat(),
        'source_manifest': str(manifest_path),
        'phase2_output': str(phase2_csv),
        'candidate_count': len(candidate_events),
        'records': records,
    }
    output = monitor_dir / f'silent-monitor-{run_at.strftime("%Y%m%dT%H%M%SZ")}.json'
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Wrote silent monitor snapshot to {output}')
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--monitor-dir', type=Path, required=True)
    ap.add_argument('--year', type=int)
    args = ap.parse_args()
    run(args.monitor_dir, args.year)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
