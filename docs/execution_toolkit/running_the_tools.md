# Running the Tools
## Q-Pathformer Governed Dataset Lifecycle Tooling

This document describes how to execute the reference tooling included in the
Q-Pathformer dataset lifecycle repository.

These tools illustrate how governance artifacts defined by the **Access-PoD
Governed Dataset Lifecycle Framework** can be transformed into executable
dataset records and controlled training inputs.

The Q-Pathformer repository provides the **execution layer** for governed
datasets, including dataset materialization and lifecycle promotion workflows.
Governance authority remains defined by the Access-PoD framework.

The lifecycle model implemented by these tools is defined in:

**APOD-TR-007 — Governed Dataset Onboarding and Lifecycle Routing for AI Training Systems**
https://github.com/Access-PoD/access-pod-artifacts/releases/tag/v1.0-apod-dataset-lifecycle

Q-Pathformer provides a compatible execution layer
for working with governed datasets produced under that model.

---

# Execution Workflow Overview

The typical dataset lifecycle execution flow is:

``` text
ID_3 Freeze Artifacts
↓
Dataset Passport Conversion
↓
Passport Validation
↓
Lifecycle Routing
↓
Authorization Control
↓
STATE_3 Dataset Materialization
↓
STATE_2 (validation / convergence)
↓
optional STATE_1 promotion
↓
Lineage Validation
```

Each stage produces machine-readable records supporting dataset governance,
authorization scope tracking, and lifecycle containment.

---

## Lifecycle Interpretation

The Q-Pathformer tooling operates within the lifecycle model
defined in **APOD-TR-007**.

Datasets normally enter the lifecycle as **STATE_3 provisional
datasets**, which contain governance reasoning signals or
synthetic training candidates.

Before durable training use, datasets may pass through
**STATE_2**, which acts as a convergence layer where
teacher and student signals are evaluated for coherence
and governance validation.

Promotion to **STATE_1** represents the creation of a
durable training dataset.

In this repository:

STATE_3 datasets are materialized by execution-layer tools.

STATE_2 represents the conceptual validation stage
described in APOD-TR-007.

STATE_1 promotion is demonstrated by the reference
promotion tooling.

---

# Prerequisites

Python 3.10+ is recommended. All commands below assume use of `py`. Replace with `python` if your environment requires it.

Install required validation dependency:

```
pip install jsonschema
```

The tools and commands are designed to run from the repository root: 

```
cd "C:\v1.0-qpath-dataset-lifecycle"
```

**Example Artifacts (ID_3 sessions) are preconfigured and included in this repository. 
Refer to the implementation_guidance files for more information on custom Access-PoD (new) workflows.** 

---

# Step 1 — Convert ID_3 Freeze Artifacts to Dataset Passport

Generate a Dataset Passport from frozen governance artifacts.

```powershell
py tools/converters/id3_freeze_to_passport.py `
  --module-baseline examples/id3_freeze_example/module_03_baseline.canonical.json `
  --module-variant examples/id3_freeze_example/module_03_variant.canonical.json `
  --session-baseline examples/id3_freeze_example/session_baseline.canonical.json `
  --session-variant examples/id3_freeze_example/session_variant.canonical.json `
  --hashes examples/id3_freeze_example/hashes.txt `
  --freeze-note examples/id3_freeze_example/ID3_FREEZE_NOTE.md `
  --passport-id QPDS-EXAMPLE-001 `
  --out examples/dataset_passport.generated.json
```

Output:

```
examples/dataset_passport.generated.json
```

The Dataset Passport records:

- provenance anchors
- lifecycle state
- authorization scope
- governance flags
- lineage references

---

# Step 2 — Validate the Dataset Passport

Validate the passport against the repository schema.

```powershell
py tools/validators/passport_validator.py `
  --schema schemas/dataset_passport.schema.json `
  --input examples/dataset_passport.generated.json
```

Expected result:

```
VALID: examples/dataset_passport.generated.json
```

---

# Step 3 — Apply Lifecycle Routing

Generate a lifecycle routing record based on the Dataset Passport.

```powershell
py tools/routing/dataset_lifecycle_router.py `
  --passport examples/dataset_passport.generated.json `
  --routing-id QPDS-ROUTE-001 `
  --out examples/dataset_routing.generated.json
```

Output:

```
examples/dataset_routing.generated.json
```

Routing determines the dataset lifecycle state:


STATE_3 — runtime / synthetic dataset
STATE_2 — validation and convergence
STATE_1 — durable training dataset
HOLD — review required
EXCLUDED — lifecycle rejection

---

# Step 4 — Apply Authorization Control

Evaluate authorization scope and produce a filtering report.

```powershell
py tools/authorization/authorization_control.py `
  --passport examples/dataset_passport.generated.json `
  --report-out examples/authorization_report.generated.json `
  --filtered-dataset-out examples/state_candidate.generated.json
```

Outputs:

```
authorization_report.generated.json
state_candidate.generated.json
```

The report records:

- authorization status
- filtering decisions
- promotion eligibility
- required review steps

---

# Step 5 — Materialize a STATE_3 Dataset

Convert ID_3 freeze artifacts into a provisional dataset.

```powershell
py tools/converters/id3_freeze_to_state3_dataset.py `
  --module examples/id3_freeze_example/module_03_baseline.canonical.json `
  --session examples/id3_freeze_example/session_baseline.canonical.json `
  --output examples/state3_dataset.generated.json
```

Output:

```
examples/state3_dataset.generated.json
```

STATE_3 datasets typically represent:

- governance reasoning captures
- simulation outputs
- exploratory signals
- runtime reasoning inputs

These datasets remain under containment.

---

# Step 6 — Apply Authorized Dataset Filtering

Filter a dataset according to authorized scopes.

```powershell
py tools/authorization/authorized_dataset_filter.py `
  --input examples/state3_dataset.generated.json `
  --output examples/state3_dataset_authorized.json `
  --scope runtime_reasoning `
  --scope synthetic_generation
```

Output:

```
examples/state3_dataset_authorized.json
```

Filtering ensures only authorized signals remain available for downstream use.

---

# Step 7 — Reference Promotion Stub (Optional)

Promote a dataset to a STATE_1 candidate when governance conditions are satisfied.

```powershell
py tools/promotion/state3_to_state1_promoter.py `
  --input examples/state3_dataset_authorized.json `
  --output examples/state1_dataset.generated.json
```

Output:

```
examples/state1_dataset.generated.json
```

Purpose

This tool illustrates the execution-layer transformation of an authorized STATE_3 dataset into a STATE_1 candidate record within the governed dataset lifecycle.

It demonstrates how authorized reasoning signals may be prepared for potential training use once governance conditions have been satisfied.

Reference Implementation Note

state3_to_state1_promoter.py is provided as a reference promotion stub.

The tool:

- converts an authorized STATE_3 dataset record into a STATE_1 candidate structure
- preserves dataset identifiers and lifecycle references
- illustrates the promotion boundary within the dataset lifecycle model

The tool does not perform governance authorization.

Promotion to durable STATE_1 status remains subject to:

- Access-PoD governance conditions
- authorization scope validation
- lineage and provenance verification
- version and release controls

The generated record should therefore be interpreted as a candidate training dataset artifact, not a final governance authorization.

---

# Step 8 — Validate Dataset Lineage

Verify structural integrity of lineage records.

```powershell
py tools/validators/lineage_validator.py `
  --input examples/dataset_lineage.example.json
```

Expected result:

```
VALID: examples/dataset_lineage.example.json
```

Note

dataset_lineage.example.json is an illustrative lineage record provided for schema validation.

In this release the lifecycle tooling validates lineage structure but does not automatically generate lineage artifacts.

---

# Repository Roles

Within the dataset lifecycle architecture:

**Access-PoD**

Defines:

- governance authority
- lifecycle semantics
- dataset passport schema
- authorization policies

**Q-Pathformer**

Provides:

- dataset materialization tooling
- lifecycle routing execution
- authorization filtering utilities
- dataset promotion workflows

Execution environments consume governed datasets but do not determine
governance authority.

---

# Summary

The Q-Pathformer repository provides a reference execution layer for
working with governed datasets.

The included tooling demonstrates how governance artifacts can be
transformed into controlled dataset records while preserving:

- provenance
- authorization scope
- lifecycle containment
- lineage traceability