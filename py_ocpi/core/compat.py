"""
Pydantic v2 compatibility layer.

This module provides imports and utilities for Pydantic v2.
Note: Pydantic v1 support has been removed as of FastAPI 0.112+.
"""

from typing import Any

import pydantic
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler, field_validator
from pydantic_core import CoreSchema, core_schema
from pydantic_settings import BaseSettings

PYDANTIC_VERSION = pydantic.VERSION
PYDANTIC_V2 = True  # We now require Pydantic v2


def get_field_name(info: Any) -> str:
    """Get field name from validation info."""
    return info.field_name if hasattr(info, "field_name") else str(info)


__all__ = [
    "PYDANTIC_VERSION",
    "PYDANTIC_V2",
    "BaseSettings",
    "field_validator",
    "get_field_name",
    "GetCoreSchemaHandler",
    "GetJsonSchemaHandler",
    "CoreSchema",
    "core_schema",
]
