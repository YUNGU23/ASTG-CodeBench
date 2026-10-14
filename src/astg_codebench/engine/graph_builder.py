"""Convert ASTG layout test cases to NetworkX graphs for analysis."""
from __future__ import annotations

import networkx as nx

from astg_codebench.schemas.layout import LayoutTestCase


def build_graph(case: LayoutTestCase) -> nx.Graph:
    """Build a NetworkX graph from an ASTG layout test case.

    Nodes represent architectural spaces with their attributes.
    Edges represent connectivity via doors or adjacency.
    """
    G = nx.Graph()

    for space in case.spaces:
        G.add_node(
            space.id,
            type=space.type.value,
            area_sf=space.area_sf,
            clear_width_in=space.clear_width_in,
            occupant_load=space.occupant_load,
            is_accessible=space.is_accessible,
            has_window=space.has_window,
        )

    for edge in case.topology:
        G.add_edge(
            edge.source,
            edge.target,
            via=edge.via,
            is_egress=edge.is_egress,
            is_accessible=edge.is_accessible,
        )

    return G


def get_egress_subgraph(G: nx.Graph) -> nx.Graph:
    """Extract the egress-route subgraph."""
    egress_edges = [
        (u, v) for u, v, d in G.edges(data=True) if d.get("is_egress", False)
    ]
    return G.edge_subgraph(egress_edges).copy()


def get_accessible_subgraph(G: nx.Graph) -> nx.Graph:
    """Extract the accessible-route subgraph."""
    accessible_edges = [
        (u, v) for u, v, d in G.edges(data=True) if d.get("is_accessible", True)
    ]
    return G.edge_subgraph(accessible_edges).copy()
