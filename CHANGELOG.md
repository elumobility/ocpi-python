# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) (YYYY.M.PATCH).

## [2026.1.9] - 2026-01-09

### Added

- **OCPI 2.3.0 support** - Full implementation including:
  - Payments module (CPO and PTP roles)
  - Enhanced Locations module with Parking support
  - Updated Sessions, CDRs, Tokens, Tariffs, and Commands modules
  - New PTP (Payment Terminal Provider) role support
- **Comprehensive test coverage** - Added 58+ new tests, reaching 83% coverage
- **Test suites for v_2_3_0 modules** - Complete test coverage for all 2.3.0 modules

### Changed

- **Package rebranding** - Renamed from `extrawest_ocpi` to `ocpi-python`
- **Repository migration** - Moved to `elumobility/ocpi-python`
- **Improved adapter calls** - All adapter methods now explicitly pass version numbers
- **Enhanced error handling** - Better validation error logging and debugging

### Fixed

- **Pydantic v2 compatibility** - Fixed all `Optional` fields to have explicit `= None` defaults
- **Deprecation warnings** - Replaced all `.dict()` calls with `.model_dump()`
- **Authentication** - Fixed token decoding for OCPI 2.3.0 (non-base64 tokens)
- **Schema validation** - Fixed multiple schema issues in 2.3.0 modules

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

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2026.1.9 | 2026-01-09 | OCPI 2.3.0 support, package rebranding, comprehensive tests |
| 2026.1.8 | 2026-01-08 | Pydantic v2 migration, FastAPI 0.115+ support |

---

## Credits

This project is based on the excellent work from [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi), with significant enhancements and modernizations.
