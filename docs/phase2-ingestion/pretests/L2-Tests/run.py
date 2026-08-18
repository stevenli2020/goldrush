from datetime import datetime
from openbb import obb
import pandas as pd
import pandas_datareader.data as web

print('=== Starting Hybrid L2 Data Retrieval Test ===')

# -------------------------------------------------------------
# 1. L2-001: DXY US Dollar Index (Source: OpenBB / Yahoo Finance)
# -------------------------------------------------------------
try:
  print('\n[Fetching L2-001: DXY US Dollar Index...]')
  dxy_result = obb.equity.price.historical(
      symbol='DX-Y.NYB', start_date='2026-01-01', provider='yfinance'
  )
  dxy_df = dxy_result.to_df()
  print(dxy_df[['open', 'high', 'low', 'close']].tail(3))
except Exception as e:
  print(f'Error fetching L2-001: {e}')

# -------------------------------------------------------------
# 2. L2-002: Broad Trade-Weighted Nominal USD (Source: pandas_datareader / FRED)
# -------------------------------------------------------------
try:
  print(
      '\n[Fetching L2-002: Broad Trade-Weighted USD (DTWEXBGS) via FRED...]'
  )
  tw_df = web.DataReader('DTWEXBGS', 'fred', '2026-01-01', datetime.today())
  print(tw_df.tail(3))
except Exception as e:
  print(f'Error fetching L2-002: {e}')

# -------------------------------------------------------------
# 3. L2-003: USD/CNY Exchange Rate (Source: OpenBB / Yahoo Finance)
# -------------------------------------------------------------
try:
  print('\n[Fetching L2-003: USD/CNY Exchange Rate (CNY=X)...]')
  cny_result = obb.equity.price.historical(
      symbol='CNY=X', start_date='2026-01-01', provider='yfinance'
  )
  cny_df = cny_result.to_df()
  print(cny_df[['open', 'high', 'low', 'close']].tail(3))
except Exception as e:
  print(f'Error fetching L2-003: {e}')

print('\n=== Hybrid Test Complete ===')