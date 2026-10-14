"""Tests for oracle determinism — same input must always produce same output."""
from astg_codebench.schemas.layout import (
    LayoutTestCase,
    Space,
    SpaceType,
    Point2D,
    Jurisdiction,
    CaseProvenance,
)
from astg_codebench.engine.oracle import audit


def _make_corridor_case(clear_width: float, occupant_load: int = 60) -> LayoutTestCase:
    """Create a simple corridor test case."""
    return LayoutTestCase(
        case_id="ASTG-US-CW-FAIL-01" if clear_width < 44 else "ASTG-US-CW-PASS-01",
        seed=12345,
        jurisdiction=Jurisdiction(
            code_edition="IBC 2024",
            section="1020.2",
        ),
        unit_type="2BR",
        spaces=[
            Space(
                id="C1",
                type=SpaceType.CORRIDOR,
                polygon=[Point2D(x=0, y=0), Point2D(x=120, y=0), Point2D(x=120, y=clear_width), Point2D(x=0, y=clear_width)],
                area_sf=(120 * clear_width) / 144,
                clear_width_in=clear_width,
                occupant_load=occupant_load,
            ),
            Space(
                id="EXIT",
                type=SpaceType.ENTRY,
                polygon=[Point2D(x=120, y=0), Point2D(x=156, y=0), Point2D(x=156, y=clear_width), Point2D(x=120, y=clear_width)],
                area_sf=20.0,
            ),
        ],
        expected_label="FAIL" if clear_width < 44 else "PASS",
        provenance=CaseProvenance(
            base_typology="US_2BR_double_loaded_corridor",
            mutation=f"corridor_width_{clear_width}in",
        ),
    )


def test_oracle_determinism():
    """Running the oracle twice on the same input must yield identical results."""
    case = _make_corridor_case(clear_width=43.0)
    result1 = audit(case)
    result2 = audit(case)
    assert result1.label == result2.label
    assert len(result1.violations) == len(result2.violations)


def test_narrow_corridor_fails():
    """A corridor at 43 inches (below 44) with OL>=50 must fail."""
    case = _make_corridor_case(clear_width=43.0, occupant_load=60)
    result = audit(case)
    assert result.label == "FAIL"
    ibc_violations = [v for v in result.violations if v.rule_id == "IBC_1020.2"]
    assert len(ibc_violations) >= 1


def test_wide_corridor_passes():
    """A corridor at 45 inches (above 44) with OL>=50 must pass corridor check."""
    case = _make_corridor_case(clear_width=45.0, occupant_load=60)
    result = audit(case)
    ibc_violations = [v for v in result.violations if v.rule_id == "IBC_1020.2"]
    assert len(ibc_violations) == 0
