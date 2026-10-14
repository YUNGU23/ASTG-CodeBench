"""Prompt templates for LLM-based architectural compliance baselines."""
from __future__ import annotations

from astg_codebench.schemas.layout import LayoutTestCase

SYSTEM_PROMPT = """You are an expert architectural code compliance auditor specializing in US building codes.
Your task is to analyze the provided multifamily apartment layout and determine whether it complies with the applicable building, accessibility, and daylighting standards.

Applicable Regulatory Provisions:
1. IBC 2024 §1020.2 (Corridor Minimum Width):
   - Corridors serving occupant load >= 50 must have clear width >= 44.0 inches.
   - Corridors serving occupant load < 50 must have clear width >= 36.0 inches.
2. IBC 2024 §1006.2 (Maximum Travel Distance to Exit):
   - Common path travel distance from any occupied room to the nearest exit (stairwell or entry) along the accessible topology shall not exceed 75.0 feet (unsprinklered) or 125.0 feet (sprinklered).
3. ADA 2010 §604 (Water Closet Clearance):
   - Clearance around water closets in accessible bathrooms must be >= 60.0 inches perpendicular from side wall and >= 56.0 inches perpendicular from rear wall.
4. ADA 2010 §404 (Door Maneuvering Clearance):
   - Accessible route doors must provide clear opening width >= 32.0 inches.
   - Latch-side clearance on the pull side must be >= 18.0 inches.
5. LEED v4.1 EQ Credit (Daylight Window-to-Floor Area Ratio):
   - Habitable rooms (bedroom, living, kitchen) must have window glazing area >= 10.0% of room floor area.

Output format requirement:
Respond in JSON format with:
{
  "label": "PASS" or "FAIL",
  "reasoning": "Brief explanation",
  "violations": [
    {
      "rule_id": "e.g. IBC_1020.2",
      "element_id": "e.g. C1",
      "issue": "description of non-compliance"
    }
  ]
}
"""

ZERO_SHOT_USER_TEMPLATE = """Please audit the following residential apartment layout for code compliance:

Case ID: {case_id}
Unit Type: {unit_type}
Building Classification: {building_type}

Spaces / Rooms:
{spaces_summary}

Doors / Openings:
{doors_summary}

Topological Adjacency:
{topology_summary}

Determine if this layout PASSES or FAILS all applicable code provisions. Return your evaluation strictly in the required JSON format.
"""

COT_USER_TEMPLATE = """Please perform a step-by-step regulatory compliance audit on the following residential apartment layout:

Case ID: {case_id}
Unit Type: {unit_type}
Building Classification: {building_type}

Spaces / Rooms:
{spaces_summary}

Doors / Openings:
{doors_summary}

Topological Adjacency:
{topology_summary}

Step-by-step instructions:
Step 1: Check each corridor clear width against IBC §1020.2 occupant load thresholds.
Step 2: Trace egress paths from each occupied space to nearest exit node and calculate travel distance against IBC §1006.2.
Step 3: Check bathroom dimensions against ADA §604 side (60") and rear (56") clearances.
Step 4: Check all doors on accessible routes against ADA §404 clear opening (32") and latch clearance (18").
Step 5: Calculate window-to-floor ratio for habitable spaces against the 10% daylight threshold.
Step 6: Synthesize all findings and output final compliance label (PASS or FAIL) and detected violations.
"""


def format_case_for_prompt(case: LayoutTestCase) -> dict[str, str]:
    """Format a LayoutTestCase into structured string summaries for prompting."""
    spaces_lines = []
    for s in case.spaces:
        details = [f"- {s.id} ({s.type.value}): area={s.area_sf:.1f} sqft"]
        if s.clear_width_in is not None:
            details.append(f"clear_width={s.clear_width_in:.1f} in")
        if s.occupant_load is not None:
            details.append(f"occupant_load={s.occupant_load}")
        if s.has_window:
            w_area = s.window_area_sf or 0.0
            details.append(f"window_area={w_area:.1f} sqft")
        else:
            details.append("no_window")
        spaces_lines.append(", ".join(details))

    doors_lines = []
    for d in case.doors:
        details = [f"- {d.id}: connects {d.from_space} -> {d.to_space}"]
        details.append(f"clear_opening={d.clear_opening_in:.1f} in")
        if d.latch_clearance_in is not None:
            details.append(f"latch_clearance={d.latch_clearance_in:.1f} in")
        doors_lines.append(", ".join(details))

    topo_lines = []
    for e in case.topology:
        egress_tag = " [EGRESS_ROUTE]" if e.is_egress else ""
        via_tag = f" via {e.via}" if e.via else ""
        topo_lines.append(f"- {e.source} <--> {e.target}{via_tag}{egress_tag}")

    return {
        "case_id": case.case_id,
        "unit_type": case.unit_type,
        "building_type": case.building_type,
        "spaces_summary": "\n".join(spaces_lines) if spaces_lines else "None",
        "doors_summary": "\n".join(doors_lines) if doors_lines else "None",
        "topology_summary": "\n".join(topo_lines) if topo_lines else "None",
    }
