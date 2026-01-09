"""Tests for ocpi.core.compat module."""

import pytest

from ocpi.core.compat import (
    PYDANTIC_VERSION,
    PYDANTIC_V2,
    BaseSettings,
    CoreSchema,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
    core_schema,
    field_validator,
    get_field_name,
)


def test_pydantic_version():
    """Test PYDANTIC_VERSION is set."""
    assert PYDANTIC_VERSION is not None
    assert isinstance(PYDANTIC_VERSION, str)


def test_pydantic_v2():
    """Test PYDANTIC_V2 is True."""
    assert PYDANTIC_V2 is True


def test_get_field_name_with_field_name():
    """Test get_field_name with object that has field_name attribute."""
    class MockInfo:
        field_name = "test_field"
    
    assert get_field_name(MockInfo()) == "test_field"


def test_get_field_name_without_field_name():
    """Test get_field_name with object without field_name attribute."""
    class MockInfo:
        pass
    
    result = get_field_name(MockInfo())
    assert isinstance(result, str)


def test_get_field_name_with_string():
    """Test get_field_name with string."""
    assert get_field_name("test") == "test"


def test_imports():
    """Test that all expected imports are available."""
    assert BaseSettings is not None
    assert GetCoreSchemaHandler is not None
    assert GetJsonSchemaHandler is not None
    assert CoreSchema is not None
    assert core_schema is not None
    assert field_validator is not None
