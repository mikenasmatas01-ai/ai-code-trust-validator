# Contributing to AI Code Trust Validator

Thanks for your interest in contributing! 🎉

## Ways to Contribute

- 🐛 **Report bugs** — Open an issue with details
- 💡 **Suggest features** — Open an issue with the `enhancement` label
- 📝 **Improve docs** — Better documentation helps everyone
- 🔧 **Submit PRs** — Fix bugs, add features, improve code

## Development Setup

```bash
# Clone the repo
git clone https://github.com/rudra496/ai-code-trust-validator.git
cd ai-code-trust-validator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .

# Format code
black .
```

## Project Structure

```
ai-code-trust-validator/
├── ai_trust_validator/
│   ├── __init__.py          # Package exports
│   ├── cli.py               # CLI commands
│   ├── config.py            # Configuration handling
│   ├── validator.py         # Main validation logic
│   └── analyzers/
│       ├── __init__.py      # Base analyzer
│       ├── security.py      # Security analysis
│       ├── hallucination.py # Hallucination detection
│       ├── logic.py         # Logic errors
│       └── best_practices.py# Best practices
├── tests/
│   └── test_validator.py    # Test suite
├── pyproject.toml           # Package config
└── README.md                # Documentation
```

## Adding a New Analyzer

1. Create a new file in `ai_trust_validator/analyzers/`
2. Inherit from `BaseAnalyzer`
3. Implement `analyze(self, tree, code) -> List[Issue]`
4. Add to `Validator._init_analyzers()`
5. Add tests
6. Update docs

Example:

```python
from ai_trust_validator.analyzers import BaseAnalyzer
from ai_trust_validator.validator import Issue

class MyAnalyzer(BaseAnalyzer):
    base_score = 100

    def analyze(self, tree, code):
        issues = []
        # Your analysis logic here
        return issues
```

## Commit Guidelines

- Use clear, descriptive commit messages
- Reference issues: `Fixes #123` or `Related to #456`
- Keep commits focused and atomic

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to public functions
- Keep functions under 50 lines

## Testing

- Write tests for new features
- Run `pytest` before submitting PRs
- Aim for >80% coverage on new code

## Questions?

Open an issue with the `question` label.

---

Thanks for helping make AI-generated code more trustworthy! 🚀
