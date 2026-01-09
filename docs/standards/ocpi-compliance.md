# OCPI Compliance Standards

This document outlines how OCPI Python ensures compliance with the OCPI protocol specifications.

## OCPI Specification References

The official OCPI specifications are stored in `docs/standards/`:

- **OCPI 2.3.0**: `OCPI-2.3.0.pdf`
- **OCPI 2.2.1**: `OCPI-2.2.1-d2.pdf`
- **OCPI 2.1.1**: Available in [OCPI repository](https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes)
- **NAP-EU Data Fields**: `NAP-EU-2023_1804-data-fields-OCPI-2.3.0.pdf`

## Version Support

### Supported Versions

- **2.3.0** - Full support including Payments module
- **2.2.1** - Full support
- **2.1.1** - Full support

### Version-Specific Behavior

#### Authentication

- **OCPI 2.1.1**: Tokens are **not** Base64-encoded
- **OCPI 2.2.1**: Tokens **must** be Base64-encoded
- **OCPI 2.3.0**: Tokens **must** be Base64-encoded

Implementation:
```python
from ocpi.core.utils import get_auth_token, decode_string_base64

if version.startswith("2.1") or version.startswith("2.0"):
    return token  # Raw token
else:
    return decode_string_base64(token)  # Base64 decoded
```

#### Module Availability

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

## Schema Compliance

### Pydantic Models

All OCPI schemas are implemented as Pydantic v2 models:

- Located in `ocpi/modules/{module}/{version}/schemas.py`
- Follow OCPI specification exactly
- Use appropriate data types from `ocpi.core.data_types`

### Required Fields

- All required fields must be present
- Optional fields use `| None` type hints
- Default values for optional fields when appropriate

### Data Types

Use OCPI-specific data types:

- `CiString(max_length)` - Case-insensitive string
- `String(max_length)` - Regular string
- `DateTime` - ISO 8601 datetime (always UTC with 'Z')
- `URL` - Valid URL string
- `Number` - Numeric value
- `Price` - Price object with excl_vat/incl_vat

## Endpoint Compliance

### URL Structure

OCPI endpoints follow this structure:

```
/{ocpi_prefix}/{role}/{version}/{module}/{object_id}
```

Example:
```
/ocpi/cpo/2.3.0/locations/LOC001
```

### HTTP Methods

- **GET**: Retrieve resources (list or single)
- **POST**: Create new resources
- **PUT**: Create or update resources
- **PATCH**: Partial update
- **DELETE**: Remove resources

### Response Format

All endpoints return OCPI response format:

```python
{
    "status_code": 1000,  # 1000 = success
    "status_message": "Success",
    "data": {...}  # Actual response data
}
```

Status codes:
- `1000` - Success
- `2000-2999` - Client errors
- `3000-3999` - Server errors

## Role Compliance

### CPO (Charge Point Operator)

- Manages charging locations
- Provides charging sessions
- Generates CDRs
- Sends commands to charge points

### EMSP (eMobility Service Provider)

- Consumes location data
- Manages user sessions
- Receives CDRs
- Sends commands to CPO

### PTP (Payment Terminal Provider)

- OCPI 2.3.0 only
- Manages payment terminals
- Handles payment transactions

## Testing for Compliance

### Specification Testing

- Test against official OCPI examples
- Verify all required fields
- Check optional field handling
- Validate data types

### Version-Specific Tests

Each OCPI version has dedicated tests:

```
tests/test_modules/
├── test_v_2_1_1/
├── test_v_2_2_1/
└── test_v_2_3_0/
```

### Compliance Checklist

When implementing new features:

- [ ] OCPI specification reviewed
- [ ] Schema matches specification exactly
- [ ] Endpoints follow OCPI URL structure
- [ ] Response format is correct
- [ ] Authentication handled correctly for version
- [ ] Tests verify OCPI compliance
- [ ] Documentation references OCPI spec

## Breaking Changes

### OCPI Version Updates

When OCPI releases a new version:

1. Review specification changes
2. Update schemas accordingly
3. Maintain backward compatibility when possible
4. Document breaking changes in CHANGELOG.md
5. Update version support matrix

### Protocol Changes

If OCPI protocol changes:

- Document the change
- Update affected modules
- Add migration guide if needed
- Update tests

## Reference Implementation

This library aims to be a **reference implementation** of OCPI:

- Follows specifications exactly
- Well-tested
- Well-documented
- Production-ready

## Reporting Compliance Issues

If you find a compliance issue:

1. Open an issue with label `bug`
2. Reference the OCPI specification section
3. Provide example of non-compliance
4. Suggest fix if possible

## Resources

- **OCPI Official Repository**: https://github.com/ocpi/ocpi
- **OCPI 2.3.0**: https://github.com/ocpi/ocpi/tree/release-2.3.0-bugfixes
- **OCPI 2.2.1**: https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes
- **OCPI 2.1.1**: https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes
- **NAP-EU Specifications**: Stored in `docs/standards/`
