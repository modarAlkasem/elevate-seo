# Python Imports
from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "apps"))
