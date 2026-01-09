# LLM-Assisted Development Guide

This guide helps you use AI coding assistants (ChatGPT, Claude, GitHub Copilot, Cursor, etc.) effectively with OCPI Python.

## Quick Reference for LLMs

When asking an LLM to help with OCPI Python, provide this context:

```
I'm working with ocpi-python, a Python library for the Open Charge Point Interface (OCPI) protocol.
- Uses FastAPI and Pydantic v2
- Supports OCPI versions 2.3.0, 2.2.1, and 2.1.1
- Main entry point: `get_application()` from `ocpi` package
- All CRUD operations are async
- Authentication uses token-based system (Token C for CPO, Token A for EMSP)
- See examples/ directory for complete working code
```

## Common Tasks

### 1. Creating a New OCPI Application

**Prompt for LLM:**
```
Help me create an OCPI CPO application using ocpi-python that:
- Uses OCPI version 2.3.0
- Implements Locations and Sessions modules
- Has a simple in-memory storage for testing
- Validates tokens from a list
```

**Expected Pattern:**
```python
from ocpi import get_application
from ocpi.core.enums import RoleEnum, ModuleID
from ocpi.modules.versions.enums import VersionNumber

# Your authenticator and CRUD classes here

app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.locations, ModuleID.sessions],
    authenticator=MyAuthenticator,
    crud=MyCrud,
)
```

### 2. Implementing Authentication

**Prompt for LLM:**
```
I need to implement an Authenticator for ocpi-python that:
- Validates tokens from a database
- Supports both Token C (CPO) and Token A (EMSP)
- Uses async database queries
```

**Expected Pattern:**
```python
from ocpi.core.authentication.authenticator import Authenticator

class DatabaseAuthenticator(Authenticator):
    @classmethod
    async def get_valid_token_c(cls) -> list[str]:
        # Query database for CPO tokens
        async with db_session() as session:
            tokens = await session.execute(
                select(Token.value).where(Token.type == "cpo")
            )
            return [token[0] for token in tokens]
    
    @classmethod
    async def get_valid_token_a(cls) -> list[str]:
        # Query database for EMSP tokens
        async with db_session() as session:
            tokens = await session.execute(
                select(Token.value).where(Token.type == "emsp")
            )
            return [token[0] for token in tokens]
```

### 3. Implementing CRUD Operations

**Prompt for LLM:**
```
Help me implement CRUD operations for Locations module using SQLAlchemy with ocpi-python:
- Store locations in a database
- Support filtering by country_code and party_id
- Return proper OCPI response format
```

**Expected Pattern:**
```python
from ocpi.core import enums
from ocpi.core.crud import CRUD

class LocationCrud(CRUD):
    @classmethod
    async def list(cls, module: enums.ModuleID, role: enums.RoleEnum,
                   filters: dict, *args, **kwargs) -> tuple[list, int, bool]:
        if module != enums.ModuleID.locations:
            return [], 0, False
        
        # Extract filters
        country_code = filters.get("country_code")
        party_id = filters.get("party_id")
        
        # Query database
        query = select(Location)
        if country_code:
            query = query.where(Location.country_code == country_code)
        if party_id:
            query = query.where(Location.party_id == party_id)
        
        async with db_session() as session:
            result = await session.execute(query)
            locations = result.scalars().all()
            return [loc.to_dict() for loc in locations], len(locations), False
    
    @classmethod
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum,
                  id: str, *args, **kwargs):
        if module != enums.ModuleID.locations:
            return None
        
        async with db_session() as session:
            location = await session.get(Location, id)
            return location.to_dict() if location else None
    
    # Implement create, update, delete similarly...
```

### 4. Adding a New Module Endpoint

**Prompt for LLM:**
```
I need to add a custom endpoint to my OCPI application that:
- Returns charging station status
- Requires authentication
- Returns OCPI-compliant response
```

**Expected Pattern:**
```python
from fastapi import APIRouter, Depends
from ocpi.core.authentication.verifier import AuthorizationVerifier
from ocpi.core.schemas import OCPIResponse
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter()

@router.get("/status")
async def get_status(
    version: VersionNumber = VersionNumber.v_2_3_0,
    auth: bool = Depends(AuthorizationVerifier(version))
):
    return OCPIResponse(
        status_code=1000,
        status_message="Success",
        data={"status": "operational"}
    )
```

## Best Practices for LLM Prompts

### ✅ Good Prompts

- **Be specific about OCPI concepts**: "I need to implement a CPO that manages charging locations"
- **Mention the library**: "Using ocpi-python library"
- **Specify version**: "For OCPI 2.3.0"
- **Include context**: "I'm building a charge point operator system"
- **Reference examples**: "Similar to the basic_cpo example but with database storage"

### ❌ Avoid These

- Generic prompts: "How do I make an API?"
- Missing context: "Help me with authentication" (without mentioning OCPI)
- Wrong assumptions: "How do I use Flask?" (we use FastAPI)
- Missing version info: "How do I handle tokens?" (different for 2.1.1 vs 2.3.0)

## Code Patterns LLMs Should Know

### 1. OCPI Response Format

All endpoints return:
```python
{
    "status_code": 1000,  # 1000 = success, 2000+ = client errors, 3000+ = server errors
    "status_message": "Success",
    "data": {...}  # The actual data
}
```

### 2. Error Handling

```python
from ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError

# Authentication failure
if token not in valid_tokens:
    raise AuthorizationOCPIError

# Resource not found
if not location:
    raise NotFoundOCPIError
```

### 3. Version-Specific Behavior

```python
from ocpi.modules.versions.enums import VersionNumber

if version == VersionNumber.v_2_3_0:
    # OCPI 2.3.0 specific logic
    token = decode_base64(token)
elif version == VersionNumber.v_2_2_1:
    # OCPI 2.2.1 specific logic
    token = decode_base64(token)
else:
    # OCPI 2.1.1 (no base64 encoding)
    pass
```

### 4. Module-Specific Imports

```python
# Locations
from ocpi.modules.locations.v_2_3_0.schemas import Location

# Sessions
from ocpi.modules.sessions.v_2_3_0.schemas import Session

# Tokens
from ocpi.modules.tokens.v_2_3_0.schemas import Token
```

## Useful Resources to Share with LLMs

When working with LLMs, you can reference:

1. **Examples Directory**: `examples/basic_cpo/`, `examples/full_cpo/`, etc.
2. **Documentation**: `docs/quickstart.md`, `docs/tutorials/`
3. **OCPI Spec**: Links to official OCPI documentation
4. **Type Hints**: All code has type hints for better LLM understanding

## Troubleshooting Common LLM Mistakes

### Issue: LLM suggests using Flask instead of FastAPI
**Fix**: Explicitly mention "FastAPI" and "ocpi-python uses FastAPI"

### Issue: LLM doesn't understand async/await
**Fix**: Emphasize "all CRUD methods are async" and show async examples

### Issue: LLM suggests wrong import paths
**Fix**: Show correct import: `from ocpi import get_application` not `from ocpi.main import`

### Issue: LLM doesn't handle OCPI versions correctly
**Fix**: Always specify version and mention version-specific differences (Base64 encoding, etc.)

## Example Conversation Flow

**You**: "I need to create an OCPI CPO application that stores locations in PostgreSQL"

**LLM should suggest**:
1. Import statements (`from ocpi import get_application`, etc.)
2. Database setup (SQLAlchemy async)
3. Authenticator implementation
4. CRUD implementation with database queries
5. Application setup with `get_application()`

**You**: "How do I handle pagination?"

**LLM should know**:
- CRUD `list()` method returns `(items, total_count, has_more)`
- Use `limit` and `offset` in filters
- Return proper OCPI response with pagination metadata

## Getting Help

If an LLM is struggling:
1. Point it to `examples/` directory
2. Share the `.cursorrules` file content
3. Reference specific documentation pages
4. Show the actual error message
5. Provide context about your use case
