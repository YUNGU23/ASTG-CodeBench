# Mathematical Formulation of the Adjacency Spatial Topological Graph (ASTG)

This document provides the formal mathematical foundation of the Adjacency Spatial Topological Graph (ASTG) representation and its associated First-Order Logic (FOL) compliance checking predicates. These formulations serve as the formal theoretical specification implemented in the **ASTG-CodeBench** benchmark suite and presented in Section 3 of the companion research paper (*ASCE Journal of Computing in Civil Engineering*).

---

## 1. Spatial Topology Representation

### Definition 1: Adjacency Spatial Topological Graph (ASTG)
An architectural layout is formalized as an attributed, directed multi-graph:

$$\mathcal{G} = (V, E, \alpha_V, \alpha_E)$$

where:
- $V = \{v_1, v_2, \dots, v_n\}$ is the finite set of vertices representing bounded spatial enclosures (rooms, corridors, vertical circulation cores, and egress discharge points).
- $E \subseteq V \times V$ is the set of directed edges representing functional connectivity and spatial adjacency between enclosures.
- $\alpha_V: V \to \mathcal{A}_V$ is a vertex attribution function mapping each space to its geometric and regulatory properties.
- $\alpha_E: E \to \mathcal{A}_E$ is an edge attribution function mapping each connection to its transition properties.

---

### Definition 2: Vertex Attribute Space $\mathcal{A}_V$
For each vertex $v \in V$, the attribute tuple is defined as:

$$\alpha_V(v) = \big( \tau(v), \mathcal{P}(v), A(v), w_{\text{clear}}(v), L_{\text{occ}}(v), \gamma(v), A_{\text{win}}(v), \sigma_{\text{acc}}(v) \big)$$

where:
1. $\tau(v) \in \mathcal{T}$ represents the functional space classification:
   $$\mathcal{T} = \{\text{living}, \text{bedroom}, \text{kitchen}, \text{bathroom}, \text{corridor}, \text{hallway}, \text{stairwell}, \text{entry}, \text{balcony}, \text{utility}\}$$
2. $\mathcal{P}(v) \subset \mathbb{R}^2$ is a closed, non-self-intersecting 2D polygon defined by vertices $\{(x_i, y_i)\}_{i=1}^k$ in inches.
3. $A(v) = \text{Area}(\mathcal{P}(v)) \in \mathbb{R}^+$ is the net floor area in square feet.
4. $w_{\text{clear}}(v) \in \mathbb{R}^+ \cup \{\bot\}$ is the minimum clear passage width in inches (evaluated for corridors).
5. $L_{\text{occ}}(v) \in \mathbb{N}_0$ is the calculated occupant load.
6. $\gamma(v) \in \{0, 1\}$ indicates the presence of exterior glazing.
7. $A_{\text{win}}(v) \in \mathbb{R}_{\ge 0}$ is the total window glazing area in square feet.
8. $\sigma_{\text{acc}}(v) \in \{0, 1\}$ is a boolean flag denoting whether the enclosure lies on an accessible route.

---

### Definition 3: Edge Attribute Space $\mathcal{A}_E$
For each edge $e = (u, v) \in E$, the attribute tuple is defined as:

$$\alpha_E(e) = \big( \delta(e), w_{\text{door}}(e), c_{\text{latch}}(e), \eta_{\text{egress}}(e), \eta_{\text{acc}}(e) \big)$$

where:
1. $\delta(e) \in \Delta = \{\text{hinged}, \text{sliding}, \text{pocket}, \text{double}, \text{open\_opening}\}$ specifies the aperture type.
2. $w_{\text{door}}(e) \in \mathbb{R}^+$ is the minimum clear opening width in inches.
3. $c_{\text{latch}}(e) \in \mathbb{R}^+ \cup \{\bot\}$ is the pull-side latch clearance in inches.
4. $\eta_{\text{egress}}(e) \in \{0, 1\}$ indicates whether the edge forms part of a designated means of egress route.
5. $\eta_{\text{acc}}(e) \in \{0, 1\}$ indicates whether the edge satisfies accessible route continuity.

---

## 2. Formalization of Regulatory Predicates

A regulatory code provision is defined as a first-order logic sentence over the graph $\mathcal{G}$. A layout $\mathcal{G}$ is compliant with respect to rule $R$ if and only if:

$$\mathcal{G} \models \Phi_R$$

The five formalized code predicates in ASTG-CodeBench v0.1 are formulated as follows:

---

### Predicate 1: IBC 2024 §1020.2 — Corridor Minimum Clear Width ($\Phi_{\text{IBC-1020}}$)

Corridors must maintain minimum clear width determined by cumulative occupant load:

$$\Phi_{\text{IBC-1020}}(\mathcal{G}) \equiv \forall v \in V, \, \Big( \tau(v) = \text{corridor} \implies w_{\text{clear}}(v) \ge \theta_{\text{width}}(L_{\text{occ}}(v)) \Big)$$

where the prescriptive threshold function $\theta_{\text{width}}: \mathbb{N}_0 \to \mathbb{R}^+$ is:

$$\theta_{\text{width}}(L) = \begin{cases} 44.0\text{ inches}, & \text{if } L \ge 50 \\ 36.0\text{ inches}, & \text{if } L < 50 \end{cases}$$

---

### Predicate 2: IBC 2024 §1006.2 — Means of Egress Travel Distance ($\Phi_{\text{IBC-1006}}$)

Let $V_{\text{exit}} \subseteq V$ denote the set of exit discharge vertices:

$$V_{\text{exit}} = \{u \in V \mid \tau(u) \in \{\text{stairwell}, \text{entry}\}\}$$

If $V_{\text{exit}} \neq \emptyset$, the shortest path distance in the topological egress subgraph $\mathcal{G}_{\text{egress}}$ from every occupied space to the nearest exit must not exceed the prescribed threshold $D_{\max}$:

$$\Phi_{\text{IBC-1006}}(\mathcal{G}) \equiv \forall v \in V \setminus V_{\text{exit}}, \, \Big( \exists u \in V_{\text{exit}} \text{ such that } d_{\mathcal{G}}(v, u) \le D_{\max} \Big)$$

where $d_{\mathcal{G}}(v, u)$ is the shortest path length along valid accessible egress edges, and:

$$D_{\max} = \begin{cases} 75.0\text{ ft}, & \text{if unsprinklered (NFPA 13)} \\ 125.0\text{ ft}, & \text{if sprinklered} \end{cases}$$

If no path exists, $d_{\mathcal{G}}(v, u) = \infty$, yielding an immediate life-safety violation.

---

### Predicate 3: ADA 2010 §604 — Water Closet Clearance ($\Phi_{\text{ADA-604}}$)

For every accessible bathroom enclosure, minimum clear floor dimensions around the water closet fixture must satisfy:

$$\Phi_{\text{ADA-604}}(\mathcal{G}) \equiv \forall v \in V, \, \Big( \big(\tau(v) = \text{bathroom} \land \sigma_{\text{acc}}(v) = 1\big) \implies \big( \Delta_x(\mathcal{P}(v)) \ge 60.0 \land \Delta_y(\mathcal{P}(v)) \ge 56.0 \big) \Big)$$

where $\Delta_x(\mathcal{P})$ and $\Delta_y(\mathcal{P})$ denote the orthogonal bounding clearances oriented to the fixture installation wall.

---

### Predicate 4: ADA 2010 §404 — Door Maneuvering Clearance ($\Phi_{\text{ADA-404}}$)

Every door along an accessible path must guarantee clear passage and latch-side maneuvering clearances:

$$\Phi_{\text{ADA-404}}(\mathcal{G}) \equiv \forall e \in E, \, \Big( \eta_{\text{acc}}(e) = 1 \implies \big( w_{\text{door}}(e) \ge 32.0\text{ in} \;\land\; c_{\text{latch}}(e) \ge 18.0\text{ in} \big) \Big)$$

---

### Predicate 5: LEED v4.1 EQ Credit — Window-to-Floor Area Ratio ($\Phi_{\text{WFR-10}}$)

For all habitable enclosures ($\mathcal{T}_{\text{hab}} = \{\text{living}, \text{bedroom}, \text{kitchen}\}$), natural daylight access requires minimum glazing area ratio:

$$\Phi_{\text{WFR-10}}(\mathcal{G}) \equiv \forall v \in V, \, \Big( \tau(v) \in \mathcal{T}_{\text{hab}} \implies \frac{A_{\text{win}}(v)}{A(v)} \ge 0.10 \Big)$$

---

## 3. Symbolic Compliance Oracle

The global compliance decision $\Omega(\mathcal{G})$ is the conjunction of all evaluated domain predicates:

$$\Omega(\mathcal{G}) = \bigwedge_{k=1}^K \Phi_k(\mathcal{G}) = \begin{cases} \text{PASS}, & \text{if all } \Phi_k(\mathcal{G}) \text{ evaluate to True} \\ \text{FAIL}, & \text{otherwise} \end{cases}$$

### Determinism Theorem
Let $\mathcal{G}$ be a valid ASTG instance. Because each predicate $\Phi_k$ is a pure mathematical function of the finite attribute sets $\alpha_V$ and $\alpha_E$ with deterministic shortest-path graph algorithms ($O(|V| + |E|)$ via Dijkstra/BFS), the evaluation function $\Omega(\mathcal{G})$ is deterministic:

$$\forall \mathcal{G}, \quad \text{Var}\big(\Omega(\mathcal{G})\big) = 0$$

This guarantees reproducibility across compute environments and eliminates the stochastic hallucination inherent in direct LLM classification.
