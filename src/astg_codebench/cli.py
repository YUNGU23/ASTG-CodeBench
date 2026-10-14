"""Command-line interface for ASTG-CodeBench."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

app = typer.Typer(
    name="astg-bench",
    help="ASTG-CodeBench: Spatial compliance benchmark toolkit.",
    add_completion=False,
)
console = Console()

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "v0.1" / "cases"


@app.command()
def audit(
    case_file: Path = typer.Argument(..., help="Path to a single test case JSON file."),
) -> None:
    """Run the compliance oracle on a single test case."""
    import json
    from astg_codebench.schemas.layout import LayoutTestCase
    from astg_codebench.engine.oracle import audit as run_audit

    with open(case_file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    case = LayoutTestCase.model_validate(raw)
    result = run_audit(case)

    console.print(f"\n[bold]Case:[/bold] {result.case_id}")
    console.print(f"[bold]Label:[/bold] {result.label}")
    console.print(f"[bold]Rules evaluated:[/bold] {result.rules_evaluated}")
    console.print(f"[bold]Violations found:[/bold] {len(result.violations)}")

    for v in result.violations:
        severity_color = {
            "life_safety": "red",
            "civil_rights": "yellow",
            "voluntary": "blue",
        }.get(v.severity.value, "white")
        console.print(
            f"  [{severity_color}]* {v.rule_id}[/{severity_color}] "
            f"{v.element_id}: {v.message}"
        )


@app.command()
def evaluate(
    data_dir: Optional[Path] = typer.Option(
        None,
        "--data-dir", "-d",
        help="Directory containing test case JSON files.",
    ),
) -> None:
    """Run the benchmark evaluation on all test cases."""
    from astg_codebench.evaluate import load_cases, evaluate_oracle, print_report

    target_dir = data_dir or DATA_DIR
    if not target_dir.exists():
        console.print(f"[red]Error: Data directory not found: {target_dir}[/red]")
        raise typer.Exit(code=1)

    cases = load_cases(target_dir)
    if not cases:
        console.print(f"[red]Error: No JSON test cases found in {target_dir}[/red]")
        raise typer.Exit(code=1)

    console.print(f"\nLoaded {len(cases)} test cases from {target_dir}")
    metrics = evaluate_oracle(cases)
    print_report(metrics)


if __name__ == "__main__":
    app()
