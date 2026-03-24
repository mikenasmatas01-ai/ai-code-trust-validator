"""
CLI interface for AI Trust Validator.

Usage:
    aitrust validate <file>
    aitrust validate <directory>
    cat code.py | aitrust validate --stdin
"""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from ai_trust_validator import Validator, Config, ValidationResult
from ai_trust_validator.validator import Issue


console = Console()


@click.group()
@click.version_option()
def main():
    """AI Code Trust Validator - Trust your AI-generated code."""
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
    import json

    data = []
    for result in results:
        data.append({
            "file_path": result.file_path,
            "trust_score": result.trust_score,
            "passed": result.passed,
            "critical_issues": len(result.critical_issues),
            "categories": {
                name: {
                    "score": cat.score,
                    "weight": cat.weight,
                    "issue_count": len(cat.issues)
                }
                for name, cat in result.categories.items()
            },
            "issues": [
                {
                    "severity": i.severity,
                    "category": i.category,
                    "message": i.message,
                    "line": i.line,
                    "suggestion": i.suggestion
                }
                for i in result.all_issues
            ]
        })

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
