"""Simple authenticator for the bookings example.

In production, implement proper token validation with database lookup.
"""

from ocpi.core.authentication.authenticator import Authenticator


class SimpleAuthenticator(Authenticator):
    """Simple authenticator using hardcoded tokens for demonstration."""

    # Demo tokens (in production, store these securely in a database)
    CPO_TOKENS = ["my-cpo-token-123", "cpo-token-456"]
    EMSP_TOKENS = ["my-emsp-token-789", "emsp-token-abc"]

    @classmethod
    async def get_valid_token_c(cls) -> list[str]:
        """Return valid CPO tokens (Token C)."""
        return cls.CPO_TOKENS

    @classmethod
    async def get_valid_token_a(cls) -> list[str]:
        """Return valid EMSP tokens (Token A)."""
        return cls.EMSP_TOKENS
