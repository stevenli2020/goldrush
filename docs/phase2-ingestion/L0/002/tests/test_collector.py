import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Ensure module path resolves correctly for pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import collector

class TestGoldCollector(unittest.TestCase):

    def test_conversion_math(self):
        # Verify Troy Ounces to Metric Tonnes conversion factor
        raw_ounces = 261498000.0  # Example US fine troy ounces
        expected_tonnes = raw_ounces * collector.MULTIPLIER
        self.assertAlmostEqual(expected_tonnes, 8133.497, places=2)

    def test_panel_entities_structure(self):
        # Verify the fixed panel keys and Euro Area code
        expected_entities = {"US", "EA", "CN", "JP", "CH", "IMF"}
        self.assertEqual(set(collector.PANEL_ENTITIES.keys()), expected_entities)
        self.assertEqual(collector.PANEL_ENTITIES["EA"], "EZB")

    @patch("collector.obb.economy.indicators")
    @patch("collector.os.path.isfile", return_value=True)
    @patch("builtins.open", new_callable=unittest.mock.mock_open())
    def test_run_collection_mock(self, mock_file, mock_isfile, mock_obb_indicators):
        # Mock DataFrame returned by OpenBB IMF provider
        mock_df = pd.DataFrame({
            "date": ["2026-06-30", "2026-01-31"],
            "value": [261498000.0, 16345000.0]
        })
        mock_response = MagicMock()
        mock_response.to_dataframe.return_value = mock_df
        mock_obb_indicators.return_value = mock_response

        # Run collection in mock mode / patched state
        try:
            collector.run_collection(mock_mode=True)
        except Exception as e:
            self.fail(f"run_collection raised an exception in offline test mode: {e}")


if __name__ == "__main__":
    unittest.main()