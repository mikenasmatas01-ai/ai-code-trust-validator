"""AI Code Trust Validator - v0.4.0"""
__version__ = "0.4.0"
__author__ = "Rudra Sarker"
__email__ = "rudra496@users.noreply.github.com"
__url__ = "https://github.com/rudra496/ai-code-trust-validator"

from ai_trust_validator.validator import Validator, ValidationResult, Issue
from ai_trust_validator.config import Config
from ai_trust_validator.multi_lang_validator import MultiLanguageValidator
from ai_trust_validator.languages import detect_language, get_parser
from ai_trust_validator.analyzers.security import SecurityAnalyzer
from ai_trust_validator.analyzers.hallucination import HallucinationAnalyzer
from ai_trust_validator.analyzers.logic import LogicAnalyzer
from ai_trust_validator.analyzers.best_practices import BestPracticesAnalyzer
from ai_trust_validator.analyzers.js_security import JSSecurityAnalyzer
from ai_trust_validator.analyzers.js_hallucination import JSHallucinationAnalyzer
from ai_trust_validator.ai_fix import AIAutoFixer, LLMConfig, FixResult, ai_fix_code
from ai_trust_validator.reporters import JSONReporter, HTMLReporter, SARIFReporter
from ai_trust_validator.fixer import FixSuggester, FixSuggestion
from ai_trust_validator.test_generator import TestGenerator
from ai_trust_validator.cache import CacheManager, CacheEntry
from ai_trust_validator.plugin import PluginManager, AnalyzerPlugin, PluginMetadata
from ai_trust_validator.watcher import Watcher, watch_with_dashboard
from ai_trust_validator.benchmark import BenchmarkSuite, run_full_benchmark
from ai_trust_validator.multi_file import MultiFileAnalyzer, MultiFileResult
from ai_trust_validator.api_server import run_server
from ai_trust_validator.lsp_server import LSPServer, run_lsp_server
from ai_trust_validator.analytics import AnalyticsDB, TeamStats, generate_analytics_report

__all__ = ["Validator", "ValidationResult", "Issue", "Config", "MultiLanguageValidator", "detect_language",
    "get_parser", "SecurityAnalyzer", "HallucinationAnalyzer", "LogicAnalyzer", "BestPracticesAnalyzer",
    "JSSecurityAnalyzer", "JSHallucinationAnalyzer", "AIAutoFixer", "LLMConfig", "FixResult", "ai_fix_code",
    "JSONReporter", "HTMLReporter", "SARIFReporter", "FixSuggester", "FixSuggestion", "TestGenerator",
    "CacheManager", "CacheEntry", "PluginManager", "AnalyzerPlugin", "PluginMetadata", "Watcher",
    "watch_with_dashboard", "BenchmarkSuite", "run_full_benchmark", "MultiFileAnalyzer", "MultiFileResult",
    "run_server", "LSPServer", "run_lsp_server", "AnalyticsDB", "TeamStats", "generate_analytics_report",
    "__version__", "__author__", "__email__", "__url__"]
