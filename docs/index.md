<p align="center">
  <img src="assets/images/logo.png" alt="OCPI Python Logo" width="200">
</p>

# Welcome to OCPI Python

A modern, production-ready Python implementation of the Open Charge Point Interface (OCPI) protocol built on FastAPI.

Open Charge Point Interface (OCPI) is an open protocol used for connections between charging station operators and service providers.

**Supported OCPI versions:** 2.3.0, 2.2.1, 2.1.1

**OCPI Documentation:**
- [2.3.0](https://github.com/ocpi/ocpi/tree/release-2.3.0-bugfixes)
- [2.2.1](https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes)
- [2.1.1](https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes)

!!! note
    It's assumed that you are familiar with the OCPI (Open Charge Point Interface) protocol.
    It is recommended to refer to the official OCPI documentation for a comprehensive understanding of the protocol specifications and guidelines.

## Features

- **Full OCPI 2.3.0 support** - Including the new Payments and Bookings modules
- **OCPI 2.2.1 and 2.1.1 compatibility** - Backward compatible with previous versions
- **Modern stack** - Built with FastAPI 0.115+ and Pydantic v2
- **Complete role support** - CPO, EMSP, and PTP (Payment Terminal Provider)
- **Comprehensive modules** - Locations, Sessions, CDRs, Tokens, Tariffs, Commands, Charging Profiles, Hub Client Info, Credentials, and Payments
- **Production-ready** - Extensive test coverage (83%+), async/await support, and robust error handling
- **Type-safe** - Full Pydantic v2 validation with modern Python 3.11+ features

## Quick Start

Get started in minutes with our [Quick Start Guide](quickstart.md) or explore our [complete examples](../examples/):

```python
from ocpi import get_application
from ocpi.core.enums import RoleEnum, ModuleID
from ocpi.modules.versions.enums import VersionNumber

# Create OCPI application
app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.locations],
)

# Run with: uvicorn main:app --reload
```

### Examples

We provide complete, working examples to help you get started:

- **[Basic CPO](../examples/basic_cpo/)** - Simple location management for Charge Point Operators
- **[EMSP Sessions](../examples/emsp_sessions/)** - Session and token management for eMobility Service Providers
- **[Full CPO](../examples/full_cpo/)** - Complete multi-module CPO application
- **[Charging Profiles](../examples/charging_profiles/)** - Smart charging control example
- **[Bookings](../examples/bookings/)** - EV charging reservations (OCPI 2.3.0)

## Supported Modules

| Module | 2.3.0 | 2.2.1 | 2.1.1 |
|--------|-------|-------|-------|
| Credentials | ✅ | ✅ | ✅ |
| Locations | ✅ | ✅ | ✅ |
| Sessions | ✅ | ✅ | ✅ |
| CDRs | ✅ | ✅ | ✅ |
| Tokens | ✅ | ✅ | ✅ |
| Tariffs | ✅ | ✅ | ✅ |
| Commands | ✅ | ✅ | ✅ |
| Charging Profiles | ✅ | ✅ | ❌ |
| Hub Client Info | ✅ | ✅ | ❌ |
| Payments | ✅ | ❌ | ❌ |
| Bookings | ✅ | ❌ | ❌ |

## Documentation

- **[Quick Start Guide](quickstart.md)** - Get your first OCPI application running
- **[Tutorials](tutorials/index.md)** - Step-by-step guides for different modules
- **[API Reference](api/index.md)** - Complete endpoint documentation
- **[Examples](../examples/)** - Production-ready code examples

## Credits

This library is based on the excellent work from [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi), with significant enhancements including OCPI 2.3.0 support, Pydantic v2 migration, and comprehensive test coverage.

**Maintainer:** [ELU Mobility](https://github.com/elumobility)
