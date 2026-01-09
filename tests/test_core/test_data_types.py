"""Tests for ocpi.core.data_types module."""

from datetime import UTC, datetime

import pytest
from pydantic import BaseModel, ValidationError

from ocpi.core.data_types import (
    CiString,
    CiStringBase,
    DateTime,
    DisplayText,
    Number,
    Price,
    String,
    StringBase,
    URL,
)


def test_string_base_valid():
    """Test StringBase with valid UTF-8 string."""
    result = StringBase("test string")
    assert isinstance(result, StringBase)
    assert result == "test string"


def test_string_factory():
    """Test String factory creates type with custom max_length."""
    CustomString = String(max_length=100)
    assert CustomString.max_length == 100


def test_string_base_valid_through_pydantic():
    """Test StringBase through Pydantic model."""
    class TestModel(BaseModel):
        value: StringBase
    
    result = TestModel(value="test")
    assert isinstance(result.value, StringBase)
    assert result.value == "test"


def test_string_base_max_length():
    """Test StringBase with max length."""
    long_string = "a" * 255
    result = StringBase(long_string)
    assert len(result) == 255


def test_string_base_exceeds_max_length():
    """Test StringBase exceeding max length raises ValidationError."""
    class TestModel(BaseModel):
        value: StringBase
    
    long_string = "a" * 256
    with pytest.raises(ValidationError):
        TestModel(value=long_string)


def test_cistring_base_valid():
    """Test CiStringBase with valid ASCII string."""
    result = CiStringBase("TEST")
    assert isinstance(result, CiStringBase)
    # Should be uppercase or lowercase based on settings
    assert result in ["TEST", "test"]


def test_cistring_factory():
    """Test CiString factory creates type with custom max_length."""
    CustomCiString = CiString(max_length=100)
    assert CustomCiString.max_length == 100


def test_cistring_base_non_ascii():
    """Test CiStringBase with non-ASCII raises ValueError."""
    class TestModel(BaseModel):
        value: CiStringBase
    
    with pytest.raises(ValidationError):
        TestModel(value="café")  # Contains non-ASCII character


def test_cistring_base_max_length():
    """Test CiStringBase with max length."""
    long_string = "a" * 255
    result = CiStringBase(long_string)
    assert len(result) == 255


def test_url_valid():
    """Test URL with valid URL."""
    result = URL("https://example.com")
    assert isinstance(result, URL)
    assert result == "https://example.com"


def test_url_max_length():
    """Test URL with max length."""
    long_url = "https://example.com/" + "a" * (255 - 22)
    result = URL(long_url)
    assert len(result) <= 255


def test_datetime_valid():
    """Test DateTime with valid RFC 3339 timestamp."""
    result = DateTime("2023-01-01T12:00:00Z")
    assert isinstance(result, DateTime)
    assert "2023-01-01T12:00:00Z" in result


def test_datetime_with_timezone():
    """Test DateTime with timezone offset."""
    result = DateTime("2023-01-01T12:00:00+00:00")
    assert isinstance(result, DateTime)
    # DateTime normalizes to Z format
    assert "2023-01-01T12:00:00" in result


def test_datetime_invalid():
    """Test DateTime with invalid timestamp raises ValueError."""
    class TestModel(BaseModel):
        value: DateTime
    
    with pytest.raises(ValidationError):
        TestModel(value="invalid-date")


def test_datetime_z_suffix():
    """Test DateTime converts Z suffix to +00:00."""
    result = DateTime("2023-01-01T12:00:00Z")
    # Should normalize to Z format
    assert result.endswith("Z")


def test_display_text_valid():
    """Test DisplayText with valid dict."""
    result = DisplayText({"language": "en", "text": "Hello"})
    assert isinstance(result, DisplayText)
    assert result["language"] == "en"
    assert result["text"] == "Hello"


def test_display_text_missing_language():
    """Test DisplayText without language raises TypeError."""
    # DisplayText raises TypeError directly, not wrapped by Pydantic
    with pytest.raises(TypeError, match="language"):
        DisplayText._validate({"text": "Hello"})


def test_display_text_missing_text():
    """Test DisplayText without text raises TypeError."""
    with pytest.raises(TypeError, match="text"):
        DisplayText._validate({"language": "en"})


def test_display_text_not_dict():
    """Test DisplayText with non-dict raises TypeError."""
    with pytest.raises(TypeError, match="dict"):
        DisplayText._validate("not a dict")


def test_display_text_text_too_long():
    """Test DisplayText with text exceeding 512 chars raises TypeError."""
    long_text = "a" * 513
    with pytest.raises(TypeError, match="too long"):
        DisplayText._validate({"language": "en", "text": long_text})


def test_display_text_text_max_length():
    """Test DisplayText with text at max length (512 chars)."""
    long_text = "a" * 512
    result = DisplayText({"language": "en", "text": long_text})
    assert len(result["text"]) == 512


def test_number_valid():
    """Test Number with valid number."""
    result = Number(42.5)
    assert isinstance(result, Number)
    assert result == 42.5


def test_number_from_string():
    """Test Number from string."""
    result = Number("42.5")
    assert isinstance(result, Number)
    assert result == 42.5


def test_number_from_int():
    """Test Number from integer."""
    result = Number(42)
    assert isinstance(result, Number)
    assert result == 42.0


def test_price_valid():
    """Test Price with valid dict."""
    result = Price({"excl_vat": 10.0})
    assert isinstance(result, Price)
    assert result["excl_vat"] == 10.0


def test_price_with_incl_vat():
    """Test Price with incl_vat."""
    result = Price({"excl_vat": 10.0, "incl_vat": 12.0})
    assert result["excl_vat"] == 10.0
    assert result["incl_vat"] == 12.0


def test_price_missing_excl_vat():
    """Test Price without excl_vat raises TypeError."""
    # Price raises TypeError directly, not wrapped by Pydantic
    with pytest.raises(TypeError, match="excl_vat"):
        Price._validate({"incl_vat": 12.0})


def test_price_not_dict():
    """Test Price with non-dict raises TypeError."""
    with pytest.raises(TypeError, match="dictionary"):
        Price._validate("not a dict")
