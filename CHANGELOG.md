# Changelog

All notable changes to this fork are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) (YYYY.M.PATCH).

## [2026.1.8] - 2026-01-08

### Breaking Changes

- **Removed Pydantic v1 support** - Now requires `pydantic>=2.0.0`
- Minimum FastAPI version is now 0.115.0

### Changed

- `py_ocpi/core/compat.py` - Simplified to Pydantic v2 only
- `py_ocpi/core/config.py` - Uses `pydantic-settings` v2 with `SettingsConfigDict`
- `py_ocpi/core/data_types.py` - All custom types use `__get_pydantic_core_schema__`
- `pyproject.toml` - Updated dependencies:
  - `pydantic>=2.0.0,<3.0.0`
  - `pydantic-settings>=2.0.0`
  - `fastapi>=0.115.0,<1.0.0`
  - `httpx>=0.27.0`

### Removed

- Pydantic v1 compatibility code
- `__get_validators__` and `__modify_schema__` methods (Pydantic v1 style)

## [2025.7.16] - Upstream

Last upstream version before forking. See [upstream releases](https://github.com/extrawest/extrawest_ocpi/releases).

---

## Upstream Sync Log

| Date | Upstream Commit | Notes |
|------|-----------------|-------|
| 2025-07-17 | 5998848 | Initial fork from upstream main |

---

## Comparison with Upstream

This fork diverges from upstream in the following ways:

1. **Pydantic v2 Only** - Upstream still supports Pydantic v1
2. **Modern FastAPI** - Requires FastAPI 0.115+ (Pydantic v2 requirement)
3. **pydantic-settings** - Added as explicit dependency

To see the full diff: [Compare with upstream](https://github.com/extrawest/extrawest_ocpi/compare/main...elumobility:extrawest_ocpi:main)
