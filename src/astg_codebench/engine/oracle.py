"""Deterministic compliance oracle for ASTG-CodeBench.

This module runs all registered rule predicates against a test case and
produces a ground-truth audit result. The oracle is the authoritative
source of compliance labels — it must never be influenced by any LLM
or probabilistic system.
"""
from __future__ import annotations

from astg_codebench.schemas.layout import LayoutTestCase
from astg_codebench.schemas.rule import AuditResult, Violation
from astg_codebench.rules import (
    ibc_1020_corridor,
    ibc_1006_egress,
    ada_604_wc,
    ada_404_door,
    daylight_wfr,
)

__version__ = "0.1.0"

# Registry of all rule evaluators
_RULE_EVALUATORS = [
    ibc_1020_corridor.evaluate,
    ibc_1006_egress.evaluate,
    ada_604_wc.evaluate,
    ada_404_door.evaluate,
    daylight_wfr.evaluate,
]


def audit(case: LayoutTestCase) -> AuditResult:
    """Run all registered rules against a layout test case.

    Returns an AuditResult with the deterministic compliance label
    and all detected violations.
    """
    all_violations: list[Violation] = []
    for evaluator in _RULE_EVALUATORS:
        violations = evaluator(case)
        all_violations.extend(violations)

    label = "FAIL" if all_violations else "PASS"

    return AuditResult(
        case_id=case.case_id,
        label=label,
        violations=all_violations,
        rules_evaluated=len(_RULE_EVALUATORS),
        oracle_version=f"astg_codebench.engine.oracle v{__version__}",
    )
