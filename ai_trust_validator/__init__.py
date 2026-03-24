"""
AI Code Trust Validator

Automatically validate AI-generated code for security vulnerabilities,
logic errors, and best practices.

Usage:
    from ai_trust_validator import Validator
    result = Validator().validate("file.py")
    print(f"Trust score: {result.trust_score}")

Features:
    - Security vulnerability detection
    - Hallucination detection for AI-generated code
    - Logic error detection
    - Best practices validation
    - Multi-file dependency analysis
    - Caching for performance
    - Plugin system for custom analyzers
    - REST API server
    - Watch mode for continuous monitoring
    - Benchmark suite
    - Test generation
    - Fix suggestions
    - Multiple report formats (JSON, HTML, SARIF)
"""

__version__ = "0.2.0"
__author__ = "Rudra Sarker"
__email__ = "rudra496@users.noreply.github.com"
__url__ = "https://github.com/rudra496/ai-code-trust-validator"

# Core
from ai_trust_validator.validator import Validator, ValidationResult, Issue
from ai_trust_validator.config import Config

# Analyzers
from ai_trust_validator.analyzers.security import SecurityAnalyzer
from ai_trust_validator.analyzers.hallucination import HallucinationAnalyzer
from ai_trust_validator.analyzers.logic import LogicAnalyzer
from ai_trust_validator.analyzers.best_practices import BestPracticesAnalyzer

# Reporters
from ai_trust_validator.reporters import JSONReporter, HTMLReporter, SARIFReporter

# Utilities
from ai_trust_validator.fixer import FixSuggester, FixSuggestion
from ai_trust_validator.test_generator import TestGenerator
from ai_trust_validator.cache import CacheManager, CacheEntry
from ai_trust_validator.plugin import PluginManager, AnalyzerPlugin, PluginMetadata
from ai_trust_validator.watcher import Watcher, watch_with_dashboard
from ai_trust_validator.benchmark import BenchmarkSuite, run_full_benchmark
from ai_trust_validator.multi_file import MultiFileAnalyzer, MultiFileResult
from ai_trust_validator.api_server import run_server

__all__ = [
    # Core
    "Validator",
    "ValidationResult",
    "Issue",
    "Config",
    
    # Analyzers
    "SecurityAnalyzer",
    "HallucinationAnalyzer",
    "LogicAnalyzer",
    "BestPracticesAnalyzer",
    
    # Reporters
    "JSONReporter",
    "HTMLReporter",
    "SARIFReporter",
    
    # Utilities
    "FixSuggester",
    "FixSuggestion",
    "TestGenerator",
    
    # Advanced features
    "CacheManager",
    "CacheEntry",
    "PluginManager",
    "AnalyzerPlugin",
    "PluginMetadata",
    "Watcher",
    "watch_with_dashboard",
    "BenchmarkSuite",
    "run_full_benchmark",
    "MultiFileAnalyzer",
    "MultiFileResult",
    "run_server",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__url__",
]
