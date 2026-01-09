"""Tests for ocpi.core.exceptions module."""

import pytest

from ocpi.core.exceptions import (
    AuthorizationOCPIError,
    NotFoundOCPIError,
    OCPIError,
)


def test_ocpi_error():
    """Test OCPIError base exception."""
    error = OCPIError("test message")
    assert isinstance(error, Exception)
    assert str(error) == "test message"


def test_authorization_ocpi_error():
    """Test AuthorizationOCPIError exception."""
    error = AuthorizationOCPIError()
    assert isinstance(error, OCPIError)
    assert str(error) == "Your authorization token is invalid."


def test_not_found_ocpi_error():
    """Test NotFoundOCPIError exception."""
    error = NotFoundOCPIError()
    assert isinstance(error, OCPIError)
    assert str(error) == "Object not found."


def test_authorization_ocpi_error_raises():
    """Test that AuthorizationOCPIError can be raised."""
    with pytest.raises(AuthorizationOCPIError) as exc_info:
        raise AuthorizationOCPIError()
    assert str(exc_info.value) == "Your authorization token is invalid."


def test_not_found_ocpi_error_raises():
    """Test that NotFoundOCPIError can be raised."""
    with pytest.raises(NotFoundOCPIError) as exc_info:
        raise NotFoundOCPIError()
    assert str(exc_info.value) == "Object not found."
