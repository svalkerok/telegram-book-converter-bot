# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it privately.

### How to Report

1. **Do NOT create a public issue**
2. Send an email to the maintainers with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Resolution**: Varies by severity

### Security Best Practices

When deploying this bot:

1. **Environment Variables**: Never commit `.env` files or tokens
2. **Server Security**: Use firewall, regular updates, non-root user
3. **Resource Limits**: Configure memory/CPU limits in production
4. **File Validation**: Bot validates uploaded files, but monitor for abuse
5. **Logging**: Review logs regularly for suspicious activity
6. **Network**: Use HTTPS for webhooks, secure server communication

### Known Security Considerations

- File uploads are limited to 50MB
- Supported file types are restricted
- Temporary files are automatically cleaned
- Bot runs with limited privileges in Docker
- No persistent storage of user files

### Disclosure Policy

- Security fixes will be released as soon as possible
- CVE will be requested for significant vulnerabilities
- Credit will be given to reporters (unless they prefer anonymity)
