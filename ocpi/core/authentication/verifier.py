from fastapi import (
    Depends,
    Header,
    Path,
    Query,
    Security,
    WebSocketException,
    status,
)
from fastapi.security import APIKeyHeader

from ocpi.core.authentication.authenticator import Authenticator
from ocpi.core.config import logger, settings
from ocpi.core.dependencies import get_authenticator
from ocpi.core.exceptions import AuthorizationOCPIError

# Import moved to function level to avoid circular import
from ocpi.modules.versions.enums import VersionNumber

api_key_header = APIKeyHeader(
    name="authorization",
    description="API key with `Token ` prefix.",
    scheme_name="Token",
)
auth_verifier = Security(api_key_header) if not settings.NO_AUTH else ""


class AuthorizationVerifier:
    """
    A class responsible for verifying authorization tokens
    based on the specified version number.

    :param version (VersionNumber): OCPI version used.
    """

    def __init__(self, version: VersionNumber) -> None:
        self.version = version

    async def __call__(
        self,
        authorization: str = auth_verifier,
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param authorization (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        if settings.NO_AUTH and authorization == "":
            logger.debug("Authentication skipped due to NO_AUTH setting.")
            return True

        try:
            token = authorization.split()[1]
            # OCPI 2.2.x and 2.3.0 both require Base64-encoded tokens in Authorization header
            if self.version.startswith("2.2") or self.version.startswith("2.3"):
                try:
                    from ocpi.core.utils import decode_string_base64

                    token = decode_string_base64(token)
                except (UnicodeDecodeError, ValueError) as e:
                    # If base64 decoding fails (bad padding, invalid chars),
                    # try authenticating with the raw token as fallback.
                    logger.debug(f"Token base64 decode failed ({e}), trying raw token.")
            await authenticator.authenticate(token)
        except IndexError:
            logger.debug(
                "Token `%s` cannot be split in parts. Check if it starts with `Token `"
            )
            raise AuthorizationOCPIError


class CredentialsAuthorizationVerifier:
    """
    A class responsible for verifying authorization tokens
    based on the specified version number.

    :param version (VersionNumber): OCPI version used.
    """

    def __init__(self, version: VersionNumber | None) -> None:
        self.version = version

    async def __call__(
        self,
        authorization: str = Security(api_key_header),
        authenticator: Authenticator = Depends(get_authenticator),
    ) -> str | dict | None:
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param authorization (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        try:
            token = authorization.split()[1]
        except IndexError:
            logger.debug(
                "Token `%s` cannot be split in parts. Check if it starts with `Token `"
            )
            raise AuthorizationOCPIError

        # OCPI 2.2.x and 2.3.0 both require Base64-encoded tokens in Authorization header
        if self.version:
            if self.version.startswith("2.2") or self.version.startswith("2.3"):
                try:
                    from ocpi.core.utils import decode_string_base64

                    token = decode_string_base64(token)
                except (UnicodeDecodeError, ValueError) as e:
                    logger.debug(f"Token base64 decode failed ({e}), trying raw token.")
        else:
            # For versions without explicit version (legacy), try to decode
            try:
                from ocpi.core.utils import decode_string_base64

                token = decode_string_base64(token)
            except (UnicodeDecodeError, ValueError):
                pass
        return await authenticator.authenticate_credentials(token)


class VersionsAuthorizationVerifier(CredentialsAuthorizationVerifier):
    """
    Verifies authorization for versions and version details endpoints.
    When VERSIONS_REQUIRE_AUTH is False, allows unauthenticated access (discovery).
    """

    async def __call__(
        self,
        authorization: str = Header(default="", alias="Authorization"),
        authenticator: Authenticator = Depends(get_authenticator),
    ) -> str | dict | None:
        """
        Verifies the authorization token for version endpoints.
        If VERSIONS_REQUIRE_AUTH is False, allows requests without token.
        """
        if settings.NO_AUTH and authorization == "":
            logger.debug("Authentication skipped due to NO_AUTH setting.")
            return ""
        if not settings.VERSIONS_REQUIRE_AUTH and (not authorization or authorization.strip() == ""):
            logger.debug("Versions/details accessed without auth (VERSIONS_REQUIRE_AUTH=false).")
            return ""
        if not authorization or authorization.strip() == "":
            return None
        return await super().__call__(authorization, authenticator)


class HttpPushVerifier:
    """
    A class responsible for verifying authorization tokens if using push.
    """

    async def __call__(
        self,
        authorization: str = Header(...) if not settings.NO_AUTH else "",
        version: VersionNumber = Path(...),
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param authorization (str): The authorization header containing
          the token.
        :param version (VersionNumber): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        if settings.NO_AUTH and authorization == "":
            logger.debug("Authentication skipped due to NO_AUTH setting.")
            return True

        try:
            token = authorization.split()[1]
            # OCPI 2.2.x and 2.3.0 both require Base64-encoded tokens in Authorization header
            if version.value.startswith("2.2") or version.value.startswith("2.3"):
                try:
                    from ocpi.core.utils import decode_string_base64

                    token = decode_string_base64(token)
                except (UnicodeDecodeError, ValueError) as e:
                    logger.debug(f"Token base64 decode failed ({e}), trying raw token.")
            await authenticator.authenticate(token)
        except IndexError:
            logger.debug(
                "Token `%s` cannot be split in parts. Check if it starts with `Token `"
            )
            raise AuthorizationOCPIError


class WSPushVerifier:
    """
    A class responsible for verifying authorization tokens if using ws push.
    """

    async def __call__(
        self,
        token: str = Query(...) if not settings.NO_AUTH else "",
        version: VersionNumber = Path(...),
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param token (str): Token parameter in ws.
        :param version (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        if settings.NO_AUTH and token == "":
            logger.debug("Authentication skipped due to NO_AUTH setting.")
            return True

        try:
            if not token:
                logger.debug("Token wasn't given.")
                raise AuthorizationOCPIError

            # OCPI 2.2.x and 2.3.0 both require Base64-encoded tokens in Authorization header
            if version.value.startswith("2.2") or version.value.startswith("2.3"):
                try:
                    from ocpi.core.utils import decode_string_base64

                    token = decode_string_base64(token)
                except (UnicodeDecodeError, ValueError) as e:
                    logger.debug(f"Token base64 decode failed ({e}), trying raw token.")
            await authenticator.authenticate(token)
        except AuthorizationOCPIError:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
