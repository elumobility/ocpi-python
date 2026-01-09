#!/usr/bin/env python3
"""Automatic version bumping script for CalVer (YYYY.M.PATCH).

This script bumps the version based on commit messages following Conventional Commits:
- feat: bumps M (minor)
- fix: bumps PATCH
- BREAKING CHANGE: bumps M (minor) and resets PATCH
- Any other: bumps PATCH

Version format: YYYY.M.PATCH (e.g., 2026.1.9)
"""

import re
import sys
from datetime import datetime
from pathlib import Path


def get_current_version() -> str:
    """Get current version from ocpi/__init__.py."""
    init_file = Path("ocpi/__init__.py")
    if not init_file.exists():
        raise FileNotFoundError("ocpi/__init__.py not found")
    
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find __version__ in ocpi/__init__.py")
    
    return match.group(1)


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse CalVer version string into (year, month, patch)."""
    match = re.match(r"(\d{4})\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}. Expected YYYY.M.PATCH")
    
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def format_version(year: int, month: int, patch: int) -> str:
    """Format version components into CalVer string."""
    return f"{year}.{month}.{patch}"


def bump_version(current_version: str, bump_type: str) -> str:
    """Bump version based on type.
    
    Args:
        current_version: Current version string (e.g., "2026.1.9")
        bump_type: One of "major", "minor", "patch", or "auto"
    
    Returns:
        New version string
    """
    year, month, patch = parse_version(current_version)
    current_year = datetime.now().year
    
    if bump_type == "major" or bump_type == "minor":
        # For CalVer, "minor" means bumping M
        # If year changed, reset to 1.0
        if year < current_year:
            return format_version(current_year, 1, 0)
        return format_version(year, month + 1, 0)
    elif bump_type == "patch":
        return format_version(year, month, patch + 1)
    elif bump_type == "auto":
        # Auto-detect from git commits (will be handled by GitHub Actions)
        # Default to patch bump
        return format_version(year, month, patch + 1)
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")


def update_version_file(new_version: str) -> None:
    """Update version in ocpi/__init__.py."""
    init_file = Path("ocpi/__init__.py")
    content = init_file.read_text()
    
    # Replace version
    new_content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    
    init_file.write_text(new_content)
    print(f"✅ Updated ocpi/__init__.py to version {new_version}")


def update_pyproject_version(new_version: str) -> None:
    """Update version in pyproject.toml if using hatch.version.path."""
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        return
    
    content = pyproject_file.read_text()
    
    # Check if using hatch.version.path
    if '[tool.hatch.version]' in content and 'path' in content:
        # Version is read from file, so we don't need to update pyproject.toml
        return
    
    print(f"ℹ️  pyproject.toml uses dynamic version from ocpi/__init__.py")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: bump_version.py <bump_type>")
        print("  bump_type: major, minor, patch, or auto")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    
    try:
        current_version = get_current_version()
        print(f"Current version: {current_version}")
        
        new_version = bump_version(current_version, bump_type)
        print(f"New version: {new_version}")
        
        if new_version == current_version:
            print("⚠️  Version unchanged")
            sys.exit(0)
        
        update_version_file(new_version)
        update_pyproject_version(new_version)
        
        print(f"\n✅ Version bumped from {current_version} to {new_version}")
        print(f"\nNext steps:")
        print(f"  1. Review the changes")
        print(f"  2. Commit: git add ocpi/__init__.py && git commit -m 'chore: bump version to {new_version}'")
        print(f"  3. Tag: git tag v{new_version}")
        print(f"  4. Push: git push && git push --tags")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
