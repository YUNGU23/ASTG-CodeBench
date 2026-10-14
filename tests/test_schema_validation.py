"""Tests for schema validation of ASTG-CodeBench data models."""
import pytest
from pydantic import ValidationError

from astg_codebench.schemas.layout import (
    LayoutTestCase,
    Space,
    SpaceType,
    Point2D,
    Jurisdiction,
    CaseProvenance,
)


def _make_minimal_case(**overrides) -> dict:
    """Create a minimal valid test case dict."""
    base = {
        "case_id": "ASTG-US-CW-PASS-01",
        "version": "0.1.0",
        "seed": 42,
        "jurisdiction": {
            "country": "US",
            "code_edition": "IBC 2024",
            "section": "1020.2",
        },
        "building_type": "R-2 Multifamily",
        "unit_type": "2BR",
        "spaces": [
            {
                "id": "C1",
                "type": "corridor",
                "polygon": [{"x": 0, "y": 0}, {"x": 100, "y": 0}, {"x": 100, "y": 45}, {"x": 0, "y": 45}],
                "area_sf": 31.25,
                "clear_width_in": 45.0,
            }
        ],
        "expected_label": "PASS",
        "provenance": {
            "generation_method": "parametric_perturbation",
            "base_typology": "US_2BR_double_loaded_corridor",
            "mutation": "baseline_compliant",
        },
    }
    base.update(overrides)
    return base


def test_valid_case_parses():
    """A minimal valid case should parse without errors."""
    data = _make_minimal_case()
    case = LayoutTestCase.model_validate(data)
    assert case.case_id == "ASTG-US-CW-PASS-01"
    assert case.expected_label == "PASS"


def test_invalid_case_id_rejected():
    """Case IDs must match the required pattern."""
    data = _make_minimal_case(case_id="bad-id")
    with pytest.raises(ValidationError):
        LayoutTestCase.model_validate(data)


def test_invalid_label_rejected():
    """Expected labels must be PASS or FAIL."""
    data = _make_minimal_case(expected_label="MAYBE")
    with pytest.raises(ValidationError):
        LayoutTestCase.model_validate(data)


def test_empty_spaces_rejected():
    """At least one space is required."""
    data = _make_minimal_case(spaces=[])
    with pytest.raises(ValidationError):
        LayoutTestCase.model_validate(data)
