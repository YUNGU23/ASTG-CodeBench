"""Floor plan visualization and violation rendering engine for ASTG-CodeBench.

Renders ASTG layout test cases as publication-quality vector SVG or PNG diagrams.
Compliant spaces are drawn with clean architectural styling; violations are
automatically highlighted with bold red bounding boxes, alert badges, and rule tags.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless rendering
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Rectangle, FancyBboxPatch

from astg_codebench.schemas.layout import LayoutTestCase, SpaceType
from astg_codebench.schemas.rule import AuditResult
from astg_codebench.engine.oracle import audit as run_audit

# Color palette for architectural spaces
SPACE_COLORS = {
    SpaceType.LIVING: "#EBF5FB",       # Soft blue
    SpaceType.BEDROOM: "#E8F8F5",      # Soft mint
    SpaceType.KITCHEN: "#FEF9E7",      # Soft warm yellow
    SpaceType.BATHROOM: "#F4ECF7",     # Soft lavender
    SpaceType.CORRIDOR: "#F2F4F4",     # Clean light grey
    SpaceType.HALLWAY: "#F2F4F4",      # Clean light grey
    SpaceType.STAIRWELL: "#EAECEE",    # Medium grey
    SpaceType.ENTRY: "#FDFEFE",        # Off-white
    SpaceType.CLOSET: "#EBEDEF",       # Muted grey
    SpaceType.BALCONY: "#D5F5E3",      # Fresh pale green
    SpaceType.UTILITY: "#EAEDED",      # Utility grey
}

VIOLATION_FILL = "#FDEDEC"             # Soft red alert tint
VIOLATION_BORDER = "#E74C3C"           # Strong crimson alert border
DEFAULT_BORDER = "#2C3E50"             # Architectural charcoal line


def render_case(
    case: LayoutTestCase,
    audit_result: Optional[AuditResult] = None,
    output_path: Optional[Path] = None,
    dpi: int = 200,
) -> plt.Figure:
    """Render a single ASTG layout test case with code compliance annotations."""
    if audit_result is None:
        audit_result = run_audit(case)

    # Collect violating element IDs and messages
    violating_elements: dict[str, list[str]] = {}
    for v in audit_result.violations:
        violating_elements.setdefault(v.element_id, []).append(f"{v.rule_id}: {v.message}")

    fig, ax = plt.subplots(figsize=(10, 8), dpi=dpi)
    ax.set_aspect("equal")

    all_xs: list[float] = []
    all_ys: list[float] = []

    # 1. Render Spaces
    for space in case.spaces:
        pts = [(p.x, p.y) for p in space.polygon]
        xs = [p.x for p in space.polygon]
        ys = [p.y for p in space.polygon]
        all_xs.extend(xs)
        all_ys.extend(ys)

        is_violating = space.id in violating_elements

        fill_color = VIOLATION_FILL if is_violating else SPACE_COLORS.get(space.type, "#F8F9F9")
        edge_color = VIOLATION_BORDER if is_violating else DEFAULT_BORDER
        line_width = 2.5 if is_violating else 1.2
        line_style = "-"

        poly = MplPolygon(
            pts,
            closed=True,
            facecolor=fill_color,
            edgecolor=edge_color,
            linewidth=line_width,
            linestyle=line_style,
            zorder=2,
        )
        ax.add_patch(poly)

        # Center label
        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)

        label_text = f"{space.id}\n({space.type.value.capitalize()})\n{space.area_sf:.1f} sqft"
        if space.clear_width_in:
            label_text += f"\nWidth: {space.clear_width_in:.0f}\""

        text_color = "#C0392B" if is_violating else "#34495E"
        font_weight = "bold" if is_violating else "normal"

        ax.text(
            cx, cy,
            label_text,
            ha="center", va="center",
            fontsize=8,
            color=text_color,
            weight=font_weight,
            zorder=4,
        )

        # Add red violation badge if applicable
        if is_violating:
            violation_summary = "\n".join(violating_elements[space.id])
            ax.annotate(
                f"[!] NON-COMPLIANT\n{violation_summary}",
                xy=(cx, cy),
                xytext=(cx, cy + (max(ys) - min(ys)) * 0.35 + 10),
                ha="center",
                fontsize=7,
                weight="bold",
                color="#FFFFFF",
                bbox=dict(boxstyle="round,pad=0.4", fc="#C0392B", ec="#922B21", lw=1.0),
                arrowprops=dict(arrowstyle="->", color="#C0392B", lw=1.5),
                zorder=6,
            )

    # 2. Render Doors
    for door in case.doors:
        is_violating = door.id in violating_elements
        # Find connecting spaces to position door annotation
        door_label = f"Door {door.id} ({door.clear_opening_in:.0f}\")"
        if is_violating:
            door_label += " [VIOLATION]"

    # 3. Overall Title and Banner
    status_color = "#27AE60" if audit_result.label == "PASS" else "#C0392B"
    status_badge = "[PASS] COMPLIANT" if audit_result.label == "PASS" else f"[FAIL] {len(audit_result.violations)} VIOLATION(S)"

    plt.suptitle(
        f"ASTG-CodeBench: {case.case_id} — {status_badge}",
        fontsize=13,
        weight="bold",
        color=status_color,
        y=0.96,
    )
    plt.title(
        f"Typology: {case.provenance.base_typology} | Unit: {case.unit_type} | Code: {case.jurisdiction.code_edition} {case.jurisdiction.section}\n"
        f"Mutation: {case.provenance.mutation}",
        fontsize=9,
        color="#7F8C8D",
        pad=10,
    )

    # Margin bounds
    if all_xs and all_ys:
        pad_x = (max(all_xs) - min(all_xs)) * 0.15 + 20
        pad_y = (max(all_ys) - min(all_ys)) * 0.20 + 20
        ax.set_xlim(min(all_xs) - pad_x, max(all_xs) + pad_x)
        ax.set_ylim(min(all_ys) - pad_y, max(all_ys) + pad_y)

    ax.axis("off")
    plt.tight_layout()

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, bbox_inches="tight", dpi=dpi)
        plt.close(fig)

    return fig


def render_all_cases(cases_dir: Path, output_dir: Path) -> int:
    """Render all JSON cases in a directory to SVG and PNG images."""
    import json
    output_dir.mkdir(parents=True, exist_ok=True)
    rendered_count = 0

    for json_file in sorted(cases_dir.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
        case = LayoutTestCase.model_validate(raw)

        svg_path = output_dir / f"{json_file.stem}.svg"
        render_case(case, output_path=svg_path)
        rendered_count += 1

    print(f"Rendered {rendered_count} floor plans to {output_dir}")
    return rendered_count


if __name__ == "__main__":
    cases = Path(__file__).parent.parent.parent / "data" / "v0.1" / "cases"
    out = Path(__file__).parent.parent.parent / "data" / "v0.1" / "renders"
    render_all_cases(cases, out)
