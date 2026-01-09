# Contributing to OCPI Python

We welcome contributions! This document provides guidelines for contributing to the project.

## Requirements

### Python Version Manager

We recommend using `uv` for managing Python versions and dependencies. Install `uv`:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or using pip:
```bash
pip install uv
```

### Python Version

Python >= 3.11

With `uv`, you can create a project with the correct Python version:

```bash
uv python install 3.11
```

## Installation

### Clone the project

```bash
git clone https://github.com/elumobility/ocpi-python.git
```

### Go to the project directory

```bash
cd ocpi-python
```

### Install dependencies

```bash
# Install all dependencies including dev tools
uv sync --all-extras

# Or install specific extras
uv sync --extra dev --extra docs
```

This will:
- Create a virtual environment
- Install all dependencies from `pyproject.toml`
- Install development and documentation dependencies

### Activate virtual environment

With `uv`, you can run commands in the virtual environment:

```bash
uv run <command>
```

Or activate the shell:
```bash
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

### Install pre-commit

```bash
uv run pre-commit install
```

## Running Tests

To run tests, use:

```bash
uv run pytest
```

Or with coverage:

```bash
uv run pytest --cov=ocpi --cov-report=term-missing
```

## Building Documentation

To build documentation locally:

```bash
# Install docs dependencies first
uv sync --extra docs

# Build and serve documentation
uv run mkdocs serve

# Build static site
uv run mkdocs build
```

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Run tests: `uv run pytest`
4. Run linting: `uv run ruff check .`
5. Run type checking: `uv run mypy ocpi`
6. Commit your changes (pre-commit hooks will run automatically)
7. Push and create a Pull Request
