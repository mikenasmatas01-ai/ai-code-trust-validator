# Security Policy for AI Code Trust Validator

## 🔒 Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**DO NOT** open a public issue for security vulnerabilities.

Instead, please:

1. **Email:** Send details to rudrasarker130@gmail.com with subject "Security Vulnerability Report"
2. **GitHub Security Advisory:** Use [GitHub's private vulnerability reporting](https://github.com/rudra496/ai-code-trust-validator/security/advisories/new)
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

| Timeframe | Action |
|-----------|--------|
| 24-48 hours | Initial response |
| 3-7 days | Vulnerability assessment |
| 7-14 days | Fix development and testing |
| 14-30 days | Coordinated disclosure |

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 0.4.x   | ✅ Active development |
| < 0.4   | ❌ Not supported |

## Security Features

AI Code Trust Validator helps identify:

- ✅ SQL injection vulnerabilities
- ✅ Command injection risks
- ✅ Hardcoded secrets and credentials
- ✅ XSS vulnerabilities
- ✅ Insecure dependencies
- ✅ AI code hallucinations

## Security Best Practices

When using this tool:

1. **Review all findings** before applying fixes
2. **Run in CI/CD pipelines** to catch issues early
3. **Keep updated** to the latest version
4. **Configure API keys securely** (use environment variables)
5. **Don't commit** `.env` files with real credentials

## Contact

**Security:** rudrasarker130@gmail.com
**GitHub:** [@rudra496](https://github.com/rudra496)

---

Thanks for keeping things secure! 🔒
