from datetime import datetime
import os
import pandas as pd
import requests
l1_mapping = {'L1-001': 'DFII10', 'L1-002': 'DFII5', 'L1-003': 'DFII10', 'L1-005': 'THREEFYTP10', 'L1-006': 'EFFR', 'L1-007': 'T5YIFR'}
START_DATE = '2023-01-01'
api_key = os.getenv('FRED_API_KEY')
if not api_key:
    raise ValueError('FRED_API_KEY environment variable is missing. Please export it first using: export FRED_API_KEY="your_key"')

def fetch_fred_series(series_id, api_key, start_date):
    """Fetches a single time series from the official FRED API, cleaning missing values."""
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {'series_id': series_id, 'api_key': api_key, 'file_type': 'json', 'observation_start': start_date}
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            observations = data.get('observations', [])
            if not observations:
                print(f'Warning: No observations returned for {series_id}.')
                return None
            df = pd.DataFrame(observations)[['date', 'value']]
            df = df[df['value'] != '.']
            df['value'] = pd.to_numeric(df['value'])
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
            return df['value']
        else:
            print(f'Error fetching {series_id}: HTTP Status {response.status_code} - {response.text}')
            return None
    except requests.exceptions.Timeout:
        print(f'Timeout error while fetching {series_id}.')
        return None
    except Exception as e:
        print(f'Exception fetching {series_id}: {e}')
        return None

def main():
    print('=== Fetching L1 Macro Variables Directly from FRED API ===')
    collected_data = {}
    for l1_id, fred_symbol in l1_mapping.items():
        print(f'Fetching {l1_id} ({fred_symbol})...')
        series_data = fetch_fred_series(fred_symbol, api_key, START_DATE)
        if series_data is not None and (not series_data.empty):
            collected_data[l1_id] = series_data
    if collected_data:
        combined_df = pd.DataFrame(collected_data)
        combined_df = combined_df.sort_index().dropna(how='all')
        print('\n--- Successfully Retrieved Combined L1 Data (Tail) ---')
        print(combined_df.tail(10))
        print('\n--- Data Summary Statistics ---')
        print(combined_df.describe())
    else:
        print('No data retrieved from FRED.')
if __name__ == '__main__':
    main()
