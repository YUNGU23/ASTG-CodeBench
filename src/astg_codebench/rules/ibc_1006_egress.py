"""IBC 2024 §1006 — Number of exits and travel distance.

Functional paraphrase: Spaces with occupant load exceeding thresholds
must have access to the required number of exits within maximum travel
distances (typically 75 ft for unsprinklered, 125 ft for sprinklered
buildings along the path of egress travel).

Note: Section identifier only. Full code text is copyrighted by ICC.
"""
from __future__ import annotations

import networkx as nx

from astg_codebench.schemas.layout import LayoutTestCase, ViolationSeverity
from astg_codebench.schemas.rule import CodeRule, Violation

RULE = CodeRule(
    rule_id="IBC_1006.2",
    name="Maximum Travel Distance to Exit",
    category="egress",
    severity=ViolationSeverity.LIFE_SAFETY,
    code_edition="IBC 2024",
    section="1006.2",
    description=(
        "Travel distance from any occupied space to the nearest exit "
        "shall not exceed code-prescribed maximums."
    ),
    threshold_value=75.0,
    threshold_unit="feet",
    comparison="lte",
)

MAX_TRAVEL_UNSPRINKLERED_FT = 75.0
MAX_TRAVEL_SPRINKLERED_FT = 125.0


def _build_egress_graph(case: LayoutTestCase) -> nx.Graph:
    """Build a NetworkX graph from the layout topology for egress analysis."""
    G = nx.Graph()
    for space in case.spaces:
        G.add_node(space.id, type=space.type.value)
    for edge in case.topology:
        G.add_edge(edge.source, edge.target, via=edge.via, is_egress=edge.is_egress)
    return G


def _find_exit_nodes(G: nx.Graph) -> list[str]:
    """Identify nodes that serve as exits (stairwells, entries marked as egress)."""
    exits = []
    for node, data in G.nodes(data=True):
        if data.get("type") in ("stairwell", "entry"):
            exits.append(node)
    return exits


def evaluate(
    case: LayoutTestCase,
    sprinklered: bool = False,
) -> list[Violation]:
    """Check travel distance from occupied spaces to nearest exit."""
    violations: list[Violation] = []
    max_dist = MAX_TRAVEL_SPRINKLERED_FT if sprinklered else MAX_TRAVEL_UNSPRINKLERED_FT

    G = _build_egress_graph(case)
    exit_nodes = _find_exit_nodes(G)

    if not exit_nodes:
        # No exits found — flag every occupied space
        for space in case.spaces:
            if space.type.value not in ("stairwell", "entry"):
                violations.append(
                    Violation(
                        rule_id=RULE.rule_id,
                        element_id=space.id,
                        measured_value=float("inf"),
                        threshold_value=max_dist,
                        units="feet",
                        severity=ViolationSeverity.LIFE_SAFETY,
                        message=f"No exit reachable from '{space.id}'.",
                    )
                )
        return violations

    for space in case.spaces:
        if space.type.value in ("stairwell", "entry"):
            continue
        try:
            shortest = min(
                nx.shortest_path_length(G, space.id, ex) for ex in exit_nodes
            )
        except nx.NetworkXNoPath:
            shortest = float("inf")

        # Convert graph hops to approximate travel distance
        # In a real implementation, edge weights would carry actual distances.
        # For the benchmark, hop count * average segment length is used.
        estimated_distance_ft = shortest * 20.0  # placeholder: 20 ft per hop

        if estimated_distance_ft > max_dist:
            violations.append(
                Violation(
                    rule_id=RULE.rule_id,
                    element_id=space.id,
                    measured_value=estimated_distance_ft,
                    threshold_value=max_dist,
                    units="feet",
                    severity=ViolationSeverity.LIFE_SAFETY,
                    message=(
                        f"Travel distance from '{space.id}' to nearest exit "
                        f"is ~{estimated_distance_ft:.0f} ft, exceeding {max_dist} ft."
                    ),
                )
            )
    return violations
