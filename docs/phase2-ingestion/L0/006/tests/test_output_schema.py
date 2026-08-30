import json
import sys
from pathlib import Path
import pytest
import jsonschema
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / 'scripts'
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
from parse_gold_recycling import GoldRecyclingCollector

@pytest.fixture
def schema_data():
    """Loads schema.json from the variable folder root."""
    schema_path = BASE_DIR / 'schema.json'
    assert schema_path.exists(), 'schema.json not found in variable root directory'
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@pytest.fixture
def mock_config(tmp_path):
    """Generates a temporary configuration file for collector validation testing."""
    cfg_path = tmp_path / 'config.yaml'
    cfg_content = f'''\nvariable_id: "L0-006"\nunit: "tonnes"\nfrequency: "quarterly"\nsource:\n  target_sheets: ["Supply"]\n  search_keywords: ["recycled gold", "recycling"]\n  header_regex: "^(Q[1-4][\\\\s'’]?\\\\d{{2,4}}|\\\\d{{4}}\\\\s?Q[1-4])$"\npaths:\n  shared_raw_workbook: "{tmp_path}/cached.xlsx"\n  seed_csv: "{tmp_path}/seed.csv"\n  processed_output: "{tmp_path}/output.json"\nvalidation:\n  hard_min_value: 0.0\n  warning_min_value: 150.0\n  warning_max_value: 600.0\n'''
    cfg_path.write_text(cfg_content)
    return str(cfg_path)

def test_schema_json_validity(schema_data):
    """Validates that schema.json itself conforms to standard JSON Schema specifications."""
    validator_cls = jsonschema.validators.validator_for(schema_data)
    validator_cls.check_schema(schema_data)

def test_collector_generated_output_against_schema(mock_config, schema_data, tmp_path):
    """Executes the pipeline collector and validates generated dictionary output against schema.json."""
    seed_path = tmp_path / 'seed.csv'
    seed_path.write_text('observation_date,value\n2026-03-31,310.5\n2026-06-30,326.0\n')
    collector = GoldRecyclingCollector(mock_config)
    output = collector.run(publication_date='2026-08-01')
    jsonschema.validate(instance=output, schema=schema_data)

def test_processed_artifact_file_against_schema(schema_data):
    """Validates the processed JSON file written to disk against schema.json if present."""
    processed_file = BASE_DIR / 'processed' / 'l0_006_gold_recycling_flow.json'
    if processed_file.exists():
        with open(processed_file, 'r', encoding='utf-8') as f:
            processed_json = json.load(f)
        jsonschema.validate(instance=processed_json, schema=schema_data)
