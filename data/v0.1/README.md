# ASTG-CodeBench v0.1 Dataset Card

## Overview

- **Version**: 0.1.0
- **Cases**: 36 procedurally generated test cases
- **Balance**: 18 PASS, 18 FAIL
- **Rule families**: 5 (IBC corridor, IBC egress, ADA WC, ADA door, daylight WFR)
- **Building type**: R-2 Multifamily (US)
- **Unit types**: Studio, 1BR, 2BR
- **Geometry units**: Inches (internal); source thresholds preserved in metadata

## Generation Method

Parametric perturbation of standard US multifamily apartment typologies.
See [METHODOLOGY.md](../../docs/METHODOLOGY.md) for full details.

## Ground Truth

Labels are produced by the deterministic oracle (`astg_codebench.engine.oracle`)
and verified against expected violations in each case file.

## Limitations

See [LIMITATIONS.md](../../docs/LIMITATIONS.md).

## License

Synthetic test case data: CC BY 4.0
