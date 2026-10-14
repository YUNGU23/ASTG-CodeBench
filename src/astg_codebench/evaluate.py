"""Benchmark evaluation runner for ASTG-CodeBench.

Compares oracle results against expected labels to produce
precision, recall, F1, and confusion matrix reports.
"""
from __future__ import annotations

import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from astg_codebench.schemas.layout import LayoutTestCase
from astg_codebench.schemas.rule import BenchmarkMetrics
from astg_codebench.engine.oracle import audit

console = Console()


def load_cases(data_dir: Path) -> list[LayoutTestCase]:
    """Load all JSON test cases from a directory."""
    cases = []
    for f in sorted(data_dir.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        cases.append(LayoutTestCase.model_validate(raw))
    return cases


def evaluate_oracle(cases: list[LayoutTestCase]) -> BenchmarkMetrics:
    """Run the deterministic oracle on all cases and compute metrics."""
    metrics = BenchmarkMetrics(total_cases=len(cases))

    for case in cases:
        result = audit(case)
        predicted_fail = result.label == "FAIL"
        expected_fail = case.expected_label == "FAIL"

        if predicted_fail and expected_fail:
            metrics.true_positives += 1
        elif not predicted_fail and not expected_fail:
            metrics.true_negatives += 1
        elif predicted_fail and not expected_fail:
            metrics.false_positives += 1
        else:
            metrics.false_negatives += 1

    return metrics


def print_report(metrics: BenchmarkMetrics) -> None:
    """Print a formatted benchmark report to the console."""
    table = Table(title="ASTG-CodeBench Oracle Evaluation Report", show_header=True)
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    table.add_row("Total Cases", str(metrics.total_cases))
    table.add_row("True Positives", str(metrics.true_positives))
    table.add_row("True Negatives", str(metrics.true_negatives))
    table.add_row("False Positives", str(metrics.false_positives))
    table.add_row("False Negatives", str(metrics.false_negatives))
    table.add_row("Precision", f"{metrics.precision:.4f}")
    table.add_row("Recall", f"{metrics.recall:.4f}")
    table.add_row("F1 Score", f"{metrics.f1:.4f}")
    table.add_row("Accuracy", f"{metrics.accuracy:.4f}")

    console.print(table)

    # Life-safety false negative alert
    if metrics.false_negatives > 0:
        console.print(
            f"\n[bold red][WARN] WARNING: {metrics.false_negatives} false negative(s) detected. "
            "Life-safety violations may have been missed.[/bold red]"
        )
    else:
        console.print(
            "\n[bold green][PASS] Zero false negatives - all violations correctly detected.[/bold green]"
        )
