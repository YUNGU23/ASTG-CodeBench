# Methodology

## Test Case Generation

ASTG-CodeBench test cases are procedurally generated using parametric perturbation
of US multifamily apartment typologies. The generation process is:

1. **Base typology selection**: Standard US multifamily configurations (studio, 1BR, 2BR, 3BR)
   informed by HUD/FHA dimensional guidelines and common double-loaded corridor layouts.

2. **Parameterization**: Key dimensions (corridor width, door clearance, bathroom dimensions,
   window area) are parameterized around code-prescribed thresholds.

3. **Controlled mutation**: Each case applies exactly one labeled mutation to a base
   compliant layout (e.g., reducing corridor width from 45" to 43"), creating matched
   pass/fail pairs around the regulatory threshold.

4. **Oracle labeling**: The deterministic rule engine evaluates each case and assigns
   ground-truth PASS/FAIL labels with specific violation annotations.

5. **Invariant checking**: Cases with unintended secondary violations from the mutation
   are discarded to maintain single-variable control.

## Rule Formalization

Each code predicate is formalized as a pure Python function that:
- Takes a `LayoutTestCase` as input
- Returns a list of `Violation` objects (empty = compliant)
- Uses only geometric measurements from the case data
- Never calls external services or probabilistic models

Rule implementations use functional paraphrases of code requirements.
Only section identifiers are stored; full code text is copyrighted.

## Dimensional Sources

Base typology dimensions are derived from:
- US HUD Fair Housing Design Manual (public document)
- IBC 2024 means-of-egress dimensional requirements (section IDs only)
- ADA 2010 Standards for Accessible Design (public document)
- Common US multifamily market standards (publicly documented)

No proprietary building plans or employer data are used.
