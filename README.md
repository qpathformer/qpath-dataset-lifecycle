# Q-Pathformer Dataset Lifecycle — reference schemas and tooling

**Release:** [v1.0-qpath-dataset-lifecycle](https://github.com/qpathformer/qpath-dataset-lifecycle/releases/tag/v1.0-qpath-dataset-lifecycle)

Q-Pathformer Dataset Lifecycle provides reference schemas, example records and tools for turning inspection artifacts into governed dataset candidates. Dataset Passports preserve provenance, lifecycle state, authorisation scope and lineage references. The examples demonstrate conversion, filtering and lifecycle boundaries; some utilities are intentionally reference stubs. Access-PoD supplies the related governance framework.

## Start here

| Goal | Reading destination |
| --- | --- |
| Understand the reference workflow | [Implementation guidance](docs/execution_toolkit/implementation_guidance.md) |
| Inspect commands and implementation limits | [Running the tools](docs/execution_toolkit/running_the_tools.md) |
| Inspect the Passport contract and example | [Dataset Passport schema](schemas/dataset_passport.schema.json) · [Illustrative Passport](examples/dataset_passport.example.json) |
| Obtain the preserved artifact set | [Published release](https://github.com/qpathformer/qpath-dataset-lifecycle/releases/tag/v1.0-qpath-dataset-lifecycle) |

**Implementation boundary.** STATE_3 materialisation is demonstrated by the tools. STATE_2 is a conceptual validation/convergence stage in this reference. The [promotion stub](tools/promotion/state3_to_state1_promoter.py) creates a STATE_1 candidate record with `promotion_status: reference_stub`; it does not grant training authority or complete the governance validation process. Illustrative records can contain placeholder hashes and do not establish audited production provenance.

The [boundary statement](compliance/BOUNDARY.md) and [release status](compliance/RELEASE_STATUS.md) define the reference scope. This live README clarifies navigation and the existing implementation; published packages, manifests and release evidence retain their original identities.

---

## Artifact Release

This repository publishes the artifact set accompanying
**APOD-TR-007 — Governed Dataset Onboarding and Lifecycle Routing for AI Training Systems**.
https://github.com/Access-PoD/access-pod-artifacts/releases/tag/v1.0-apod-dataset-lifecycle

The framework defines a governance-aligned mechanism for transforming structured artifacts into machine-readable datasets while preserving provenance, lifecycle state, authorization scope, and lineage traceability.

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

The published packages include **sealed artifact manifests** for verification of their identified release snapshots:

- `manifest.internal.json` — enumerates repository files and SHA256 hashes  
- `manifest.external.json` — describes the packaged release artifact  
- `sealed_*.zip` and companion `.sha256` verification files

These manifests support deterministic inspection and verification of the
published artifact set. They are historical snapshot records, not an inventory of later live README or maintenance updates.

Release reference

The canonical release artifact for this version is available at:

https://github.com/qpathformer/qpath-dataset-lifecycle/releases/tag/v1.0-qpath-dataset-lifecycle

---

## Relationship to Access-PoD

Access-PoD defines the governance framework, lifecycle semantics and Dataset Passport model in [APOD-TR-007 and its artifact release](https://github.com/Access-PoD/access-pod-artifacts/releases/tag/v1.0-apod-dataset-lifecycle). Q-Pathformer supplies compatible conversion, routing, filtering and reference promotion tools. Execution outputs provide evidence for review; they do not establish governance authority or certification.

### Governed Dataset Lifecycle (Access-PoD → Q-Pathformer)

The following is the conceptual lifecycle described by APOD-TR-007. It does not imply that this repository implements every validation or promotion gate:

```text
ID_3 inspection artifacts
        ↓
Dataset Passport and STATE_3 materialisation
        ↓
STATE_2 validation / signal convergence
(conceptual stage in this reference)
        ↓
STATE_1 durable training dataset
(requires governance validation and authorisation)
```

The repository's promotion utility demonstrates a candidate-record transformation. A generated STATE_1 label alone is not evidence that the required validation and authorisation occurred. Follow the [command guide](docs/execution_toolkit/running_the_tools.md) for the implemented steps and stub boundaries.

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

- [Repository overview](docs/repository_overview.md) — illustrative structure and documentation roles.
- [SPDX notice guidance](docs/SPDX_LICENSE.md)

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
Optional STATE_1 Candidate Transformation (reference stub)
        ↓
Lineage Validation
        ↓
STATE_1 candidate record (governance authorisation still required)
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

The commands above demonstrate the implemented conversion and routing steps. The STATE_2 stage remains conceptual and the promotion utility remains a candidate-producing stub, as stated in the opening implementation boundary. Model training and production orchestration require separately defined implementation and review.

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

## Lifecycle Model and Governance Boundary

The APOD-TR-007 lifecycle distinguishes STATE_3 runtime/synthetic resources, STATE_2 validation and convergence, and STATE_1 durable training datasets. These are governance lifecycle stages, separate from the states of a learning architecture. The [Access-PoD relationship](#relationship-to-access-pod) and opening implementation boundary distinguish that model from the tools implemented here.

Governance authority remains external to this repository. Dataset preparation and a lifecycle label do not certify a dataset or authorise training.

---

## License

Q-Pathformer is licensed under the **QPATHFORMER-PLATFORM-1.0** license.

This license permits research, evaluation, and internal experimentation
while protecting the integrity of the platform architecture.

See:

- [QPATHFORMER-PLATFORM-1.0.txt](QPATHFORMER-PLATFORM-1.0.txt)
- [Historical licence PDF](<docs/QPATHFORMER-PLATFORM-1.0 LICENSE.pdf>)

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
