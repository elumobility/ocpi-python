# Extrawest OCPI (ELU Mobility Fork)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-blue.svg)](https://docs.pydantic.dev/)
[![FastAPI 0.115+](https://img.shields.io/badge/fastapi-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **This is a fork of [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi)** maintained by [ELU Mobility](https://github.com/elumobility) with Pydantic v2 and modern FastAPI support.

---

Python implementation of Open Charge Point Interface (OCPI) protocol based on FastAPI.

**Supported OCPI versions:** 2.2.1, 2.1.1

**OCPI Documentation:** [2.2.1](https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes), [2.1.1](https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes)

---

## Fork Changes

This fork adds the following improvements over the upstream repository:

### Pydantic v2 Support (Breaking Change)

- **Removed Pydantic v1 support** - Now requires pydantic>=2.0.0
- Updated all custom validators to use Pydantic v2 syntax
- Uses pydantic-settings for configuration management
- Compatible with FastAPI 0.115+ (which dropped Pydantic v1 support)

### Modern Dependencies

| Package | Version |
|---------|---------|
| Python | >=3.11 |
| Pydantic | >=2.0.0, <3.0.0 |
| pydantic-settings | >=2.0.0 |
| FastAPI | >=0.115.0, <1.0.0 |
| httpx | >=0.27.0 |

### Bug Fixes

- Allow extra environment variables without validation errors

---

## Installation

### From GitHub (recommended for this fork)

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

### From PyPI (original upstream)

```bash
# Note: PyPI version may not have Pydantic v2 support
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

# Run with uvicorn
# uvicorn main:app --reload
```

For detailed documentation, see the [upstream docs](https://extrawest-ocpi.readthedocs.io/en/latest/).

---

## Syncing with Upstream

This fork is kept in sync with the upstream repository. To pull latest changes:

```bash
# Add upstream remote (one time)
git remote add upstream https://github.com/extrawest/extrawest_ocpi.git

# Fetch upstream changes
git fetch upstream

# Merge upstream main into fork main
git checkout main
git merge upstream/main

# Resolve any conflicts, then push
git push origin main
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2026.1.8 | 2026-01-08 | Pydantic v2 only, FastAPI 0.115+, removed v1 compat |
| 2025.7.17 | 2025-07-17 | Added Pydantic v1/v2 compatibility layer |
| 2025.7.16 | - | Last upstream version before fork |

---

## Contributing

### To this fork

Please open issues or PRs at [elumobility/extrawest_ocpi](https://github.com/elumobility/extrawest_ocpi).

### To upstream

For changes that benefit the wider community, please contribute to [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi).

---

## License

This project is licensed under the terms of the [MIT](LICENSE) license.

---

## Credits

- **Original Project:** [extrawest/extrawest_ocpi](https://github.com/extrawest/extrawest_ocpi) by [Extrawest](https://www.extrawest.com/)
- **Fork Maintainer:** [ELU Mobility](https://github.com/elumobility)
- **Inspiration:** [PY_OCPI](https://github.com/TECHS-Technological-Solutions/ocpi)
