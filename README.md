# ASTG-CodeBench

**A Standardized Spatial Topological Benchmark for Automated US Building Code Compliance Evaluation**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/YUNGU23/ASTG-CodeBench/actions/workflows/ci.yml/badge.svg)](https://github.com/YUNGU23/ASTG-CodeBench/actions/workflows/ci.yml)

---

## Overview

ASTG-CodeBench is a research benchmark suite for evaluating automated building code compliance checking systems. It provides:

- **36 curated test cases** representing US multifamily apartment layouts with deterministic ground-truth compliance labels
- **5 formalized code predicates** covering IBC 2024 (egress), ADA 2010 (accessibility), and LEED v4.1 (daylight)
- **A deterministic symbolic oracle** that produces reproducible, auditable compliance verdicts
- **Standardized evaluation metrics** (precision, recall, F1, confusion matrix) for benchmarking any compliance system

### Why This Benchmark?

Existing LLM-based and AI-driven building code compliance research (2024–2026) focuses primarily on text-to-rule translation and regulatory question answering. **No existing open benchmark** combines:

1. US building code predicates (IBC/ADA/FHA)
2. Structured spatial topological graph representation
3. Ground-truth compliance labels with paired pass/fail threshold cases

ASTG-CodeBench fills this gap by providing a controlled, reproducible evaluation framework for spatial compliance systems.

## Quick Start

```bash
# Install from source
git clone https://github.com/YUNGU23/ASTG-CodeBench.git
cd ASTG-CodeBench
pip install -e ".[dev]"

# Audit a single test case
astg-bench audit data/v0.1/cases/CW-FAIL-01.json

# Run the full benchmark evaluation
astg-bench evaluate --data-dir data/v0.1/cases/

# Compare against LLM baseline models (generates Table 1)
astg-bench compare
```

## Benchmark Design

### Test Case Structure

Each test case is a JSON file containing:
- **Geometry**: Room polygons, corridor dimensions, door clearances (in inches)
- **Topology**: NetworkX-compatible adjacency graph (spaces as nodes, doors as edges)
- **Ground truth**: Expected PASS/FAIL label and specific violation annotations
- **Provenance**: Generation method, seed, and mutation description for reproducibility

### Rule Families (5 Predicates)

| Rule ID | Code Section | Domain | Severity |
|:--------|:-------------|:-------|:---------|
| `IBC_1020.2` | IBC 2024 §1020 | Corridor minimum clear width | Life Safety |
| `IBC_1006.2` | IBC 2024 §1006 | Travel distance to exit | Life Safety |
| `ADA_604` | ADA 2010 §604 | Water closet clearance | Civil Rights |
| `ADA_404` | ADA 2010 §404 | Door maneuvering clearance | Civil Rights |
| `WFR_10PCT` | LEED v4.1 (voluntary) | Window-to-floor ratio | Voluntary |

### Paired-Threshold Design

For each rule family, the benchmark includes 6 paired cases:
- **Pass-near**: value just above the threshold
- **Fail-near**: value just below the threshold
- **Pass-obvious**: comfortably compliant
- **Fail-obvious**: clearly noncompliant
- **Compound**: two interacting violations
- **Topology-edge**: disconnected route or blocked access

Total: **36 cases (18 pass, 18 fail)** — balanced and deterministic.

### Benchmark Results (Table 1)

Comparative performance of automated compliance checking methods on ASTG-CodeBench ($N=36$):

| Compliance Checking Method | Paradigm | Precision | Recall | F1 Score | Accuracy | Life-Safety FN | Latency / Case |
|:---------------------------|:---------|:---------:|:------:|:--------:|:--------:|:--------------:|:--------------:|
| **ASTG Deterministic Oracle (Ours)** | Symbolic Graph | **1.000** | **1.000** | **1.000** | **1.000** | **0 [PASS]** | **0.1 ms** |
| Chain-of-Thought LLM (Few-Shot GPT-4o) | LLM | 1.000 | 0.889 | 0.941 | 0.944 | 0 [PASS] | 1.99 s |
| Vanilla LLM (Zero-Shot GPT-4o) | LLM | 0.857 | 0.667 | 0.750 | 0.778 | 2 [FAIL] | 1.02 s |
| Simplified Heuristic Baseline | Heuristic | 1.000 | 1.000 | 1.000 | 1.000 | 0 [PASS] | 6.5 ms |

> [!NOTE]
> ASTG Deterministic Oracle achieves **zero false negatives** across all life-safety and accessibility provisions, eliminating critical structural and egress non-compliance traps that frontier LLMs fail to detect without symbolic graph analysis.

## Documentation & Protocols

- [Methodology](docs/METHODOLOGY.md) — Parametric perturbation and test case generation design.
- [Limitations & Scope](docs/LIMITATIONS.md) — Scope boundaries, assumptions, and known biases.
- [Code Provenance & Copyright](docs/CODE_PROVENANCE.md) — Fair use, section identifiers, and copyright compliance.
- [Independent Evaluation Protocol](docs/INDEPENDENT_EVALUATION_GUIDE.md) — Standardized audit protocol and evaluation form for external researchers and licensed architects.
- [Zenodo Integration Guide](docs/ZENODO_INTEGRATION_GUIDE.md) — Instructions for minting persistent academic DOIs via Zenodo.

## Architecture

```
src/astg_codebench/
├── schemas/          # Pydantic v2 data models (layout, rules, results)
├── rules/            # 5 deterministic code predicates (IBC, ADA, LEED)
├── engine/           # Oracle evaluator and graph builder
├── baselines/        # LLM evaluator and comparative benchmark runners
├── evaluate.py       # Benchmark runner with metrics
├── generator.py      # Procedural dataset generator
├── render.py         # Matplotlib SVG floor plan renderer
└── cli.py            # Command-line interface
```

### Key Design Principles

1. **Deterministic oracle**: All ground-truth labels come from symbolic rule evaluation, never from LLMs
2. **Reproducible**: Every case has a fixed seed and documented mutation
3. **Copyright-safe**: Only section identifiers and functional paraphrases; no copyrighted code text
4. **Separation of concerns**: The oracle that labels cases is independent of any system being benchmarked

## Technical Stack

| Component | Library | Purpose |
|:----------|:--------|:--------|
| Graph topology | `networkx` | Spatial adjacency and egress path analysis |
| 2D geometry | `shapely` | Polygon operations and clearance calculations |
| Data validation | `pydantic` v2 | Strict schema enforcement |
| CLI | `typer` | Type-safe command-line interface |
| Visualization | `matplotlib` | Annotated floor-plan diagrams |

## Data Availability

All data, models, and code generated during the study are available in this repository.
A persistent DOI is available via Zenodo: `[DOI pending release]`

## Citation

If you use ASTG-CodeBench in your research, please cite:

```bibtex
@dataset{gu_astg_codebench_2026,
  author       = {Gu, Yun},
  title        = {ASTG-CodeBench: A Standardized Spatial Topological Benchmark for Automated US Building Code Compliance Evaluation},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v0.1.0},
  doi          = {DOI_PENDING},
}
```

## Limitations

- This benchmark contains **procedurally generated synthetic layouts**, not real building plans
- Test cases cover a **narrow subset** of US building codes (5 predicates from IBC/ADA/LEED)
- Ground-truth labels are produced by a **simplified deterministic oracle** using bounding-box approximations
- This tool is **not a permitting authority, legal opinion, or substitute for jurisdictional review**
- Consult locally adopted code editions and licensed professionals for actual compliance determinations

## License

Code: [Apache License 2.0](LICENSE)  
Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (synthetic test cases)

## Disclaimer

This project is an independent open-source research initiative. It is not affiliated with, endorsed by, or sponsored by Amazon Web Services or any employer. The benchmark is designed to advance academic research in automated building code compliance.
