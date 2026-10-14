"""Pydantic v2 data models for code-rule definitions and audit results."""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from .layout import ViolationSeverity


class RuleCategory(str, Enum):
    """Regulatory domain classification."""
    EGRESS = "egress"
    ACCESSIBILITY = "accessibility"
    ENVIRONMENTAL = "environmental"


class CodeRule(BaseModel):
    """Definition of a single building-code compliance predicate."""
    rule_id: str = Field(..., description="Unique rule identifier, e.g. 'IBC_1020.2'")
    name: str = Field(..., description="Human-readable rule name")
    category: RuleCategory
    severity: ViolationSeverity
    code_edition: str = Field(..., description="e.g., 'IBC 2024'")
    section: str = Field(..., description="e.g., '1020.2'")
    description: str = Field(..., description="Plain-language functional paraphrase of the requirement")
    threshold_value: float
    threshold_unit: str = "inches"
    comparison: str = Field(..., description="'gte' for >= threshold, 'lte' for <= threshold")
    source_note: str = Field(
        default="Section identifier only. Full code text is copyrighted; consult the adopted edition.",
        description="Copyright-safe provenance note",
    )


class Violation(BaseModel):
    """A detected violation from the oracle or a system under test."""
    rule_id: str
    element_id: str
    measured_value: float
    threshold_value: float
    units: str = "inches"
    severity: ViolationSeverity
    message: str = ""


class AuditResult(BaseModel):
    """Complete audit result for a single test case."""
    case_id: str
    label: str = Field(..., pattern=r"^(PASS|FAIL)$")
    violations: list[Violation] = Field(default_factory=list)
    rules_evaluated: int = Field(..., ge=0)
    oracle_version: str = ""


class BenchmarkMetrics(BaseModel):
    """Aggregate benchmark evaluation metrics."""
    total_cases: int
    true_positives: int = 0
    true_negatives: int = 0
    false_positives: int = 0
    false_negatives: int = 0

    @property
    def precision(self) -> float:
        denom = self.true_positives + self.false_positives
        return self.true_positives / denom if denom > 0 else 0.0

    @property
    def recall(self) -> float:
        denom = self.true_positives + self.false_negatives
        return self.true_positives / denom if denom > 0 else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) > 0 else 0.0

    @property
    def accuracy(self) -> float:
        total = self.total_cases
        return (self.true_positives + self.true_negatives) / total if total > 0 else 0.0
