"""
Pytest configuration file
"""

import pytest
import sys
from pathlib import Path

# Add src directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "src"))
sys.path.insert(0, str(BASE_DIR / "api"))
