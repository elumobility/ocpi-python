# Automatic Versioning

This project uses **automatic versioning** based on [Calendar Versioning (CalVer)](https://calver.org/) with the format `YYYY.M.PATCH` (e.g., `2026.1.9`).

## How It Works

### Automatic Version Bumping

The version is automatically bumped based on commit messages following [Conventional Commits](https://www.conventionalcommits.org/):

- **`feat:`** or **`feat(scope):`** → Bumps **M** (minor version)
  - Example: `feat: add new payment endpoint` → `2026.1.9` → `2026.2.0`

- **`fix:`** or **`fix(scope):`** → Bumps **PATCH**
  - Example: `fix: resolve authentication bug` → `2026.1.9` → `2026.1.10`

- **`BREAKING CHANGE:`** or **`!:`** → Bumps **M** (minor) and resets PATCH to 0
  - Example: `feat!: remove deprecated API` → `2026.1.9` → `2026.2.0`

- **Any other commit** → Bumps **PATCH**
  - Example: `docs: update README` → `2026.1.9` → `2026.1.10`

### Workflow

1. **On push to main**: The `version-bump.yml` workflow analyzes recent commits
2. **Detects bump type**: Based on commit message patterns
3. **Creates PR**: Automatically opens a PR with the version bump
4. **After merge**: When the PR is merged, you can create a tag manually or it will be created automatically
5. **On tag push**: The `release.yml` workflow builds and publishes to PyPI

### Manual Version Bump

You can also manually trigger a version bump:

1. Go to **Actions** → **Version Bump** → **Run workflow**
2. Select bump type: `patch`, `minor`, or `major`
3. The workflow will:
   - Bump the version
   - Commit the change
   - Create a git tag
   - Push everything

### Version Format

- **YYYY**: Current year (e.g., 2026)
- **M**: Minor version (incremented for features or breaking changes)
- **PATCH**: Patch version (incremented for fixes and other changes)

If the year changes, the version resets to `YYYY.1.0`.

## Commit Message Guidelines

To ensure automatic versioning works correctly, use conventional commit messages:

```bash
# Feature (bumps minor)
git commit -m "feat: add new charging profile endpoint"
git commit -m "feat(locations): support parking types"

# Fix (bumps patch)
git commit -m "fix: resolve token validation issue"
git commit -m "fix(sessions): handle timezone correctly"

# Breaking change (bumps minor)
git commit -m "feat!: remove deprecated API endpoint"
git commit -m "feat(api)!: change response format

BREAKING CHANGE: The response format has changed from JSON to XML"

# Other (bumps patch)
git commit -m "docs: update installation guide"
git commit -m "chore: update dependencies"
git commit -m "test: add coverage for new module"
```

## Files Updated

The version is stored in:
- `ocpi/__init__.py` - `__version__` variable
- `pyproject.toml` - Uses dynamic version from `ocpi/__init__.py`

## Scripts

- `scripts/bump_version.py` - Standalone script to bump version manually
  ```bash
  python scripts/bump_version.py patch   # Bump patch version
  python scripts/bump_version.py minor   # Bump minor version
  python scripts/bump_version.py major    # Bump major version
  ```

## GitHub Actions

- `.github/workflows/version-bump.yml` - Automatic version detection and PR creation
- `.github/workflows/release.yml` - Build and publish to PyPI on tag push

## Best Practices

1. **Always use conventional commits** for automatic versioning
2. **Review version bump PRs** before merging
3. **Create tags manually** after merging version bump PRs (or automate with a workflow)
4. **Update CHANGELOG.md** manually or with a tool like `towncrier`

## Troubleshooting

### Version not bumping automatically?

- Check that commits follow conventional commit format
- Verify the workflow ran (check Actions tab)
- Check if a PR was already created (may need to close and reopen)

### Want to skip automatic versioning?

Add `[skip version]` or `[no bump]` to your commit message:
```bash
git commit -m "docs: update README [skip version]"
```

### Need to manually set a version?

Edit `ocpi/__init__.py` directly and commit:
```python
__version__ = "2026.1.10"
```
