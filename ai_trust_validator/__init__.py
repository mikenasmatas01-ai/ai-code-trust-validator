"""
AI Code Trust Validator

Automatically validate AI-generated code for security vulnerabilities,
logic errors, and best practices.
"""

__version__ = "0.1.0"
__author__ = "rudra496"

from ai_trust_validator.validator import Validator, ValidationResult
from ai_trust_validator.config import Config

__all__ = ["Validator", "ValidationResult", "Config", "__version__"]
