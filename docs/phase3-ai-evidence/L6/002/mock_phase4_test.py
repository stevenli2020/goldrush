"""Run an isolated Bank Markazi Phase 4 notification test."""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

import requests


HERE = Path(__file__).parent
SOURCE_URL = 'https://ofac.treasury.gov/recent-actions/20260714'
NAME = 'BANK MARKAZI JOMHOURI ISLAMI IRAN'


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    scorer = load('scorer')
    monitor = load('silent_monitor')
    text = requests.get(SOURCE_URL, timeout=60).text
    record = {
        'variable_id': 'L6-002',
        'target_name': NAME,
        'action_type': 'UPDATE',
        'retrieval_status': 'FOUND',
        'source_url': SOURCE_URL,
        'primary_document_text': text,
    }
    record.update(scorer.score_record(record))
    if record['score'] != 30 or record['score_breakdown'] != {
        'legal_action': 0,
        'sovereign_relevance': 30,
        'asset_scope': 0,
        'legal_authority': 0,
    }:
        raise AssertionError(f'unexpected Bank Markazi result: {record}')
    result = {
        'variable_id': 'L6-002',
        'run_status': 'MOCK_TEST_COMPLETE',
        'notifications_sent': False,
        'run_at': datetime.now(timezone.utc).isoformat(),
        'candidate_count': 1,
        'records': [record],
    }
    dashboard = monitor.publish_phase4(
        result,
        HERE / 'live-monitor',
        HERE.parents[1] / 'credentials.json',
        human_review_required=True,
        subject_prefix='[TEST] ',
        event_type='MOCK_TEST',
    )
    if not dashboard['human_review_required'] or not dashboard['notifications_sent']:
        raise AssertionError(f'mock notification/dashboard failed: {dashboard}')
    print(json.dumps({'status': 'MOCK_PHASE4_PASS', 'score': record['score'], 'score_breakdown': record['score_breakdown'], 'dashboard': dashboard}, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
