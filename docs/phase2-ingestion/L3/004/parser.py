"""Build L3-004 cumulative policy-outcome probabilities from preserved inputs."""
from __future__ import annotations
import argparse
import calendar
import csv
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path
VARIABLE_ID = 'L3-004'
PARSER_VERSION = '0.1.0'
METHOD = 'cumulative_cme_fedwatch_probability_tree_v1'
SOURCE_NAME = 'Calculated CME-method policy outcome probability'
FIELDS = ['variable_id', 'observation_date', 'meeting_date', 'contract', 'target_rate_lower_pct', 'target_rate_upper_pct', 'probability', 'probability_sum_original', 'calculation_method', 'source_name', 'source_settlement_identifiers', 'effr_observation_date', 'effr_pct', 'current_target_lower_pct', 'current_target_upper_pct', 'retrieved_at', 'source_manifest_path', 'cme_raw_path', 'effr_raw_path', 'target_lower_raw_path', 'target_upper_raw_path', 'schedule_path', 'package_version', 'parser_version', 'is_revision', 'prior_probability', 'validation_status', 'availability_status']
MONTH_NAMES = {1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP', 10: 'OCT', 11: 'NOV', 12: 'DEC'}
MONTH_CODES = {1: 'F', 2: 'G', 3: 'H', 4: 'J', 5: 'K', 6: 'M', 7: 'N', 8: 'Q', 9: 'U', 10: 'V', 11: 'X', 12: 'Z'}

class ScheduleExpiredError(ValueError):
    pass

def metadata_file(path: Path) -> str:
    return None

def month_label(value: date) -> str:
    return f'{MONTH_NAMES[value.month]} {value.year % 100:02d}'

def contract_code(value: date) -> str:
    return f'ZQ{MONTH_CODES[value.month]}{value.year % 10}'

def next_month(value: date) -> date:
    return date(value.year + (value.month == 12), 1 if value.month == 12 else value.month + 1, 1)

def latest_fred_value(payload: dict, observation_date: date) -> tuple[date, float]:
    values = []
    for item in payload.get('observations', []):
        try:
            obs = date.fromisoformat(item['date'])
            value = float(item['value'])
        except (KeyError, TypeError, ValueError):
            continue
        if obs <= observation_date and math.isfinite(value):
            values.append((obs, value))
    if not values:
        raise ValueError('FRED input has no numeric observation on or before the CME settlement date')
    return max(values)

def load_and_verify(manifest_path: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('variable_id') != VARIABLE_ID:
        raise ValueError('wrong manifest variable_id')
    cme = manifest['cme']
    cme_path = Path(cme['raw_path'])
    schedule = manifest['schedule']
    schedule_path = Path(schedule['raw_path'])
    for series_id in ('EFFR', 'DFEDTARL', 'DFEDTARU'):
        record = manifest['fred'][series_id]
        if record.get('series_id') != series_id:
            raise ValueError(f'wrong FRED series ID for {series_id}')
    return manifest

def source_inputs(manifest_path: Path) -> dict:
    manifest = load_and_verify(manifest_path)
    observation_date = date.fromisoformat(manifest['observation_date'])
    cme = json.loads(Path(manifest['cme']['raw_path']).read_text(encoding='utf-8'))
    actual = datetime.strptime(cme['tradeDate'], '%m/%d/%Y').date()
    if actual != observation_date or manifest['cme'].get('trade_date') != observation_date.isoformat():
        raise ValueError('CME settlement date does not match manifest observation_date')
    settlements = {}
    for item in cme.get('settlements', []):
        if item.get('month') == 'Total':
            continue
        try:
            value = float(item['settle'])
        except (KeyError, TypeError, ValueError):
            continue
        if item['month'] in settlements and settlements[item['month']] != value:
            raise ValueError(f"conflicting CME settlement {item['month']}")
        settlements[item['month']] = value
    fred_values = {}
    for series_id in ('EFFR', 'DFEDTARL', 'DFEDTARU'):
        payload = json.loads(Path(manifest['fred'][series_id]['raw_path']).read_text(encoding='utf-8'))
        fred_values[series_id] = latest_fred_value(payload, observation_date)
    effr_date, effr = fred_values['EFFR']
    _, target_lower = fred_values['DFEDTARL']
    _, target_upper = fred_values['DFEDTARU']
    if not math.isclose(target_upper - target_lower, 0.25, abs_tol=1e-09):
        raise ValueError('current FOMC target range is not 25 basis points')
    schedule = json.loads(Path(manifest['schedule']['raw_path']).read_text(encoding='utf-8'))
    state = schedule.get('schedule_status', {}).get('state')
    if state == 'expired':
        raise ScheduleExpiredError('preserved FOMC schedule is expired')
    if state not in {'ok', 'expiring'}:
        raise ValueError('invalid schedule_status')
    meetings = sorted((date.fromisoformat(item) for item in schedule.get('meetings', []) if date.fromisoformat(item) > observation_date))
    if len(meetings) < 3:
        raise ScheduleExpiredError('preserved FOMC schedule has fewer than three future meetings')
    return {'manifest': manifest, 'observation_date': observation_date, 'settlements': settlements, 'effr_date': effr_date, 'effr': effr, 'target_lower': target_lower, 'target_upper': target_upper, 'schedule': schedule, 'meetings': meetings[:3], 'schedule_state': state}

def adjacent_transition(expected_moves: float) -> dict[int, float]:
    if not math.isfinite(expected_moves):
        raise ValueError('non-finite expected policy move')
    floor_moves = math.floor(expected_moves)
    fraction = expected_moves - floor_moves
    result = {floor_moves: 1.0 - fraction}
    if fraction > 0:
        result[floor_moves + 1] = fraction
    return result

def convolve(left: dict[int, float], right: dict[int, float]) -> dict[int, float]:
    result: dict[int, float] = {}
    for left_moves, left_probability in left.items():
        for right_moves, right_probability in right.items():
            total = left_moves + right_moves
            result[total] = result.get(total, 0.0) + left_probability * right_probability
    return result

def calculate_tree(inputs: dict) -> list[dict]:
    settlements = inputs['settlements']
    meetings = inputs['meetings']
    pre_rate = inputs['effr']
    cumulative = {0: 1.0}
    results = []
    for index, meeting in enumerate(meetings):
        meeting_key = month_label(meeting)
        if meeting_key not in settlements:
            raise ValueError(f'missing CME settlement for {meeting_key}')
        implied_month_rate = 100.0 - settlements[meeting_key]
        days_in_month = calendar.monthrange(meeting.year, meeting.month)[1]
        days_pre = meeting.day
        days_post = days_in_month - meeting.day
        source_ids = [meeting_key]
        anchor_month = next_month(meeting)
        month_has_meeting = any((item.year == anchor_month.year and item.month == anchor_month.month for item in meetings))
        if days_post <= 3 and (not month_has_meeting):
            anchor_key = month_label(anchor_month)
            if anchor_key not in settlements:
                raise ValueError(f'missing non-meeting anchor settlement for {anchor_key}')
            post_rate = 100.0 - settlements[anchor_key]
            source_ids.append(anchor_key)
        else:
            if days_post <= 0:
                raise ValueError(f'meeting has no post-decision calendar days: {meeting}')
            post_rate = (implied_month_rate * days_in_month - pre_rate * days_pre) / days_post
        transition = adjacent_transition((post_rate - pre_rate) / 0.25)
        cumulative = convolve(cumulative, transition)
        results.append({'meeting_date': meeting, 'contract': contract_code(meeting), 'distribution': cumulative, 'conditional_transition': transition, 'source_settlement_identifiers': source_ids, 'expected_post_rate': post_rate})
        pre_rate = post_rate
    return results

def prior_values(path: Path | None) -> dict[tuple[str, str, float, float], float]:
    if path is None or not path.exists():
        return {}
    with path.open(newline='', encoding='utf-8') as handle:
        return {(row['observation_date'], row['meeting_date'], float(row['target_rate_lower_pct']), float(row['target_rate_upper_pct'])): float(row['probability']) for row in csv.DictReader(handle) if row.get('validation_status') in {'PASS', 'FLAG'}}

def parse_manifest(manifest_path: Path, prior_path: Path | None=None, production_meetings: int=2, stale_after_days: int=3) -> list[dict]:
    inputs = source_inputs(manifest_path)
    tree = calculate_tree(inputs)
    previous = prior_values(prior_path)
    manifest = inputs['manifest']
    retrieved = datetime.fromisoformat(manifest['retrieved_at'].replace('Z', '+00:00'))
    age = (retrieved.date() - inputs['observation_date']).days
    if age < 0:
        raise ValueError('retrieval timestamp predates observation_date')
    validation = 'FLAG' if inputs['schedule_state'] == 'expiring' else 'PASS'
    availability = 'STALE' if age > stale_after_days else 'AVAILABLE'
    manifest_metadata = None
    rows = []
    for meeting in tree[:production_meetings]:
        total = sum(meeting['distribution'].values())
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"probability sum outside tolerance for {meeting['meeting_date']}: {total}")
        for moves, probability in sorted(meeting['distribution'].items()):
            if not math.isfinite(probability) or not 0 <= probability <= 1:
                raise ValueError('probability outside 0..1')
            lower = inputs['target_lower'] + moves * 0.25
            upper = inputs['target_upper'] + moves * 0.25
            key = (inputs['observation_date'].isoformat(), meeting['meeting_date'].isoformat(), lower, upper)
            prior = previous.get(key)
            fred = manifest['fred']
            rows.append({'variable_id': VARIABLE_ID, 'observation_date': inputs['observation_date'].isoformat(), 'meeting_date': meeting['meeting_date'].isoformat(), 'contract': meeting['contract'], 'target_rate_lower_pct': lower, 'target_rate_upper_pct': upper, 'probability': probability, 'probability_sum_original': total, 'calculation_method': METHOD, 'source_name': SOURCE_NAME, 'source_settlement_identifiers': '|'.join(meeting['source_settlement_identifiers']), 'effr_observation_date': inputs['effr_date'].isoformat(), 'effr_pct': inputs['effr'], 'current_target_lower_pct': inputs['target_lower'], 'current_target_upper_pct': inputs['target_upper'], 'retrieved_at': manifest['retrieved_at'], 'source_manifest_path': str(manifest_path), 'cme_raw_path': manifest['cme']['raw_path'], 'effr_raw_path': fred['EFFR']['raw_path'], 'target_lower_raw_path': fred['DFEDTARL']['raw_path'], 'target_upper_raw_path': fred['DFEDTARU']['raw_path'], 'schedule_path': manifest['schedule']['raw_path'], 'package_version': manifest['package_version'], 'parser_version': PARSER_VERSION, 'is_revision': prior is not None and (not math.isclose(prior, probability, abs_tol=1e-12)), 'prior_probability': prior if prior is not None and (not math.isclose(prior, probability, abs_tol=1e-12)) else None, 'validation_status': validation, 'availability_status': availability})
    return rows

def carry_forward(prior_path: Path) -> list[dict]:
    if not prior_path.exists():
        raise FileNotFoundError('no prior L3-004 distribution is available')
    with prior_path.open(newline='', encoding='utf-8') as handle:
        rows = [row for row in csv.DictReader(handle) if row.get('validation_status') in {'PASS', 'FLAG'}]
    if not rows:
        raise ValueError('prior L3-004 output contains no valid distribution')
    latest = max((row['observation_date'] for row in rows))
    result = [row for row in rows if row['observation_date'] == latest]
    for row in result:
        row['availability_status'] = 'STALE'
    return result

def write_csv(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix('.status.json').unlink(missing_ok=True)
    with output.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

def write_blocked(output: Path, reason: str) -> Path:
    path = output.with_suffix('.status.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'variable_id': VARIABLE_ID, 'status': 'BLOCKED', 'availability_status': 'BLOCKED', 'reason': reason, 'checked_at': datetime.now(timezone.utc).isoformat(), 'parser_version': PARSER_VERSION}, indent=2) + '\n', encoding='utf-8')
    return path

def main(argv: list[str] | None=None) -> int:
    cli = argparse.ArgumentParser(description='Build L3-004 cumulative policy probabilities')
    cli.add_argument('--manifest', type=Path)
    cli.add_argument('--prior', type=Path)
    cli.add_argument('--output', type=Path, default=Path('docs/phase2-ingestion/L3/004/data/processed/L3_004_probabilities.csv'))
    args = cli.parse_args(argv)
    try:
        if args.manifest:
            rows = parse_manifest(args.manifest, args.prior)
        elif args.prior:
            rows = carry_forward(args.prior)
        else:
            raise ValueError('provide --manifest or --prior')
    except ScheduleExpiredError as exc:
        path = write_blocked(args.output, str(exc))
        print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        if args.prior:
            try:
                rows = carry_forward(args.prior)
            except (OSError, ValueError) as fallback_exc:
                path = write_blocked(args.output, str(fallback_exc))
                print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
                return 0
        else:
            path = write_blocked(args.output, str(exc))
            print(json.dumps({'status': 'BLOCKED', 'status_path': str(path)}))
            return 0
    write_csv(rows, args.output)
    print(json.dumps({'rows': len(rows), 'observation_date': rows[-1]['observation_date']}))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
