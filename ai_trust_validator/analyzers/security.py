"""
Security Analyzer

Detects security vulnerabilities in AI-generated code:
- SQL injection patterns
- Command injection
- Hardcoded secrets
- Insecure configurations
- Dangerous function calls
"""

import ast
import re
from typing import List

from ai_trust_validator.analyzers import BaseAnalyzer
from ai_trust_validator.validator import Issue


class SecurityAnalyzer(BaseAnalyzer):
    """Analyzes code for security vulnerabilities."""

    base_score = 100

    # Patterns for hardcoded secrets
    SECRET_PATTERNS = [
        (r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']+(["\'])', "Hardcoded password"),
        (r'(?i)(api_key|apikey|api-key)\s*=\s*["\'][^"\']+(["\'])', "Hardcoded API key"),
        (r'(?i)(secret|token)\s*=\s*["\'][^"\']+(["\'])', "Hardcoded secret/token"),
        (r'(?i)(aws_access_key|aws_secret)\s*=\s*["\'][^"\']+(["\'])', "Hardcoded AWS credentials"),
    ]

    # Dangerous functions that should be flagged
    DANGEROUS_FUNCTIONS = {
        "eval": "Use of eval() can execute arbitrary code",
        "exec": "Use of exec() can execute arbitrary code",
        "compile": "Compiling strings can execute arbitrary code",
        "__import__": "Dynamic imports can be exploited",
        "input": "In Python 2, input() evaluates code (use raw_input)",
    }

    # SQL injection patterns
    SQL_INJECTION_PATTERNS = [
        r'execute\s*\(\s*f["\']',  # execute(f"...")
        r'execute\s*\(\s*["\'].*%s.*["\'].*%',  # execute("...%s", ...)
        r'\+\s*["\'].*SELECT',  # string concat with SQL
        r'f["\'].*SELECT.*\{',  # f-string with SQL
    ]

    def analyze(self, tree: ast.AST, code: str) -> List[Issue]:
        """Analyze code for security issues."""
        issues: List[Issue] = []

        # Check for hardcoded secrets
        issues.extend(self._check_secrets(code))

        # Walk AST for structural issues
        for node in ast.walk(tree):
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                issues.extend(self._check_dangerous_call(node))

            # Check for SQL injection patterns
            if isinstance(node, ast.Call):
                issues.extend(self._check_sql_injection(node, code))

            # Check for insecure subprocess calls
            if isinstance(node, ast.Call):
                issues.extend(self._check_subprocess(node))

            # Check for os.system calls
            issues.extend(self._check_os_system(node))

        return issues

    def _check_secrets(self, code: str) -> List[Issue]:
        """Check for hardcoded secrets."""
        issues: List[Issue] = []
        lines = code.split("\n")

        for pattern, message in self.SECRET_PATTERNS:
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    issues.append(Issue(
                        severity="high",
                        category="security",
                        message=message,
                        line=i,
                        suggestion="Use environment variables or secret management"
                    ))

        return issues

    def _check_dangerous_call(self, node: ast.Call) -> List[Issue]:
        """Check for dangerous function calls."""
        issues: List[Issue] = []

        func_name = self._get_func_name(node)
        if func_name in self.DANGEROUS_FUNCTIONS:
            severity = "critical" if func_name in ("eval", "exec") else "high"
            issues.append(Issue(
                severity=severity,
                category="security",
                message=self.DANGEROUS_FUNCTIONS[func_name],
                line=self._get_line(node),
                suggestion=f"Avoid {func_name}() or sanitize inputs carefully"
            ))

        return issues

    def _check_sql_injection(self, node: ast.Call, code: str) -> List[Issue]:
        """Check for SQL injection patterns."""
        issues: List[Issue] = []

        func_name = self._get_func_name(node)
        if func_name in ("execute", "executemany", "raw"):
            # Check if the call uses f-string or string formatting
            if node.args:
                arg = node.args[0]
                if isinstance(arg, ast.JoinedStr):  # f-string
                    issues.append(Issue(
                        severity="critical",
                        category="security",
                        message="Potential SQL injection via f-string",
                        line=self._get_line(node),
                        suggestion="Use parameterized queries with placeholders"
                    ))
                elif isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Mod):
                    issues.append(Issue(
                        severity="high",
                        category="security",
                        message="Potential SQL injection via string formatting",
                        line=self._get_line(node),
                        suggestion="Use parameterized queries instead of % formatting"
                    ))

        return issues

    def _check_subprocess(self, node: ast.Call) -> List[Issue]:
        """Check for insecure subprocess calls."""
        issues: List[Issue] = []

        func_name = self._get_func_name(node)
        if func_name == "call" or func_name == "run":
            # Check if shell=True
            for kw in node.keywords:
                if kw.arg == "shell":
                    if isinstance(kw.value, ast.Constant) and kw.value.value:
                        issues.append(Issue(
                            severity="high",
                            category="security",
                            message="subprocess with shell=True is vulnerable to injection",
                            line=self._get_line(node),
                            suggestion="Remove shell=True and pass arguments as list"
                        ))

        return issues

    def _check_os_system(self, node: ast.AST) -> List[Issue]:
        """Check for os.system calls."""
        issues: List[Issue] = []

        if isinstance(node, ast.Call):
            func_name = self._get_func_name(node)
            if func_name == "system":
                issues.append(Issue(
                    severity="high",
                    category="security",
                    message="os.system() is vulnerable to command injection",
                    line=self._get_line(node),
                    suggestion="Use subprocess.run() with shell=False"
                ))

        return issues

    def _get_func_name(self, node: ast.Call) -> str:
        """Extract function name from Call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return ""
