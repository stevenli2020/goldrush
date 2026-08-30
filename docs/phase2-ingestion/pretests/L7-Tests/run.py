import datetime
from pandas_datareader import data as web
import pandas as pd
l7_indicators = {'L7-001 (CB Balance Sheet Liquidity)': 'WALCL', 'L7-003 (Private Non-Financial Credit/GDP)': 'QUSPAM770A', 'L7-004 (Credit-Spread Financial Stress)': 'BAMLH0A0HYM2', 'L7-005 (Repo Funding Stress - SOFR)': 'SOFR'}
start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime.today()
print('=' * 60)
print('L7 INDICATORS DATA RETRIEVAL TEST')
print('=' * 60)
for indicator_name, ticker in l7_indicators.items():
    print(f'\nFetching {indicator_name} [Ticker: {ticker}]...')
    try:
        df = web.DataReader(ticker, 'fred', start_date, end_date)
        print(f'Status: SUCCESS ({len(df)} records retrieved)')
        print('Latest 3 observations:')
        print(df.tail(3))
        print('-' * 40)
    except Exception as e:
        print(f'Status: FAILED for {ticker}')
        print(f'Error: {e}')
        print('-' * 40)
print('\nTest execution complete.')
