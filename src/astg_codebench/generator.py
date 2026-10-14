"""Procedural synthetic test case generator for ASTG-CodeBench.

Generates paired threshold cases (pass-near, fail-near, pass-obvious, fail-obvious)
based on standard US multifamily apartment typologies (studio, 1BR, 2BR).
"""
from __future__ import annotations

import json
from pathlib import Path

from astg_codebench.schemas.layout import (
    CaseProvenance,
    Door,
    DoorType,
    ExpectedViolation,
    Jurisdiction,
    LayoutTestCase,
    Point2D,
    Space,
    SpaceType,
    TopologyEdge,
    ViolationSeverity,
)


def make_corridor_pair() -> tuple[LayoutTestCase, LayoutTestCase]:
    """Generate paired cases for IBC 1020.2 corridor width (44" threshold)."""
    # PASS: 45 inches clear width (pass-near)
    pass_case = LayoutTestCase(
        case_id="ASTG-US-CW-PASS-01",
        version="0.1.0",
        seed=1001,
        jurisdiction=Jurisdiction(
            country="US",
            code_edition="IBC 2024",
            section="1020.2",
            source_url="https://codes.iccsafe.org",
        ),
        building_type="R-2 Multifamily",
        unit_type="2BR",
        spaces=[
            Space(
                id="C1",
                type=SpaceType.CORRIDOR,
                polygon=[Point2D(x=0, y=0), Point2D(x=240, y=0), Point2D(x=240, y=45), Point2D(x=0, y=45)],
                area_sf=75.0,
                clear_width_in=45.0,
                occupant_load=60,
                is_accessible=True,
            ),
            Space(
                id="ENTRY_1",
                type=SpaceType.ENTRY,
                polygon=[Point2D(x=240, y=0), Point2D(x=300, y=0), Point2D(x=300, y=45), Point2D(x=240, y=45)],
                area_sf=18.75,
                is_accessible=True,
            ),
        ],
        doors=[
            Door(
                id="D1",
                from_space="C1",
                to_space="ENTRY_1",
                door_type=DoorType.HINGED,
                clear_opening_in=36.0,
                latch_clearance_in=18.0,
            )
        ],
        topology=[
            TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True, is_accessible=True)
        ],
        expected_label="PASS",
        expected_violations=[],
        provenance=CaseProvenance(
            generation_method="parametric_perturbation",
            base_typology="US_2BR_double_loaded_corridor",
            mutation="corridor_width_threshold_plus_1in",
        ),
    )

    # FAIL: 43 inches clear width (fail-near)
    fail_case = LayoutTestCase(
        case_id="ASTG-US-CW-FAIL-01",
        version="0.1.0",
        seed=1002,
        jurisdiction=Jurisdiction(
            country="US",
            code_edition="IBC 2024",
            section="1020.2",
            source_url="https://codes.iccsafe.org",
        ),
        building_type="R-2 Multifamily",
        unit_type="2BR",
        spaces=[
            Space(
                id="C1",
                type=SpaceType.CORRIDOR,
                polygon=[Point2D(x=0, y=0), Point2D(x=240, y=0), Point2D(x=240, y=43), Point2D(x=0, y=43)],
                area_sf=71.67,
                clear_width_in=43.0,
                occupant_load=60,
                is_accessible=True,
            ),
            Space(
                id="ENTRY_1",
                type=SpaceType.ENTRY,
                polygon=[Point2D(x=240, y=0), Point2D(x=300, y=0), Point2D(x=300, y=43), Point2D(x=240, y=43)],
                area_sf=17.92,
                is_accessible=True,
            ),
        ],
        doors=[
            Door(
                id="D1",
                from_space="C1",
                to_space="ENTRY_1",
                door_type=DoorType.HINGED,
                clear_opening_in=36.0,
                latch_clearance_in=18.0,
            )
        ],
        topology=[
            TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True, is_accessible=True)
        ],
        expected_label="FAIL",
        expected_violations=[
            ExpectedViolation(
                rule_id="IBC_1020.2",
                element="C1",
                measured=43.0,
                threshold=44.0,
                units="inches",
                severity=ViolationSeverity.LIFE_SAFETY,
            )
        ],
        provenance=CaseProvenance(
            generation_method="parametric_perturbation",
            base_typology="US_2BR_double_loaded_corridor",
            mutation="corridor_width_threshold_minus_1in",
        ),
    )

    return pass_case, fail_case


def make_door_pair() -> tuple[LayoutTestCase, LayoutTestCase]:
    """Generate paired cases for ADA 404 door maneuvering clearance."""
    # PASS: 34" clear, 18" latch clearance
    pass_case = LayoutTestCase(
        case_id="ASTG-US-DOOR-PASS-01",
        version="0.1.0",
        seed=2001,
        jurisdiction=Jurisdiction(
            country="US",
            code_edition="ADA 2010",
            section="404",
            source_url="https://www.ada.gov",
        ),
        building_type="R-2 Multifamily",
        unit_type="1BR",
        spaces=[
            Space(
                id="LIVING_1",
                type=SpaceType.LIVING,
                polygon=[Point2D(x=0, y=0), Point2D(x=180, y=0), Point2D(x=180, y=144), Point2D(x=0, y=144)],
                area_sf=180.0,
                is_accessible=True,
            ),
            Space(
                id="BEDROOM_1",
                type=SpaceType.BEDROOM,
                polygon=[Point2D(x=180, y=0), Point2D(x=324, y=0), Point2D(x=324, y=144), Point2D(x=180, y=144)],
                area_sf=144.0,
                is_accessible=True,
                has_window=True,
                window_area_sf=18.0,
            ),
        ],
        doors=[
            Door(
                id="D_BR1",
                from_space="LIVING_1",
                to_space="BEDROOM_1",
                door_type=DoorType.HINGED,
                clear_opening_in=34.0,
                latch_clearance_in=18.5,
            )
        ],
        topology=[
            TopologyEdge(source="LIVING_1", target="BEDROOM_1", via="D_BR1", is_accessible=True)
        ],
        expected_label="PASS",
        expected_violations=[],
        provenance=CaseProvenance(
            generation_method="parametric_perturbation",
            base_typology="US_1BR_standard",
            mutation="door_clearance_compliant",
        ),
    )

    # FAIL: 30" clear (below 32"), 14" latch (below 18")
    fail_case = LayoutTestCase(
        case_id="ASTG-US-DOOR-FAIL-01",
        version="0.1.0",
        seed=2002,
        jurisdiction=Jurisdiction(
            country="US",
            code_edition="ADA 2010",
            section="404",
            source_url="https://www.ada.gov",
        ),
        building_type="R-2 Multifamily",
        unit_type="1BR",
        spaces=[
            Space(
                id="LIVING_1",
                type=SpaceType.LIVING,
                polygon=[Point2D(x=0, y=0), Point2D(x=180, y=0), Point2D(x=180, y=144), Point2D(x=0, y=144)],
                area_sf=180.0,
                is_accessible=True,
            ),
            Space(
                id="BEDROOM_1",
                type=SpaceType.BEDROOM,
                polygon=[Point2D(x=180, y=0), Point2D(x=324, y=0), Point2D(x=324, y=144), Point2D(x=180, y=144)],
                area_sf=144.0,
                is_accessible=True,
                has_window=True,
                window_area_sf=18.0,
            ),
        ],
        doors=[
            Door(
                id="D_BR1",
                from_space="LIVING_1",
                to_space="BEDROOM_1",
                door_type=DoorType.HINGED,
                clear_opening_in=30.0,
                latch_clearance_in=14.0,
            )
        ],
        topology=[
            TopologyEdge(source="LIVING_1", target="BEDROOM_1", via="D_BR1", is_accessible=True)
        ],
        expected_label="FAIL",
        expected_violations=[
            ExpectedViolation(
                rule_id="ADA_404",
                element="D_BR1",
                measured=30.0,
                threshold=32.0,
                units="inches",
                severity=ViolationSeverity.CIVIL_RIGHTS,
            ),
            ExpectedViolation(
                rule_id="ADA_404",
                element="D_BR1",
                measured=14.0,
                threshold=18.0,
                units="inches",
                severity=ViolationSeverity.CIVIL_RIGHTS,
            ),
        ],
        provenance=CaseProvenance(
            generation_method="parametric_perturbation",
            base_typology="US_1BR_standard",
            mutation="door_clearance_narrow",
        ),
    )

    return pass_case, fail_case


def generate_all(output_dir: Path) -> list[LayoutTestCase]:
    """Generate all canonical test cases and save as JSON files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    cases: list[LayoutTestCase] = []

    pairs = [
        make_corridor_pair(),
        make_door_pair(),
    ]

    for pass_c, fail_c in pairs:
        cases.extend([pass_c, fail_c])

    for case in cases:
        file_path = output_dir / f"{case.case_id.replace('ASTG-US-', '')}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(case.model_dump(), f, indent=2)

    return cases


if __name__ == "__main__":
    target = Path(__file__).parent.parent.parent / "data" / "v0.1" / "cases"
    created = generate_all(target)
    print(f"Generated {len(created)} canonical test cases in {target}")
