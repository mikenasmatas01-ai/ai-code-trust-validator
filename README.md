<div align="center">

# 🛡️ AI Code Trust Validator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/rudra496/ai-code-trust-validator.svg?style=social)](https://github.com/rudra496/ai-code-trust-validator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/rudra496/ai-code-trust-validator.svg?style=social)](https://github.com/rudra496/ai-code-trust-validator/network/members)

**Trust your AI-generated code before shipping to production.**

*The missing quality gate for AI-assisted development*

[Installation](#installation) • [Quick Start](#quick-start) • [Features](#features) • [Examples](#examples) • [Documentation](#documentation)

</div>

---

## The Problem

**84% of developers use AI coding tools. Only 29% trust the output.**

AI writes code fast, but that code often contains:
- 🔓 **Security vulnerabilities** — SQL injection, hardcoded secrets, command injection
- 🎭 **Hallucinations** — Fake imports, invented functions, imaginary APIs
- 🐛 **Logic errors** — Unreachable code, infinite loops, type mismatches
- 📉 **Technical debt** — Missing docs, poor naming, deep nesting

**You can't ship what you can't trust.**

## The Solution

AI Code Trust Validator automatically analyzes AI-generated code and scores its trustworthiness. It catches what your eyes miss and what AI won't tell you.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔒 **Security Analysis** | Detects SQL injection, XSS, hardcoded secrets, dangerous function calls |
| 🎯 **Hallucination Detection** | Finds fake imports, non-existent packages, invented functions |
| 🧠 **Logic Validation** | Identifies unreachable code, infinite loops, dead branches |
| 📊 **Trust Score** | Single 0-100 score with weighted category breakdown |
| 📝 **Auto Test Generation** | Generates tests to validate AI code behavior |
| 🤖 **AI-Powered Fix Suggestions** | Intelligent recommendations for each issue |
| 🔄 **CI/CD Ready** | Drop into any pipeline, fail on low trust scores |
| 📦 **Multi-Language Support** | Python (v0.1), JavaScript/TypeScript (coming soon) |

## Installation

```bash
# From PyPI (recommended)
pip install ai-trust-validator

# From source
git clone https://github.com/rudra496/ai-code-trust-validator.git
cd ai-code-trust-validator
pip install -e .
```

## Quick Start

```bash
# Validate a single file
aitrust validate generated_code.py

# Validate with strict mode (fail if score < 80)
aitrust validate generated_code.py --strict --min-score 80

# Validate entire directory
aitrust validate src/

# Pipe AI output directly
cat ai_output.py | aitrust validate --stdin

# Output as JSON for CI integration
aitrust validate src/ --json
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
└─────────────────────────────────────────────────────┘

🚨 Critical Issues:
  [HALLUCINATION] Line 12: Import 'fancy_lib' does not exist
  [HALLUCINATION] Line 18: Function 'quick_sort_v2' not defined
  [SECURITY] Line 24: Potential SQL injection via f-string

💡 AI Suggestions:
  → Replace 'fancy_lib' with 'numpy' or 'pandas'
  → Use built-in sorted() instead of 'quick_sort_v2'
  → Use parameterized queries: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

✅ Run 'aitrust fix generated_code.py' for auto-fix suggestions
```

## Features Deep Dive

### 🔒 Security Analysis

Detects vulnerabilities that AI often introduces:

```python
# ❌ AI often writes this (SQL injection risk)
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# ✅ Validator catches it and suggests:
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

**Detects:**
- SQL injection patterns
- Command injection risks
- Hardcoded passwords, API keys, secrets
- Dangerous functions (`eval`, `exec`, `os.system`)
- Insecure subprocess calls (`shell=True`)
- Path traversal vulnerabilities

### 🎯 Hallucination Detection

AI frequently invents packages and functions that don't exist:

```python
# ❌ AI hallucinated this
import quick_sort_v2  # Doesn't exist!
from smart_parser import parse_all  # Made up!
result = fast_hash(data)  # Never defined

# ✅ Validator catches all of them
# Suggests real alternatives or flags as hallucination
```

### 🧠 Logic Validation

Catches logical errors AI makes:

```python
# ❌ Unreachable code
def process():
    return result
    cleanup()  # Never runs!

# ❌ Infinite loop
while True:
    do_work()  # No break condition

# ❌ Always-false condition
if False:
    important_code()  # Never executes
```

### 📝 Auto Test Generation

Generates tests to validate AI code:

```bash
aitrust generate-tests generated_code.py --output tests/
```

Creates pytest-compatible tests covering edge cases.

## CI/CD Integration

### GitHub Actions

```yaml
name: AI Code Trust Check

on: [pull_request]

jobs:
  trust-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install validator
        run: pip install ai-trust-validator
      
      - name: Validate AI-generated code
        run: aitrust validate src/ --min-score 75 --fail-low --json > trust-report.json
      
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: trust-report
          path: trust-report.json
```

### GitLab CI

```yaml
trust-check:
  stage: test
  script:
    - pip install ai-trust-validator
    - aitrust validate src/ --min-score 75
  artifacts:
    reports:
      junit: trust-report.xml
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ai-trust-validator
        name: AI Code Trust Validator
        entry: aitrust validate
        language: system
        types: [python]
        args: ['--min-score', '70']
```

## Configuration

Create `.aitrust.yaml` in your project:

```yaml
# Minimum trust score to pass
min_score: 75

# Strict mode: fail on any critical issues
strict_mode: true

# Weighted scoring (higher = more impact)
checks:
  security:
    enabled: true
    weight: 2.0
  hallucinations:
    enabled: true
    weight: 2.5  # Most critical for AI code
  logic:
    enabled: true
    weight: 1.0
  best_practices:
    enabled: true
    weight: 0.5

# Ignore patterns
ignore:
  - "tests/*"
  - "migrations/*"
  - "vendor/*"
```

## API Usage

```python
from ai_trust_validator import Validator, Config

# Create validator with custom config
config = Config(min_score=80, strict_mode=True)
validator = Validator(config)

# Validate code string
result = validator.validate(code_string, is_file=False)

# Validate file
result = validator.validate("path/to/file.py")

# Check results
print(f"Trust Score: {result.trust_score}")
print(f"Passed: {result.passed}")
print(f"Critical Issues: {len(result.critical_issues)}")

# Get detailed issues
for issue in result.all_issues:
    print(f"[{issue.severity}] {issue.category}: {issue.message}")
    if issue.suggestion:
        print(f"  → {issue.suggestion}")
```

## Why This Matters

**The AI Trust Gap is real:**

| Metric | 2024 | 2025 | Change |
|--------|------|------|--------|
| AI Tool Usage | 76% | 84% | +8% |
| Trust in AI Output | 40% | 29% | **-11%** |
| Time Fixing AI Code | 15% | 35% | +20% |

Source: Stack Overflow Developer Survey 2025

**We're using AI more but trusting it less.** This tool bridges that gap.

## Roadmap

- [x] Core validation engine
- [x] Security analyzer
- [x] Hallucination detector
- [x] Logic analyzer
- [x] Best practices checker
- [x] CLI with rich output
- [x] CI/CD integration
- [ ] JavaScript/TypeScript support
- [ ] Auto-fix suggestions (AI-powered)
- [ ] VS Code extension
- [ ] JetBrains plugin
- [ ] Web dashboard
- [ ] Team analytics
- [ ] Custom rule builder

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to help:**
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repo!

## Statistics

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rudra496/ai-code-trust-validator)
![GitHub last commit](https://img.shields.io/github/last-commit/rudra496/ai-code-trust-validator)
![GitHub code size](https://img.shields.io/github/languages/code-size/rudra496/ai-code-trust-validator)

## License

MIT License — use it freely. Just don't blame us if AI breaks production. 😉

---

<div align="center">

## 🔗 Connect with the Creator

**[Rudra Sarker](https://rudra496.github.io/site)** • Developer & Researcher

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/rudrasarker)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-green?logo=google-chrome)](https://rudra496.github.io/site)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com/rudra496)

---

**Built to close the AI trust gap.** 

*If this helped you, consider giving it a ⭐ — it helps others find it too!*

**Made with ❤️ by [Rudra Sarker](https://rudra496.github.io/site)**

</div>
