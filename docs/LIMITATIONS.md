# Limitations

## Scope Limitations

1. **Synthetic data only**: All test cases are procedurally generated.
   They do not represent real permitted buildings or actual code violations
   encountered in practice.

2. **Narrow rule coverage**: Only 5 code predicates are implemented.
   Real compliance review involves hundreds of interacting requirements
   across structural, mechanical, electrical, plumbing, and fire protection codes.

3. **Simplified geometry**: Spatial relationships use bounding-box approximations.
   Real compliance checking requires precise CAD/BIM geometry with wall thicknesses,
   structural elements, and 3D spatial relationships.

4. **Single jurisdiction**: The v0.1 benchmark uses baseline model code thresholds.
   It does not model state amendments or municipal overlay zones.

5. **No performance-based codes**: Only prescriptive (dimensional threshold)
   requirements are evaluated. Performance-based alternatives are not addressed.

## Usage Limitations

- This benchmark is a **research evaluation tool**, not a compliance checking system
- Results should not be interpreted as legal determinations
- Consult licensed professionals and locally adopted code editions for actual compliance
- The oracle's simplified geometry model may not capture all real-world edge cases

## Known Biases

- Test cases are balanced (50% pass, 50% fail) by design; this does not
  reflect the distribution of violations in real permitting workflows
- All layouts use rectangular room geometries; irregular shapes are not represented
- Accessibility paths are simplified to graph connectivity; actual route
  geometry (turning radii, ramp slopes) is not modeled
