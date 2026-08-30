import io
import logging
import sys
import pandas as pd
import requests
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger('L9_001_Pipeline')

class L9001Pipeline:
    """Pipeline L9-001: Extract, Transform, and Load SGE Daily Benchmark Prices."""
    TARGET_URL = 'https://en.sge.com.cn/data_BenchmarkPrice_Daily'
    EXPECTED_COLUMNS = ['Trade Date', 'Contract', 'Benchmark Price AM', 'Benchmark Price PM']

    def __init__(self, timeout: int=15):
        self.timeout = timeout
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

    def extract(self) -> str:
        """Extract raw payload from target URL."""
        logger.info(f'[Extract] Requesting URL: {self.TARGET_URL}')
        response = requests.get(self.TARGET_URL, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def transform(self, raw_html: str) -> pd.DataFrame:
        """Transform raw HTML snippet into a cleaned Pandas DataFrame using Method 1."""
        logger.info('[Transform] Parsing and cleaning raw HTML payload...')
        html_content = raw_html
        if '<table>' not in html_content.lower():
            html_content = f'<table>{html_content}</table>'
        dfs = pd.read_html(io.StringIO(html_content))
        if not dfs:
            raise ValueError('No tabular data could be extracted from payload.')
        df = dfs[0]
        df['Trade Date'] = pd.to_datetime(df['Trade Date'], format='%Y%m%d')
        df['Benchmark Price AM'] = pd.to_numeric(df['Benchmark Price AM'], errors='coerce')
        df['Benchmark Price PM'] = pd.to_numeric(df['Benchmark Price PM'], errors='coerce')
        return df

    def load(self, df: pd.DataFrame, output_path: str=None) -> pd.DataFrame:
        """Load/Export the transformed data."""
        logger.info(f'[Load] Processed {len(df)} rows successfully.')
        if output_path:
            df.to_csv(output_path, index=False)
            logger.info(f'[Load] Exported data to {output_path}')
        return df

    def run(self, output_path: str=None) -> pd.DataFrame:
        """Execute complete ETL workflow."""
        raw_html = self.extract()
        df = self.transform(raw_html)
        return self.load(df, output_path=output_path)

def test_l9_001_pipeline():
    """Integration test runner for L9-001 pipeline validation."""
    logger.info('=== Starting L9-001 Pipeline Test Run ===')
    pipeline = L9001Pipeline()
    df = pipeline.run()
    assert df is not None, 'Assertion Error: DataFrame returned as None'
    assert not df.empty, 'Assertion Error: DataFrame is empty'
    for col in L9001Pipeline.EXPECTED_COLUMNS:
        assert col in df.columns, f"Assertion Error: Missing expected column '{col}'"
    logger.info('✅ ALL L9-001 TEST ASSERTIONS PASSED')
    print('\n--- Processed Dataset Sample ---')
    print(df.head())
    print('\n--- Schema Information ---')
    print(df.dtypes)
if __name__ == '__main__':
    test_l9_001_pipeline()
