"""
Pytest configuration file
"""

import pytest
import sys
from pathlib import Path

# Add src and api directories to Python path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "src"))
sys.path.insert(0, str(ROOT_DIR / "api"))
