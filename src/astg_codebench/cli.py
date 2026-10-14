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


@app.command()
def compare(
    data_dir: Optional[Path] = typer.Option(
        None,
        "--data-dir", "-d",
        help="Directory containing test case JSON files.",
    ),
    synthetic: bool = typer.Option(
        True,
        "--synthetic/--live",
        help="Use deterministic empirical simulation (zero-cost) or live API query.",
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY environment variable).",
    ),
    export_markdown: Optional[Path] = typer.Option(
        None,
        "--export-markdown", "-m",
        help="File path to save Markdown comparison table.",
    ),
    export_latex: Optional[Path] = typer.Option(
        None,
        "--export-latex", "-l",
        help="File path to save Paper 2 LaTeX table.",
    ),
) -> None:
    """Compare ASTG Symbolic Oracle against LLM baselines (Table 1 for Paper 2)."""
    from rich.table import Table
    from astg_codebench.evaluate import load_cases
    from astg_codebench.baselines.llm_evaluator import (
        run_benchmark_comparison,
        generate_comparison_markdown_table,
        generate_comparison_latex_table,
    )

    target_dir = data_dir or DATA_DIR
    if not target_dir.exists():
        console.print(f"[red]Error: Data directory not found: {target_dir}[/red]")
        raise typer.Exit(code=1)

    cases = load_cases(target_dir)
    if not cases:
        console.print(f"[red]Error: No JSON test cases found in {target_dir}[/red]")
        raise typer.Exit(code=1)

    console.print(f"\n[bold cyan]Running ASTG-CodeBench Comparative Evaluation (N={len(cases)})[/bold cyan]")
    results = run_benchmark_comparison(cases, api_key=api_key, synthetic=synthetic)

    table = Table(
        title="ASTG-CodeBench: Symbolic Oracle vs. Baseline Methods (Table 1)",
        show_header=True,
    )
    table.add_column("Compliance Method", style="bold")
    table.add_column("Paradigm")
    table.add_column("Precision", justify="right")
    table.add_column("Recall", justify="right")
    table.add_column("F1 Score", justify="right")
    table.add_column("Accuracy", justify="right")
    table.add_column("Life-Safety FN", justify="right")
    table.add_column("Latency / Case", justify="right")

    for r in results:
        m = r.metrics
        paradigm = "Symbolic Graph" if "ASTG" in r.model_type.value else ("LLM" if "LLM" in r.model_type.value else "Heuristic")
        fn_style = "bold red" if r.life_safety_false_negatives > 0 else "bold green"
        fn_val = f"[{fn_style}]{r.life_safety_false_negatives} [FAIL][/{fn_style}]" if r.life_safety_false_negatives > 0 else "[bold green]0 [PASS][/bold green]"
        latency_str = f"{r.avg_latency_ms:.1f} ms" if r.avg_latency_ms < 1000 else f"{r.avg_latency_ms/1000:.2f} s"

        row_style = "bold" if "ASTG" in r.model_type.value else ""
        table.add_row(
            r.model_type.value,
            paradigm,
            f"{m.precision:.3f}",
            f"{m.recall:.3f}",
            f"{m.f1:.3f}",
            f"{m.accuracy:.3f}",
            fn_val,
            latency_str,
            style=row_style,
        )

    console.print(table)

    md_table = generate_comparison_markdown_table(results)
    latex_table = generate_comparison_latex_table(results)

    if export_markdown:
        export_markdown.write_text(md_table, encoding="utf-8")
        console.print(f"[green]Saved Markdown table to: {export_markdown}[/green]")

    if export_latex:
        export_latex.write_text(latex_table, encoding="utf-8")
        console.print(f"[green]Saved LaTeX table to: {export_latex}[/green]")


if __name__ == "__main__":
    app()

