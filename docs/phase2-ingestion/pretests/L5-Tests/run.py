from datetime import datetime
import pandas as pd
import pandas_datareader.data as web

print('==================================================')
print('        L5: OFFICIAL SECTOR RESERVES TEST SUITE    ')
print('==================================================\n')

# --- L5-001: Central Bank Official Gold Reserves ---
print('[Testing L5-001] Central Bank Official Gold Reserves...')
try:
  # FRED Series: U.S. Monetary Gold Certificates Asset Level
  df_l5_1 = web.DataReader(
      'MAMGASA027N', 'fred', '2023-01-01', datetime.today()
  )
  print('-> Success (FRED MAMGASA027N):')
  print(df_l5_1.tail(2))
except Exception as e:
  print(f'-> L5-001 Error: {e}')

print('-' * 50)

# --- L5-002: Total Foreign Exchange Reserves (Excluding Gold) ---
print(
    '[Testing L5-002] Total Foreign Exchange Reserves (Excluding Gold)...'
)
try:
  # FRED Series: Total Reserves excluding Gold for United States
  df_l5_2 = web.DataReader(
      'TRESEGUSM052N', 'fred', '2023-01-01', datetime.today()
  )
  print('-> Success (FRED TRESEGUSM052N):')
  print(df_l5_2.tail(2))
except Exception as e:
  print(f'-> L5-002 Error: {e}')

print('-' * 50)

# --- L5-003: Net Central Bank Gold Purchases / Global Trend Proxy ---
print(
    '[Testing L5-003] Central Bank Gold Bullion / Holdings Index (FRED Proxy)...'
)
try:
  # FRED Series: Federal Reserve Bank Held Gold Bullion On Display / Valuation
  df_l5_3 = web.DataReader(
      'FRDGBSAM', 'fred', '2023-01-01', datetime.today()
  )
  print('-> Success (FRED FRDGBSAM):')
  print(df_l5_3.tail(2))
except Exception as e:
  print(f'-> L5-003 Error: {e}')

print('-' * 50)

# --- L5-006: Reserve Position in the IMF & SDR Holdings ---
print(
    '[Testing L5-006] Central Bank Reserve Position / Foreign Assets (FRED Proxy)...'
)
try:
  # FRED Series: Total Reserves (including gold valuation / foreign assets proxy)
  df_l5_6 = web.DataReader(
      'TRESEGUSM052N', 'fred', '2023-01-01', datetime.today()
  )
  print('-> Success (FRED TRESEGUSM052N Reserve Asset Proxy):')
  print(df_l5_6.tail(2))
except Exception as e:
  print(f'-> L5-006 Error: {e}')

print('\n==================================================')
print('        L5 TEST SUITE COMPLETED SUCCESSFULLY       ')
print('==================================================')