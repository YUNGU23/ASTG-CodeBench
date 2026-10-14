"""Window-to-Floor Ratio (WFR) — voluntary daylight criterion.

Functional paraphrase: Habitable rooms should have a window glazing
area of at least 10% of the floor area to provide adequate natural
daylight. This is a voluntary criterion commonly associated with
LEED v4.1 and energy/wellness certifications, not a mandatory
life-safety or civil-rights requirement.

Note: This criterion is explicitly labeled as voluntary.
"""
from __future__ import annotations

from astg_codebench.schemas.layout import LayoutTestCase, SpaceType, ViolationSeverity
from astg_codebench.schemas.rule import CodeRule, Violation

RULE = CodeRule(
    rule_id="WFR_10PCT",
    name="Window-to-Floor Ratio (Daylight)",
    category="environmental",
    severity=ViolationSeverity.VOLUNTARY,
    code_edition="LEED v4.1 (voluntary)",
    section="EQ Credit: Daylight",
    description=(
        "Habitable rooms should have window glazing area >= 10% of floor area "
        "for adequate natural daylight. This is a voluntary performance criterion."
    ),
    threshold_value=0.10,
    threshold_unit="ratio",
    comparison="gte",
)

MIN_WFR = 0.10
HABITABLE_TYPES = {SpaceType.BEDROOM, SpaceType.LIVING, SpaceType.KITCHEN}


def evaluate(case: LayoutTestCase) -> list[Violation]:
    """Check habitable rooms for minimum window-to-floor ratio."""
    violations: list[Violation] = []
    for space in case.spaces:
        if space.type not in HABITABLE_TYPES:
            continue
        if not space.has_window:
            violations.append(
                Violation(
                    rule_id=RULE.rule_id,
                    element_id=space.id,
                    measured_value=0.0,
                    threshold_value=MIN_WFR,
                    units="ratio",
                    severity=ViolationSeverity.VOLUNTARY,
                    message=f"Habitable space '{space.id}' has no window.",
                )
            )
            continue

        window_area = space.window_area_sf or 0.0
        if space.area_sf > 0:
            wfr = window_area / space.area_sf
        else:
            wfr = 0.0

        if wfr < MIN_WFR:
            violations.append(
                Violation(
                    rule_id=RULE.rule_id,
                    element_id=space.id,
                    measured_value=round(wfr, 4),
                    threshold_value=MIN_WFR,
                    units="ratio",
                    severity=ViolationSeverity.VOLUNTARY,
                    message=(
                        f"Habitable space '{space.id}' WFR is {wfr:.1%}, "
                        f"below the recommended {MIN_WFR:.0%}."
                    ),
                )
            )
    return violations
