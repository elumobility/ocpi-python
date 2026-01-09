"""Python Implementation of OCPI

A modern, production-ready Python implementation of the Open Charge Point Interface (OCPI) protocol.

Supports OCPI 2.3.0, 2.2.1, and 2.1.1 with FastAPI and Pydantic v2.
"""

__version__ = "2026.1.9"

from .core import enums, data_types
from .main import get_application
