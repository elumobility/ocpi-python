"""Conftest for example tests to ensure proper isolation."""

import sys
from pathlib import Path

# Ensure examples directory is in path for all example tests
examples_dir = Path(__file__).parent.parent.parent / "examples"
if str(examples_dir) not in sys.path:
    sys.path.insert(0, str(examples_dir))
