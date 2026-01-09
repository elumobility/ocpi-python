# Project Standards

This directory contains the standards and guidelines for the OCPI Python project.

## Standards Documentation

### Development Standards

- **[Coding Standards](coding-standards.md)** - Code style, conventions, and best practices
- **[Development Workflow](development-workflow.md)** - Branch strategy, PR process, and release workflow
- **[OCPI Compliance](ocpi-compliance.md)** - OCPI protocol compliance guidelines

### OCPI Specifications

The official OCPI protocol specifications are stored here as PDFs:

- **OCPI 2.3.0**: `OCPI-2.3.0.pdf` - Latest version with Payments module
- **OCPI 2.2.1**: `OCPI-2.2.1-d2.pdf` - Previous stable version
- **OCPI 2.3.0 Booking**: `OCPI-2.3.0-booking-1.0.pdf` - Booking extension
- **NAP-EU Data Fields**: `NAP-EU-2023_1804-data-fields-OCPI-2.3.0.pdf` - European data fields

These PDFs are reference documents for OCPI protocol compliance.

## Quick Reference

### Code Style

- **Formatter**: Ruff
- **Type Checker**: MyPy
- **Python Version**: 3.11+
- **Type Hints**: Required for all functions

### Development Process

1. Create feature branch: `feat/description`
2. Make changes following coding standards
3. Write tests (aim for 90%+ coverage)
4. Run pre-commit hooks
5. Create PR with conventional commit message
6. Get code owner approval
7. Merge after CI passes

### Versioning

- **Format**: CalVer (YYYY.M.PATCH)
- **Automatic**: Based on commit messages
- **Manual**: Use `scripts/bump_version.py`

## Related Documentation

- [Contributing Guide](../../CONTRIBUTING.md) - How to contribute
- [Code of Conduct](../../CODE_OF_CONDUCT.md) - Community standards
- [API Reference](../api/index.md) - API documentation
- [Tutorials](../tutorials/index.md) - Step-by-step guides

## Standards Compliance

All code in this project must:

- ✅ Follow coding standards
- ✅ Pass all linting and type checks
- ✅ Include adequate tests
- ✅ Comply with OCPI specifications
- ✅ Be properly documented

## Questions?

If you have questions about standards:

- Open a discussion on GitHub
- Check existing documentation
- Review similar code in the repository
- Ask in PR comments
