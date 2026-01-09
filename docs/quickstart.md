# Quick Start Guide

Get up and running with OCPI Python in minutes! This guide will walk you through creating your first OCPI application.

## Installation

First, install OCPI Python:

```bash
uv pip install ocpi-python
```

Or if installing from source:

```bash
uv pip install git+https://github.com/elumobility/ocpi-python.git
```

## Your First OCPI Application

Let's create a simple CPO (Charge Point Operator) application that manages charging locations.

### Step 1: Project Setup

Create a new directory for your project:

```bash
mkdir my-ocpi-app
cd my-ocpi-app
```

### Step 2: Create the Application Files

Create the following files:

**`main.py`** - Your main application file:

```python
from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

# Import your custom classes (we'll create these next)
from auth import SimpleAuthenticator
from crud import SimpleCrud

# Create the OCPI application
app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.locations],
    authenticator=SimpleAuthenticator,
    crud=SimpleCrud,
)
```

**`auth.py`** - Authentication logic:

```python
from typing import List
from ocpi.core.authentication.authenticator import Authenticator


class SimpleAuthenticator(Authenticator):
    """Simple authenticator that validates tokens against a list."""
    
    # In production, fetch these from your database or configuration
    VALID_TOKENS = {
        "token_c": ["my-cpo-token-123"],
        "token_a": ["my-emsp-token-456"],
    }

    @classmethod
    async def get_valid_token_c(cls) -> List[str]:
        """Return list of valid CPO tokens."""
        return cls.VALID_TOKENS["token_c"]

    @classmethod
    async def get_valid_token_a(cls) -> List[str]:
        """Return list of valid EMSP tokens."""
        return cls.VALID_TOKENS["token_a"]
```

**`crud.py`** - Business logic and data operations:

```python
from typing import Any
from ocpi.core.crud import Crud
from ocpi.core.enums import ModuleID, RoleEnum


# Simple in-memory storage (use a database in production!)
storage = {}


class SimpleCrud(Crud):
    """Simple CRUD implementation using in-memory storage."""
    
    @classmethod
    async def get(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> dict | None:
        """Get a single object by ID."""
        key = f"{module.value}:{id}"
        return storage.get(key)

    @classmethod
    async def list(
        cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
    ) -> tuple[list[dict], int, bool]:
        """Get a paginated list of objects."""
        # Simple implementation - return all items
        items = [v for k, v in storage.items() if k.startswith(f"{module.value}:")]
        total = len(items)
        is_last_page = True
        return items, total, is_last_page

    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> dict:
        """Create a new object."""
        location_id = data.get("id")
        key = f"{module.value}:{location_id}"
        storage[key] = data
        return data

    @classmethod
    async def update(
        cls, module: ModuleID, role: RoleEnum, data: dict, id: str, *args, **kwargs
    ) -> dict:
        """Update an existing object."""
        key = f"{module.value}:{id}"
        if key in storage:
            storage[key].update(data)
            return storage[key]
        return data

    @classmethod
    async def delete(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> None:
        """Delete an object."""
        key = f"{module.value}:{id}"
        storage.pop(key, None)

    @classmethod
    async def do(
        cls,
        module: ModuleID,
        role: RoleEnum | None,
        action: Any,
        *args,
        data: dict | None = None,
        **kwargs,
    ) -> Any:
        """Handle non-CRUD actions."""
        # Implement action-specific logic here
        return {}
```

### Step 3: Run the Application

Install uvicorn if you haven't already:

```bash
uv pip install uvicorn
```

Run your application:

```bash
uvicorn main:app --reload
```

Your OCPI API is now running at `http://127.0.0.1:8000`!

### Step 4: Test Your API

#### Check Available Versions

```bash
curl http://127.0.0.1:8000/ocpi/versions
```

#### View API Documentation

Open your browser and visit:
- Swagger UI: `http://127.0.0.1:8000/ocpi/docs`
- ReDoc: `http://127.0.0.1:8000/ocpi/redoc`

#### Create a Location

```bash
curl -X PUT 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/DE/ABC/LOC001' \
  -H 'Authorization: Token my-cpo-token-123' \
  -H 'Content-Type: application/json' \
  -d '{
    "country_code": "DE",
    "party_id": "ABC",
    "id": "LOC001",
    "publish": true,
    "name": "Berlin Central Charging Station",
    "address": "Unter den Linden 1",
    "city": "Berlin",
    "postal_code": "10117",
    "country": "DEU",
    "coordinates": {
      "latitude": "52.5200",
      "longitude": "13.4050"
    },
    "evses": [],
    "last_updated": "2024-01-01T00:00:00Z"
  }'
```

#### Get All Locations

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/' \
  -H 'Authorization: Token my-cpo-token-123'
```

#### Get a Specific Location

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/DE/ABC/LOC001' \
  -H 'Authorization: Token my-cpo-token-123'
```

## Next Steps

Now that you have a basic OCPI application running, you can:

1. **Explore Complete Examples** - Check out our [complete working examples](../examples/):
   - [Basic CPO](../examples/basic_cpo/) - Simple location management
   - [EMSP Sessions](../examples/emsp_sessions/) - Session and token management
   - [Full CPO](../examples/full_cpo/) - Multi-module CPO application
   - [Charging Profiles](../examples/charging_profiles/) - Smart charging control
2. **Add More Modules** - Extend your application with Sessions, CDRs, Tokens, and more
3. **Use a Real Database** - Replace the in-memory storage with MongoDB, PostgreSQL, or your preferred database
4. **Implement Push Notifications** - Enable real-time updates between CPO and EMSP
5. **Add Multiple Roles** - Support both CPO and EMSP roles in the same application

## Configuration

You can customize your OCPI application using environment variables. Create a `.env` file:

```bash
# .env
ENVIRONMENT=development
NO_AUTH=False
PROJECT_NAME=My OCPI App
OCPI_HOST=localhost:8000
OCPI_PREFIX=ocpi
COUNTRY_CODE=DE
PARTY_ID=ABC
PROTOCOL=http
```

See the [Configuration Documentation](installation.md#configuration) for all available options.

## Common Use Cases

### CPO (Charge Point Operator)
- Manage charging locations
- Track charging sessions
- Generate CDRs (Charge Detail Records)
- Handle commands from EMSPs

### EMSP (eMobility Service Provider)
- Query available locations
- Start and stop charging sessions
- Authorize tokens
- Receive CDRs

### PTP (Payment Terminal Provider) - OCPI 2.3.0+
- Manage payment terminals
- Handle financial advice confirmations

## Need Help?

- **[Complete Examples](../examples/)** - Production-ready code examples you can run immediately
  - [Basic CPO](../examples/basic_cpo/) - Location management example
  - [EMSP Sessions](../examples/emsp_sessions/) - Session management example
  - [Full CPO](../examples/full_cpo/) - Complete multi-module example
  - [Charging Profiles](../examples/charging_profiles/) - Smart charging example
- **[Tutorials](tutorials/index.md)** - Step-by-step guides for different modules
- **[API Reference](api/index.md)** - Complete endpoint documentation

## What's Next?

Ready to build something more advanced? Check out our [tutorials](tutorials/index.md) which cover:

- [Managing Locations](tutorials/locations.md) - Complete location management
- [Handling Sessions](tutorials/sessions.md) - Session lifecycle management
- [Token Authorization](tutorials/tokens.md) - Token validation and authorization
- [CDR Generation](tutorials/cdrs.md) - Creating and managing Charge Detail Records
- [Commands](tutorials/commands.md) - Sending commands to charge points
- [Charging Profiles](tutorials/charging_profiles.md) - Smart charging control
