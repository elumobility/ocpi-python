"""
Pydantic v1/v2 compatibility layer.

This module provides compatibility between Pydantic v1 and v2.
"""

from typing import Any

import pydantic

PYDANTIC_V2 = int(pydantic.VERSION.split(".")[0]) >= 2

if PYDANTIC_V2:
    from pydantic import field_validator
    from pydantic_settings import BaseSettings

    # In Pydantic v2, validators use different signature
    def get_field_name(info: Any) -> str:
        """Get field name from validation info."""
        return info.field_name if hasattr(info, 'field_name') else str(info)

    # For custom types in v2
    from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
    from pydantic_core import CoreSchema, core_schema

    HAS_PYDANTIC_CORE = True

else:
    from pydantic import validator as field_validator
    from pydantic import BaseSettings
    from pydantic.fields import ModelField

    def get_field_name(field: Any) -> str:
        """Get field name from ModelField."""
        return field.name if hasattr(field, 'name') else str(field)

    HAS_PYDANTIC_CORE = False


__all__ = [
    "PYDANTIC_V2",
    "BaseSettings",
    "field_validator",
    "get_field_name",
    "HAS_PYDANTIC_CORE",
]
