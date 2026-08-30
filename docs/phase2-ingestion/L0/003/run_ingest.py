import json
import os
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
from parse_etf_holding import GoldETFHoldingsParser
SOURCE_FILE = Path('data/gold_etf_holdings/ETF_Flows_2026-08-04_1202.xlsx')
OUTPUT_CSV = Path('processed/L0_003_observations.csv')
LOG_FILE = Path('archive/ingest.log')
PUB_DATE = '2026-08-04'
DL_DATE = '2026-08-04'
OPERATOR = os.getenv('USER', 's101')
PARSER_VERSION = '1.0.0'

def calculate_metadata(filepath: Path) -> str:
    return None

def main():
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(f'Missing source file: {SOURCE_FILE}')
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_metadata = None
    run_timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    parser = GoldETFHoldingsParser(parser_version=PARSER_VERSION, log_path=str(LOG_FILE))
    records = parser.parse_file(file_path=SOURCE_FILE, publication_date=PUB_DATE, download_date=DL_DATE)
    pass_count = sum((1 for r in records if r.get('validation_status') == 'PASS'))
    flag_count = sum((1 for r in records if r.get('validation_status') == 'FLAG'))
    fail_count = len(parser.validation_errors)
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    audit_entry = {'run_timestamp': run_timestamp, 'operator': OPERATOR, 'parser_version': PARSER_VERSION, 'source_filename': SOURCE_FILE.name, 'total_parsed_records': len(records), 'validation_counts': {'PASS': pass_count, 'FLAG': flag_count, 'FAIL': fail_count}, 'rejected_rows_count': fail_count, 'warnings': parser.validation_errors, 'output_path': str(OUTPUT_CSV)}
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(audit_entry) + '\n')
    print('\n================ LIVE PASS RUN EVIDENCE ================')
    print(f'Timestamp:        {run_timestamp}')
    print(f'Operator:         {OPERATOR}')
    print(f'Source File:      {SOURCE_FILE.name}')
    print(f'source metadata:          ')
    print(f'Output File:      {OUTPUT_CSV}')
    print(f'Records Extracted:{len(records)}')
    print(f'Validation summary: PASS={pass_count} | FLAG={flag_count} | FAIL={fail_count}')
    print('=======================================================\n')
if __name__ == '__main__':
    main()
