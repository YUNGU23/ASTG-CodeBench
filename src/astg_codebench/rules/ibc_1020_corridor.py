"""IBC 2024 §1020 — Corridor minimum clear width.

Functional paraphrase: Corridors serving an occupant load of 50 or more
shall have a minimum clear width of 44 inches. Corridors serving an
occupant load less than 50 may have a minimum clear width of 36 inches.

Note: Section identifier only. Full code text is copyrighted by ICC;
consult the locally adopted edition for authoritative requirements.
"""
from __future__ import annotations

from astg_codebench.schemas.layout import LayoutTestCase, SpaceType, ViolationSeverity
from astg_codebench.schemas.rule import CodeRule, Violation

RULE = CodeRule(
    rule_id="IBC_1020.2",
    name="Corridor Minimum Clear Width",
    category="egress",
    severity=ViolationSeverity.LIFE_SAFETY,
    code_edition="IBC 2024",
    section="1020.2",
    description=(
        "Corridors serving occupant load >= 50 require minimum 44-inch clear width; "
        "corridors serving occupant load < 50 require minimum 36-inch clear width."
    ),
    threshold_value=44.0,
    threshold_unit="inches",
    comparison="gte",
)

THRESHOLD_HIGH = 44.0  # OL >= 50
THRESHOLD_LOW = 36.0   # OL < 50


def evaluate(case: LayoutTestCase) -> list[Violation]:
    """Check all corridors in the layout against IBC 1020.2."""
    violations: list[Violation] = []
    for space in case.spaces:
        if space.type != SpaceType.CORRIDOR:
            continue
        if space.clear_width_in is None:
            continue

        occupant_load = space.occupant_load or 0
        threshold = THRESHOLD_HIGH if occupant_load >= 50 else THRESHOLD_LOW

        if space.clear_width_in < threshold:
            violations.append(
                Violation(
                    rule_id=RULE.rule_id,
                    element_id=space.id,
                    measured_value=space.clear_width_in,
                    threshold_value=threshold,
                    units="inches",
                    severity=ViolationSeverity.LIFE_SAFETY,
                    message=(
                        f"Corridor '{space.id}' clear width {space.clear_width_in}\" "
                        f"is below the required {threshold}\" "
                        f"(occupant load: {occupant_load})."
                    ),
                )
            )
    return violations
