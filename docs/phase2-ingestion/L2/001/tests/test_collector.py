import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).parents[1]))
import collector

class FakeResult:

    def to_df(self):
        import pandas as pd
        return pd.DataFrame({'open': [100.0], 'high': [101.0], 'low': [99.0], 'close': [100.5], 'volume': [0]}, index=pd.Index(['2026-08-24'], name='date'))

class CollectorTests(unittest.TestCase):
    pass
if __name__ == '__main__':
    unittest.main()
