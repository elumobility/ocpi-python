"""
OCPI data types based on https://github.com/ocpi/ocpi/blob/2.2.1/types.asciidoc

Requires Pydantic v2.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema


class StringBase(str):
    """
    Case sensitive String. Only printable UTF-8 allowed.
    """

    max_length: int = 255

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(max_length=cls.max_length),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "maxLength": cls.max_length}

    @classmethod
    def _validate(cls, v: str) -> "StringBase":
        try:
            v.encode("UTF-8")
        except UnicodeError as e:
            raise ValueError("invalid string format") from e
        return cls(v)


class CiStringBase(str):
    """
    Case Insensitive String. Only printable ASCII allowed.
    """

    max_length: int = 255

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(max_length=cls.max_length),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "maxLength": cls.max_length}

    @classmethod
    def _validate(cls, v: str) -> "CiStringBase":
        if not v.isascii():
            raise ValueError("invalid cistring format")
        # Preserve original case. CiString means case-insensitive *comparison*,
        # not that the value should be mutated. Lowercasing/uppercasing destroys
        # identifiers like OCPP charge point IDs (e.g. "K0032832A").
        return cls(v)


class URL(str):
    """URL type - String(255) following URI spec."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(max_length=255),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "format": "uri", "maxLength": 255}

    @classmethod
    def _validate(cls, v: str) -> "URL":
        return cls(v)


class DateTime(str):
    """RFC 3339 timestamp in UTC."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "string",
            "format": "date-time",
            "examples": [
                datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
            ],
        }

    @classmethod
    def _validate(cls, v: str) -> "DateTime":
        if v.endswith("Z"):
            v = f"{v[:-1]}+00:00"
        try:
            formatted_v = datetime.fromisoformat(v)
        except ValueError as e:
            raise ValueError(f"Invalid RFC 3339 timestamp: {v}") from e
        return cls(formatted_v.isoformat(timespec="seconds").replace("+00:00", "Z"))


class DisplayText(dict):
    """Display text with language."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.dict_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "object",
            "properties": {
                "language": {"type": "string", "maxLength": 2},
                "text": {"type": "string", "maxLength": 512},
            },
            "required": ["language", "text"],
        }

    @classmethod
    def _validate(cls, v: dict) -> "DisplayText":
        if not isinstance(v, dict):
            raise TypeError(f"expected dict but received {type(v)}")
        if "language" not in v:
            raise TypeError('property "language" required')
        if "text" not in v:
            raise TypeError('property "text" required')
        if len(v["text"]) > 512:
            raise TypeError("text too long")
        return cls(v)


class Number(float):
    """OCPI Number type."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.float_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "number"}

    @classmethod
    def _validate(cls, v: Any) -> "Number":
        return cls(float(v))


class Price(dict):
    """OCPI Price type with excl_vat and optional incl_vat."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.dict_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {
            "type": "object",
            "properties": {
                "excl_vat": {"type": "number"},
                "incl_vat": {"type": "number"},
            },
            "required": ["excl_vat"],
        }

    @classmethod
    def _validate(cls, v: dict) -> "Price":
        if not isinstance(v, dict):
            raise TypeError("dictionary required")
        if "excl_vat" not in v:
            raise TypeError('property "excl_vat" required')
        return cls(v)


# Factory functions for parameterized types
class String:
    """Factory for String types with custom max_length."""

    def __new__(cls, max_length: int = 255) -> type[str]:  # type: ignore[misc]
        return type("String", (StringBase,), {"max_length": max_length})


class CiString:
    """Factory for CiString types with custom max_length."""

    def __new__(cls, max_length: int = 255) -> type:  # type: ignore[misc]
        return type("CiString", (CiStringBase,), {"max_length": max_length})
