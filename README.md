# Extrawest OCPI (Pydantic v2 Fork)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-blue.svg)](https://docs.pydantic.dev/)
[![FastAPI 0.115+](https://img.shields.io/badge/fastapi-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Community fork of [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi)** with Pydantic v2 and modern FastAPI support.

---

Python implementation of Open Charge Point Interface (OCPI) protocol based on FastAPI.

**Supported OCPI versions:** 2.2.1, 2.1.1

**OCPI Documentation:** [2.2.1](https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes), [2.1.1](https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes)

---

## Why This Fork?

The upstream `extrawest_ocpi` library uses Pydantic v1. Since **FastAPI 0.112+** dropped Pydantic v1 support, this fork provides:

- Full **Pydantic v2** compatibility
- Support for **FastAPI 0.115+** (latest versions)
- Modern Python 3.11+ features

---

## Fork Changes

### Breaking Changes (from upstream)

- **Removed Pydantic v1 support** - Now requires `pydantic>=2.0.0`
- Minimum FastAPI version is 0.115.0

### Dependencies

| Package | Version |
|---------|---------|
| Python | >=3.11 |
| Pydantic | >=2.0.0, <3.0.0 |
| pydantic-settings | >=2.0.0 |
| FastAPI | >=0.115.0, <1.0.0 |
| httpx | >=0.27.0 |

### Technical Changes

- Custom validators use `__get_pydantic_core_schema__` (Pydantic v2 style)
- Settings use `pydantic-settings` with `SettingsConfigDict`
- Extra environment variables are ignored (`extra="ignore"`)

---

## Installation

### From This Fork (recommended)

```bash
# Using pip
pip install git+https://github.com/elumobility/extrawest_ocpi.git

# Using Poetry
poetry add git+https://github.com/elumobility/extrawest_ocpi.git
```

### In pyproject.toml (Poetry)

```toml
[tool.poetry.dependencies]
extrawest-ocpi = { git = "https://github.com/elumobility/extrawest_ocpi.git", branch = "main" }
```

### From PyPI (upstream - Pydantic v1)

```bash
# Note: PyPI version uses Pydantic v1
pip install extrawest-ocpi
```

---

## Quick Start

```python
from py_ocpi import get_application
from py_ocpi.core.enums import RoleEnum
from py_ocpi.modules.versions.enums import VersionNumber

# Create OCPI application
app = get_application(
    version_numbers=[VersionNumber.v_2_2_1],
    roles=[RoleEnum.cpo],
)

# Run with: uvicorn main:app --reload
```

For detailed documentation, see [upstream docs](https://extrawest-ocpi.readthedocs.io/en/latest/).

---

## Syncing with Upstream

```bash
# Add upstream remote (one time)
git remote add upstream https://github.com/extrawest/extrawest_ocpi.git

# Fetch and merge upstream changes
git fetch upstream
git checkout main
git merge upstream/main

# Resolve conflicts and push
git push origin main
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2026.1.8 | 2026-01-08 | Pydantic v2 only, FastAPI 0.115+ |
| 2025.7.16 | - | Last upstream version before fork |

See [CHANGELOG.md](CHANGELOG.md) for details.

---

## Contributing

- **Fork issues/PRs**: [This repository](https://github.com/elumobility/extrawest_ocpi/issues)
- **Upstream improvements**: [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi)

---

## License

[MIT License](LICENSE) - Same as upstream.

---

## Credits

- **Original**: [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi) by [Extrawest](https://www.extrawest.com/)
- **Inspiration**: [PY_OCPI](https://github.com/TECHS-Technological-Solutions/ocpi)
