# Contributing to ASTG-CodeBench

Thank you for your interest in contributing to **ASTG-CodeBench**! This project welcomes academic contributions, additional building code predicates, and layout test cases.

---

## 1. Guiding Principles

1. **Deterministic Verification**: All ground-truth annotations must be verifiable by deterministic symbolic rule engines. Heuristics or probabilistic models may not serve as oracle ground truth.
2. **Copyright Safety**:
   - Only cite model code section identifiers (e.g., `IBC 2024 §1020.2`) and functional paraphrases.
   - **Never** copy copyrighted verbatim text, diagrams, commentary, or tables from ICC or NFPA publications.
3. **Paired-Threshold Control**: New benchmark cases must be submitted in balanced pass/fail pairs around regulatory thresholds to ensure rigorous discrimination testing.
4. **Reproducibility**: All layout generation scripts must use explicit random seeds (`seed: int`).

---

## 2. Development Setup

```bash
git clone https://github.com/YUNGU23/ASTG-CodeBench.git
cd ASTG-CodeBench

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -e ".[dev]"
pytest -v
```

---

## 3. How to Propose a New Code Predicate

1. Open an issue using the [Rule Proposal Template](.github/ISSUE_TEMPLATE/rule_proposal.md).
2. Create a module under `src/astg_codebench/rules/<rule_id>.py`.
3. Implement an `evaluate(case: LayoutTestCase) -> list[Violation]` function.
4. Register your evaluator in `src/astg_codebench/engine/oracle.py`.
5. Add unit tests in `tests/` verifying determinism and threshold boundaries.

---

## 4. Code Style & Verification

- Formatter: `ruff format`
- Linter: `ruff check`
- Type checking: `mypy src/astg_codebench`
- Test suite: `pytest -v`

All pull requests must pass GitHub Actions CI checks before merging.
