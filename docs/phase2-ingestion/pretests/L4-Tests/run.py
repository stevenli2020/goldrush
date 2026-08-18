from datetime import datetime
import pandas as pd
import pandas_datareader.data as web

# Define the L4 mapping to official FRED Series IDs
l4_metrics = {
    'L4-001': {
        'name': 'CPI Inflation (Headline)',
        'id': 'CPIAUCSL',
    },
    'L4-002': {
        'name': 'Core PCE Price Index',
        'id': 'PCEPILFE',
    },
    'L4-003': {
        'name': '5-Year Breakeven Inflation Rate',
        'id': 'T5YIE',
    },
    'L4-004': {
        'name': '10-Year Breakeven Inflation Rate',
        'id': 'T10YIE',
    },
    'L4-006': {
        'name': 'Federal Surplus/Deficit as % of GDP',
        'id': 'FYFSGDA188S',
    },
    'L4-007': {
        'name': 'Federal Debt Total Public Debt as % of GDP',
        'id': 'GFDEGDQ188S',
    },
    'L4-008': {
        'name': 'Federal Interest Outlays as % of GDP (Proxy)',
        'id': 'FYOIGDA188S',
    },
}


def test_l4_data_retrieval():
  print('=' * 65)
  print('Initializing L4 Data Retrieval Test (via FRED / pandas_datareader)...')
  print('=' * 65)

  results = {}
  start_date = '2020-01-01'

  for code, info in l4_metrics.items():
    print(f"\n[Testing] {code}: {info['name']} (FRED ID: {info['id']})")
    try:
      # Fetch series data using pandas_datareader
      df = web.DataReader(info['id'], 'fred', start_date, datetime.today())

      if not df.empty:
        # Drop NaN values that are common in quarterly/annual fiscal series
        df_clean = df.dropna()
        latest_date = df_clean.index[-1].strftime('%Y-%m-%d')
        latest_value = df_clean.iloc[-1].values[0]

        results[code] = {
            'status': 'SUCCESS',
            'rows': len(df_clean),
            'latest_date': latest_date,
            'latest_value': round(float(latest_value), 3),
        }
        print('  Status       : SUCCESS ✅')
        print(f"  Records Found: {results[code]['rows']}")
        print(f"  Latest Date  : {latest_date}")
        print(f"  Latest Value : {results[code]['latest_value']}")
      else:
        results[code] = {'status': 'EMPTY', 'rows': 0}
        print('  Status       : WARNING ⚠️ (Empty dataset returned)')

    except Exception as e:
      results[code] = {'status': 'FAILED', 'error': str(e)}
      print('  Status       : FAILED ❌')
      print(f'  Error Details: {e}')

  # Print Summary Report Table
  print('\n' + '=' * 65)
  print('TEST EXECUTION SUMMARY REPORT')
  print('=' * 65)

  summary_data = []
  for k in l4_metrics.keys():
    res = results.get(k, {})
    summary_data.append({
        'L4 Code': k,
        'Metric Name': l4_metrics[k]['name'],
        'FRED ID': l4_metrics[k]['id'],
        'Status': res.get('status', 'N/A'),
        'Rows': res.get('rows', 0),
        'Latest Value': res.get('latest_value', 'N/A'),
        'Latest Date': res.get('latest_date', 'N/A'),
    })

  summary_df = pd.DataFrame(summary_data)
  print(summary_df.to_string(index=False))
  print('=' * 65)


if __name__ == '__main__':
  test_l4_data_retrieval()