"""
CLI interface for AI Code Trust Validator.

Commands:
    aitrust validate <path>     - Validate code and show trust score
    aitrust report <path>       - Generate detailed report (JSON/HTML/SARIF)
    aitrust suggest-fixes <path>- Show fix suggestions for issues
    aitrust generate-tests <path>- Generate pytest tests
"""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from ai_trust_validator import (
    Validator, Config, ValidationResult, Issue,
    FixSuggester, TestGenerator,
    JSONReporter, HTMLReporter, SARIFReporter
)


console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="ai-trust-validator")
def main():
    """
    🛡️ AI Code Trust Validator - Trust your AI-generated code.
    
    Validate AI-generated code for security, hallucinations, and logic errors.
    
    Examples:
        aitrust validate src/ --min-score 75
        aitrust report src/ --format html --output report.html
        aitrust suggest-fixes buggy_code.py
        aitrust generate-tests module.py --output tests/
    """
    pass


@main.command()
@click.argument("path", type=click.Path(exists=False), required=False)
@click.option("--stdin", is_flag=True, help="Read code from stdin")
@click.option("--min-score", default=70, help="Minimum trust score to pass")
@click.option("--strict", is_flag=True, help="Fail on any critical issues")
@click.option("--json", "json_output", is_flag=True, help="Output as JSON")
@click.option("--config", type=click.Path(exists=True), help="Path to config file")
def validate(
    path: Optional[str],
    stdin: bool,
    min_score: int,
    strict: bool,
    json_output: bool,
    config: Optional[str]
):
    """
    Validate AI-generated code and produce a trust score.
    
    PATH can be a file or directory. Use --stdin to read from stdin.
    """
    # Load config
    if config:
        cfg = Config.from_file(config)
    else:
        cfg = Config.find_and_load()

    cfg.min_score = min_score
    cfg.strict_mode = strict or cfg.strict_mode

    validator = Validator(cfg)

    # Get source
    if stdin:
        code = sys.stdin.read()
        result = validator.validate(code, is_file=False)
        results = [result]
    elif path:
        path_obj = Path(path)
        if path_obj.is_file():
            result = validator.validate(path_obj)
            results = [result]
        elif path_obj.is_dir():
            results = validator.validate_directory(path_obj)
        else:
            console.print(f"[red]Error: {path} does not exist[/red]")
            sys.exit(1)
    else:
        console.print("[red]Error: Provide a PATH or use --stdin[/red]")
        sys.exit(1)

    # Output results
    if json_output:
        _output_json(results)
    else:
        _output_rich(results, cfg)

    # Exit code
    all_passed = all(
        r.trust_score >= cfg.min_score and len(r.critical_issues) == 0
        for r in results
    )
    if not all_passed:
        sys.exit(1)


@main.command("report")
@click.argument("path", type=click.Path(exists=True))
@click.option("--format", "report_format", type=click.Choice(["json", "html", "sarif"]), default="html", help="Report format")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--min-score", default=70, help="Minimum trust score to pass")
def report(path: str, report_format: str, output: Optional[str], min_score: int):
    """Generate a detailed report in JSON, HTML, or SARIF format."""
    path_obj = Path(path)
    cfg = Config.find_and_load()
    cfg.min_score = min_score
    validator = Validator(cfg)

    if path_obj.is_file():
        results = [validator.validate(path_obj)]
    else:
        results = validator.validate_directory(path_obj)

    # Generate report
    if report_format == "json":
        reporter = JSONReporter()
        content = reporter.generate(results)
        default_output = "trust-report.json"
    elif report_format == "html":
        reporter = HTMLReporter()
        content = reporter.generate(results)
        default_output = "trust-report.html"
    elif report_format == "sarif":
        reporter = SARIFReporter()
        content = reporter.generate(results)
        default_output = "trust-report.sarif.json"

    # Write output
    output_path = output or default_output
    Path(output_path).write_text(content, encoding="utf-8")
    console.print(f"[green]✓ Report saved to {output_path}[/green]")


@main.command("suggest-fixes")
@click.argument("path", type=click.Path(exists=True))
@click.option("--apply", is_flag=True, help="Show diff of suggested fixes")
def suggest_fixes(path: str, apply: bool):
    """Generate fix suggestions for detected issues."""
    path_obj = Path(path)
    code = path_obj.read_text(encoding="utf-8")
    
    cfg = Config.find_and_load()
    validator = Validator(cfg)
    result = validator.validate(path_obj)

    if not result.all_issues:
        console.print("[green]✓ No issues found - nothing to fix![/green]")
        return

    suggester = FixSuggester()
    fixes = suggester.suggest_fixes(result, code)

    if not fixes:
        console.print("[yellow]No automatic fixes available for the detected issues.[/yellow]")
        return

    console.print(f"\n💡 [bold]Fix Suggestions for {path}[/bold]\n")

    for fix in fixes:
        severity = fix.issue.severity.upper()
        color = _severity_color(fix.issue.severity)
        
        console.print(f"[{color}]{severity}[/{color}] {fix.issue.message}")
        if fix.issue.line:
            console.print(f"  [dim]Line {fix.issue.line}[/dim]")
        
        console.print(f"\n  [dim]Original:[/dim]")
        console.print(f"  {fix.original_code}")
        
        console.print(f"\n  [green]Suggested:[/green]")
        for line in fix.suggested_fix.split("\n"):
            console.print(f"  {line}")
        
        console.print(f"\n  [dim]Confidence: {fix.confidence:.0%} | Auto-applicable: {'Yes' if fix.auto_applicable else 'No'}[/dim]")
        console.print()


@main.command("generate-tests")
@click.argument("path", type=click.Path(exists=True))
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--module", "-m", default="module", help="Module name for imports")
def generate_tests(path: str, output: Optional[str], module: str):
    """Generate pytest tests for a Python file."""
    path_obj = Path(path)
    code = path_obj.read_text(encoding="utf-8")

    generator = TestGenerator()
    test_code = generator.generate_tests(code, module)

    if output:
        output_path = Path(output)
        output_path.write_text(test_code, encoding="utf-8")
        console.print(f"[green]✓ Tests saved to {output_path}[/green]")
    else:
        console.print(test_code)


def _output_rich(results: list[ValidationResult], cfg: Config):
    """Pretty print results using Rich."""
    for result in results:
        # Header
        if result.file_path:
            console.print(f"\n🔍 Analyzing: {result.file_path}")
        console.print("━" * 60)

        # Trust score with color
        score = result.trust_score
        if score >= 80:
            score_color = "green"
            score_icon = "✅"
        elif score >= 60:
            score_color = "yellow"
            score_icon = "⚠️"
        else:
            score_color = "red"
            score_icon = "❌"

        console.print(f"\n📊 TRUST SCORE: [{score_color}]{score}/100[/{score_color}] {score_icon}\n")

        # Category table
        if result.categories:
            table = Table(show_header=True, header_style="bold")
            table.add_column("Category", style="cyan")
            table.add_column("Score", justify="right")
            table.add_column("Issues", justify="left")

            for name, cat in result.categories.items():
                issue_count = len(cat.issues)
                critical = len([i for i in cat.issues if i.severity == "critical"])
                issue_str = f"{issue_count} issues"
                if critical > 0:
                    issue_str += f" ({critical} critical)"

                table.add_row(
                    name.replace("_", " ").title(),
                    str(cat.score),
                    issue_str
                )

            console.print(table)
            console.print()

        # Critical issues
        if result.critical_issues or result.high_issues:
            console.print("🚨 Critical Issues:\n")
            for issue in result.critical_issues[:5] + result.high_issues[:5]:
                line_info = f"Line {issue.line}: " if issue.line else ""
                console.print(f"  [{_severity_color(issue.severity)}]{issue.severity.upper()}[/{_severity_color(issue.severity)}] {line_info}{issue.message}")
                if issue.suggestion:
                    console.print(f"    💡 {issue.suggestion}")
            console.print()

        # Suggestions
        if result.all_issues:
            console.print("💡 Top Suggestions:\n")
            seen = set()
            for issue in result.all_issues[:3]:
                if issue.suggestion and issue.suggestion not in seen:
                    console.print(f"  • {issue.suggestion}")
                    seen.add(issue.suggestion)
            console.print()

        # Pass/fail
        if result.trust_score >= cfg.min_score and len(result.critical_issues) == 0:
            console.print(Panel("[green]✓ PASSED[/green]", expand=False))
        else:
            console.print(Panel("[red]✗ FAILED[/red]\n"
                              f"Score below {cfg.min_score} or critical issues found", 
                              expand=False))


def _severity_color(severity: str) -> str:
    """Get color for severity level."""
    colors = {
        "critical": "red",
        "high": "orange1",
        "medium": "yellow",
        "low": "dim",
        "info": "blue"
    }
    return colors.get(severity, "white")


def _output_json(results: list[ValidationResult]):
    """Output results as JSON."""
    reporter = JSONReporter()
    print(reporter.generate(results))


if __name__ == "__main__":
    main()
