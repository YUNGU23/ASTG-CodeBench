# Protocol for Independent Academic & Professional Verification

This protocol establishes the standardized procedure for independent researchers, licensed architects (AIA / RA), and civil engineering professionals to audit, verify, and evaluate the **ASTG-CodeBench** benchmark suite.

---

## 1. Objectives of Independent Evaluation

The objective is to provide objective, external reproducibility confirmation for:
1. **Mathematical correctness**: Verification of 2D geometric and topological graph formulations against adopted US building standards (IBC 2024, ADA 2010, LEED v4.1).
2. **Determinism**: Confirmation that the symbolic oracle produces identical compliance verdicts across multiple executions and hardware architectures.
3. **Safety critical accuracy**: Empirical verification that the benchmark correctly identifies life-safety means of egress non-compliances with 0 false negatives.

---

## 2. Verification Procedure (Estimated Time: 15–30 Minutes)

### Step 1: Environment Setup & Automated Test Suite
Clone the repository and install the benchmark package in an isolated virtual environment:

```bash
git clone https://github.com/YUNGU23/ASTG-CodeBench.git
cd ASTG-CodeBench
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Run full test suite
pytest -v
```
**Expected outcome**: All 9 unit tests pass without errors or warnings.

### Step 2: Full Benchmark Oracle Audit
Execute the deterministic oracle across the complete 36-case test suite:

```bash
astg-bench evaluate --data-dir data/v0.1/cases/
```
**Expected outcome**:
- Total Cases: 36
- Precision: 1.0000
- Recall: 1.0000
- False Negatives: 0 (Zero life-safety violations missed)

### Step 3: Comparative Evaluation Against LLM Baselines
Run the comparative benchmarking suite to evaluate symbolic methods vs. probabilistic LLMs:

```bash
astg-bench compare
```
**Expected outcome**:
- Review Table 1 showing the comparison between the ASTG Symbolic Oracle and baseline models.
- Inspect the false negative rate of LLM baselines on multi-hop egress graph reasoning.

### Step 4: Visual Inspection of Paired-Threshold Test Cases
Open the interactive Jupyter notebook or inspect SVG renders:

```bash
jupyter notebook notebooks/quick_start.ipynb
```
Verify the following 5 core regulatory predicate families in `data/v0.1/renders/`:
1. `IBC_1020.2` (Corridor Clear Width: 44" threshold for OL $\ge$ 50)
2. `IBC_1006.2` (Means of Egress: 75 ft travel limit along spatial graph)
3. `ADA_604` (Water Closet: 60" side $\times$ 56" rear clearance)
4. `ADA_404` (Door Maneuvering: 32" clear opening width)
5. `WFR_10PCT` (Habitable Room Daylight: $\ge 10\%$ glazing ratio)

---

## 3. Independent Evaluator Audit Form (Template)

```markdown
### ASTG-CodeBench Technical Audit Certificate

- **Evaluator Name**: __________________________________________________
- **Professional Title / Affiliation**: ________________________________
- **Professional License / Registration # (if applicable)**: ___________
- **Date of Verification**: ____________________________________________
- **Commit Hash / Version Tested**: `v0.1.0` (Commit: `a56b58a` / latest)

#### Technical Findings:
1. Environment and test suite verification:
   [ ] PASSED (All automated unit tests succeeded)
   [ ] FAILED (Issues observed: ______________________________________)

2. Benchmark oracle evaluation:
   - Total cases audited: [ 36 / 36 ]
   - Observed Precision: [ 100.0% ]
   - Observed Recall: [ 100.0% ]
   - Life-Safety False Negatives: [ 0 ]

3. Geometric and Topological Validity:
   [ ] Confirmed: Dimensional thresholds conform to published IBC 2024 and ADA 2010 standards.
   [ ] Confirmed: NetworkX graph topological path formulation accurately models means of egress.

4. Evaluator Remarks & Observations:
   ____________________________________________________________________
   ____________________________________________________________________
   ____________________________________________________________________

**Signature**: ___________________________ **Date**: ___________________
```
