from abc import ABC, abstractmethod

from ocpi.core.config import logger
from ocpi.core.exceptions import AuthorizationOCPIError


class Authenticator(ABC):
    """
    Base class for OCPI token authentication.

    Implement this class to provide token validation for your OCPI application.
    You must implement get_valid_token_c() and get_valid_token_a() methods.

    Token Types:
        - Token C: Used by CPO (Charge Point Operator) for server-to-server communication
        - Token A: Used by EMSP (eMobility Service Provider) for credentials exchange

    Example:
        ```python
        from ocpi.core.authentication.authenticator import Authenticator

        class MyAuthenticator(Authenticator):
            @classmethod
            async def get_valid_token_c(cls) -> list[str]:
                # Return list of valid CPO tokens (Token C)
                # In production, fetch from database or configuration
                return ["cpo-token-123", "cpo-token-456"]

            @classmethod
            async def get_valid_token_a(cls) -> list[str]:
                # Return list of valid EMSP tokens (Token A)
                return ["emsp-token-789"]
        ```
    """

    @classmethod
    async def authenticate(cls, auth_token: str) -> None:
        """
        Authenticate a given authorization token (Token C).

        Validates that the provided token is in the list of valid CPO tokens.
        Raises AuthorizationOCPIError if token is invalid.

        Args:
            auth_token: The authorization token to validate (Token C).

        Raises:
            AuthorizationOCPIError: If the token is not in the valid tokens list.

        Example:
            ```python
            authenticator = MyAuthenticator()
            try:
                await authenticator.authenticate("cpo-token-123")
                # Token is valid, proceed with request
            except AuthorizationOCPIError:
                # Token is invalid, request will be rejected
                pass
            ```
        """
        list_token_c = await cls.get_valid_token_c()
        if auth_token not in list_token_c:
            logger.debug(f"Given `{auth_token}` token is not valid")
            raise AuthorizationOCPIError

    @classmethod
    async def authenticate_credentials(
        cls,
        auth_token: str,
    ) -> str | dict | None:
        """Authenticate given auth token where both tokens valid."""
        if auth_token:
            list_token_a = await cls.get_valid_token_a()
            if auth_token in list_token_a:
                logger.debug(f"Token A `{auth_token}` is used.")
                return {}

            list_token_c = await cls.get_valid_token_c()
            if auth_token in list_token_c:
                logger.debug(f"Token C `{auth_token}` is used.")
                return auth_token
        logger.debug(f"Token `{auth_token}` is not of type A or C.")
        return None

    @classmethod
    @abstractmethod
    async def get_valid_token_c(cls) -> list[str]:
        """
        Return list of valid CPO tokens (Token C).

        This method must be implemented by subclasses. It should return
        a list of all valid Token C values that can be used for authentication.

        Returns:
            list[str]: List of valid CPO token strings.

        Example:
            ```python
            @classmethod
            async def get_valid_token_c(cls) -> list[str]:
                # Simple in-memory list
                return ["token1", "token2"]

                # Or fetch from database
                async with db_session() as session:
                    tokens = await session.execute(
                        select(Token.value).where(Token.type == "cpo")
                    )
                    return [t[0] for t in tokens]
            ```
        """
        pass

    @classmethod
    @abstractmethod
    async def get_valid_token_a(cls) -> list[str]:
        """
        Return list of valid EMSP tokens (Token A).

        This method must be implemented by subclasses. It should return
        a list of all valid Token A values used for credentials exchange.

        Returns:
            list[str]: List of valid EMSP token strings.

        Example:
            ```python
            @classmethod
            async def get_valid_token_a(cls) -> list[str]:
                # Simple in-memory list
                return ["emsp-token-1", "emsp-token-2"]

                # Or fetch from database
                async with db_session() as session:
                    tokens = await session.execute(
                        select(Token.value).where(Token.type == "emsp")
                    )
                    return [t[0] for t in tokens]
            ```
        """
        pass
