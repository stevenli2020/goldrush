"""Keep legacy same-name local modules isolated during aggregate collection.

Several variable packages intentionally expose a local ``parser.py``.  Tests
add their package directory to ``sys.path``; removing the previous top-level
module before each test module is imported prevents pytest from reusing a
different variable's parser.
"""
import sys

def pytest_collect_file(file_path, parent):
    if file_path.suffix == '.py' and file_path.name.startswith('test_'):
        for module_name in ('parser', 'collector'):
            sys.modules.pop(module_name, None)
    return None
