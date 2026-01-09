"""Simple authentication implementation for the EMSP sessions example."""

from ocpi.core.authentication.authenticator import Authenticator


class SimpleAuthenticator(Authenticator):
    """Simple authenticator that validates tokens against a list."""

    VALID_TOKENS = {
        "token_c": ["my-cpo-token-123"],
        "token_a": ["my-emsp-token-456"],
    }

    @classmethod
    async def get_valid_token_c(cls) -> list[str]:
        """Return list of valid CPO tokens."""
        return cls.VALID_TOKENS["token_c"]

    @classmethod
    async def get_valid_token_a(cls) -> list[str]:
        """Return list of valid EMSP tokens."""
        return cls.VALID_TOKENS["token_a"]
