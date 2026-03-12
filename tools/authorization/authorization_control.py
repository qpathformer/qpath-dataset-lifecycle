# SPDX-License-Identifier: QPATHFORMER-PLATFORM-1.0
# Copyright (c) 2026 Anthony Siljeg
# Project: Q-Pathformer Dataset Lifecycle Reference Implementation
# File: authorization_control.py
# Description: Reference tooling for governed dataset lifecycle workflows

#!/usr/bin/env python3
"""
Apply conservative authorization filtering to a dataset passport or dataset payload.

This starter version:
- reads a passport
- determines whether fine-tuning is allowed
- writes a small authorization report
- can optionally produce a filtered dataset stub
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def build_authorization_report(passport: dict[str, Any]) -> dict[str, Any]:
    auth = passport["authorization_scope"]
    lifecycle = passport["lifecycle"]
    flags = passport["governance_flags"]

    fine_tuning_allowed = bool(auth.get("fine_tuning", False))
    external_training_allowed = bool(auth.get("external_training", False))
    human_review_required = bool(auth.get("human_review_required", True))

    removed_reasons: list[str] = []
    if not fine_tuning_allowed:
        removed_reasons.append("Removed from STATE_1 candidate set: fine-tuning not authorized")
    if not external_training_allowed:
        removed_reasons.append("External training use prohibited")
    if flags.get("signals_not_decisions", True):
        removed_reasons.append("Signals remain non-authoritative under containment")
    if human_review_required:
        removed_reasons.append("Manual review still required before durable promotion")

    return {
        "authorization_control_version": "qpds_authorization_control_v1.0",
        "dataset_passport_id": passport["dataset_passport_id"],
        "input_state": lifecycle["state"],
        "authorization_status": {
            "runtime_reasoning": bool(auth.get("runtime_reasoning", False)),
            "synthetic_generation": bool(auth.get("synthetic_generation", False)),
            "fine_tuning": fine_tuning_allowed,
            "external_training": external_training_allowed,
            "human_review_required": human_review_required,
        },
        "filtering_outcome": {
            "state1_eligible": fine_tuning_allowed and not human_review_required,
            "filter_applied": True,
            "elements_removed_count": len(removed_reasons),
            "removal_reasons": removed_reasons,
        },
        "next_recommended_state": (
            "STATE_1"
            if fine_tuning_allowed and not human_review_required
            else "STATE_2"
            if lifecycle["state"] in ("STATE_2", "STATE_3")
            else lifecycle["state"]
        ),
        "recorded_at_utc": utc_now(),
    }


def build_filtered_dataset_stub(passport: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    return {
        "dataset_version": "qpds_filtered_dataset_stub_v1.0",
        "dataset_passport_id": passport["dataset_passport_id"],
        "lifecycle_state": report["next_recommended_state"],
        "authorized_for_fine_tuning": report["filtering_outcome"]["state1_eligible"],
        "notes": report["filtering_outcome"]["removal_reasons"],
        "generated_at_utc": utc_now(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply authorization filtering based on a dataset passport.")
    parser.add_argument("--passport", required=True, type=Path)
    parser.add_argument("--report-out", required=True, type=Path)
    parser.add_argument("--filtered-dataset-out", type=Path)
    args = parser.parse_args()

    passport = read_json(args.passport)
    report = build_authorization_report(passport)

    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    with args.report_out.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(f"Wrote authorization report: {args.report_out}")

    if args.filtered_dataset_out:
        filtered = build_filtered_dataset_stub(passport, report)
        args.filtered_dataset_out.parent.mkdir(parents=True, exist_ok=True)
        with args.filtered_dataset_out.open("w", encoding="utf-8") as f:
            json.dump(filtered, f, indent=2)
            f.write("\n")
        print(f"Wrote filtered dataset stub: {args.filtered_dataset_out}")


if __name__ == "__main__":
    main()