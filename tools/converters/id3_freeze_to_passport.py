# SPDX-License-Identifier: QPATHFORMER-PLATFORM-1.0
# Copyright (c) 2026 Anthony Siljeg
# Project: Q-Pathformer Dataset Lifecycle Reference Implementation
# File: id3_freeze_to_passport.py
# Description: Reference tooling for governed dataset lifecycle workflows

#!/usr/bin/env python3
"""
Convert an Access-PoD ID_3 freeze package into a Dataset Passport JSON.

Expected inputs:
- module_03_baseline.canonical.json
- module_03_variant.canonical.json
- session_baseline.canonical.json
- session_variant.canonical.json
- hashes.txt
- ID3_FREEZE_NOTE.md
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

FREEZE_TS_RE = re.compile(r"frozen_at_utc:\s*([0-9T:\-]+Z)")
FREEZE_ID_RE = re.compile(r"outbox_freeze_folder:\s*(.+)")
HASH_LINE_RE = re.compile(r"^([a-fA-F0-9]{64})\s+(.+)$")


@dataclass
class FreezeArtifacts:
    module_baseline: Path
    module_variant: Path
    session_baseline: Path
    session_variant: Path
    hashes: Path
    freeze_note: Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_hashes(path: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for line in read_text(path).splitlines():
        match = HASH_LINE_RE.match(line.strip())
        if match:
            sha, name = match.groups()
            hashes[name.strip()] = sha.strip()
    return hashes


def parse_freeze_note(path: Path) -> tuple[str | None, str | None]:
    text = read_text(path)
    ts_match = FREEZE_TS_RE.search(text)
    freeze_match = FREEZE_ID_RE.search(text)
    frozen_at = ts_match.group(1) if ts_match else None
    freeze_id = None
    if freeze_match:
        raw = freeze_match.group(1).strip()
        freeze_id = Path(raw).name
    return frozen_at, freeze_id


def build_passport(
    artifacts: FreezeArtifacts,
    owner_name: str,
    jurisdiction: str,
    passport_id: str,
) -> dict[str, Any]:
    module_base = read_json(artifacts.module_baseline)
    module_var = read_json(artifacts.module_variant)
    session_base = read_json(artifacts.session_baseline)
    session_var = read_json(artifacts.session_variant)
    hashes = parse_hashes(artifacts.hashes)
    frozen_at, freeze_id = parse_freeze_note(artifacts.freeze_note)

    scenario_title = module_base.get("module", {}).get("module_title", "Unknown Module")
    dataset_title = f"{scenario_title} Signals"
    session_id = session_base.get("session", {}).get("session_id", "unknown-session")
    module_id = module_base.get("module", {}).get("module_id", "unknown-module")

    teacher_signals = [
        "scenario_seeds",
        "stressors",
        "signals_observed",
        "fragility_points",
        "authority_drift_flags",
        "uncertainty_notes",
        "escalation_triggers",
    ]

    freeze_note_sha = "0" * 64
    hashes_sha = "0" * 64

    passport = {
        "passport_version": "qpds_passport_v1.0",
        "dataset_passport_id": passport_id,
        "dataset_title": dataset_title,
        "dataset_description": (
            "Dataset passport derived from Access-PoD ID_3 frozen baseline and variant "
            "session/module artifacts. Contains governance reasoning signals, not decisions."
        ),
        "dataset_kind": "governed_training_input",
        "dataset_origin": "access_pod_id3_freeze",
        "dataset_owner": {
            "owner_type": "project",
            "owner_name": owner_name,
            "jurisdiction": jurisdiction,
        },
        "provenance": {
            "source_system": "Access-PoD",
            "source_access_mode": "ID_3",
            "source_record_class": "mixed_record",
            "source_session_id": session_id,
            "source_module_id": str(module_id),
            "source_freeze_id": freeze_id or "unknown-freeze-id",
            "inspection_status": "frozen_under_ID_3",
            "frozen_at_utc": frozen_at or utc_now(),
            "hash_manifest_algorithm": "SHA-256",
            "freeze_hash_verified": True,
            "canonical_artifacts": [
                {
                    "artifact_name": artifacts.module_baseline.name,
                    "artifact_role": "primary_module_record",
                    "sha256": hashes.get(artifacts.module_baseline.name, "0" * 64),
                    "path_hint": str(artifacts.module_baseline),
                },
                {
                    "artifact_name": artifacts.module_variant.name,
                    "artifact_role": "variant_module_record",
                    "sha256": hashes.get(artifacts.module_variant.name, "0" * 64),
                    "path_hint": str(artifacts.module_variant),
                },
                {
                    "artifact_name": artifacts.session_baseline.name,
                    "artifact_role": "parent_session_record",
                    "sha256": hashes.get(artifacts.session_baseline.name, "0" * 64),
                    "path_hint": str(artifacts.session_baseline),
                },
                {
                    "artifact_name": artifacts.session_variant.name,
                    "artifact_role": "variant_session_record",
                    "sha256": hashes.get(artifacts.session_variant.name, "0" * 64),
                    "path_hint": str(artifacts.session_variant),
                },
                {
                    "artifact_name": artifacts.freeze_note.name,
                    "artifact_role": "freeze_note",
                    "sha256": freeze_note_sha,
                    "path_hint": str(artifacts.freeze_note),
                },
                {
                    "artifact_name": artifacts.hashes.name,
                    "artifact_role": "hash_manifest",
                    "sha256": hashes_sha,
                    "path_hint": str(artifacts.hashes),
                },
            ],
            "evidence_note": (
                "Canonical artifacts stamped prior to hashing; final under ID_3 means final "
                "packaging and deterministic archive verification, not compliance or approval."
            ),
        },
        "lifecycle": {
            "state": "STATE_3",
            "state_reason": (
                "ID_3 frozen operational reasoning signals suitable for runtime reasoning "
                "and synthetic preparation, but not yet authorized for durable fine-tuning."
            ),
            "state2_review_required": True,
            "promotion_to_state1_allowed": True,
            "promotion_blockers": [
                "Fine-tuning not yet authorized",
                "Authorization filtering required before durable training use",
                "Human review required before promotion",
            ],
        },
        "authorization_scope": {
            "runtime_reasoning": True,
            "synthetic_generation": True,
            "fine_tuning": False,
            "external_training": False,
            "research_experimentation": True,
            "third_party_model_use": False,
            "human_review_required": True,
            "authorization_basis": "internal_governance_review",
            "authorization_note": (
                "Use limited to contained runtime reasoning, synthetic preparation, and "
                "research experimentation. Signals are not decisions and do not imply "
                "adequacy, compliance, or approval."
            ),
            "effective_from_utc": frozen_at or utc_now(),
        },
        "governance_flags": {
            "human_decision_required": bool(module_base.get("human_decision_required", True)),
            "signals_not_decisions": True,
            "non_certifying": True,
            "non_compliance_claim": True,
            "non_trust_claim": True,
            "contains_sensitive_data": False,
            "contains_synthetic_content": False,
            "dataset_containment_principle_applies": True,
        },
        "lineage": {
            "lineage_record_type": "mixed_lineage",
            "parent_refs": [
                {
                    "ref_type": "session",
                    "ref_id": session_id,
                    "note": "Baseline session",
                },
                {
                    "ref_type": "session",
                    "ref_id": session_var.get("session", {}).get("session_id", "unknown-variant-session"),
                    "note": "Variant time-pressure session",
                },
                {
                    "ref_type": "module",
                    "ref_id": str(module_id),
                    "note": scenario_title,
                },
                {
                    "ref_type": "artifact",
                    "ref_id": freeze_id or "unknown-freeze-id",
                    "note": "ID_3 outbox freeze package",
                },
            ],
            "policy_refs": [
                {
                    "document_id": "APOD-TR-004",
                    "title": "A WEB of Sharing Trust–Responsibility Toward a Trustless Future Vol.2",
                    "edition": "Second Edition — Version C",
                    "section_ref": "Onboarding and containment posture",
                },
                {
                    "document_id": "APOD-TR-007",
                    "title": "Governed Dataset Onboarding and Lifecycle Routing for AI Training Systems",
                    "edition": "First Edition — Draft A",
                    "section_ref": "Dataset Passport model",
                },
            ],
        },
        "signal_profile": {
            "teacher_signals": teacher_signals,
            "student_interpretation_mode": (
                "pattern extraction for governance reasoning signals under containment"
            ),
            "signal_note": (
                "Teacher signals derived from baseline and variant simulation records. "
                "Student interpretation remains non-authoritative and subject to State 2 "
                "convergence review before any durable training use."
            ),
        },
        "execution_profile": {
            "enabled": False,
            "environment": "none",
        },
        "created_at_utc": utc_now(),
        "updated_at_utc": utc_now(),
    }
    return passport


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert ID_3 freeze artifacts to a dataset passport.")
    parser.add_argument("--module-baseline", required=True, type=Path)
    parser.add_argument("--module-variant", required=True, type=Path)
    parser.add_argument("--session-baseline", required=True, type=Path)
    parser.add_argument("--session-variant", required=True, type=Path)
    parser.add_argument("--hashes", required=True, type=Path)
    parser.add_argument("--freeze-note", required=True, type=Path)
    parser.add_argument("--owner-name", default="Access-PoD / Governed Dataset Lifecycle Framework")
    parser.add_argument("--jurisdiction", default="Australia")
    parser.add_argument("--passport-id", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    artifacts = FreezeArtifacts(
        module_baseline=args.module_baseline,
        module_variant=args.module_variant,
        session_baseline=args.session_baseline,
        session_variant=args.session_variant,
        hashes=args.hashes,
        freeze_note=args.freeze_note,
    )

    passport = build_passport(
        artifacts=artifacts,
        owner_name=args.owner_name,
        jurisdiction=args.jurisdiction,
        passport_id=args.passport_id,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(passport, f, indent=2)
        f.write("\n")

    print(f"Wrote dataset passport: {args.out}")


if __name__ == "__main__":
    main()