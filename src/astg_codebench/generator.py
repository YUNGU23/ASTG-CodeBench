"""Procedural synthetic test case generator for ASTG-CodeBench v0.1.0.

Generates the complete 36 canonical paired-threshold benchmark suite across
5 US building code rule families (IBC 1020, IBC 1006, ADA 604, ADA 404, WFR)
plus compound multi-rule cases.

Design: 18 PASS cases, 18 FAIL cases — perfectly balanced and deterministic.
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


def _rect(x: float, y: float, w: float, h: float) -> list[Point2D]:
    """Helper to create rectangular polygon vertices in clockwise order."""
    return [
        Point2D(x=x, y=y),
        Point2D(x=x + w, y=y),
        Point2D(x=x + w, y=y + h),
        Point2D(x=x, y=y + h),
    ]


# -----------------------------------------------------------------------------
# Family 1: IBC 1020.2 Corridor Minimum Clear Width (6 cases: 3 PASS, 3 FAIL)
# -----------------------------------------------------------------------------
def make_corridor_cases() -> list[LayoutTestCase]:
    cases = []
    jurisdiction = Jurisdiction(
        code_edition="IBC 2024",
        section="1020.2",
        source_url="https://codes.iccsafe.org",
    )

    # 1. CW-PASS-01: Pass-near (45" clear, required 44", OL=60)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CW-PASS-01",
        seed=101,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 240, 45), area_sf=75.0, clear_width_in=45.0, occupant_load=60),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(240, 0, 60, 45), area_sf=18.75),
        ],
        doors=[Door(id="D1", from_space="C1", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=18.0)],
        topology=[TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True)],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_2BR_corridor", mutation="width_threshold_plus_1in"),
    ))

    # 2. CW-FAIL-01: Fail-near (43" clear, required 44", OL=60)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CW-FAIL-01",
        seed=102,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 240, 43), area_sf=71.7, clear_width_in=43.0, occupant_load=60),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(240, 0, 60, 43), area_sf=17.9),
        ],
        doors=[Door(id="D1", from_space="C1", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=18.0)],
        topology=[TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True)],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="IBC_1020.2", element="C1", measured=43.0, threshold=44.0, severity=ViolationSeverity.LIFE_SAFETY)],
        provenance=CaseProvenance(base_typology="US_2BR_corridor", mutation="width_threshold_minus_1in"),
    ))

    # 3. CW-PASS-02: Pass-obvious (60" generous public corridor, OL=80)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CW-PASS-02",
        seed=103,
        jurisdiction=jurisdiction,
        unit_type="3BR",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 360, 60), area_sf=150.0, clear_width_in=60.0, occupant_load=80),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(360, 0, 72, 60), area_sf=30.0),
        ],
        doors=[Door(id="D1", from_space="C1", to_space="ENTRY_1", clear_opening_in=40.0, latch_clearance_in=24.0)],
        topology=[TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True)],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_3BR_corridor", mutation="generous_width_60in"),
    ))

    # 4. CW-FAIL-02: Fail-obvious (32" narrow pinch corridor, OL=60)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CW-FAIL-02",
        seed=104,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 200, 32), area_sf=44.4, clear_width_in=32.0, occupant_load=60),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(200, 0, 60, 32), area_sf=13.3),
        ],
        doors=[Door(id="D1", from_space="C1", to_space="ENTRY_1", clear_opening_in=32.0, latch_clearance_in=18.0)],
        topology=[TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True)],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="IBC_1020.2", element="C1", measured=32.0, threshold=44.0, severity=ViolationSeverity.LIFE_SAFETY)],
        provenance=CaseProvenance(base_typology="US_1BR_corridor", mutation="pinch_width_32in"),
    ))

    # 5. CW-PASS-03: Small building corridor (38" clear, OL=30 < 50 threshold -> required 36")
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CW-PASS-03",
        seed=105,
        jurisdiction=jurisdiction,
        unit_type="STUDIO",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 180, 38), area_sf=47.5, clear_width_in=38.0, occupant_load=30),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(180, 0, 48, 38), area_sf=12.7),
        ],
        doors=[Door(id="D1", from_space="C1", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=18.0)],
        topology=[TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True)],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_studio_corridor", mutation="low_occupancy_pass_38in"),
    ))

    # 6. CW-FAIL-03: Small building corridor (34" clear, OL=30 < 50 -> required 36")
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CW-FAIL-03",
        seed=106,
        jurisdiction=jurisdiction,
        unit_type="STUDIO",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 180, 34), area_sf=42.5, clear_width_in=34.0, occupant_load=30),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(180, 0, 48, 34), area_sf=11.3),
        ],
        doors=[Door(id="D1", from_space="C1", to_space="ENTRY_1", clear_opening_in=34.0, latch_clearance_in=18.0)],
        topology=[TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True)],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="IBC_1020.2", element="C1", measured=34.0, threshold=36.0, severity=ViolationSeverity.LIFE_SAFETY)],
        provenance=CaseProvenance(base_typology="US_studio_corridor", mutation="low_occupancy_fail_34in"),
    ))

    return cases


# -----------------------------------------------------------------------------
# Family 2: IBC 1006.2 Egress Travel Distance (6 cases: 3 PASS, 3 FAIL)
# -----------------------------------------------------------------------------
def make_egress_cases() -> list[LayoutTestCase]:
    cases = []
    jurisdiction = Jurisdiction(code_edition="IBC 2024", section="1006.2", source_url="https://codes.iccsafe.org")

    # 1. EG-PASS-01: Direct exit access (1 hop = ~20 ft <= 75 ft limit)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-EG-PASS-01",
        seed=201,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="R1", type=SpaceType.LIVING, polygon=_rect(0, 0, 180, 144), area_sf=180.0, has_window=True, window_area_sf=20.0),
            Space(id="STAIR_1", type=SpaceType.STAIRWELL, polygon=_rect(180, 0, 100, 144), area_sf=100.0),
        ],
        doors=[Door(id="D1", from_space="R1", to_space="STAIR_1", clear_opening_in=36.0, latch_clearance_in=18.0)],
        topology=[TopologyEdge(source="R1", target="STAIR_1", via="D1", is_egress=True)],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_1BR_direct_egress", mutation="short_travel_1hop"),
    ))

    # 2. EG-FAIL-01: Remote dead-end unit (4 hops = ~80 ft > 75 ft limit)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-EG-FAIL-01",
        seed=202,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="R1", type=SpaceType.BEDROOM, polygon=_rect(0, 0, 144, 120), area_sf=120.0, has_window=True, window_area_sf=15.0),
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(144, 0, 120, 48), area_sf=40.0, clear_width_in=48.0, occupant_load=20),
            Space(id="C2", type=SpaceType.CORRIDOR, polygon=_rect(264, 0, 120, 48), area_sf=40.0, clear_width_in=48.0, occupant_load=20),
            Space(id="C3", type=SpaceType.CORRIDOR, polygon=_rect(384, 0, 120, 48), area_sf=40.0, clear_width_in=48.0, occupant_load=20),
            Space(id="STAIR_1", type=SpaceType.STAIRWELL, polygon=_rect(504, 0, 100, 100), area_sf=69.4),
        ],
        doors=[
            Door(id="D1", from_space="R1", to_space="C1", clear_opening_in=34.0, latch_clearance_in=18.0),
            Door(id="D2", from_space="C1", to_space="C2", clear_opening_in=48.0, latch_clearance_in=18.0),
            Door(id="D3", from_space="C2", to_space="C3", clear_opening_in=48.0, latch_clearance_in=18.0),
            Door(id="D4", from_space="C3", to_space="STAIR_1", clear_opening_in=36.0, latch_clearance_in=18.0),
        ],
        topology=[
            TopologyEdge(source="R1", target="C1", via="D1", is_egress=True),
            TopologyEdge(source="C1", target="C2", via="D2", is_egress=True),
            TopologyEdge(source="C2", target="C3", via="D3", is_egress=True),
            TopologyEdge(source="C3", target="STAIR_1", via="D4", is_egress=True),
        ],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="IBC_1006.2", element="R1", measured=80.0, threshold=75.0, units="feet", severity=ViolationSeverity.LIFE_SAFETY)],
        provenance=CaseProvenance(base_typology="US_2BR_extended_corridor", mutation="travel_distance_80ft"),
    ))

    # 3. EG-PASS-02: Intermediate corridor (2 hops = ~40 ft <= 75 ft)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-EG-PASS-02",
        seed=203,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="R1", type=SpaceType.BEDROOM, polygon=_rect(0, 0, 144, 120), area_sf=120.0, has_window=True, window_area_sf=15.0),
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(144, 0, 180, 48), area_sf=60.0, clear_width_in=48.0, occupant_load=20),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(324, 0, 80, 80), area_sf=44.4),
        ],
        doors=[
            Door(id="D1", from_space="R1", to_space="C1", clear_opening_in=34.0, latch_clearance_in=18.0),
            Door(id="D2", from_space="C1", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=18.0),
        ],
        topology=[
            TopologyEdge(source="R1", target="C1", via="D1", is_egress=True),
            TopologyEdge(source="C1", target="ENTRY_1", via="D2", is_egress=True),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_2BR_central_core", mutation="moderate_travel_40ft"),
    ))

    # 4. EG-FAIL-02: Isolated room with no exit path
    cases.append(LayoutTestCase(
        case_id="ASTG-US-EG-FAIL-02",
        seed=204,
        jurisdiction=jurisdiction,
        unit_type="STUDIO",
        spaces=[
            Space(id="R1", type=SpaceType.LIVING, polygon=_rect(0, 0, 180, 144), area_sf=180.0, has_window=True, window_area_sf=20.0),
            Space(id="STAIR_1", type=SpaceType.STAIRWELL, polygon=_rect(300, 0, 100, 100), area_sf=69.4),
        ],
        doors=[],
        topology=[],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="IBC_1006.2", element="R1", measured=9999.0, threshold=75.0, units="feet", severity=ViolationSeverity.LIFE_SAFETY)],
        provenance=CaseProvenance(base_typology="US_studio_isolated", mutation="disconnected_topology_trap"),
    ))

    # 5. EG-PASS-03: Dual exit redundancy (3 hops = ~60 ft <= 75 ft)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-EG-PASS-03",
        seed=205,
        jurisdiction=jurisdiction,
        unit_type="3BR",
        spaces=[
            Space(id="R1", type=SpaceType.LIVING, polygon=_rect(0, 0, 200, 160), area_sf=222.2, has_window=True, window_area_sf=25.0),
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(200, 0, 150, 48), area_sf=50.0, clear_width_in=48.0, occupant_load=40),
            Space(id="STAIR_NORTH", type=SpaceType.STAIRWELL, polygon=_rect(350, 0, 80, 80), area_sf=44.4),
        ],
        doors=[
            Door(id="D1", from_space="R1", to_space="C1", clear_opening_in=36.0, latch_clearance_in=18.0),
            Door(id="D2", from_space="C1", to_space="STAIR_NORTH", clear_opening_in=36.0, latch_clearance_in=18.0),
        ],
        topology=[
            TopologyEdge(source="R1", target="C1", via="D1", is_egress=True),
            TopologyEdge(source="C1", target="STAIR_NORTH", via="D2", is_egress=True),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_3BR_dual_exit", mutation="dual_exit_accessible"),
    ))

    # 6. EG-FAIL-03: Excessive corridor traversal (5 hops = ~100 ft > 75 ft)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-EG-FAIL-03",
        seed=206,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="R1", type=SpaceType.BEDROOM, polygon=_rect(0, 0, 140, 120), area_sf=116.7, has_window=True, window_area_sf=14.0),
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(140, 0, 100, 48), area_sf=33.3, clear_width_in=48.0, occupant_load=20),
            Space(id="C2", type=SpaceType.CORRIDOR, polygon=_rect(240, 0, 100, 48), area_sf=33.3, clear_width_in=48.0, occupant_load=20),
            Space(id="C3", type=SpaceType.CORRIDOR, polygon=_rect(340, 0, 100, 48), area_sf=33.3, clear_width_in=48.0, occupant_load=20),
            Space(id="C4", type=SpaceType.CORRIDOR, polygon=_rect(440, 0, 100, 48), area_sf=33.3, clear_width_in=48.0, occupant_load=20),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(540, 0, 80, 80), area_sf=44.4),
        ],
        doors=[
            Door(id="D1", from_space="R1", to_space="C1", clear_opening_in=34.0, latch_clearance_in=18.0),
            Door(id="D2", from_space="C1", to_space="C2", clear_opening_in=48.0, latch_clearance_in=18.0),
            Door(id="D3", from_space="C2", to_space="C3", clear_opening_in=48.0, latch_clearance_in=18.0),
            Door(id="D4", from_space="C3", to_space="C4", clear_opening_in=48.0, latch_clearance_in=18.0),
            Door(id="D5", from_space="C4", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=18.0),
        ],
        topology=[
            TopologyEdge(source="R1", target="C1", via="D1", is_egress=True),
            TopologyEdge(source="C1", target="C2", via="D2", is_egress=True),
            TopologyEdge(source="C2", target="C3", via="D3", is_egress=True),
            TopologyEdge(source="C3", target="C4", via="D4", is_egress=True),
            TopologyEdge(source="C4", target="ENTRY_1", via="D5", is_egress=True),
        ],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="IBC_1006.2", element="R1", measured=100.0, threshold=75.0, units="feet", severity=ViolationSeverity.LIFE_SAFETY)],
        provenance=CaseProvenance(base_typology="US_2BR_linear_run", mutation="travel_distance_100ft"),
    ))

    return cases


# -----------------------------------------------------------------------------
# Family 3: ADA 604 Water Closet Clearance (6 cases: 3 PASS, 3 FAIL)
# -----------------------------------------------------------------------------
def make_ada_wc_cases() -> list[LayoutTestCase]:
    cases = []
    jurisdiction = Jurisdiction(code_edition="ADA 2010", section="604", source_url="https://www.ada.gov")

    # 1. WC-PASS-01: Pass-near (62" width x 58" depth, required 60" x 56")
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WC-PASS-01",
        seed=301,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(0, 0, 62, 58), area_sf=25.0, is_accessible=True),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_1BR_accessible_bath", mutation="clearance_62x58in"),
    ))

    # 2. WC-FAIL-01: Fail-near (58" width x 58" depth, side clearance < 60")
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WC-FAIL-01",
        seed=302,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(0, 0, 58, 58), area_sf=23.4, is_accessible=True),
        ],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="ADA_604", element="BATH_1", measured=58.0, threshold=60.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS)],
        provenance=CaseProvenance(base_typology="US_1BR_accessible_bath", mutation="side_clearance_narrow_58in"),
    ))

    # 3. WC-PASS-02: Generous bathroom (72" x 66" full turning circle)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WC-PASS-02",
        seed=303,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(0, 0, 72, 66), area_sf=33.0, is_accessible=True),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_2BR_primary_bath", mutation="generous_accessible_72x66in"),
    ))

    # 4. WC-FAIL-02: Fail-obvious (48" x 48" tight powder room)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WC-FAIL-02",
        seed=304,
        jurisdiction=jurisdiction,
        unit_type="STUDIO",
        spaces=[
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(0, 0, 48, 48), area_sf=16.0, is_accessible=True),
        ],
        expected_label="FAIL",
        expected_violations=[
            ExpectedViolation(rule_id="ADA_604", element="BATH_1", measured=48.0, threshold=60.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS),
            ExpectedViolation(rule_id="ADA_604", element="BATH_1", measured=48.0, threshold=56.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS),
        ],
        provenance=CaseProvenance(base_typology="US_studio_powder", mutation="severe_pinch_48x48in"),
    ))

    # 5. WC-PASS-03: Standard 5'x8' bathroom (60" x 96" fully compliant)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WC-PASS-03",
        seed=305,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(0, 0, 96, 60), area_sf=40.0, is_accessible=True),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_standard_5x8_bath", mutation="standard_fha_96x60in"),
    ))

    # 6. WC-FAIL-03: Rear clearance violation (64" width x 50" depth, rear < 56")
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WC-FAIL-03",
        seed=306,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(0, 0, 64, 50), area_sf=22.2, is_accessible=True),
        ],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="ADA_604", element="BATH_1", measured=50.0, threshold=56.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS)],
        provenance=CaseProvenance(base_typology="US_1BR_shallow_bath", mutation="rear_clearance_50in"),
    ))

    return cases


# -----------------------------------------------------------------------------
# Family 4: ADA 404 Door Maneuvering Clearance (6 cases: 3 PASS, 3 FAIL)
# -----------------------------------------------------------------------------
def make_ada_door_cases() -> list[LayoutTestCase]:
    cases = []
    jurisdiction = Jurisdiction(code_edition="ADA 2010", section="404", source_url="https://www.ada.gov")

    # 1. DOOR-PASS-01: Pass-near (34" clear, 18.5" latch)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-DOOR-PASS-01",
        seed=401,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 180, 144), area_sf=180.0, has_window=True, window_area_sf=20.0),
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(180, 0, 144, 144), area_sf=144.0, has_window=True, window_area_sf=16.0),
        ],
        doors=[Door(id="D_BR1", from_space="LIVING_1", to_space="BEDROOM_1", clear_opening_in=34.0, latch_clearance_in=18.5)],
        topology=[TopologyEdge(source="LIVING_1", target="BEDROOM_1", via="D_BR1")],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_1BR_unit", mutation="clearance_34_18.5in"),
    ))

    # 2. DOOR-FAIL-01: Fail-near (30" clear < 32", 14" latch < 18")
    cases.append(LayoutTestCase(
        case_id="ASTG-US-DOOR-FAIL-01",
        seed=402,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 180, 144), area_sf=180.0, has_window=True, window_area_sf=20.0),
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(180, 0, 144, 144), area_sf=144.0, has_window=True, window_area_sf=16.0),
        ],
        doors=[Door(id="D_BR1", from_space="LIVING_1", to_space="BEDROOM_1", clear_opening_in=30.0, latch_clearance_in=14.0)],
        topology=[TopologyEdge(source="LIVING_1", target="BEDROOM_1", via="D_BR1")],
        expected_label="FAIL",
        expected_violations=[
            ExpectedViolation(rule_id="ADA_404", element="D_BR1", measured=30.0, threshold=32.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS),
            ExpectedViolation(rule_id="ADA_404", element="D_BR1", measured=14.0, threshold=18.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS),
        ],
        provenance=CaseProvenance(base_typology="US_1BR_unit", mutation="narrow_opening_30in"),
    ))

    # 3. DOOR-PASS-02: Generous 36" commercial-grade entry door
    cases.append(LayoutTestCase(
        case_id="ASTG-US-DOOR-PASS-02",
        seed=403,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(0, 0, 72, 72), area_sf=36.0),
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(72, 0, 200, 150), area_sf=208.3, has_window=True, window_area_sf=25.0),
        ],
        doors=[Door(id="D_MAIN", from_space="ENTRY_1", to_space="LIVING_1", clear_opening_in=36.0, latch_clearance_in=24.0)],
        topology=[TopologyEdge(source="ENTRY_1", target="LIVING_1", via="D_MAIN")],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_2BR_entry", mutation="wide_door_36in"),
    ))

    # 4. DOOR-FAIL-02: Latch side clearance failure only (34" clear, but 12" latch < 18")
    cases.append(LayoutTestCase(
        case_id="ASTG-US-DOOR-FAIL-02",
        seed=404,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="HALL_1", type=SpaceType.HALLWAY, polygon=_rect(0, 0, 120, 48), area_sf=40.0),
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(120, 0, 140, 140), area_sf=136.1, has_window=True, window_area_sf=15.0),
        ],
        doors=[Door(id="D_BR1", from_space="HALL_1", to_space="BEDROOM_1", clear_opening_in=34.0, latch_clearance_in=12.0)],
        topology=[TopologyEdge(source="HALL_1", target="BEDROOM_1", via="D_BR1")],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="ADA_404", element="D_BR1", measured=12.0, threshold=18.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS)],
        provenance=CaseProvenance(base_typology="US_1BR_hallway", mutation="latch_clearance_fail_12in"),
    ))

    # 5. DOOR-PASS-03: Sliding pocket door on accessible path (34" clear opening, 0" latch allowed for sliding)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-DOOR-PASS-03",
        seed=405,
        jurisdiction=jurisdiction,
        unit_type="STUDIO",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 180, 160), area_sf=200.0, has_window=True, window_area_sf=22.0),
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(180, 0, 72, 60), area_sf=30.0, is_accessible=True),
        ],
        doors=[Door(id="D_BATH", from_space="LIVING_1", to_space="BATH_1", door_type=DoorType.SLIDING, clear_opening_in=34.0, latch_clearance_in=20.0)],
        topology=[TopologyEdge(source="LIVING_1", target="BATH_1", via="D_BATH")],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_studio_pocket", mutation="sliding_door_34in"),
    ))

    # 6. DOOR-FAIL-03: 28" narrow closet/utility door repurposed on accessible route
    cases.append(LayoutTestCase(
        case_id="ASTG-US-DOOR-FAIL-03",
        seed=406,
        jurisdiction=jurisdiction,
        unit_type="STUDIO",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 180, 160), area_sf=200.0, has_window=True, window_area_sf=22.0),
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(180, 0, 72, 60), area_sf=30.0, is_accessible=True),
        ],
        doors=[Door(id="D_BATH", from_space="LIVING_1", to_space="BATH_1", door_type=DoorType.HINGED, clear_opening_in=28.0, latch_clearance_in=10.0)],
        topology=[TopologyEdge(source="LIVING_1", target="BATH_1", via="D_BATH")],
        expected_label="FAIL",
        expected_violations=[
            ExpectedViolation(rule_id="ADA_404", element="D_BATH", measured=28.0, threshold=32.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS),
            ExpectedViolation(rule_id="ADA_404", element="D_BATH", measured=10.0, threshold=18.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS),
        ],
        provenance=CaseProvenance(base_typology="US_studio_narrow", mutation="substandard_opening_28in"),
    ))

    return cases


# -----------------------------------------------------------------------------
# Family 5: Daylight WFR >= 10% (6 cases: 3 PASS, 3 FAIL)
# -----------------------------------------------------------------------------
def make_daylight_cases() -> list[LayoutTestCase]:
    cases = []
    jurisdiction = Jurisdiction(code_edition="LEED v4.1 (voluntary)", section="EQ Credit: Daylight", source_url="https://www.usgbc.org")

    # 1. WFR-PASS-01: Pass-near (11.1% WFR, 16 sf glazing on 144 sf bedroom)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WFR-PASS-01",
        seed=501,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(0, 0, 144, 144), area_sf=144.0, has_window=True, window_area_sf=16.0),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_1BR_bedroom", mutation="wfr_11pct_pass"),
    ))

    # 2. WFR-FAIL-01: Fail-near (8.3% WFR, 12 sf glazing on 144 sf bedroom)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WFR-FAIL-01",
        seed=502,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(0, 0, 144, 144), area_sf=144.0, has_window=True, window_area_sf=12.0),
        ],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="WFR_10PCT", element="BEDROOM_1", measured=0.0833, threshold=0.10, units="ratio", severity=ViolationSeverity.VOLUNTARY)],
        provenance=CaseProvenance(base_typology="US_1BR_bedroom", mutation="wfr_8pct_fail"),
    ))

    # 3. WFR-PASS-02: Generous daylight (18.8% WFR in corner living room)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WFR-PASS-02",
        seed=503,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 192, 144), area_sf=192.0, has_window=True, window_area_sf=36.0),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_2BR_corner_living", mutation="generous_wfr_19pct"),
    ))

    # 4. WFR-FAIL-02: Interior landlocked bedroom with no exterior window
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WFR-FAIL-02",
        seed=504,
        jurisdiction=jurisdiction,
        unit_type="STUDIO",
        spaces=[
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(0, 0, 144, 120), area_sf=120.0, has_window=False, window_area_sf=0.0),
        ],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="WFR_10PCT", element="BEDROOM_1", measured=0.0, threshold=0.10, units="ratio", severity=ViolationSeverity.VOLUNTARY)],
        provenance=CaseProvenance(base_typology="US_studio_den", mutation="windowless_bedroom"),
    ))

    # 5. WFR-PASS-03: Two habitable rooms both passing (Living 15%, BR 12%)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WFR-PASS-03",
        seed=505,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 200, 150), area_sf=208.3, has_window=True, window_area_sf=32.0),
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(200, 0, 140, 140), area_sf=136.1, has_window=True, window_area_sf=18.0),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_1BR_suite", mutation="multi_room_daylight_pass"),
    ))

    # 6. WFR-FAIL-03: One passing living room, one failing kitchen/nook (5% WFR)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-WFR-FAIL-03",
        seed=506,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 200, 150), area_sf=208.3, has_window=True, window_area_sf=32.0),
            Space(id="KITCHEN_1", type=SpaceType.KITCHEN, polygon=_rect(200, 0, 120, 100), area_sf=83.3, has_window=True, window_area_sf=4.0),
        ],
        expected_label="FAIL",
        expected_violations=[ExpectedViolation(rule_id="WFR_10PCT", element="KITCHEN_1", measured=0.048, threshold=0.10, units="ratio", severity=ViolationSeverity.VOLUNTARY)],
        provenance=CaseProvenance(base_typology="US_2BR_open_kitchen", mutation="kitchen_underglazed_5pct"),
    ))

    return cases


# -----------------------------------------------------------------------------
# Family 6: Compound Multi-Rule Interacting Cases (6 cases: 3 PASS, 3 FAIL)
# -----------------------------------------------------------------------------
def make_compound_cases() -> list[LayoutTestCase]:
    cases = []
    jurisdiction = Jurisdiction(code_edition="IBC 2024 / ADA 2010", section="Composite", source_url="https://codes.iccsafe.org")

    # 1. CMP-PASS-01: Complete 1BR apartment passing all IBC, ADA, and LEED rules
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CMP-PASS-01",
        seed=601,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 240, 48), area_sf=80.0, clear_width_in=48.0, occupant_load=40),
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 48, 200, 150), area_sf=208.3, has_window=True, window_area_sf=28.0),
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(200, 48, 140, 140), area_sf=136.1, has_window=True, window_area_sf=18.0),
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(200, 188, 80, 64), area_sf=35.6, is_accessible=True),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(240, 0, 60, 48), area_sf=20.0),
        ],
        doors=[
            Door(id="D_MAIN", from_space="C1", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=18.0),
            Door(id="D_LIVING", from_space="C1", to_space="LIVING_1", clear_opening_in=34.0, latch_clearance_in=18.0),
            Door(id="D_BR1", from_space="LIVING_1", to_space="BEDROOM_1", clear_opening_in=34.0, latch_clearance_in=18.0),
            Door(id="D_BATH", from_space="BEDROOM_1", to_space="BATH_1", clear_opening_in=34.0, latch_clearance_in=18.0),
        ],
        topology=[
            TopologyEdge(source="C1", target="ENTRY_1", via="D_MAIN", is_egress=True),
            TopologyEdge(source="C1", target="LIVING_1", via="D_LIVING"),
            TopologyEdge(source="LIVING_1", target="BEDROOM_1", via="D_BR1"),
            TopologyEdge(source="BEDROOM_1", target="BATH_1", via="D_BATH"),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_1BR_full_suite", mutation="fully_compliant_baseline"),
    ))

    # 2. CMP-FAIL-01: 1BR with corridor narrow + bathroom pinch (2 interacting violations)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CMP-FAIL-01",
        seed=602,
        jurisdiction=jurisdiction,
        unit_type="1BR",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 240, 42), area_sf=70.0, clear_width_in=42.0, occupant_load=60),
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(0, 42, 54, 54), area_sf=20.3, is_accessible=True),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(240, 0, 60, 42), area_sf=17.5),
        ],
        doors=[Door(id="D1", from_space="C1", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=18.0)],
        topology=[TopologyEdge(source="C1", target="ENTRY_1", via="D1", is_egress=True)],
        expected_label="FAIL",
        expected_violations=[
            ExpectedViolation(rule_id="IBC_1020.2", element="C1", measured=42.0, threshold=44.0, severity=ViolationSeverity.LIFE_SAFETY),
            ExpectedViolation(rule_id="ADA_604", element="BATH_1", measured=54.0, threshold=60.0, severity=ViolationSeverity.CIVIL_RIGHTS),
        ],
        provenance=CaseProvenance(base_typology="US_1BR_full_suite", mutation="compound_corridor_and_wc_violation"),
    ))

    # 3. CMP-PASS-02: Complete 2BR family unit passing all checks
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CMP-PASS-02",
        seed=603,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 300, 50), area_sf=104.2, clear_width_in=50.0, occupant_load=50),
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 50, 220, 160), area_sf=244.4, has_window=True, window_area_sf=35.0),
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(220, 50, 150, 140), area_sf=145.8, has_window=True, window_area_sf=20.0),
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(220, 190, 96, 60), area_sf=40.0, is_accessible=True),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(300, 0, 70, 50), area_sf=24.3),
        ],
        doors=[
            Door(id="D_MAIN", from_space="C1", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=20.0),
            Door(id="D_LIVING", from_space="C1", to_space="LIVING_1", clear_opening_in=36.0, latch_clearance_in=18.0),
            Door(id="D_BR1", from_space="LIVING_1", to_space="BEDROOM_1", clear_opening_in=34.0, latch_clearance_in=18.0),
            Door(id="D_BATH", from_space="LIVING_1", to_space="BATH_1", clear_opening_in=34.0, latch_clearance_in=18.0),
        ],
        topology=[
            TopologyEdge(source="C1", target="ENTRY_1", via="D_MAIN", is_egress=True),
            TopologyEdge(source="C1", target="LIVING_1", via="D_LIVING"),
            TopologyEdge(source="LIVING_1", target="BEDROOM_1", via="D_BR1"),
            TopologyEdge(source="LIVING_1", target="BATH_1", via="D_BATH"),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_2BR_family_suite", mutation="2br_compliant_baseline"),
    ))

    # 4. CMP-FAIL-02: 2BR unit with narrow door (30") + insufficient bedroom daylight (7% WFR)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CMP-FAIL-02",
        seed=604,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 200, 150), area_sf=208.3, has_window=True, window_area_sf=30.0),
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(200, 0, 140, 140), area_sf=136.1, has_window=True, window_area_sf=10.0),
        ],
        doors=[Door(id="D_BR1", from_space="LIVING_1", to_space="BEDROOM_1", clear_opening_in=30.0, latch_clearance_in=18.0)],
        topology=[TopologyEdge(source="LIVING_1", target="BEDROOM_1", via="D_BR1")],
        expected_label="FAIL",
        expected_violations=[
            ExpectedViolation(rule_id="ADA_404", element="D_BR1", measured=30.0, threshold=32.0, units="inches", severity=ViolationSeverity.CIVIL_RIGHTS),
            ExpectedViolation(rule_id="WFR_10PCT", element="BEDROOM_1", measured=0.0735, threshold=0.10, units="ratio", severity=ViolationSeverity.VOLUNTARY),
        ],
        provenance=CaseProvenance(base_typology="US_2BR_family_suite", mutation="compound_door_and_daylight_violation"),
    ))

    # 5. CMP-PASS-03: Compact studio layout passing all checks
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CMP-PASS-03",
        seed=605,
        jurisdiction=jurisdiction,
        unit_type="STUDIO",
        spaces=[
            Space(id="LIVING_1", type=SpaceType.LIVING, polygon=_rect(0, 0, 220, 180), area_sf=275.0, has_window=True, window_area_sf=35.0),
            Space(id="BATH_1", type=SpaceType.BATHROOM, polygon=_rect(220, 0, 72, 60), area_sf=30.0, is_accessible=True),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(0, 180, 60, 60), area_sf=25.0),
        ],
        doors=[
            Door(id="D_ENTRY", from_space="ENTRY_1", to_space="LIVING_1", clear_opening_in=36.0, latch_clearance_in=18.0),
            Door(id="D_BATH", from_space="LIVING_1", to_space="BATH_1", clear_opening_in=34.0, latch_clearance_in=18.0),
        ],
        topology=[
            TopologyEdge(source="ENTRY_1", target="LIVING_1", via="D_ENTRY", is_egress=True),
            TopologyEdge(source="LIVING_1", target="BATH_1", via="D_BATH"),
        ],
        expected_label="PASS",
        provenance=CaseProvenance(base_typology="US_studio_efficient", mutation="studio_compliant_baseline"),
    ))

    # 6. CMP-FAIL-03: Triple-violation torture case (Corridor narrow + door latch pinch + windowless bedroom)
    cases.append(LayoutTestCase(
        case_id="ASTG-US-CMP-FAIL-03",
        seed=606,
        jurisdiction=jurisdiction,
        unit_type="2BR",
        spaces=[
            Space(id="C1", type=SpaceType.CORRIDOR, polygon=_rect(0, 0, 240, 40), area_sf=66.7, clear_width_in=40.0, occupant_load=60),
            Space(id="BEDROOM_1", type=SpaceType.BEDROOM, polygon=_rect(0, 40, 140, 120), area_sf=116.7, has_window=False, window_area_sf=0.0),
            Space(id="ENTRY_1", type=SpaceType.ENTRY, polygon=_rect(240, 0, 60, 40), area_sf=16.7),
        ],
        doors=[
            Door(id="D_ENTRY", from_space="C1", to_space="ENTRY_1", clear_opening_in=36.0, latch_clearance_in=18.0),
            Door(id="D_BR1", from_space="C1", to_space="BEDROOM_1", clear_opening_in=34.0, latch_clearance_in=12.0),
        ],
        topology=[
            TopologyEdge(source="C1", target="ENTRY_1", via="D_ENTRY", is_egress=True),
            TopologyEdge(source="C1", target="BEDROOM_1", via="D_BR1"),
        ],
        expected_label="FAIL",
        expected_violations=[
            ExpectedViolation(rule_id="IBC_1020.2", element="C1", measured=40.0, threshold=44.0, severity=ViolationSeverity.LIFE_SAFETY),
            ExpectedViolation(rule_id="ADA_404", element="D_BR1", measured=12.0, threshold=18.0, severity=ViolationSeverity.CIVIL_RIGHTS),
            ExpectedViolation(rule_id="WFR_10PCT", element="BEDROOM_1", measured=0.0, threshold=0.10, severity=ViolationSeverity.VOLUNTARY),
        ],
        provenance=CaseProvenance(base_typology="US_2BR_corridor", mutation="triple_torture_case"),
    ))

    return cases


def generate_all(output_dir: Path) -> list[LayoutTestCase]:
    """Generate all 36 canonical test cases and save as JSON files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    all_cases: list[LayoutTestCase] = []
    all_cases.extend(make_corridor_cases())    # 6 cases
    all_cases.extend(make_egress_cases())      # 6 cases
    all_cases.extend(make_ada_wc_cases())      # 6 cases
    all_cases.extend(make_ada_door_cases())    # 6 cases
    all_cases.extend(make_daylight_cases())    # 6 cases
    all_cases.extend(make_compound_cases())    # 6 cases

    pass_count = sum(1 for c in all_cases if c.expected_label == "PASS")
    fail_count = sum(1 for c in all_cases if c.expected_label == "FAIL")

    for case in all_cases:
        file_name = f"{case.case_id.replace('ASTG-US-', '')}.json"
        file_path = output_dir / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(case.model_dump(), f, indent=2)

    # Generate sha256 manifest
    import hashlib
    manifest_path = output_dir.parent / "manifest.sha256"
    with open(manifest_path, "w", encoding="utf-8") as mf:
        for case in all_cases:
            file_name = f"{case.case_id.replace('ASTG-US-', '')}.json"
            content = (output_dir / file_name).read_bytes()
            h = hashlib.sha256(content).hexdigest()
            mf.write(f"{h}  cases/{file_name}\n")

    print(f"Generated {len(all_cases)} test cases ({pass_count} PASS, {fail_count} FAIL) in {output_dir}")
    print(f"Manifest written to {manifest_path}")
    return all_cases


if __name__ == "__main__":
    target = Path(__file__).parent.parent.parent / "data" / "v0.1" / "cases"
    generate_all(target)
