"""ADA 2010 §404 — Door maneuvering clearance.

Functional paraphrase: Doorways on accessible routes shall provide a
minimum clear opening of 32 inches. The latch side of the door shall
have a minimum 18-inch maneuvering clearance on the pull side.

Note: Section identifier only. Consult 2010 ADA Standards for Accessible Design.
"""
from __future__ import annotations

from astg_codebench.schemas.layout import LayoutTestCase, ViolationSeverity
from astg_codebench.schemas.rule import CodeRule, Violation

RULE = CodeRule(
    rule_id="ADA_404",
    name="Door Maneuvering Clearance",
    category="accessibility",
    severity=ViolationSeverity.CIVIL_RIGHTS,
    code_edition="ADA 2010",
    section="404",
    description=(
        "Doors on accessible routes: minimum 32-inch clear opening; "
        "minimum 18-inch latch-side maneuvering clearance (pull side)."
    ),
    threshold_value=32.0,
    threshold_unit="inches",
    comparison="gte",
)

MIN_CLEAR_OPENING_IN = 32.0
MIN_LATCH_CLEARANCE_IN = 18.0


def evaluate(case: LayoutTestCase) -> list[Violation]:
    """Check all doors for ADA 404 maneuvering clearance."""
    violations: list[Violation] = []
    # Build a set of accessible space IDs
    accessible_spaces = {
        s.id for s in case.spaces if s.is_accessible
    }

    for door in case.doors:
        # Only check doors on accessible routes
        if door.from_space not in accessible_spaces and door.to_space not in accessible_spaces:
            continue

        if door.clear_opening_in < MIN_CLEAR_OPENING_IN:
            violations.append(
                Violation(
                    rule_id=RULE.rule_id,
                    element_id=door.id,
                    measured_value=door.clear_opening_in,
                    threshold_value=MIN_CLEAR_OPENING_IN,
                    units="inches",
                    severity=ViolationSeverity.CIVIL_RIGHTS,
                    message=(
                        f"Door '{door.id}' clear opening {door.clear_opening_in}\" "
                        f"is below the required {MIN_CLEAR_OPENING_IN}\"."
                    ),
                )
            )

        if (
            door.latch_clearance_in is not None
            and door.latch_clearance_in < MIN_LATCH_CLEARANCE_IN
        ):
            violations.append(
                Violation(
                    rule_id=RULE.rule_id,
                    element_id=door.id,
                    measured_value=door.latch_clearance_in,
                    threshold_value=MIN_LATCH_CLEARANCE_IN,
                    units="inches",
                    severity=ViolationSeverity.CIVIL_RIGHTS,
                    message=(
                        f"Door '{door.id}' latch-side clearance {door.latch_clearance_in}\" "
                        f"is below the required {MIN_LATCH_CLEARANCE_IN}\"."
                    ),
                )
            )
    return violations
