# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue. Instead, please report it privately to:

**Email**: dev@elu-energy.it

Please include the following information in your report:

- Type of vulnerability (e.g., XSS, SQL injection, authentication bypass)
- Full paths of source file(s) related to the vulnerability
- The location of the affected code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability, including how an attacker might exploit it

We will acknowledge receipt of your report within 48 hours and provide a more detailed response within 7 days indicating the next steps in handling your report.

## Security Update Process

1. **Report Received**: We acknowledge receipt within 48 hours
2. **Investigation**: We investigate and verify the vulnerability
3. **Fix Development**: We develop a fix in a private branch
4. **Testing**: We thoroughly test the fix
5. **Release**: We release a security update
6. **Disclosure**: We publicly disclose the vulnerability (after users have had time to update)

## Security Best Practices

When using OCPI Python in production:

- Always use the latest stable version
- Keep your dependencies up to date
- Use HTTPS for all OCPI communications
- Implement proper authentication and authorization
- Validate and sanitize all inputs
- Use environment variables for sensitive configuration
- Regularly review and rotate API tokens and credentials
- Monitor your application logs for suspicious activity

## Security Considerations

- **Authentication**: Ensure proper token validation and authorization checks
- **Data Validation**: All OCPI data should be validated using Pydantic schemas
- **Rate Limiting**: Consider implementing rate limiting for production deployments
- **Error Handling**: Avoid exposing sensitive information in error messages
- **Dependencies**: Keep all dependencies up to date to avoid known vulnerabilities

Thank you for helping keep OCPI Python and its users safe!
