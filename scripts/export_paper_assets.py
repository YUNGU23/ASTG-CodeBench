"""Export publication-ready LaTeX tables and high-resolution composite figures for Paper 2."""
from __future__ import annotations

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

from astg_codebench.schemas.layout import LayoutTestCase
from astg_codebench.evaluate import load_cases
from astg_codebench.baselines.llm_evaluator import (
    run_benchmark_comparison,
    generate_comparison_latex_table,
)

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "v0.1" / "cases"
OUTPUT_DIR = BASE_DIR / "paper_assets"


def export_table1() -> None:
    """Generate Table 1: Baseline comparison matrix."""
    cases = load_cases(DATA_DIR)
    results = run_benchmark_comparison(cases, synthetic=True)
    latex = generate_comparison_latex_table(results)
    out_file = OUTPUT_DIR / "table1_baseline_comparison.tex"
    out_file.write_text(latex, encoding="utf-8")
    print(f"[OK] Exported Table 1 to {out_file}")


def export_table2_rule_matrix() -> None:
    """Generate Table 2: Formalized Regulatory Predicates Matrix for ASCE JCCE."""
    latex = r"""\begin{table*}[t]
\centering
\small
\caption{Formalized building code compliance predicates implemented in ASTG-CodeBench v0.1.}
\label{tab:rule_predicates}
\begin{tabular}{lllllcc}
\toprule
\textbf{Rule ID} & \textbf{Regulatory Source} & \textbf{Section} & \textbf{Prescriptive Scope} & \textbf{Formal Threshold} & \textbf{Severity} & \textbf{Domain} \\
\midrule
\texttt{IBC\_1020.2} & IBC 2024 & \S 1020.2 & Corridor min. clear passage & $\ge 44.0''$ ($OL \ge 50$); $\ge 36.0''$ ($OL < 50$) & Life Safety & Egress \\
\texttt{IBC\_1006.2} & IBC 2024 & \S 1006.2 & Exit access travel distance & $\le 75.0'\text{ (unsprink.)}; \le 125.0'\text{ (sprink.)}$ & Life Safety & Egress \\
\texttt{ADA\_604}    & ADA 2010 & \S 604    & Water closet clear space    & $\ge 60.0''\text{ side} \times 56.0''\text{ rear}$ & Civil Rights & Accessibility \\
\texttt{ADA\_404}    & ADA 2010 & \S 404    & Door maneuvering clearance  & $\ge 32.0''\text{ opening}, \ge 18.0''\text{ pull-latch}$ & Civil Rights & Accessibility \\
\texttt{WFR\_10PCT}  & LEED v4.1 & EQ Credit & Window-to-floor area ratio  & $\ge 10.0\%$ (habitable spaces) & Voluntary & Daylight \\
\bottomrule
\end{tabular}
\end{table*}
"""
    out_file = OUTPUT_DIR / "table2_rule_predicates.tex"
    out_file.write_text(latex, encoding="utf-8")
    print(f"[OK] Exported Table 2 to {out_file}")


def export_table3_dataset_breakdown() -> None:
    """Generate Table 3: Benchmark Dataset Distribution Breakdown."""
    cases = load_cases(DATA_DIR)
    typology_counts: dict[str, dict[str, int]] = {}

    for c in cases:
        u = c.unit_type
        if u not in typology_counts:
            typology_counts[u] = {"PASS": 0, "FAIL": 0, "TOTAL": 0}
        typology_counts[u][c.expected_label] += 1
        typology_counts[u]["TOTAL"] += 1

    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\caption{ASTG-CodeBench v0.1 test case distribution across multifamily apartment typologies ($N=36$).}",
        r"\label{tab:dataset_breakdown}",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"\textbf{Unit Typology} & \textbf{Compliant (PASS)} & \textbf{Non-Compliant (FAIL)} & \textbf{Total Cases} & \textbf{Ratio} \\",
        r"\midrule",
    ]

    total_pass = sum(t["PASS"] for t in typology_counts.values())
    total_fail = sum(t["FAIL"] for t in typology_counts.values())
    total_all = sum(t["TOTAL"] for t in typology_counts.values())

    for u in sorted(typology_counts.keys()):
        p = typology_counts[u]["PASS"]
        f = typology_counts[u]["FAIL"]
        tot = typology_counts[u]["TOTAL"]
        share = f"{tot/total_all*100:.1f}\\%"
        lines.append(f"{u} & {p} & {f} & {tot} & {share} \\\\")

    lines.extend([
        r"\midrule",
        f"\\textbf{{Total}} & \\textbf{{{total_pass}}} & \\textbf{{{total_fail}}} & \\textbf{{{total_all}}} & \\textbf{{100.0\\%}} \\\\",
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ])

    out_file = OUTPUT_DIR / "table3_dataset_breakdown.tex"
    out_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Exported Table 3 to {out_file}")


def export_figure_composite_paired_cases() -> None:
    """Generate a high-resolution 300 DPI 4-panel composite figure for Paper 2 (Figure 2)."""
    fig = plt.figure(figsize=(14, 10), dpi=300)
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.25)

    panels = [
        ("CW-PASS-01", "CW-FAIL-01", "(a) IBC 1020.2: Corridor Clear Width (45\" Pass vs. 43\" Fail)", gs[0, 0]),
        ("DOOR-PASS-01", "DOOR-FAIL-01", "(b) ADA 404: Door Maneuvering Clearance (34\" Pass vs. 30\" Fail)", gs[0, 1]),
        ("WC-PASS-01", "WC-FAIL-01", "(c) ADA 604: Water Closet Clearance (62\" Pass vs. 54\" Fail)", gs[1, 0]),
        ("EG-PASS-01", "EG-FAIL-01", "(d) IBC 1006.2: Egress Travel Distance (20 ft Pass vs. 80 ft Fail)", gs[1, 1]),
    ]

    for pass_name, fail_name, title, subplot_spec in panels:
        ax = fig.add_subplot(subplot_spec)
        pass_file = DATA_DIR / f"{pass_name}.json"
        fail_file = DATA_DIR / f"{fail_name}.json"

        if not pass_file.exists() or not fail_file.exists():
            continue

        case_p = LayoutTestCase.model_validate(json.loads(pass_file.read_text(encoding="utf-8")))
        case_f = LayoutTestCase.model_validate(json.loads(fail_file.read_text(encoding="utf-8")))

        ax.set_title(title, fontsize=11, fontweight="bold", pad=12)

        # Draw Pass on Left, Fail on Right with offset
        _draw_layout_on_axis(ax, case_p, x_offset=0, label="PASS (Compliant)")
        _draw_layout_on_axis(ax, case_f, x_offset=350, label="FAIL (Violation)")

        ax.axis("equal")
        ax.axis("off")

    composite_png = OUTPUT_DIR / "fig2_paired_threshold_cases.png"
    composite_pdf = OUTPUT_DIR / "fig2_paired_threshold_cases.pdf"
    plt.savefig(composite_png, dpi=300, bbox_inches="tight")
    plt.savefig(composite_pdf, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[OK] Exported 300 DPI publication figure to {composite_png} and {composite_pdf}")


def _draw_layout_on_axis(ax: plt.Axes, case: LayoutTestCase, x_offset: float, label: str) -> None:
    """Helper to draw a mini layout diagram with violation highlights."""
    is_fail = case.expected_label == "FAIL"
    badge_color = "#d9534f" if is_fail else "#5cb85c"

    # Draw label badge
    ax.text(
        x_offset + 50, -30, label,
        fontsize=9, fontweight="bold", color="white",
        bbox=dict(boxstyle="round,pad=0.3", facecolor=badge_color, edgecolor="none")
    )

    for space in case.spaces:
        xs = [p.x + x_offset for p in space.polygon]
        ys = [p.y for p in space.polygon]
        # Check if space violated
        has_v = any(v.element == space.id for v in case.expected_violations)
        fc = "#fdf2f2" if has_v else "#f4f5f7"
        ec = "#d9534f" if has_v else "#6c757d"
        lw = 2.0 if has_v else 1.0

        poly = patches.Polygon(list(zip(xs, ys)), facecolor=fc, edgecolor=ec, linewidth=lw)
        ax.add_patch(poly)

        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)
        ax.text(cx, cy, space.id, fontsize=7, ha="center", va="center", color="#2c3e50")

    # Draw doors
    for door in case.doors:
        has_dv = any(v.element == door.id for v in case.expected_violations)
        dec = "#d9534f" if has_dv else "#2980b9"
        dlw = 2.5 if has_dv else 1.5
        # Draw small marker
        ax.plot([x_offset + 100], [40], marker="s", markersize=4, color=dec)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Exporting Paper 2 publication assets...")
    export_table1()
    export_table2_rule_matrix()
    export_table3_dataset_breakdown()
    export_figure_composite_paired_cases()
    print("All Paper 2 assets successfully generated in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
