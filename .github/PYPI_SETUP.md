# PyPI Publishing Setup Guide

This guide explains how to configure PyPI publishing for automatic releases.

## Prerequisites

1. **PyPI Account**: You need an account on [PyPI](https://pypi.org) (or [TestPyPI](https://test.pypi.org) for testing)
2. **Project Name**: `ocpi-python` (already configured in `pyproject.toml`)

## Step 1: Create PyPI API Token

### For Production PyPI (pypi.org)

1. Go to: https://pypi.org/manage/account/token/
2. Click **"Add API token"**
3. Configure:
   - **Token name**: `ocpi-python-github-actions` (or any descriptive name)
   - **Scope**: 
     - **Project**: Select `ocpi-python` (if project already exists)
     - OR **Entire account** (if project doesn't exist yet - you'll need to create it first)
4. Click **"Add token"**
5. **Copy the token immediately** (you won't be able to see it again!)
   - Format: `pypi-...` (starts with `pypi-`)

### For Test PyPI (test.pypi.org) - Recommended for First Test

1. Go to: https://test.pypi.org/manage/account/token/
2. Follow the same steps as above
3. Use TestPyPI token for initial testing

## Step 2: Add Token to GitHub Secrets

### Option 1: Via GitHub Web Interface (Recommended)

1. Go to: https://github.com/elumobility/ocpi-python/settings/secrets/actions
2. Click **"New repository secret"**
3. Configure:
   - **Name**: `PYPI_API_TOKEN`
   - **Secret**: Paste your PyPI API token (starts with `pypi-`)
4. Click **"Add secret"**

### Option 2: Via GitHub CLI

```bash
gh secret set PYPI_API_TOKEN --body "pypi-your-token-here"
```

## Step 3: Verify Package Name Availability

Check if `ocpi-python` is available on PyPI:

```bash
# Check if name is taken
curl -s https://pypi.org/pypi/ocpi-python/json | jq .info.name
```

If it returns an error (404), the name is available. If it returns the name, it's taken and you may need to choose a different name.

## Step 4: Test the Setup

### Test with TestPyPI First

1. Add TestPyPI token as `TEST_PYPI_API_TOKEN` secret
2. Update `.github/workflows/release.yml` to use TestPyPI for testing
3. Create a test tag: `git tag v2026.1.10-test && git push --tags`
4. Check the Actions tab to see if it publishes successfully

### Test with Production PyPI

Once TestPyPI works:

1. Ensure `PYPI_API_TOKEN` secret is set
2. Create a version tag: `git tag v2026.1.10 && git push --tags`
3. The workflow will automatically:
   - Build the package
   - Verify version matches
   - Publish to PyPI

## Step 5: Verify Publication

After the workflow completes:

1. Check PyPI: https://pypi.org/project/ocpi-python/
2. Verify installation works:
   ```bash
   uv pip install ocpi-python
   ```

## Current Configuration

The release workflow (`.github/workflows/release.yml`) is already configured to:
- ✅ Build the package using `python -m build`
- ✅ Verify version matches between tag and code
- ✅ Publish to PyPI using `pypa/gh-action-pypi-publish@release/v1`
- ✅ Use the `PYPI_API_TOKEN` secret

## Troubleshooting

### "403 Forbidden" Error

- Check that the API token has the correct scope
- Verify the token hasn't expired
- Ensure the token is for the correct PyPI instance (production vs test)

### "Package name already exists"

- The name `ocpi-python` might be taken
- Check: https://pypi.org/project/ocpi-python/
- If taken, update `pyproject.toml` with a different name

### "Version already exists"

- The version tag already exists on PyPI
- Use a new version number

## Security Best Practices

1. **Never commit tokens** to the repository
2. **Use project-scoped tokens** when possible (not account-wide)
3. **Rotate tokens periodically**
4. **Use TestPyPI first** to test the workflow
5. **Review workflow logs** after each publish

## Next Steps After Setup

1. ✅ Add `PYPI_API_TOKEN` secret
2. ✅ Test with TestPyPI (optional but recommended)
3. ✅ Create your first release tag
4. ✅ Monitor the release workflow
5. ✅ Verify package on PyPI

## Manual Publishing (Alternative)

If you prefer to publish manually:

```bash
# Build package
uv run python -m build

# Upload to PyPI (requires twine)
uv pip install twine
uv run twine upload dist/*
# Enter username: __token__
# Enter password: pypi-your-token-here
```

But the automated workflow is recommended for consistency and safety.
