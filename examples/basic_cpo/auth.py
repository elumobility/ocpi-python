"""Simple authentication implementation for the basic CPO example."""

import base64
from ocpi.core.authentication.authenticator import Authenticator


class SimpleAuthenticator(Authenticator):
    """Simple authenticator that validates tokens against a list.

    In production, fetch these from your database or configuration service.
    
    Note: For OCPI 2.3.0, tokens must be base64-encoded in the Authorization header.
    The authenticator receives the decoded token.
    """

    # Store plain tokens - they will be base64 encoded in the header
    # For OCPI 2.3.0, the library decodes base64 tokens automatically
    VALID_TOKENS = {
        "token_c": ["my-cpo-token-123"],
        "token_a": ["my-emsp-token-456"],
    }

    @classmethod
    async def get_valid_token_c(cls) -> list[str]:
        """Return list of valid CPO tokens (plain text, not base64)."""
        return cls.VALID_TOKENS["token_c"]

    @classmethod
    async def get_valid_token_a(cls) -> list[str]:
        """Return list of valid EMSP tokens (plain text, not base64)."""
        return cls.VALID_TOKENS["token_a"]


# Helper function to encode tokens for use in Authorization header
def encode_token(token: str) -> str:
    """Encode a plain token to base64 for OCPI 2.3.0 Authorization header."""
    return base64.b64encode(token.encode("utf-8")).decode("utf-8")
