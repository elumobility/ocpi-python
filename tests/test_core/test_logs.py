"""Tests for ocpi.core.logs module."""

import logging

import pytest

from ocpi.core.enums import EnvironmentType
from ocpi.core.logs import CustomFormatter, LoggingConfig, logger


def test_custom_formatter_info():
    """Test CustomFormatter with INFO level."""
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    result = formatter.format(record)
    assert "Test message" in result
    assert "test.py:1" in result


def test_custom_formatter_warning():
    """Test CustomFormatter with WARNING level."""
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.WARNING,
        pathname="test.py",
        lineno=1,
        msg="Test warning",
        args=(),
        exc_info=None,
    )
    result = formatter.format(record)
    assert "Test warning" in result


def test_custom_formatter_error():
    """Test CustomFormatter with ERROR level."""
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname="test.py",
        lineno=1,
        msg="Test error",
        args=(),
        exc_info=None,
    )
    result = formatter.format(record)
    assert "Test error" in result


def test_custom_formatter_debug():
    """Test CustomFormatter with DEBUG level."""
    formatter = CustomFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.DEBUG,
        pathname="test.py",
        lineno=1,
        msg="Test debug",
        args=(),
        exc_info=None,
    )
    result = formatter.format(record)
    assert "Test debug" in result


def test_logging_config_production():
    """Test LoggingConfig with production environment."""
    test_logger = logging.getLogger("test_production")
    config = LoggingConfig(EnvironmentType.production.value, test_logger)
    config.configure_logger()
    assert test_logger.level == logging.INFO


def test_logging_config_development():
    """Test LoggingConfig with development environment."""
    test_logger = logging.getLogger("test_development")
    config = LoggingConfig(EnvironmentType.development.value, test_logger)
    config.configure_logger()
    assert test_logger.level == logging.DEBUG


def test_logging_config_testing():
    """Test LoggingConfig with testing environment."""
    test_logger = logging.getLogger("test_testing")
    config = LoggingConfig(EnvironmentType.testing.value, test_logger)
    config.configure_logger()
    assert test_logger.level == logging.DEBUG


def test_logging_config_invalid_environment():
    """Test LoggingConfig with invalid environment raises ValueError."""
    test_logger = logging.getLogger("test_invalid")
    config = LoggingConfig("invalid", test_logger)
    with pytest.raises(ValueError, match="Invalid environment"):
        config.configure_logger()


def test_logger_exists():
    """Test that logger is configured."""
    assert logger is not None
    assert logger.name == "OCPI-Logger"
    assert len(logger.handlers) > 0
