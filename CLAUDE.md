# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A FastAPI-based Python library implementing the [OCPI protocol](https://evroaming.org/ocpi-background/) (Open Charge Point Interface) for EV charging networks. Users integrate it by implementing abstract base classes and calling `get_application()`.

## Commands

All commands use `uv`:

```bash
uv sync --all-extras          # Install all dependencies including dev/docs
uv run pytest                 # Run all tests
uv run pytest tests/path/to/test_file.py::TestClass::test_method  # Run single test
uv run pytest --cov=ocpi      # Run tests with coverage
uv run ruff check .           # Lint
uv run ruff format .          # Format
uv run ruff format --check .  # Check formatting without modifying
uv run mypy ocpi              # Type check
uv run mkdocs serve           # Local docs server (requires: uv sync --extra docs)
uv run pre-commit install     # Install pre-commit hooks
```

## Architecture

### Entry Point

`get_application()` in `ocpi/main.py` (re-exported from `ocpi/__init__.py`) is the sole public API for creating a FastAPI instance. It wires together routers, middleware, and dependency injection based on the provided versions, roles, CRUD implementation, and authenticator.

### What Users Must Implement

Two abstract base classes define the integration contract:

1. **`ocpi/core/crud.py` — `Crud`**: Six async methods (`list`, `get`, `create`, `update`, `delete`, `do`). Each receives `module`, `role`, `version` as kwargs so one implementation handles all OCPI modules/versions/roles.

2. **`ocpi/core/authentication/authenticator.py` — `Authenticator`**: Must implement `get_valid_token_c()` (Token C for CPO authentication) and `get_valid_token_a()` (Token A for EMSP credentials exchange). The base class provides `authenticate()` and `authenticate_credentials()` using these.

Optional: subclass `ocpi/core/adapter.py` — `Adapter` to transform your data models into OCPI schemas.

### Module Organization

`ocpi/modules/` contains 12 OCPI modules (locations, sessions, cdrs, tokens, tariffs, commands, credentials, versions, chargingprofiles, hubclientinfo, payments, bookings). Each module folder typically has:
- `v_X_X_X/` subfolders for version-specific schemas and routers
- CPO and EMSP router variants

`ocpi/core/routers/` aggregates module routers by version (v_2_1_1, v_2_2_1, v_2_3_0).

### Configuration

`ocpi/core/config.py` uses Pydantic Settings. Key env vars:
- `ENVIRONMENT`: production/development/testing
- `NO_AUTH`: disable all authentication
- `VERSIONS_REQUIRE_AUTH`: whether version/details endpoints require auth (default `True`)
- `OCPI_HOST`, `OCPI_PREFIX`, `PROTOCOL`: URL construction
- `COUNTRY_CODE`, `PARTY_ID`: OCPI party identifiers

### Authentication Flow

`ocpi/core/authentication/verifier.py` handles token verification. Supports both plain tokens and base64-encoded `Token <value>` format. Used via FastAPI dependency injection in `ocpi/core/dependencies.py`.

### Response Format

All endpoints return `OCPIResponse` (defined in `ocpi/core/schemas.py`) wrapping data with OCPI status codes from `ocpi/core/status.py`.

## Testing Conventions

Tests are organized by OCPI version and role:
- `tests/test_modules/test_v_2_1_1/`, `test_v_2_2_1/`, `test_v_2_3_0/`
- Within each: per-module directories with `test_cpo.py` and `test_emsp.py`
- Shared mock implementations: `tests/test_modules/utils.py` (`MockCrud`, `ClientAuthenticator`)
- Each test folder has a `conftest.py` setting up the test FastAPI app via `get_application()`

When adding a new module or endpoint, follow the pattern of existing module tests.

## Supported OCPI Versions

2.3.0, 2.2.1, 2.1.1

Roles: CPO, EMSP, HUB, NAP, NSP, SCSP, PTP (defined in `ocpi/core/enums.py` as `RoleEnum`).
