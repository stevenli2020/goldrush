from datetime import datetime
import pandas as pd
import yfinance as yf
etf_tickers = ['GLD', 'IAU']
print('Fetching Gold ETF market data for L8-001 (GLD & IAU)...')
data = yf.download(etf_tickers, period='1mo', progress=False)
close_prices = data['Close']
volumes = data['Volume']
dollar_volume = close_prices * volumes
summary_df = pd.DataFrame()
for ticker in etf_tickers:
    summary_df[f'{ticker} Close ($)'] = close_prices[ticker]
    summary_df[f'{ticker} Volume'] = volumes[ticker]
    summary_df[f'{ticker} Dollar Vol ($M)'] = (dollar_volume[ticker] / 1000000.0).round(2)
print('\n=== L8-001: Gold ETF Activity Proxy (GLD & IAU) ===')
print(summary_df.tail().to_string())
