# AI Code Trust Validator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/rudra496/ai-code-trust-validator.svg?style=social)](https://github.com/rudra496/ai-code-trust-validator/stargazers)

**Trust your AI-generated code before shipping to production.**

## The Problem

84% of developers use AI coding tools. Only 29% trust the output.

AI writes code fast, but that code often contains:
- Security vulnerabilities
- Hallucinated imports and functions
- Logic errors that look correct
- Inconsistent patterns and style
- Hidden technical debt

**You can't ship what you can't trust.**

## The Solution

AI Code Trust Validator automatically analyzes AI-generated code and scores its trustworthiness. It catches what your eyes miss and what AI won't tell you.

### Features

- 🔒 **Security Analysis** — Detects vulnerabilities, injection risks, exposed secrets
- 🎯 **Hallucination Detection** — Finds fake imports, non-existent functions, invented APIs
- 🧠 **Logic Validation** — Identifies unreachable code, infinite loops, type mismatches
- 📊 **Trust Score** — Single 0-100 score with detailed breakdown
- 📝 **Test Generation** — Auto-generates tests to validate behavior
- 🔄 **CI/CD Ready** — Drop into any pipeline, fail on low trust scores

## Quick Start

```bash
# Install
pip install ai-trust-validator

# Validate a file
aitrust validate generated_code.py

# Validate with strict mode (fail if score < 80)
aitrust validate generated_code.py --strict --min-score 80

# Validate stdin (perfect for AI tool chains)
cat generated_code.py | aitrust validate --stdin
```

## Example Output

```
🔍 Analyzing: generated_code.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 TRUST SCORE: 67/100 ⚠️

┌─────────────────────────────────────────────────────┐
│ Category              Score   Issues               │
├─────────────────────────────────────────────────────┤
│ Security              72      2 medium, 1 low      │
│ Hallucinations        45      3 critical           │
│ Logic                 85      1 minor              │
│ Best Practices        70      2 warnings           │
│ Testability           65      needs improvement    │
└─────────────────────────────────────────────────────┘

🚨 Critical Issues:
  [HALLUCINATION] Line 12: Import 'fancy_lib' does not exist
  [HALLUCINATION] Line 18: Function 'quick_sort_v2' not defined
  [SECURITY] Line 24: Potential SQL injection via string formatting

💡 Suggestions:
  - Replace 'fancy_lib' with standard library alternative
  - Define 'quick_sort_v2' or use built-in sorted()
  - Use parameterized queries instead of f-string

✅ Would you like to generate tests? [y/N]
```

## How It Works

1. **Static Analysis** — Parses code into AST, analyzes structure
2. **Hallucination Check** — Verifies imports against package indices
3. **Security Scan** — Pattern matching for common vulnerabilities
4. **Logic Flow** — Detects unreachable code, type issues, infinite patterns
5. **Scoring Engine** — Weighted algorithm produces final trust score

## Use Cases

### For Individual Developers
```bash
# Before committing AI-generated code
aitrust validate src/new_feature.py --strict
```

### For Teams
```yaml
# .github/workflows/trust-check.yml
name: AI Code Trust Check
on: [pull_request]
jobs:
  trust-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ai-trust-validator
      - run: aitrust validate src/ --min-score 75 --fail-low
```

### For AI Tool Builders
```python
from ai_trust_validator import Validator

validator = Validator()
result = validator.validate(ai_generated_code)

if result.trust_score < 70:
    print(f"⚠️ Low trust score: {result.trust_score}")
    print(f"Issues: {result.critical_issues}")
    # Re-prompt AI to fix issues
```

## Installation

### From PyPI
```bash
pip install ai-trust-validator
```

### From Source
```bash
git clone https://github.com/rudra496/ai-code-trust-validator.git
cd ai-code-trust-validator
pip install -e .
```

## Configuration

Create `.aitrust.yaml` in your project root:

```yaml
min_score: 75
strict_mode: true

checks:
  security:
    enabled: true
    weight: 2.0
  hallucinations:
    enabled: true
    weight: 2.5
  logic:
    enabled: true
    weight: 1.0
  best_practices:
    enabled: true
    weight: 0.5

ignore:
  - "tests/*"
  - "migrations/*"
```

## Roadmap

- [x] Core validation engine
- [x] Hallucination detection
- [x] Security scanning
- [ ] JavaScript/TypeScript support
- [ ] AI-powered auto-fix suggestions
- [ ] IDE extensions (VS Code, JetBrains)
- [ ] Self-hosted web dashboard
- [ ] Team analytics and trends

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — use it freely, just don't blame us if AI breaks production.

---

**Built because 84% of us use AI, but only 29% trust it.**

Let's close that gap. 🚀
