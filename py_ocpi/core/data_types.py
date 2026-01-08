"""
OCPI data types based on https://github.com/ocpi/ocpi/blob/2.2.1/types.asciidoc

Supports both Pydantic v1 and v2.
"""

from datetime import datetime, timezone
from typing import Any, Type

from .compat import PYDANTIC_V2
from .config import settings


if PYDANTIC_V2:
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
            if settings.CI_STRING_LOWERCASE_PREFERENCE:
                return cls(v.lower())
            return cls(v.upper())

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
                    datetime.now(timezone.utc)
                    .isoformat(timespec="seconds")
                    .replace("+00:00", "Z")
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
            return cls(
                formatted_v.isoformat(timespec="seconds").replace("+00:00", "Z")
            )

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

else:
    # Pydantic v1 implementation
    from pydantic.fields import ModelField

    class StringBase(str):
        """
        Case sensitive String. Only printable UTF-8 allowed.
        """

        max_length: int

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(examples=["String"])

        @classmethod
        def validate(cls, v, field: ModelField):
            if not isinstance(v, str):
                raise TypeError(f"expected string but received {type(v)}")
            try:
                v.encode("UTF-8")
            except UnicodeError as e:
                raise ValueError("invalid string format") from e
            if len(v) > cls.max_length:
                raise ValueError(
                    f"{field.name} length must be lower or equal to {cls.max_length}"
                )
            return cls(v)

        def __repr__(self):
            return f"String({super().__repr__()})"

    class CiStringBase(str):
        """
        Case Insensitive String. Only printable ASCII allowed.
        """

        max_length: int

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(examples=["string"])

        @classmethod
        def validate(cls, v, field: ModelField):
            if not isinstance(v, str):
                raise TypeError(f"expected string but received {type(v)}")
            if not v.isascii():
                raise ValueError("invalid cistring format")
            if len(v) > cls.max_length:
                raise ValueError(
                    f"{field.name} length must be lower or equal to {cls.max_length}"
                )
            if settings.CI_STRING_LOWERCASE_PREFERENCE:
                return cls(v.lower())
            return cls(v.upper())

        def __repr__(self):
            return f"CiString({super().__repr__()})"

    class URL(str):
        """URL type."""

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(
                examples=["http://www.w3.org/Addressing/URL/uri-spec.html"]
            )

        @classmethod
        def validate(cls, v, field: ModelField):
            v = String(255).validate(v, field)  # type: ignore
            return cls(v)

        def __repr__(self):
            return f"URL({super().__repr__()})"

    class DateTime(str):
        """RFC 3339 timestamp."""

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(
                examples=[
                    datetime.now(timezone.utc)
                    .isoformat(timespec="seconds")
                    .replace("+00:00", "Z")
                ]
            )

        @classmethod
        def validate(cls, v):
            if v.endswith("Z"):
                v = f"{v[:-1]}+00:00"
            try:
                formatted_v = datetime.fromisoformat(v)
            except ValueError as e:
                raise ValueError(f"Invalid RFC 3339 timestamp: {v}") from e
            return cls(
                formatted_v.isoformat(timespec="seconds").replace("+00:00", "Z")
            )

        def __repr__(self):
            return f"DateTime({super().__repr__()})"

    class DisplayText(dict):
        """Display text."""

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(
                examples=[{"language": "en", "text": "Standard Tariff"}]
            )

        @classmethod
        def validate(cls, v):
            if not isinstance(v, dict):
                raise TypeError(f"expected dict but received {type(v)}")
            if "language" not in v:
                raise TypeError('property "language" required')
            if "text" not in v:
                raise TypeError('property "text" required')
            if len(v["text"]) > 512:
                raise TypeError("text too long")
            return cls(v)

        def __repr__(self):
            return f"DisplayText({super().__repr__()})"

    class Number(float):
        """OCPI Number."""

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(examples=[])

        @classmethod
        def validate(cls, v):
            if not any([isinstance(v, float), isinstance(v, int)]):
                TypeError(f"expected float but received {type(v)}")
            return cls(float(v))

        def __repr__(self):
            return f"Number({super().__repr__()})"

    class Price(dict):
        """OCPI Price."""

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @classmethod
        def __modify_schema__(cls, field_schema):
            field_schema.update(
                examples=[{"excl_vat": 1.0000, "incl_vat": 1.2500}]
            )

        @classmethod
        def validate(cls, v):
            if not isinstance(v, dict):
                raise TypeError("dictionary required")
            if "excl_vat" not in v:
                raise TypeError('property "excl_vat" required')
            return cls(v)

        def __repr__(self):
            return f"Price({super().__repr__()})"


# Factory functions for parameterized types
class String:
    def __new__(cls, max_length: int = 255) -> Type[str]:  # type: ignore
        return type("String", (StringBase,), {"max_length": max_length})


class CiString:
    def __new__(cls, max_length: int = 255) -> type:  # type: ignore
        return type("CiString", (CiStringBase,), {"max_length": max_length})
