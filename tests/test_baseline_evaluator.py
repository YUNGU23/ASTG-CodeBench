"""Tests for ASTG-CodeBench baseline evaluation models and metrics."""
from pathlib import Path
import pytest

from astg_codebench.evaluate import load_cases
from astg_codebench.baselines.llm_evaluator import (
    BaselineModelType,
    evaluate_baseline,
    run_benchmark_comparison,
)

DATA_DIR = Path(__file__).parent.parent / "data" / "v0.1" / "cases"


def test_oracle_baseline_evaluation():
    """Deterministic oracle must achieve 100% precision, recall, and zero life-safety FN."""
    cases = load_cases(DATA_DIR)
    assert len(cases) == 36

    res = evaluate_baseline(
        cases=cases,
        model_type=BaselineModelType.ASTG_ORACLE,
        synthetic=True,
    )
    assert res.metrics.precision == 1.0
    assert res.metrics.recall == 1.0
    assert res.metrics.f1 == 1.0
    assert res.metrics.accuracy == 1.0
    assert res.life_safety_false_negatives == 0


def test_comparative_benchmark_runner():
    """Comparison runner must return results for all benchmark models."""
    cases = load_cases(DATA_DIR)
    results = run_benchmark_comparison(cases=cases, synthetic=True)
    assert len(results) == 4

    model_names = [r.model_type for r in results]
    assert BaselineModelType.ASTG_ORACLE in model_names
    assert BaselineModelType.VANILLA_ZERO_SHOT in model_names
    assert BaselineModelType.FEW_SHOT_COT in model_names

    # Check oracle is top performer
    oracle_res = next(r for r in results if r.model_type == BaselineModelType.ASTG_ORACLE)
    assert oracle_res.life_safety_false_negatives == 0
