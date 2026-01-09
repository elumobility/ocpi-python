# Installation

## Install library

OCPI Python is available from GitHub. To install it, run:

```bash
uv pip install git+https://github.com/elumobility/ocpi-python.git
```

Or using Poetry:

```bash
poetry add git+https://github.com/elumobility/ocpi-python.git
```

In pyproject.toml (Poetry):

```toml
[tool.poetry.dependencies]
ocpi-python = { git = "https://github.com/elumobility/ocpi-python.git", branch = "main" }
```

## Install supported ASGI-server

Make sure to install any ASGI-server supported by FastAPI. Let's install `uvicorn` as an example:

```bash
uv pip install uvicorn
```

## Requirements

| Package | Version |
|---------|---------|
| Python | >=3.11 |
| Pydantic | >=2.0.0, <3.0.0 |
| pydantic-settings | >=2.0.0 |
| FastAPI | >=0.115.0, <1.0.0 |
| httpx | >=0.27.0 |

## Next steps

That's it! Once installed, you are ready to create your first OCPI application.
See [Quick Start](quickstart.md) for more.
