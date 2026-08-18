from datetime import datetime
import pandas as pd
import yfinance as yf

# Primary physical gold ETFs representing global institutional flows (L8-001)
etf_tickers = ['GLD', 'IAU']

print('Fetching Gold ETF market data for L8-001 (GLD & IAU)...')

# Download historical data for the last month
data = yf.download(etf_tickers, period='1mo', progress=False)

# Extract Close prices and Volumes
close_prices = data['Close']
volumes = data['Volume']

# Compute daily dollar volume (a primary proxy for institutional liquidity & capital rotation)
dollar_volume = close_prices * volumes

# Combine into a clean summary DataFrame
summary_df = pd.DataFrame()
for ticker in etf_tickers:
  summary_df[f'{ticker} Close ($)'] = close_prices[ticker]
  summary_df[f'{ticker} Volume'] = volumes[ticker]
  summary_df[f'{ticker} Dollar Vol ($M)'] = (
      dollar_volume[ticker] / 1e6
  ).round(2)

print('\n=== L8-001: Gold ETF Activity Proxy (GLD & IAU) ===')
print(summary_df.tail().to_string())