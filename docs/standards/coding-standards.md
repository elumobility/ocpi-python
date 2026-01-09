# Coding Standards

This document defines the coding standards and conventions for OCPI Python.

## Python Version

- **Minimum Python version**: 3.11
- **Supported versions**: 3.11, 3.12
- Use modern Python features (type hints, dataclasses, etc.)

## Code Style

### Formatter: Ruff

We use [Ruff](https://github.com/astral-sh/ruff) for both linting and formatting.

```bash
# Format code
ruff format .

# Check formatting
ruff format --check .

# Lint code
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Type Hints

- **Always use type hints** for function parameters and return types
- Use `from __future__ import annotations` for postponed evaluation when needed
- Prefer `X | Y` over `Union[X, Y]` (Python 3.10+)
- Use `typing.Any` sparingly, prefer specific types

**Good:**
```python
from typing import Optional

async def get_location(
    location_id: str,
    version: VersionNumber,
) -> Optional[Location]:
    ...
```

**Bad:**
```python
async def get_location(location_id, version):
    ...
```

### Import Organization

1. Standard library imports
2. Third-party imports
3. Local application imports

Use absolute imports:
```python
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.locations.v_2_3_0.schemas import Location
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `Authenticator`, `BaseAdapter`)
- **Functions/Methods**: `snake_case` (e.g., `get_application`, `authenticate`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Private**: Prefix with `_` (e.g., `_internal_method`)
- **Module names**: `snake_case` (e.g., `data_types.py`, `authenticator.py`)

### Docstrings

Use Google-style docstrings:

```python
def get_application(
    version_numbers: list[VersionNumber],
    roles: list[RoleEnum],
    modules: list[ModuleID],
) -> FastAPI:
    """Create an OCPI FastAPI application.

    Args:
        version_numbers: List of OCPI versions to support.
        roles: List of OCPI roles (CPO, EMSP, PTP).
        modules: List of OCPI modules to enable.

    Returns:
        Configured FastAPI application instance.

    Raises:
        ValueError: If unsupported version is provided.

    Example:
        ```python
        app = get_application(
            version_numbers=[VersionNumber.v_2_3_0],
            roles=[RoleEnum.cpo],
            modules=[ModuleID.locations],
        )
        ```
    """
    ...
```

### Async/Await

- All I/O operations must be `async`
- All CRUD methods must be `async`
- Use `await` for all async calls
- Use `asyncio.gather()` for concurrent operations when appropriate

```python
# Good
async def get_locations(filters: dict) -> list[Location]:
    data = await crud.list(ModuleID.locations, RoleEnum.cpo, filters)
    return data

# Bad
def get_locations(filters: dict) -> list[Location]:
    data = crud.list(ModuleID.locations, RoleEnum.cpo, filters)  # Missing await
    return data
```

### Error Handling

- Use custom exceptions from `ocpi.core.exceptions`
- Provide meaningful error messages
- Log errors with appropriate severity

```python
from ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError

if token not in valid_tokens:
    logger.debug(f"Invalid token: {token}")
    raise AuthorizationOCPIError

if not location:
    raise NotFoundOCPIError
```

### Pydantic V2

- Use `.model_dump()` instead of `.dict()`
- Use `.model_validate()` instead of `.parse_obj()`
- Use `Field()` for field configuration
- Use `field_validator` for custom validation

```python
from pydantic import BaseModel, Field, field_validator

class Location(BaseModel):
    id: str = Field(..., max_length=36)
    name: str
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
```

## File Organization

### Module Structure

```
ocpi/
├── core/              # Core functionality
│   ├── authentication/
│   ├── endpoints/
│   └── routers/
├── modules/           # OCPI modules
│   ├── locations/
│   │   ├── v_2_1_1/
│   │   ├── v_2_2_1/
│   │   └── v_2_3_0/
│   └── ...
└── routers/          # Version-specific routers
```

### File Naming

- Use `snake_case` for all Python files
- Group related functionality in modules
- Keep files focused (single responsibility)

## Testing Standards

### Test File Naming

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Test Organization

```
tests/
├── test_core/        # Core module tests
├── test_modules/     # Module tests
│   ├── test_v_2_1_1/
│   ├── test_v_2_2_1/
│   └── test_v_2_3_0/
└── test_examples/    # Example application tests
```

### Test Requirements

- All tests must be async when testing async code
- Use `pytest.mark.asyncio` for async tests
- Mock external dependencies
- Aim for 90%+ coverage for core modules
- Test both success and error paths

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_get_location_success():
    mock_crud = AsyncMock()
    mock_crud.get.return_value = {"id": "loc-123"}
    
    result = await get_location("loc-123", mock_crud)
    assert result is not None
```

## Commit Message Standards

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature (bumps minor version)
- `fix:` - Bug fix (bumps patch version)
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks
- `BREAKING CHANGE:` or `!:` - Breaking changes (bumps minor version)

Examples:
```bash
feat: add new payment endpoint
fix: resolve token validation issue
docs: update installation guide
feat!: remove deprecated API endpoint
```

## Pre-commit Hooks

We use pre-commit hooks to enforce standards:

- **Ruff**: Linting and formatting
- **MyPy**: Type checking
- **General file checks**: Trailing whitespace, end of file, etc.

Install hooks:
```bash
uv run pre-commit install
```

## Code Review Guidelines

### What to Review

1. **Functionality**: Does it work as intended?
2. **Code quality**: Is it readable and maintainable?
3. **Tests**: Are there adequate tests?
4. **Documentation**: Is it documented?
5. **OCPI compliance**: Does it follow OCPI specifications?
6. **Version compatibility**: Works for all supported versions?

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Type hints are present
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] OCPI specification compliance verified
