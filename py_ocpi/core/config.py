"""
OCPI Server Configuration using Pydantic Settings v2.
"""


from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from py_ocpi.core.logs import LoggingConfig, logger


class Settings(BaseSettings):
    """OCPI Server settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",  # Ignore extra env vars
    )

    ENVIRONMENT: str = "production"
    NO_AUTH: bool = False
    PROJECT_NAME: str = "OCPI"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    OCPI_HOST: str = "www.example.com"
    OCPI_PREFIX: str = "ocpi"
    PUSH_PREFIX: str = "push"
    COUNTRY_CODE: str = "US"
    PARTY_ID: str = "NON"
    PROTOCOL: str = "https"
    COMMAND_AWAIT_TIME: int = 5
    GET_ACTIVE_PROFILE_AWAIT_TIME: int = 5
    TRAILING_SLASH: bool = True
    CI_STRING_LOWERCASE_PREFERENCE: bool = True

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()

logging_config = LoggingConfig(settings.ENVIRONMENT, logger)
logging_config.configure_logger()
