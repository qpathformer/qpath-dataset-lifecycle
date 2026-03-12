# Implementation Guidance
## Governed Dataset Lifecycle Framework  
*(APOD-TR-007 Companion Document)*

---

## 1. Purpose

This document provides practical guidance for implementing the **Governed Dataset Lifecycle Framework** described in **APOD-TR-007**.

The framework enables organizations to transform governance artifacts into machine-readable datasets while preserving:

- provenance anchors
- lifecycle state
- authorization scope
- lineage traceability
- containment constraints

Reference implementation tooling is provided in the Q-Pathformer
dataset lifecycle repository.

---

## 2. Lifecycle Implementation Overview

The implementation workflow follows a consistent pipeline:

```text
ID_3 Freeze Artifacts
        ↓
Dataset Converter
        ↓
Dataset Passport
        ↓
Lifecycle Router
        ↓
Authorization Control
        ↓
STATE_3 → STATE_2 → STATE_1
```

STATE_3 and STATE_1 represent stable lifecycle states.
STATE_2 functions as a transitional validation layer used
to evaluate dataset signals before durable training promotion.

Each stage produces machine-readable records that preserve governance traceability.

---

## 3. Prepare Example Artifacts

*(This step is preconfigured for the example artifacts included in this
repository. It should only be used when preparing a new ID_3 freeze session.)*

Execute the script from the (custom) canonical ID_3 freeze artifacts folder in PS7.

**Implementation begins with preparing canonical governance artifacts produced during inspection workflows.**

For Access-PoD (new) workflows, these artifacts commonly originate from ID_3 freeze sessions Access-Mode release:
https://github.com/Access-PoD/access-pod-artifacts/releases/tag/ID_3-operator

Run:

```powershell
pwsh tools/setup_examples.ps1
```

This copies freeze artifacts into:

examples/id3_freeze_example/

Expected files:

```
hashes.txt
ID3_FREEZE_NOTE.md
module_03_baseline.canonical.json
module_03_variant.canonical.json
session_baseline.canonical.json
session_variant.canonical.json
```

---

## 4. Convert ID_3 Freeze to Dataset Passport

Run the converter tool:

```powershell
py tools/converters/id3_freeze_to_passport.py `
  --module-baseline examples/id3_freeze_example/module_03_baseline.canonical.json `
  --module-variant examples/id3_freeze_example/module_03_variant.canonical.json `
  --session-baseline examples/id3_freeze_example/session_baseline.canonical.json `
  --session-variant examples/id3_freeze_example/session_variant.canonical.json `
  --hashes examples/id3_freeze_example/hashes.txt `
  --freeze-note examples/id3_freeze_example/ID3_FREEZE_NOTE.md `
  --passport-id QPDS-2026-02-10-M03-TIMEPRESSURE-001 `
  --out examples/dataset_passport.generated.json
```
Output:

examples/dataset_passport.generated.json

This file represents the Dataset Passport.

---

## 5. Validate the Dataset Passport

Validate the generated passport against the schema.

Run:

```powershell
py tools/validators/passport_validator.py `
  --schema schemas/dataset_passport.schema.json `
  --input examples/dataset_passport.generated.json
```

Expected result:

VALID

Successful validation confirms that the Dataset Passport conforms to the schema definitions located in:

schemas/

---

## 6. Apply Lifecycle Routing

Generate a routing record for the dataset.

Run:

```powershell
py tools/routing/dataset_lifecycle_router.py `
  --passport examples/dataset_passport.generated.json `
  --routing-id QPDS-ROUTE-2026-02-10-M03-001 `
  --out examples/dataset_routing.generated.json
```

Output:

examples/dataset_routing.generated.json

The routing record determines the dataset lifecycle state.

Possible lifecycle outcomes:

STATE_3   — Runtime or synthetic dataset
STATE_2   — Validation and convergence layer
STATE_1   — Durable training dataset
HOLD      — Review required
EXCLUDED  — Removed from lifecycle processing

---

## 7. Authorization Filtering

*(Note: This Access-PoD release provides example governance records such as
Dataset Passports, routing records, and authorization reports. It does not
produce durable datasets. The execution layer provided in the Q-Pathformer
release performs dataset materialization and controlled promotion of datasets
between lifecycle states.)*

Durable dataset materialization and lifecycle promotion are demonstrated
by the execution tooling contained in the Q-Pathformer dataset lifecycle
repository.

Before a dataset can be considered for durable training use, authorization
filtering must be applied.

Run:

```powershell
py tools/authorization/authorization_control.py `
  --passport examples/dataset_passport.generated.json `
  --report-out examples/authorization_report.generated.json `
  --filtered-dataset-out examples/state_candidate.generated.json
```

Generated outputs:

authorization_report.generated.json
state_candidate.generated.json

The authorization report records filtering decisions and resulting eligibility status.

Filtering may remove dataset elements that:

- exceed authorization scope
- contain restricted signals
- conflict with governance policies
- require additional review before promotion

---

## 8. Resulting Dataset State

ID_3 freeze artifacts typically produce a:

STATE_3 dataset

This occurs because these artifacts represent:

- governance reasoning signals
- operational analysis
- simulation records

These artifacts are signals, not decisions, and therefore are not automatically eligible for durable training.

Promotion to STATE_1 requires explicit authorization and lifecycle promotion review.

---

## 9. Execution Environment Integration

Execution environments may consume Dataset Passports for training or runtime reasoning.

Examples include:

- Q-Pathformer capsule pipelines
- dataset clustering systems
- runtime reasoning environments

Execution metadata may optionally be included in the Dataset Passport.

However:

- execution metadata does not alter governance authority

- execution metadata does not change lifecycle state

Execution environments interpret the passport but do not independently authorize dataset promotion.

---

## 10. Summary

The Governed Dataset Lifecycle Framework provides a reproducible method for transforming governance artifacts into machine-readable datasets.

The implementation workflow follows this sequence:

```
ID_3 Freeze Artifacts
        ↓
Dataset Converter
        ↓
Dataset Passport
        ↓
Lifecycle Router
        ↓
Authorization Control
        ↓
STATE_3 → STATE_2 (transitional) → STATE_1
```

STATE_3 and STATE_1 represent stable lifecycle states.
STATE_2 functions as a transitional validation layer
used to evaluate dataset signals before durable
training promotion.

Each stage produces structured records that preserve:

- dataset provenance
- lifecycle containment
- authorization scope
- lineage traceability

This process ensures that datasets derived from governance artifacts remain traceable and governed throughout their lifecycle.