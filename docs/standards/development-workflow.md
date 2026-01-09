# Development Workflow Standards

This document outlines the standard development workflow for contributing to OCPI Python.

## Branch Strategy

### Main Branch

- `main` - Production-ready code
- Protected branch (requires PR and approval)
- All commits must pass CI checks

### Branch Naming

Use conventional branch names:

- `feat/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions
- `chore/description` - Maintenance tasks

Examples:
- `feat/add-payment-module`
- `fix/token-validation-bug`
- `docs/update-api-reference`

## Pull Request Process

### Before Creating PR

1. **Update branch**: `git pull origin main`
2. **Run tests**: `uv run pytest`
3. **Run linting**: `uv run ruff check .`
4. **Run type checking**: `uv run mypy ocpi`
5. **Check coverage**: `uv run pytest --cov=ocpi --cov-report=term-missing`

### PR Requirements

- [ ] All CI checks passing
- [ ] Code owner approval (automatic via CODEOWNERS)
- [ ] At least 1 approval required
- [ ] No merge conflicts
- [ ] Conventional commit message
- [ ] Description explains changes

### PR Template

Use the PR template (`.github/pull_request_template.md`) which includes:

- Description of changes
- Related issues
- Testing performed
- Checklist

## Version Management

### Automatic Versioning

We use automatic versioning based on commit messages:

- `feat:` → Minor bump (M)
- `fix:` → Patch bump (PATCH)
- `BREAKING CHANGE:` → Minor bump (M)

### Manual Version Bump

If needed, use the version bump script:

```bash
python scripts/bump_version.py patch   # or minor, major
```

### Creating Releases

1. Version is automatically bumped via PR
2. Merge the version bump PR
3. Create git tag: `git tag v2026.2.0`
4. Push tag: `git push --tags`
5. Release workflow automatically publishes to PyPI

## Testing Requirements

### Coverage Goals

- **Core modules**: 90%+ coverage
- **Module APIs**: 80%+ coverage
- **Overall**: 85%+ coverage

### Test Types

1. **Unit tests**: Test individual functions/classes
2. **Integration tests**: Test module interactions
3. **Example tests**: Verify example applications work

### Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=ocpi --cov-report=term-missing

# Specific test file
uv run pytest tests/test_core/test_utils.py

# Specific test
uv run pytest tests/test_core/test_utils.py::test_get_auth_token
```

## Documentation Standards

### Documentation Types

1. **API Documentation**: Auto-generated from docstrings
2. **Tutorials**: Step-by-step guides
3. **Examples**: Complete working applications
4. **Standards**: This directory

### Documentation Updates

- Update docs when adding features
- Include code examples
- Keep examples up-to-date
- Use European countries/currencies in examples (DE, ES, CH, DK)

### Building Documentation

```bash
# Serve locally
uv run mkdocs serve

# Build static site
uv run mkdocs build
```

## Code Review Process

### Reviewer Responsibilities

1. **Functionality**: Verify the code works
2. **Standards**: Check coding standards compliance
3. **Tests**: Ensure adequate test coverage
4. **Documentation**: Verify documentation is updated
5. **OCPI Compliance**: Check OCPI specification adherence

### Author Responsibilities

1. **Self-review**: Review your own PR first
2. **Address feedback**: Respond to all comments
3. **Update PR**: Make requested changes
4. **Keep PR focused**: One feature/fix per PR

## CI/CD Pipeline

### Automated Checks

1. **Lint**: Ruff formatting and linting
2. **Type Check**: MyPy type checking
3. **Tests**: Pytest on Python 3.11 and 3.12
4. **Coverage**: Codecov coverage reporting

### Workflow Triggers

- **Push to main**: Runs all checks
- **Pull Request**: Runs all checks
- **Tag push**: Triggers release workflow
- **Version bump**: Creates PR automatically

## Release Process

### Pre-Release Checklist

- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped
- [ ] Tag created

### Release Steps

1. Version bump PR is merged
2. Create git tag: `git tag v2026.2.0`
3. Push tag: `git push --tags`
4. Release workflow:
   - Builds package
   - Verifies version
   - Publishes to PyPI

### Post-Release

- [ ] Verify package on PyPI
- [ ] Test installation: `uv pip install ocpi-python`
- [ ] Update release notes on GitHub
- [ ] Announce release (if applicable)

## Issue Management

### Issue Types

- **Bug Report**: Use `.github/ISSUE_TEMPLATE/bug_report.md`
- **Feature Request**: Use `.github/ISSUE_TEMPLATE/feature_request.md`
- **Question**: Use GitHub Discussions

### Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `question` - Further information is requested
- `good first issue` - Good for newcomers

## Communication Standards

### Code Comments

- Explain **why**, not **what**
- Use docstrings for public APIs
- Keep comments up-to-date with code

### Commit Messages

- Use conventional commit format
- Be descriptive but concise
- Reference issues when applicable

### PR Descriptions

- Explain what changed and why
- Include related issue numbers
- Add screenshots for UI changes
- List breaking changes
