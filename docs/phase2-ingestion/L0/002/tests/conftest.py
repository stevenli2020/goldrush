"""Keep L0-002's legacy ``collector`` import isolated during aggregate runs."""
import sys
from pathlib import Path
PACKAGE_DIR = Path(__file__).resolve().parent.parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))
sys.modules.pop('collector', None)
