"""ADA 2010 §604 — Water closet (toilet) clearance requirements.

Functional paraphrase: Clearance around water closets shall be a minimum
of 60 inches measured perpendicular from the side wall and 56 inches
measured perpendicular from the rear wall. A 60-inch diameter turning
space is required within the bathroom.

Note: Section identifier only. Full standards text is maintained by the
U.S. Access Board; consult the 2010 ADA Standards for Accessible Design.
"""
from __future__ import annotations

from astg_codebench.schemas.layout import LayoutTestCase, SpaceType, ViolationSeverity
from astg_codebench.schemas.rule import CodeRule, Violation

RULE = CodeRule(
    rule_id="ADA_604",
    name="Water Closet Clearance",
    category="accessibility",
    severity=ViolationSeverity.CIVIL_RIGHTS,
    code_edition="ADA 2010",
    section="604",
    description=(
        "Clearance around water closets: minimum 60 inches from side wall, "
        "56 inches from rear wall. 60-inch turning circle required."
    ),
    threshold_value=60.0,
    threshold_unit="inches",
    comparison="gte",
)

MIN_SIDE_CLEARANCE_IN = 60.0
MIN_REAR_CLEARANCE_IN = 56.0
MIN_TURNING_DIAMETER_IN = 60.0


def evaluate(case: LayoutTestCase) -> list[Violation]:
    """Check bathroom spaces for ADA 604 water closet clearance."""
    violations: list[Violation] = []
    for space in case.spaces:
        if space.type != SpaceType.BATHROOM:
            continue
        if not space.is_accessible:
            continue

        # Use polygon bounding box as simplified clearance proxy
        xs = [p.x for p in space.polygon]
        ys = [p.y for p in space.polygon]
        width = max(xs) - min(xs)
        depth = max(ys) - min(ys)

        # Check side clearance (width dimension)
        side_clearance = max(width, depth)
        rear_clearance = min(width, depth)

        if side_clearance < MIN_SIDE_CLEARANCE_IN:
            violations.append(
                Violation(
                    rule_id=RULE.rule_id,
                    element_id=space.id,
                    measured_value=side_clearance,
                    threshold_value=MIN_SIDE_CLEARANCE_IN,
                    units="inches",
                    severity=ViolationSeverity.CIVIL_RIGHTS,
                    message=(
                        f"Bathroom '{space.id}' side clearance {side_clearance:.1f}\" "
                        f"is below the required {MIN_SIDE_CLEARANCE_IN}\"."
                    ),
                )
            )

        if rear_clearance < MIN_REAR_CLEARANCE_IN:
            violations.append(
                Violation(
                    rule_id=RULE.rule_id,
                    element_id=space.id,
                    measured_value=rear_clearance,
                    threshold_value=MIN_REAR_CLEARANCE_IN,
                    units="inches",
                    severity=ViolationSeverity.CIVIL_RIGHTS,
                    message=(
                        f"Bathroom '{space.id}' rear clearance {rear_clearance:.1f}\" "
                        f"is below the required {MIN_REAR_CLEARANCE_IN}\"."
                    ),
                )
            )
    return violations
