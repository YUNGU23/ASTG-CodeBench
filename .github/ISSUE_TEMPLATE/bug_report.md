---
name: Bug Report
about: Report an incorrect ground truth label, geometric parsing failure, or oracle bug
title: '[BUG]: '
labels: 'bug'
assignees: ''
---

### Affected Case ID / Rule ID
- **Case ID**: (e.g. `ASTG-US-CW-PASS-01`)
- **Rule ID**: (e.g. `IBC_1020.2`)

### Expected vs. Actual Result
- **Expected Compliance Label**: (PASS or FAIL)
- **Actual Oracle Output**: (PASS or FAIL)

### Steps to Reproduce
```bash
astg-bench audit data/v0.1/cases/<case_id>.json
```

### Environment
- OS: (Windows / Linux / macOS)
- Python Version:
- ASTG-CodeBench Version: (e.g. 0.1.0)
