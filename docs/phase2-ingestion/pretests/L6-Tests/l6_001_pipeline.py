import os
import re
import subprocess
from urllib.parse import urljoin
import numpy as np
import pandas as pd


def fetch_and_extract_gpr():
  page_url = 'https://www.matteoiacoviello.com/gpr.htm'
  output_dir = './data/gpr'

  # Ensure the target directory exists
  os.makedirs(output_dir, exist_ok=True)

  # Step 1: Scrape page HTML using curl
  print(f'[1/4] Scraping page HTML from: {page_url}')
  result = subprocess.run(
      ['curl', '-s', '-L', page_url],
      capture_output=True,
      text=True,
      check=True,
  )
  html_content = result.stdout

  # Step 2: Extract relative link matching .dta, daily, and gpr (case-insensitive)
  print('[2/4] Searching for matching .dta file link...')
  matches = re.findall(
      r'href=["\']?([^"\'>\s]+\.dta[^"\'>\s]*)["\']?',
      html_content,
      re.IGNORECASE,
  )

  target_relative_url = None
  for link in matches:
    link_lower = link.lower()
    if (
        '.dta' in link_lower
        and 'daily' in link_lower
        and 'gpr' in link_lower
    ):
      target_relative_url = link
      break

  if not target_relative_url:
    raise ValueError(
        'Could not find a .dta link containing "daily" and "gpr" on the page.'
    )

  # Step 3: Reconstruct full absolute URL & target file path
  full_download_url = urljoin(page_url, target_relative_url)
  filename = os.path.basename(target_relative_url.split('?')[0])
  save_path = os.path.join(output_dir, filename)

  print(f'      Found relative link  : {target_relative_url}')
  print(f'      Resolved absolute URL: {full_download_url}')

  # Step 4: Download Stata file using curl (overwriting existing file)
  print(f'[3/4] Downloading file to: {save_path}')
  subprocess.run(
      ['curl', '-s', '-L', '-o', save_path, full_download_url], check=True
  )
  print('      Download completed successfully.')

  # Step 5: Read Stata (.dta) file into Pandas
  print('[4/4] Reading Stata file...')
  df = pd.read_stata(save_path)

  return df, save_path


def engineer_l6_001_features(df):
  """Engineers quantitative features for variable L6-001 (Geopolitical Risk):

  1. 30-Day Rolling Z-Score for Headline GPRD (isolates sudden shocks).
  2. 30-Day Rolling Z-Scores for Threat and Act sub-indices.
  3. Threat-to-Act Ratio (rumor vs. realization balance).
  """
  # Ensure date column is formatted properly and set as index
  df['date'] = pd.to_datetime(df['date'])
  df = df.sort_values('date').set_index('date')

  # 1. Rolling 30-Day Stats for Headline GPRD
  rolling_30_mean = df['GPRD'].rolling(window=30, min_periods=10).mean()
  rolling_30_std = df['GPRD'].rolling(window=30, min_periods=10).std()

  # 2. 30-Day Z-Score calculation
  df['GPRD_Z30'] = (df['GPRD'] - rolling_30_mean) / rolling_30_std.replace(
      0, np.nan
  )

  # 3. Z-Scores for Sub-Indices (Threats & Acts)
  df['GPRD_THREAT_Z30'] = (
      df['GPRD_THREAT']
      - df['GPRD_THREAT'].rolling(window=30, min_periods=10).mean()
  ) / df['GPRD_THREAT'].rolling(window=30, min_periods=10).std().replace(
      0, np.nan
  )

  df['GPRD_ACT_Z30'] = (
      df['GPRD_ACT']
      - df['GPRD_ACT'].rolling(window=30, min_periods=10).mean()
  ) / df['GPRD_ACT'].rolling(window=30, min_periods=10).std().replace(
      0, np.nan
  )

  # 4. Threat-to-Act Sentiment Ratio
  df['THREAT_ACT_RATIO'] = df['GPRD_THREAT'] / df['GPRD_ACT'].replace(0, np.nan)

  return df


if __name__ == '__main__':
  try:
    # Execute pipeline
    raw_df, raw_file_path = fetch_and_extract_gpr()
    featured_df = engineer_l6_001_features(raw_df)

    # Format terminal output width for clean printing
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    print(
        '\n========================================================================='
    )
    print(
        '                L6-001: GEOPOLITICAL RISK FEATURE OUTPUT                 '
    )
    print(
        '========================================================================='
    )
    print(f'Stata File Location : {raw_file_path}')
    print(f'Total Daily Records : {len(featured_df)}')

    display_cols = [
        'GPRD',
        'GPRD_Z30',
        'GPRD_THREAT',
        'GPRD_THREAT_Z30',
        'GPRD_ACT',
        'GPRD_ACT_Z30',
        'THREAT_ACT_RATIO',
    ]

    print('\nLatest Records with Engineered Features:')
    print(
        '-------------------------------------------------------------------------'
    )
    print(featured_df[display_cols].tail(10).to_string())
    print(
        '=========================================================================\n'
    )

  except Exception as e:
    print(f'\nError occurred: {e}')