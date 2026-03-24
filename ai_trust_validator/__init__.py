"""
AI Code Trust Validator

Automatically validate AI-generated code for security vulnerabilities,
logic errors, and best practices.

Usage:
    from ai_trust_validator import Validator
    result = Validator().validate("file.py")
    print(f"Trust score: {result.trust_score}")
"""

__version__ = "0.1.0"
__author__ = "Rudra Sarker"
__email__ = "rudra496@users.noreply.github.com"

from ai_trust_validator.validator import Validator, ValidationResult, Issue
from ai_trust_validator.config import Config
from ai_trust_validator.fixer import FixSuggester, FixSuggestion
from ai_trust_validator.test_generator import TestGenerator
from ai_trust_validator.reporters import JSONReporter, HTMLReporter, SARIFReporter

__all__ = [
    # Core
    "Validator",
    "ValidationResult",
    "Issue",
    "Config",
    
    # Fix suggestions
    "FixSuggester",
    "FixSuggestion",
    
    # Test generation
    "TestGenerator",
    
    # Reporters
    "JSONReporter",
    "HTMLReporter", 
    "SARIFReporter",
    
    # Metadata
    "__version__",
    "__author__",
]
