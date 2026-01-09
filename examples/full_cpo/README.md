# Full CPO Example

A complete Charge Point Operator (CPO) application with multiple modules.

This example demonstrates:
- Multi-module CPO setup (Locations, Sessions, CDRs, Tariffs, Commands)
- Complete CRUD operations for all modules
- Command handling
- CDR generation
- Tariff management

## Running the Example

```bash
cd examples/full_cpo
uvicorn main:app --reload
```

## Testing

See individual module tests in the test files.
