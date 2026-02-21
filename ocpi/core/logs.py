"""Logging configuration."""

import logging

from ocpi.core.enums import EnvironmentType


class CustomFormatter(logging.Formatter):
    """Custom logging formatter."""

    grey = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    blue = "\x1b[34;20m"
    reset = "\x1b[0m"
    form = "%(asctime)s | [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.INFO: f"{grey}{form}{reset}",
        logging.WARNING: f"{yellow}{form}{reset}",
        logging.ERROR: f"{red}{form}{reset}",
        logging.DEBUG: f"{blue}{form}{reset}",
    }

    def format(self, record):
        """Return formatted logging message."""
        log_fmt = self.FORMATS.get(record.levelno)  # noqa
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


_ENV_ALIASES: dict[str, str] = {
    "prod": EnvironmentType.production.value,
    "production": EnvironmentType.production.value,
    "dev": EnvironmentType.development.value,
    "development": EnvironmentType.development.value,
    "staging": EnvironmentType.development.value,
    "test": EnvironmentType.testing.value,
    "testing": EnvironmentType.testing.value,
}


class LoggingConfig:
    def __init__(self, environment: str, logger) -> None:
        self.environment = environment
        self.logger = logger

    def configure_logger(self):
        normalized = _ENV_ALIASES.get(self.environment.lower())
        if normalized is None:
            raise ValueError("Invalid environment")
        if normalized == EnvironmentType.production.value:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)


logger = logging.getLogger("OCPI-Logger")

handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())

logger.addHandler(handler)
