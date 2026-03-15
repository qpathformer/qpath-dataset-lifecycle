# Governed Dataset Lifecycle Framework  
**Release:** v1.0-qpath-dataset-lifecycle

Q-Pathformer provides execution tooling compatible with governed datasets
defined by the Access-PoD governance framework.

The tooling demonstrates how inspection artifacts can be transformed into
lifecycle-governed datasets while preserving provenance, authorization scope,
lineage traceability, and lifecycle containment.

Reference workflows included in this repository illustrate Dataset Passport
generation, STATE_3 dataset materialization, authorization filtering, and
controlled promotion to STATE_1 durable training datasets.

Within the lifecycle model defined in APOD-TR-007, STATE_3 datasets function
as provisional runtime resources that support contextual reasoning and
synthetic dataset preparation. Conceptually, this layer may be viewed as
a governed form of working memory for dataset signals before validation
and durable training promotion.

Governance authority remains defined by the Access-PoD framework.

The tooling in this repository converts ID_3 freeze artifacts into
governed datasets for lifecycle processing.

These workflows support:

- Dataset Passport generation
- STATE_3 dataset materialization
- authorization filtering
- optional promotion into STATE_1 durable training form

The resulting artifacts are governance-aligned dataset records that may
be consumed by compatible execution environments such as Q-Pathformer.

---

## Artifact Release

This repository publishes the artifact set accompanying
**APOD-TR-007 — Governed Dataset Onboarding and Lifecycle Routing for AI Training Systems**.
https://github.com/Access-PoD/access-pod-artifacts/releases/tag/v1.0-apod-dataset-lifecycle

The framework defines a governance-aligned mechanism for transforming structured artifacts into machine-readable datasets while preserving provenance, lifecycle state, authorization scope, and lineage traceability.

## Governed Dataset Lifecycle & Passport Extensions

Q-Pathformer provides **implementation tooling and execution extensions** for working with governed datasets defined under the **Access-PoD governance framework**.

This repository contains reference implementations for:

* Dataset Passport generation
* Dataset lifecycle routing
* Authorization filtering
* Dataset promotion workflows
* Execution extensions compatible with Q-Pathformer training environments

The governance authority, lifecycle semantics, and policy framework remain defined in the **Access-PoD publications**.

---

## Release boundary and status

See:
- `compliance/BOUNDARY.md`
- `compliance/RELEASE_STATUS.md`

---

## Release Manifest

This release contains the following artifact groups.

| Category | Location | Description |
|---|---|---|
| Governance schemas | `schemas/` | Machine-readable schema definitions for dataset passports, routing records, lineage records, and execution profiles |
| Execution extensions | `extensions/` | Optional Q-Pathformer execution metadata extensions (UGCCMT, capsule profiles, execution environment hints) |
| Example records | `examples/` | Example dataset passports, routing records, lineage records, and generated lifecycle artifacts |
| ID_3 inspection artifacts | `examples/id3_freeze_example/` | Canonical inspection artifacts used as source records for dataset lifecycle workflows |
| Mapping documentation | `mappings/` | Documentation describing how inspection artifacts map into dataset passports and lifecycle states |
| Tooling reference implementation | `tools/` | Reference scripts demonstrating dataset conversion, routing, authorization filtering, and dataset promotion |
| Governance boundary declarations | `compliance/` | Release boundary and publication status statements |
| Supporting documentation | `docs/` | Implementation guidance, repository overview, and architecture reference documents |

This release also includes **sealed artifact manifests** used for reproducible verification of the repository contents:

- `manifest.internal.json` — enumerates repository files and SHA256 hashes  
- `manifest.external.json` — describes the packaged release artifact  
- `sealed_*.zip` and companion `.sha256` verification files

These manifests support deterministic inspection and verification of the
published artifact set.

Release reference

The canonical release artifact for this version is available at:

https://github.com/qpathformer/qpath-dataset-lifecycle/releases/tag/v1.0-qpath-dataset-lifecycle

---

## Relationship to Access-PoD

This repository provides implementation tooling and execution extensions
compatible with the Access-PoD governed dataset lifecycle framework.

Governance authority, lifecycle state definitions, and Dataset Passport
semantics remain defined by Access-PoD publications and releases.

Q-Pathformer consumes governed datasets but does not determine governance
authority or certification status.

Access-PoD defines the governance layer.
https://github.com/Access-PoD/access-pod-artifacts/releases/tag/v1.0-apod-dataset-lifecycle

Q-Pathformer provides a compatible **execution and tooling layer**.

```
Access-PoD
    Governance framework
    Dataset lifecycle model
    Dataset Passport definition

        ↓

Q-Pathformer
    Implementation tooling
    Execution extensions
    Dataset ingestion workflows
```

Execution environments may consume governed datasets but **do not determine governance authority or lifecycle state**.

---

### Governed Dataset Lifecycle (Access-PoD → Q-Pathformer)

The lifecycle model defined in **APOD-TR-007** separates governance
authority from execution tooling.

```text
Access-PoD (Governance Layer)
    Dataset Passport
    Lifecycle Routing
    Authorization Scope
            │
            ▼
        STATE_3
Runtime / Synthetic Dataset Layer
            │
            ▼
        STATE_2
Signal Convergence / Validation
(teacher–student evaluation)
            │
            ▼
        STATE_1
Durable Training Dataset
            │
            ▼
Q-Pathformer (Execution Layer)
Dataset materialization
Dataset filtering
Dataset promotion
```

Dataset promotion and materialization are executed within compatible
execution environments such as **Q-Pathformer** but remain subject to
Access-PoD governance conditions.

This diagram illustrates the separation between governance
authority and execution tooling:

Access-PoD governance
        ↓
dataset lifecycle states
        ↓
Q-Pathformer execution

Which matches the TR-007 model. 

---

## Documentation

Supporting documentation for this repository is located in `docs/`.

### Governance Framework

docs/relationship_to_apod_dataset_lifecycle_release/

Contains the foundational documents describing the governance model
and conceptual architecture.

• **APOD-TR-007 — Governed Dataset Onboarding and Lifecycle Routing**  
• **QPATH-ARCH-001 — Q-Pathformer Multi-State Machine Learning Architecture**

These documents define the governance framework and architectural context.

---

### Implementation Toolkit Guidance

docs/execution_toolkit/

Contains the implementation guidance companion demonstrating how
the repository tooling may be used to process governance artifacts
into lifecycle-governed datasets.

Both Markdown and Word versions are provided.

Includes:

• implementation_guidance.md and Implementation Guidance.docx  
  (Implementation Guidance Companion)

• running_the_tools.md  
  (execution examples for the repository tooling)

---

### Repository Documentation

Additional operational documentation includes:

• `docs/repository_overview.md`    
• `docs/SPDX_LICENSE.md`

---

## Repository Layout

The repository is organized to separate governance lifecycle schemas,
execution extensions, tooling, and example artifacts.

```text
compliance/
    Governance boundary declarations and release status documentation

docs/
    Repository overview, implementation guidance, licensing notice,
    and tool usage documentation

examples/
    Example Dataset Passport, routing, lineage, authorization,
    execution profile, and generated dataset artifacts

    id3_freeze_example/
        Canonical ID_3 freeze artifacts used as source records
        for dataset passport generation and lifecycle workflows

extensions/
    Optional Q-Pathformer execution extension schemas
    (UGCCMT metadata, capsule profiles, execution profile extensions)

mappings/
    Field mappings and lifecycle state reference matrices

schemas/
    Core governed dataset lifecycle schemas defining
    dataset passport structure, routing, lineage,
    policy lineage, and base execution profile schema

tools/

    authorization/
        authorization_control.py
        authorized_dataset_filter.py

    converters/
        id3_freeze_to_passport.py
        id3_freeze_to_state3_dataset.py

    promotion/
        state3_to_state1_promoter.py

    routing/
        dataset_lifecycle_router.py

    validators/
        passport_validator.py
        lineage_validator.py

    setup_examples.ps1
```

Root files:

```
    README.md
    manifest.external.json
    release_notes.md
    CHANGELOG.md
    CONTRIBUTORS.md
    LICENSE
    QPATHFORMER-PLATFORM-1.0.txt
```

---

### Tooling Dependencies

Some validation tools require Python dependencies.

Example:

```
pip install jsonschema
```

This dependency is required by:

```
tools/validators/passport_validator.py
```
---

## Core Schemas

Core lifecycle schemas are located in `schemas/`.

```
dataset_passport.schema.json
dataset_routing.schema.json
dataset_lineage.schema.json
policy_lineage.schema.json
execution_profile.schema.json
```

These schemas define the governed dataset lifecycle model, including:

```
- Dataset Passport structure
- lifecycle routing rules
- dataset lineage records
- policy lineage references
- base execution profile metadata
```

---

## Optional Q-Pathformer Execution Extensions

located in `extensions/`.

```
qpath_execution_profile.schema.json
ugccmt_extension.schema.json
capsule_profile.schema.json
```

These extensions support execution-environment metadata used by
Q-Pathformer-compatible training environments.

Typical extension metadata may include:

```
- dataset cluster identifiers
- capsule identifiers
- training stage indicators
- UGCCMT metadata
- execution environment hints
```

Execution extensions do not alter governance lifecycle semantics
and remain optional metadata attached to Dataset Passport records.

---

## Example Records

Example records are located in `examples/`.

```
dataset_passport.example.json
dataset_routing.example.json
dataset_lineage.example.json
policy_lineage.example.json
execution_profile.example.json
```

Reference tooling may also generate example artifacts, including:

```
dataset_passport.generated.json
dataset_routing.generated.json
authorization_report.generated.json
state3_dataset.generated.json
state3_dataset_authorized.json
state_candidate.generated.json
state1_dataset.generated.json
```

These examples demonstrate the lifecycle progression from ID_3
inspection artifacts into governed datasets.

---

## Example Workflow

```text
Typical dataset lifecycle workflow:

ID_3 Freeze Artifacts
        ↓
Dataset Passport Generation
        ↓
Passport Validation
        ↓
Lifecycle Routing
        ↓
Authorization Filtering
        ↓
STATE_3 Dataset Materialization
        ↓
Optional STATE_1 Promotion
        ↓
Lineage Validation
        ↓
STATE_1 durable training dataset
```

### Example tooling used in this workflow:

```
tools/converters/id3_freeze_to_passport.py
tools/converters/id3_freeze_to_state3_dataset.py
tools/validators/passport_validator.py
tools/routing/dataset_lifecycle_router.py
tools/authorization/authorization_control.py
tools/authorization/authorized_dataset_filter.py
tools/promotion/state3_to_state1_promoter.py
tools/validators/lineage_validator.py
```

### Reference Implementation Notice

The tooling in this repository provides reference implementations
for governed dataset lifecycle workflows.

Several utilities intentionally produce reference stub outputs
designed to demonstrate lifecycle processing rather than execute
full production training pipelines.

Execution environments may extend these tools with additional
dataset processing, model training, and orchestration logic.

---

## Example Artifact Preparation

Example artifacts may be prepared from ID_3 freeze packages using the helper script:

tools/setup_examples.ps1

This script copies canonical inspection artifacts into the repository
example folder structure used by the reference workflows.

Example destination:

examples/id3_freeze_example/

Typical artifacts include:

hashes.txt  
ID3_FREEZE_NOTE.md  
module_03_baseline.canonical.json  
module_03_variant.canonical.json  
session_baseline.canonical.json  
session_variant.canonical.json

These artifacts serve as the input records for dataset passport
generation and lifecycle routing.

---

## Lifecycle Model

The dataset lifecycle implemented by this repository follows the
model defined in **APOD-TR-007**.
https://github.com/Access-PoD/access-pod-artifacts/releases/tag/v1.0-apod-dataset-lifecycle


Datasets typically progress through three governance states:

STATE_3 — runtime and synthetic dataset layer  
STATE_2 — validation and signal convergence layer, where teacher–student signals are evaluated before durable training 
promotion. 
STATE_1 — durable training dataset layer

These states represent governance lifecycle stages rather than
execution stages of a training architecture.

Q-Pathformer provides the execution tooling that materializes
datasets and supports controlled promotion between lifecycle states.

---

## Governance Boundary

This repository **does not define governance authority**.

Lifecycle rules, Dataset Passport semantics, and governance boundaries are defined by **Access-PoD publications**.

Q-Pathformer consumes governed datasets but does not certify them.

---

## License

Q-Pathformer is licensed under the **QPATHFORMER-PLATFORM-1.0** license.

This license permits research, evaluation, and internal experimentation
while protecting the integrity of the platform architecture.

See:

- `QPATHFORMER-PLATFORM-1.0.txt`
- `docs/QPATHFORMER-PLATFORM-1.0_LICENSE.pdf`

---

## Status

Version: v1.0-qpath-dataset-lifecycle

```
Reference implementation
Standards exploration support
Execution-compatible tooling
```

Future releases may expand:

* promotion tooling
* execution profiles
* schema extensions
* integration with Q-Pathformer training pipelines.
