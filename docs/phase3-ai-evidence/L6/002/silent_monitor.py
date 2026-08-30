"""Run one silent L6-002 live-feed snapshot through retrieval and scoring."""
from __future__ import annotations

import argparse
import importlib.util
import json
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
COLLECTOR_PATH = ROOT / 'phase2-ingestion/L6/002/collector.py'
PARSER_PATH = ROOT / 'phase2-ingestion/L6/002/parser.py'
RETRIEVAL_PATH = Path(__file__).with_name('retrieval.py')
SCORER_PATH = Path(__file__).with_name('scorer.py')
RECIPIENTS = ('s101@hotmail.com', 'aiproxy214@gmail.com')


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def notify_research_team(records: list[dict], credentials_path: Path) -> None:
    credentials = json.loads(credentials_path.read_text(encoding='utf-8'))
    sender = credentials['email']
    password = credentials['app-key'].replace(' ', '')
    message = EmailMessage()
    message['Subject'] = 'GoldRush L6-002 Phase 4 review required'
    message['From'] = sender
    message['To'] = ', '.join(RECIPIENTS)
    message.set_content(json.dumps({'variable_id': 'L6-002', 'records': records}, indent=2))
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender, password)
        smtp.send_message(message)


def publish_phase4(result: dict, monitor_dir: Path, credentials_path: Path) -> dict:
    review_until_iso = (datetime.now(timezone.utc) + timedelta(days=7)).replace(microsecond=0).isoformat()
    dashboard_record = {
        'phase4_status': 'ACTIVE',
        'human_review_required': True,
        'human_review_required_until': review_until_iso,
        'run_at': result['run_at'],
        'variable_id': result['variable_id'],
        'records': result['records'],
        'notifications_sent': bool(result['records']),
    }
    if result['records']:
        notify_research_team(result['records'], credentials_path)
    dashboard = monitor_dir / 'phase4-dashboard.jsonl'
    with dashboard.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(dashboard_record, ensure_ascii=False) + '\n')
    return dashboard_record


def run(monitor_dir: Path, year: int | None = None, *, activate_phase4: bool = False, credentials_path: Path | None = None) -> dict:
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
    manifest_path = Path(manifest['manifest_path'])
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
    if activate_phase4:
        if credentials_path is None:
            raise ValueError('credentials_path is required when Phase 4 is active')
        result['phase4'] = publish_phase4(result, monitor_dir, credentials_path)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Wrote silent monitor snapshot to {output}')
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--monitor-dir', type=Path, required=True)
    ap.add_argument('--year', type=int)
    ap.add_argument('--activate-phase4', action='store_true')
    ap.add_argument('--credentials', type=Path, default=Path(__file__).parents[2] / 'credentials.json')
    args = ap.parse_args()
    run(args.monitor_dir, args.year, activate_phase4=args.activate_phase4, credentials_path=args.credentials)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
