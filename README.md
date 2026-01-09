<p align="center">
  <img src="docs/assets/images/logo.png" alt="OCPI Python Logo" width="200">
</p>

<h1 align="center">OCPI Python</h1>

<p align="center">
  <a href="https://github.com/elumobility/ocpi-python/actions/workflows/ci.yml"><img src="https://github.com/elumobility/ocpi-python/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python 3.11+"></a>
  <a href="https://docs.pydantic.dev/"><img src="https://img.shields.io/badge/pydantic-v2-blue.svg" alt="Pydantic v2"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/fastapi-0.115+-green.svg" alt="FastAPI 0.115+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT%20OR%20EUPL--1.2-blue.svg" alt="License: MIT OR EUPL-1.2"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Code style: ruff"></a>
</p>

A modern, production-ready Python implementation of the Open Charge Point Interface (OCPI) protocol built on FastAPI.

**Supported OCPI versions:** 2.3.0, 2.2.1, 2.1.1

**OCPI Documentation:** [2.3.0](https://github.com/ocpi/ocpi/tree/release-2.3.0-bugfixes), [2.2.1](https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes), [2.1.1](https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes)

---

## Features

- **Full OCPI 2.3.0 support** - Including the new Payments module
- **OCPI 2.2.1 and 2.1.1 compatibility** - Backward compatible with previous versions
- **Modern stack** - Built with FastAPI 0.115+ and Pydantic v2
- **Complete role support** - CPO, EMSP, and PTP (Payment Terminal Provider)
- **Comprehensive modules** - Locations, Sessions, CDRs, Tokens, Tariffs, Commands, Charging Profiles, Hub Client Info, Credentials, and Payments
- **Production-ready** - Extensive test coverage (83%+), async/await support, and robust error handling
- **Type-safe** - Full Pydantic v2 validation with modern Python 3.11+ features

---

## Installation

### From PyPI (when published)

```bash
uv pip install ocpi-python
```

### From GitHub

```bash
uv pip install git+https://github.com/elumobility/ocpi-python.git
```

### In pyproject.toml

```toml
[project]
dependencies = [
    "ocpi-python @ git+https://github.com/elumobility/ocpi-python.git",
]
```

Then install with:
```bash
uv pip install -e .
```

---

## Quick Start

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

---

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

---

## Requirements

| Package | Version |
|---------|---------|
| Python | >=3.11 |
| Pydantic | >=2.0.0, <3.0.0 |
| pydantic-settings | >=2.0.0 |
| FastAPI | >=0.115.0, <1.0.0 |
| httpx | >=0.27.0 |

---

## Documentation

📚 **[Full Documentation](https://elumobility.github.io/ocpi-python/)** - Complete API reference, tutorials, and examples

- [Quick Start Guide](https://elumobility.github.io/ocpi-python/quickstart/)
- [Tutorials](https://elumobility.github.io/ocpi-python/tutorials/)
- [API Reference](https://elumobility.github.io/ocpi-python/api/)
- [Examples](https://github.com/elumobility/ocpi-python/tree/main/examples) - Production-ready code examples

---

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting a Pull Request.

We welcome:
- 🐛 Bug reports
- 💡 Feature requests
- 📝 Documentation improvements
- 🧪 Test coverage improvements
- 🔧 Code refactoring

See our [Issue Templates](.github/ISSUE_TEMPLATE/) for guidelines on reporting bugs or requesting features.

---

## License

This project is **dual-licensed** under:
- **[MIT License](LICENSE)** - Permissive, allows proprietary use
- **[European Union Public Licence (EUPL) v.1.2](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12)** - Copyleft, ideal for European public sector

You may use this software under either license at your choice. See [LICENSE](LICENSE) for full details.

---

## Credits

This library is based on the excellent work from [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi), with significant enhancements including OCPI 2.3.0 support, Pydantic v2 migration, and comprehensive test coverage.

**Maintainer:** [ELU Mobility](https://github.com/elumobility)
