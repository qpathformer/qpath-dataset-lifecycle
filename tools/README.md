# Q-Pathformer Dataset Lifecycle Tooling

This directory contains the reference scripts used to demonstrate
execution workflows for the **Governed Dataset Lifecycle Framework**
defined in **APOD-TR-007**.

The scripts illustrate how governance artifacts can be transformed into
machine-readable datasets while preserving provenance, lifecycle state,
authorization scope, and lineage traceability.

These tools are **reference implementations** intended for standards
exploration and demonstration of lifecycle processing. They are not
production training pipelines.

Governance authority remains defined by the **Access-PoD framework**.

---

# Prepared Example Artifacts

*(This step is preconfigured for the example artifacts included in this
repository. `setup_examples.ps1` should only be used when preparing artifacts
from a new ID_3 freeze session.)*

Implementation begins with preparing canonical governance artifacts produced
during inspection workflows.

For Access-PoD workflows, these artifacts commonly originate from
**ID_3 freeze sessions** published in the Access-Mode release:

https://github.com/Access-PoD/access-pod-artifacts/releases/tag/ID_3-operator

Execute the helper script from the canonical ID_3 freeze artifacts folder
using PowerShell 7.

Run:

```
pwsh tools/setup_examples.ps1
```

Example working directory:

```
cd "C:\v1.0-qpath-dataset-lifecycle"
```

The script copies canonical inspection artifacts into the repository example
folder used by the lifecycle tooling:

examples/id3_freeze_example/

Typical artifacts include:

```
hashes.txt
ID3_FREEZE_NOTE.md
module_03_baseline.canonical.json
module_03_variant.canonical.json
session_baseline.canonical.json
session_variant.canonical.json
```

These artifacts act as the source records for dataset passport generation
and lifecycle routing.