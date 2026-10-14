"""Pydantic v2 data models for the Adjacency Spatial Topological Graph (ASTG).

These schemas define the canonical representation of multifamily floor-plan
test cases used throughout the ASTG-CodeBench benchmark suite.
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SpaceType(str, Enum):
    """Functional classification of architectural spaces."""
    BEDROOM = "bedroom"
    LIVING = "living"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    CORRIDOR = "corridor"
    HALLWAY = "hallway"
    STAIRWELL = "stairwell"
    ENTRY = "entry"
    CLOSET = "closet"
    BALCONY = "balcony"
    UTILITY = "utility"


class DoorType(str, Enum):
    """Door operation type affecting maneuvering clearance requirements."""
    HINGED = "hinged"
    SLIDING = "sliding"
    POCKET = "pocket"
    DOUBLE = "double"


class ViolationSeverity(str, Enum):
    """Regulatory severity classification."""
    LIFE_SAFETY = "life_safety"       # IBC means-of-egress: mandatory
    CIVIL_RIGHTS = "civil_rights"     # ADA/FHA accessibility: mandatory
    VOLUNTARY = "voluntary"           # LEED/green criteria: optional


class Point2D(BaseModel):
    """A 2D coordinate point in inches."""
    x: float
    y: float


class Space(BaseModel):
    """A named architectural space with geometry and attributes."""
    id: str = Field(..., description="Unique space identifier (e.g., 'R1', 'C1')")
    type: SpaceType
    polygon: list[Point2D] = Field(..., min_length=3, description="Boundary polygon vertices in inches")
    area_sf: float = Field(..., gt=0, description="Floor area in square feet")
    clear_width_in: Optional[float] = Field(None, description="Minimum clear width in inches (corridors)")
    occupant_load: Optional[int] = Field(None, ge=0, description="Calculated occupant load")
    has_window: bool = Field(False, description="Whether space has an exterior window")
    window_area_sf: Optional[float] = Field(None, ge=0, description="Window glazing area in sq ft")
    is_accessible: bool = Field(True, description="Whether space is on an accessible route")


class Door(BaseModel):
    """A door connecting two spaces with accessibility-relevant dimensions."""
    id: str = Field(..., description="Unique door identifier")
    from_space: str = Field(..., description="Source space ID")
    to_space: str = Field(..., description="Destination space ID")
    door_type: DoorType = DoorType.HINGED
    clear_opening_in: float = Field(..., gt=0, description="Clear opening width in inches")
    latch_clearance_in: Optional[float] = Field(None, ge=0, description="Latch-side maneuvering clearance in inches")


class TopologyEdge(BaseModel):
    """An edge in the spatial adjacency graph."""
    source: str
    target: str
    via: Optional[str] = Field(None, description="Door ID connecting these spaces")
    is_egress: bool = Field(False, description="Whether this edge is part of an egress route")
    is_accessible: bool = Field(True, description="Whether this edge is on an accessible route")


class Jurisdiction(BaseModel):
    """Regulatory jurisdiction and code edition metadata."""
    country: str = "US"
    code_edition: str = Field(..., description="e.g., 'IBC 2024'")
    section: str = Field(..., description="e.g., '1020.2'")
    source_url: Optional[str] = Field(None, description="Public URL for code reference")


class ExpectedViolation(BaseModel):
    """A ground-truth violation annotation."""
    rule_id: str = Field(..., description="e.g., 'IBC_1020.2'")
    element: str = Field(..., description="ID of the violating space or door")
    measured: float = Field(..., description="Actual measured value")
    threshold: float = Field(..., description="Code-required minimum or maximum")
    units: str = "inches"
    severity: ViolationSeverity


class CaseProvenance(BaseModel):
    """Generation provenance for reproducibility."""
    generation_method: str = "parametric_perturbation"
    base_typology: str = Field(..., description="e.g., 'US_2BR_double_loaded_corridor'")
    mutation: str = Field(..., description="e.g., 'corridor_width_minus_1in'")


class LayoutTestCase(BaseModel):
    """A complete ASTG-CodeBench test case with geometry, topology, and ground truth."""
    case_id: str = Field(..., pattern=r"^ASTG-US-[A-Z]{2,4}-(?:PASS|FAIL)-\d{2}$")
    version: str = "0.1.0"
    seed: int = Field(..., description="Deterministic random seed for reproducibility")
    jurisdiction: Jurisdiction
    building_type: str = "R-2 Multifamily"
    unit_type: str = Field(..., description="e.g., '1BR', '2BR', 'STUDIO'")
    spaces: list[Space] = Field(..., min_length=1)
    doors: list[Door] = Field(default_factory=list)
    topology: list[TopologyEdge] = Field(default_factory=list)
    expected_label: str = Field(..., pattern=r"^(PASS|FAIL)$")
    expected_violations: list[ExpectedViolation] = Field(default_factory=list)
    oracle_version: Optional[str] = None
    provenance: CaseProvenance
