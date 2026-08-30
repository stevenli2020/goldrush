import json, sys, importlib.util, subprocess, re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import pytest
spec = importlib.util.spec_from_file_location('l6_001_parser', Path(__file__).parents[1] / 'parser.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)
cspec = importlib.util.spec_from_file_location('l6_001_collector', Path(__file__).parents[1] / 'collector.py')
collector = importlib.util.module_from_spec(cspec)
cspec.loader.exec_module(collector)

def fixture(tmp_path):
    raw = tmp_path / 'gpr.dta'
    pd.DataFrame({'date': ['2026-08-20', '2026-08-21'], 'GPRD': [1.0, 2.0], 'GPRD_THREAT': [0.5, 1.0], 'GPRD_ACT': [0.2, 0.4]}).to_stata(raw, write_index=False)
    mp = tmp_path / 'm.json'
    m = {'source_url': 'https://example/data_gpr_daily_recent_20260821.dta', 'retrieved_at': '2026-08-24T00:00:00+00:00', 'source_vintage_date': '2026-08-21', 'raw_path': str(raw), 'size_bytes': raw.stat().st_size, 'collector_version': 'test'}
    mp.write_text(json.dumps(m))
    return (raw, mp)

def test_parse_and_order(tmp_path):
    raw, mp = fixture(tmp_path)
    rows = parser.parse(raw, mp, as_of='2026-08-24')
    assert [r['observation_date'] for r in rows] == ['2026-08-20', '2026-08-21']
    assert rows[-1]['gpr_act_index'] == 0.4

def test_bad_negative_and_duplicate(tmp_path):
    raw, mp = fixture(tmp_path)
    df = pd.DataFrame({'date': ['2026-08-20'], 'GPRD': [-1.0], 'GPRD_THREAT': [1.0], 'GPRD_ACT': [1.0]})
    df.to_stata(raw, write_index=False)
    m = json.loads(mp.read_text())
    m.update(size_bytes=raw.stat().st_size, metadata=None)
    mp.write_text(json.dumps(m))
    with pytest.raises(ValueError):
        parser.parse(raw, mp)

def test_fallback_and_blocked_cli(tmp_path):
    out = tmp_path / 'out.csv'
    status = parser.blocked(out, 'no prior')
    assert json.loads(status.read_text())['status'] == 'BLOCKED'
    raw, mp = fixture(tmp_path)
    rows = parser.parse(raw, mp)
    parser.write(rows, out)
    assert parser.carry_forward(out)[0]['availability_status'] == 'STALE'

def test_missing_markers_are_skipped(tmp_path):
    raw = tmp_path / 'gpr.dta'
    pd.DataFrame({'date': ['2026-08-20', '2026-08-21'], 'GPRD': [1.0, None], 'GPRD_THREAT': [0.5, 1.0], 'GPRD_ACT': [0.2, 0.4]}).to_stata(raw, write_index=False)
    mp = tmp_path / 'm.json'
    m = {'source_url': 'https://example/x', 'retrieved_at': '2026-08-24T00:00:00+00:00', 'source_vintage_date': '2026-08-21', 'raw_path': str(raw), 'size_bytes': raw.stat().st_size, 'collector_version': 'test'}
    mp.write_text(json.dumps(m))
    assert len(parser.parse(raw, mp)) == 1

def test_missing_columns_and_nonfinite_values_rejected(tmp_path):
    raw = tmp_path / 'gpr.dta'
    pd.DataFrame({'date': ['2026-08-20'], 'GPRD': ['not-a-number'], 'GPRD_ACT': ['1'], 'GPRD_THREAT': ['1']}).to_stata(raw, write_index=False)
    mp = tmp_path / 'm.json'
    m = {'source_url': 'https://example/x', 'retrieved_at': '2026-08-24T00:00:00+00:00', 'source_vintage_date': '2026-08-21', 'raw_path': str(raw), 'size_bytes': raw.stat().st_size, 'collector_version': 'test'}
    mp.write_text(json.dumps(m))
    with pytest.raises(ValueError):
        parser.parse(raw, mp)
    raw2 = tmp_path / 'missing.dta'
    pd.DataFrame({'date': ['2026-08-20'], 'GPRD': [1.0], 'GPRD_THREAT': [1.0]}).to_stata(raw2, write_index=False)
    m['raw_path'] = str(raw2)
    m['size_bytes'] = raw2.stat().st_size
    mp.write_text(json.dumps(m))
    with pytest.raises(ValueError):
        parser.parse(raw2, mp)

def test_conflicting_duplicate_dates_and_prior_replay(tmp_path):
    raw = tmp_path / 'dup.dta'
    pd.DataFrame({'date': ['2026-08-20', '2026-08-20'], 'GPRD': [1.0, 2.0], 'GPRD_THREAT': [1.0, 1.0], 'GPRD_ACT': [1.0, 1.0]}).to_stata(raw, write_index=False)
    mp = tmp_path / 'm.json'
    m = {'source_url': 'https://example/x', 'retrieved_at': '2026-08-24T00:00:00+00:00', 'source_vintage_date': '2026-08-21', 'raw_path': str(raw), 'size_bytes': raw.stat().st_size, 'collector_version': 'test'}
    mp.write_text(json.dumps(m))
    with pytest.raises(ValueError):
        parser.parse(raw, mp)
    out = tmp_path / 'prior.csv'
    parser.write(parser.parse(*fixture(tmp_path)), out)
    assert parser.carry_forward(out)[0]['availability_status'] == 'STALE'

def test_immutable_manifest_replay(tmp_path):

    class Resp:
        status_code = 200
        content = b''
        headers = {'Last-Modified': 'Sun, 23 Aug 2026 21:40:30 GMT'}
        text = '<a href="data_gpr_daily_recent_20260823.dta">x</a>'

        def __init__(self, content=None):
            self.content = content or Resp.content
    raw_bytes = tmp_path / 'fixture.dta'
    pd.DataFrame({'date': ['2026-08-20'], 'GPRD': [1.0], 'GPRD_THREAT': [1.0], 'GPRD_ACT': [1.0]}).to_stata(raw_bytes, write_index=False)
    data = raw_bytes.read_bytes()

    class Session:

        def get(self, url, **kwargs):
            return Resp(data if url.endswith('.dta') else None)
    first = collector.collect(tmp_path / 'raw', tmp_path / 'manifests', session=Session())
    second = collector.collect(tmp_path / 'raw', tmp_path / 'manifests', session=Session())
    assert first['manifest_path'] != second['manifest_path']
    assert len(list((tmp_path / 'raw').glob('*.dta'))) == 1
