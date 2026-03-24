<div align="center">

# 🛡️ AI Code Trust Validator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/rudra496/ai-code-trust-validator.svg?style=social)](https://github.com/rudra496/ai-code-trust-validator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/rudra496/ai-code-trust-validator.svg?style=social)](https://github.com/rudra496/ai-code-trust-validator/network/members)
[![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)](https://github.com/rudra496/ai-code-trust-validator/pkgs/container/ai-code-trust-validator)
[![VS Code](https://img.shields.io/badge/VS%20Code-Extension-blue?logo=visualstudiocode)](vscode-extension/)

**Trust your AI-generated code before shipping to production.**

*The complete quality gate for AI-assisted development*

[Installation](#-installation) • [Quick Start](#-quick-start) • [Features](#-features) • [CLI Reference](#-cli-reference) • [Documentation](#-documentation)

</div>

---

## 🎯 The Problem

**84% of developers use AI coding tools. Only 29% trust the output.** *(Stack Overflow 2025)*

AI writes code fast, but that code often contains:
- 🔓 **Security vulnerabilities** — SQL injection, hardcoded secrets, command injection
- 🎭 **Hallucinations** — Fake imports, invented functions, imaginary APIs
- 🐛 **Logic errors** — Unreachable code, infinite loops, dead branches
- 📉 **Technical debt** — Missing docs, poor naming, deep nesting
- 🔗 **Dependency issues** — Circular imports, missing modules, unused code

**You can't ship what you can't trust.**

---

## ✨ Features

| Category | Features |
|----------|----------|
| **🔍 Analysis** | Security scanning, Hallucination detection, Logic validation, Best practices |
| **📊 Reports** | JSON, HTML (beautiful dashboard), SARIF (GitHub Security), PDF |
| **🔧 Fixes** | Auto-fix suggestions, Confidence scores, One-click apply |
| **🧪 Testing** | Auto-generate pytest tests, Edge case detection, Coverage analysis |
| **🌐 API** | REST API server, OpenAPI docs, Batch validation, Webhook support |
| **👀 Monitoring** | File watch mode, Live dashboard, Continuous validation |
| **📦 Multi-file** | Dependency analysis, Circular dependency detection, Import validation |
| **⚡ Performance** | Intelligent caching, Incremental analysis, ~10,000+ lines/sec |
| **🔌 Extensible** | Plugin system, Custom analyzers, Hook system |
| **🐳 Deployment** | Docker, Docker Compose, GitHub Action, Pre-commit hooks |
| **💻 IDE Integration** | VS Code extension, LSP server, JetBrains (coming soon) |
| **📈 Team Analytics** | Dashboard, Leaderboards, Trend analysis, Project breakdown |

---

## 📦 Installation

```bash
# From PyPI (recommended)
pip install ai-trust-validator

# With server support
pip install ai-trust-validator[server]

# With all extras
pip install ai-trust-validator[all]

# From source
git clone https://github.com/rudra496/ai-code-trust-validator.git
cd ai-code-trust-validator
pip install -e ".[all]"

# Docker
docker pull ghcr.io/rudra496/ai-code-trust-validator:latest
docker run -v ./code:/code ghcr.io/rudra496/ai-code-trust-validator validate /code
```

---

## 🚀 Quick Start

### CLI

```bash
# Validate a file
aitrust validate generated_code.py

# Validate directory with minimum score
aitrust validate src/ --min-score 75 --strict

# Generate HTML report
aitrust report src/ --format html --output report.html

# Get fix suggestions
aitrust suggest-fixes buggy_code.py

# Generate tests
aitrust generate-tests module.py --output tests/test_module.py

# Start API server
aitrust serve --port 8080

# Watch for changes with live dashboard
aitrust watch src/ --dashboard

# Analyze dependencies
aitrust analyze-deps src/

# Run benchmarks
aitrust benchmark --iterations 100

# View team analytics
aitrust analytics --days 30

# Start LSP server (for IDE integration)
aitrust lsp
```

### Python API

```python
from ai_trust_validator import Validator, Config

# Simple validation
validator = Validator()
result = validator.validate("generated_code.py")

print(f"Trust Score: {result.trust_score}/100")
print(f"Passed: {result.passed}")

for issue in result.critical_issues:
    print(f"[CRITICAL] {issue.message}")
    if issue.suggestion:
        print(f"  💡 {issue.suggestion}")

# With custom config
config = Config(min_score=80, strict_mode=True)
validator = Validator(config)
result = validator.validate_code(code_string)

# Multi-file analysis
from ai_trust_validator import MultiFileAnalyzer
analyzer = MultiFileAnalyzer(validator)
result = analyzer.analyze_directory("src/")
print(f"Circular deps: {result.circular_dependencies}")

# Team analytics
from ai_trust_validator import AnalyticsDB
db = AnalyticsDB()
db.record_validation("file.py", result, user="dev1", project="myapp")
stats = db.get_stats(days=30)
print(f"Team avg: {stats.average_score}")
```

### REST API

```bash
# Start server
aitrust serve --port 8080

# Validate via API
curl -X POST http://localhost:8080/validate \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): print(\"world\")"}'

# Batch validation
curl -X POST http://localhost:8080/validate/batch \
  -H "Content-Type: application/json" \
  -d '{"files": [{"name": "a.py", "code": "..."}]}'
```

### Web Dashboard

```bash
# Start server with dashboard
aitrust serve --port 8080

# Open browser to http://localhost:8080
# Or serve the static dashboard
cd dashboard && python -m http.server 3000
```

---

## 📊 Example Output

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
  → Use parameterized queries: cursor.execute("... WHERE id = ?", (user_id,))
```

---

## 🔧 CLI Reference

| Command | Description |
|---------|-------------|
| `aitrust validate <path>` | Validate code and show trust score |
| `aitrust report <path>` | Generate detailed report (JSON/HTML/SARIF) |
| `aitrust suggest-fixes <path>` | Show fix suggestions for issues |
| `aitrust generate-tests <path>` | Generate pytest tests |
| `aitrust serve` | Start REST API server |
| `aitrust watch <path>` | Watch files for changes |
| `aitrust benchmark` | Run performance benchmarks |
| `aitrust analyze-deps <path>` | Multi-file dependency analysis |
| `aitrust analytics` | View team analytics |
| `aitrust cache <action>` | Manage validation cache |
| `aitrust lsp` | Start LSP server for IDEs |

---

## 🐳 Docker & Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  validator:
    image: ghcr.io/rudra496/ai-code-trust-validator:latest
    ports:
      - "8080:8080"
    command: serve --port 8080
    volumes:
      - ./code:/code:ro
      - ./.aitrust_cache:/app/.aitrust_cache
```

### GitHub Action

```yaml
name: AI Code Trust Check
on: [pull_request]

jobs:
  trust-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Validate AI Code
        uses: rudra496/ai-code-trust-validator@v0.3.0
        with:
          path: 'src/'
          min-score: '75'
          format: 'sarif'
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/rudra496/ai-code-trust-validator
    rev: v0.3.0
    hooks:
      - id: ai-trust-validator
        args: ['--min-score', '70']
```

---

## 💻 IDE Integration

### VS Code

```bash
# Install from VS Code Marketplace
# Search for "AI Trust Validator"

# Or install manually
cd vscode-extension
npm install
npm run compile
```

Features:
- Real-time diagnostics
- Trust score in status bar
- Quick fix suggestions
- Hover information
- Auto-validate on save

### LSP Server (Neovim, Emacs, etc.)

```bash
# Start LSP server
aitrust lsp

# Configure in your LSP client
# Command: aitrust lsp
# Language: python
```

---

## 🔌 Plugin System

Create custom analyzers:

```python
from ai_trust_validator import AnalyzerPlugin, PluginMetadata, Issue

class MyCustomAnalyzer(AnalyzerPlugin):
    @property
    def metadata(self):
        return PluginMetadata(
            name="my_custom",
            version="1.0.0",
            author="You",
            description="Custom analyzer"
        )
    
    def analyze(self, tree, code, context):
        issues = []
        # Your analysis logic
        return issues

# Register
from ai_trust_validator import PluginManager
manager = PluginManager()
manager.register(MyCustomAnalyzer())
```

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Throughput | 10,000+ lines/sec |
| Avg validation | 5-20ms per file |
| Memory | <50MB typical |
| Cache hit rate | 95%+ on re-runs |

Run your own benchmarks:
```bash
aitrust benchmark --iterations 1000
```

---

## 🗺️ Roadmap

### Completed ✅

- [x] Core validation engine
- [x] Security analyzer
- [x] Hallucination detector
- [x] Logic analyzer
- [x] Best practices checker
- [x] CLI with rich output
- [x] JSON/HTML/SARIF reports
- [x] Fix suggestions
- [x] Test generation
- [x] REST API server
- [x] Docker support
- [x] GitHub Action
- [x] Pre-commit hooks
- [x] Plugin system
- [x] Multi-file analysis
- [x] Watch mode
- [x] Caching system
- [x] LSP server
- [x] VS Code extension
- [x] Web dashboard
- [x] Team analytics

### Coming Soon 🚧

- [ ] JavaScript/TypeScript support
- [ ] AI-powered auto-fix (LLM integration)
- [ ] JetBrains plugin (IntelliJ, PyCharm)
- [ ] Cloud hosted version

---

## 📊 Statistics

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/rudra496/ai-code-trust-validator)
![GitHub last commit](https://img.shields.io/github/last-commit/rudra496/ai-code-trust-validator)
![GitHub code size](https://img.shields.io/github/languages/code-size/rudra496/ai-code-trust-validator)
![GitHub issues](https://img.shields.io/github/issues/rudra496/ai-code-trust-validator)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Ways to help:**
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repo!

---

## 📄 License

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
