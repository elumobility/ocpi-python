# OCPI Python Examples

This directory contains complete, working examples demonstrating different use cases of OCPI Python.

## Available Examples

### [Basic CPO](basic_cpo/)
A simple Charge Point Operator application that manages charging locations. Perfect for getting started.

**Features:**
- Location management (CRUD operations)
- Simple in-memory storage
- Basic authentication

### [EMSP Sessions](emsp_sessions/)
An eMobility Service Provider application that manages charging sessions and token authorization.

**Features:**
- Session lifecycle management
- Token authorization
- Session tracking

### [Full CPO](full_cpo/)
A complete Charge Point Operator application with multiple modules.

**Features:**
- Locations management
- Sessions tracking
- CDR generation
- Tariff management
- Command handling

### [Charging Profiles](charging_profiles/)
Smart charging control using charging profiles (OCPI 2.2.1+).

**Features:**
- Set charging profiles
- Get active charging profiles
- Clear charging profiles
- Smart charging control

## Running Examples

Each example is self-contained and can be run independently:

```bash
cd examples/<example_name>
uvicorn main:app --reload
```

## Testing Examples

Each example includes:
- Complete working code
- README with usage instructions
- Test files to verify functionality

Run the tests:

```bash
# From the project root
pytest tests/test_examples/
```

## Production Considerations

These examples use simple in-memory storage for demonstration purposes. For production use:

1. **Replace storage** - Use a real database (PostgreSQL, MongoDB, etc.)
2. **Secure authentication** - Implement proper token management and validation
3. **Add error handling** - Implement comprehensive error handling and logging
4. **Add monitoring** - Add metrics, logging, and monitoring
5. **Configure properly** - Use environment variables for configuration
6. **Add tests** - Write comprehensive test suites

## Next Steps

After exploring these examples:

1. Check out the [Tutorials](../docs/tutorials/) for detailed guides
2. Read the [API Reference](../docs/api/) for complete endpoint documentation
3. Review the [Quick Start Guide](../docs/quickstart.md) for setup instructions
