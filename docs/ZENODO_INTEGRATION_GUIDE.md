# Zenodo Academic DOI Integration Guide

This document outlines the standard procedure to archive **ASTG-CodeBench** releases on [Zenodo](https://zenodo.org/) to obtain a persistent, citable Digital Object Identifier (DOI) for academic publications and data availability statements.

---

## 1. Why Zenodo?

- **Persistent citable DOI**: Satisfies ASCE, IEEE, and Elsevier Data Availability Policy requirements.
- **Permanent preservation**: Hosted by CERN Data Centre, ensuring long-term accessibility even if code repositories move.
- **Direct GitHub integration**: Automatically mints a new DOI snapshot every time a GitHub Release is published.

---

## 2. Three-Step Setup Procedure

### Step 1: Log in and Authorize GitHub
1. Navigate to [https://zenodo.org/](https://zenodo.org/).
2. Click **Log in** in the upper right corner.
3. Select **Log in with GitHub** and authorize Zenodo to read your public repositories.

### Step 2: Enable ASTG-CodeBench Repository
1. Navigate to your Zenodo GitHub settings: [https://zenodo.org/account/settings/github/](https://zenodo.org/account/settings/github/).
2. Search for `YUNGU23/ASTG-CodeBench` in the repository list.
3. Toggle the switch next to `ASTG-CodeBench` to **ON**.

### Step 3: Trigger DOI Minting via GitHub Release
1. Go to the repository releases page: [https://github.com/YUNGU23/ASTG-CodeBench/releases](https://github.com/YUNGU23/ASTG-CodeBench/releases).
2. Click **Draft a new release** (or **Create release from tag** `v0.1.0`).
3. Set:
   - **Tag version**: `v0.1.0`
   - **Release title**: `ASTG-CodeBench v0.1.0: Initial Benchmark Release`
   - **Description**: Paste the release notes from Section 3 below.
4. Click **Publish release**.
5. Within 60 seconds, Zenodo will automatically archive the release and assign a permanent DOI badge (e.g. `10.5281/zenodo.XXXXXXX`).

---

## 3. Recommended GitHub Release Notes Template (v0.1.0)

```markdown
## ASTG-CodeBench v0.1.0: Standardized Spatial Topological Benchmark for Automated Building Code Compliance

Initial release of the ASTG-CodeBench benchmark suite companion for ASCE Journal of Computing in Civil Engineering research.

### What's Included:
- **36 Curated Multifamily Test Cases** (18 PASS, 18 FAIL) with paired-threshold perturbations.
- **5 Formalized Code Predicates**:
  - `IBC_1020.2`: Corridor clear width (44" / 36" thresholds).
  - `IBC_1006.2`: Means of egress topological shortest-path travel distance (75 ft limit).
  - `ADA_604`: Water closet clearance (60" side x 56" rear).
  - `ADA_404`: Door maneuvering clearance (32" opening, 18" latch clearance).
  - `WFR_10PCT`: Habitable room daylight window-to-floor area ratio (>= 10%).
- **Deterministic Symbolic Oracle**: 100% precision, 100% recall, 0 false negatives on life safety.
- **LLM Baseline Evaluator**: Comparison module generating Table 1 (Oracle vs. Zero-Shot GPT-4o vs. CoT).
- **36 Annotated SVG Floor Plans**: Red-highlighted non-compliant elements with violation badges.
- **Quick-Start Jupyter Notebook**: One-click interactive evaluation and rendering demo.

### Verification:
- Automated test suite: 9/9 passed.
- SHA-256 integrity manifest: `data/v0.1/manifest.sha256`.
```

---

## 4. Updating Repository Badges

Once your DOI is minted on Zenodo:
1. Copy the DOI markdown badge from Zenodo (e.g. `[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)`).
2. Update `README.md` and `CITATION.cff` by replacing `[DOI pending release]` with your actual DOI.
