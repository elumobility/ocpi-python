# Tutorials

Comprehensive tutorials for using OCPI Python in different scenarios.

## Getting Started

- **[Quick Start Guide](../quickstart.md)** - Get your first OCPI application running in minutes

## Module Tutorials

### Core Modules

- **[Managing Locations](locations.md)** - Complete guide to location management
  - Creating locations with EVSEs and connectors
  - CRUD operations
  - Advanced features (operating hours, energy mix, images)

- **[Handling Sessions](sessions.md)** - Session lifecycle management
  - Starting and stopping sessions
  - Tracking energy consumption
  - Session status management
  - Charging preferences

- **[Token Authorization](tokens.md)** - Token validation and authorization
  - Token types (RFID, mobile app, etc.)
  - Authorization flow
  - Whitelist management

- **[CDR Generation](cdrs.md)** - Creating Charge Detail Records
  - CDR structure
  - Cost calculation
  - Tariff integration
  - Charging periods

### Advanced Modules

- **[Commands](commands.md)** - Sending commands to charge points
  - START_SESSION, STOP_SESSION
  - RESERVE_NOW, UNLOCK_CONNECTOR
  - Command handling and responses

- **[Charging Profiles](charging_profiles.md)** - Smart charging control
  - Setting charging profiles
  - Getting active profiles
  - Clearing profiles
  - Load balancing

## Complete Working Examples

Ready-to-run examples with full source code:

- **[Basic CPO](../../examples/basic_cpo/)** - Simple location management for CPO
  - Complete CRUD implementation
  - In-memory storage (easily replaceable with a database)
  
- **[EMSP Sessions](../../examples/emsp_sessions/)** - Session and token management
  - Session lifecycle management
  - Token authorization flow
  
- **[Full CPO](../../examples/full_cpo/)** - Complete multi-module CPO application
  - Multiple modules (Locations, Sessions, CDRs, Tariffs, Commands)
  - Production-ready structure
  
- **[Charging Profiles](../../examples/charging_profiles/)** - Smart charging control
  - Charging profile management
  - Load balancing examples

## Additional Resources

- **[CRUD Operations](crud.md)** - Detailed CRUD implementation guide
- **[Database Interface](db_interface.md)** - Database integration patterns
- **[Push Notifications](push.md)** - Real-time updates between parties

## Next Steps

After completing these tutorials:

1. Explore the [API Reference](../api/) for complete endpoint documentation
2. Check out [Complete Examples](../../examples/) for production-ready code
3. Review the [Installation Guide](../installation.md) for deployment options
