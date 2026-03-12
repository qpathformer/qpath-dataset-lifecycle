# SPDX-License-Identifier: QPATHFORMER-PLATFORM-1.0
# Copyright (c) 2026 Anthony Siljeg
# Project: Q-Pathformer Dataset Lifecycle Reference Implementation
# File: dataset_lifecycle_router.py
# Description: Reference tooling for governed dataset lifecycle workflows

#!/usr/bin/env python3
"""
Create a routing record from a dataset passport.
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


def route_from_passport(passport: dict[str, Any], routing_id: str) -> dict[str, Any]:
    passport_id = passport["dataset_passport_id"]
    auth = passport["authorization_scope"]
    lifecycle = passport["lifecycle"]
    flags = passport["governance_flags"]

    current_state = lifecycle["state"]
    target_state = current_state
    decision = "route_to_state3"
    reason_code = "provisional_runtime_only"
    reason_text = "Default containment route for provisional governed dataset."

    if current_state == "STATE_1":
        decision = "route_to_state1"
        reason_code = "authorized_for_finetune"
        reason_text = "Dataset already authorized for durable fine-tuning."
    elif current_state == "STATE_2":
        decision = "route_to_state2"
        reason_code = "state2_validation_required"
        reason_text = "Dataset requires validation and convergence review."
    elif current_state == "HOLD":
        decision = "hold_for_review"
        reason_code = "policy_hold"
        reason_text = "Dataset held pending governance review."
        target_state = "HOLD"
    elif current_state == "EXCLUDED":
        decision = "exclude"
        reason_code = "policy_hold"
        reason_text = "Dataset excluded from lifecycle processing."
        target_state = "EXCLUDED"

    routing = {
        "routing_version": "qpds_routing_v1.0",
        "routing_id": routing_id,
        "dataset_passport_id": passport_id,
        "current_state": current_state,
        "default_target_state": target_state,
        "routing_decision": {
            "decision": decision,
            "reason_code": reason_code,
            "reason_text": reason_text,
        },
        "authorization_checks": {
            "runtime_reasoning_allowed": bool(auth.get("runtime_reasoning", False)),
            "synthetic_generation_allowed": bool(auth.get("synthetic_generation", False)),
            "fine_tuning_allowed": bool(auth.get("fine_tuning", False)),
            "external_training_allowed": bool(auth.get("external_training", False)),
            "human_review_required": bool(auth.get("human_review_required", True)),
            "authorization_basis": auth.get("authorization_basis", "unknown"),
        },
        "containment_checks": {
            "dataset_containment_principle_applies": bool(
                flags.get("dataset_containment_principle_applies", True)
            ),
            "signals_not_decisions": bool(flags.get("signals_not_decisions", True)),
            "sensitive_content_present": bool(flags.get("contains_sensitive_data", False)),
            "authorization_filter_required": not bool(auth.get("fine_tuning", False)),
        },
        "teacher_student_convergence": {
            "evaluated": current_state in ("STATE_2", "STATE_3"),
            "state2_convergence_result": "pending" if current_state != "STATE_1" else "aligned",
            "convergence_note": (
                "Teacher-student convergence review required before durable training promotion."
                if current_state != "STATE_1"
                else "Convergence already satisfied for current durable training state."
            ),
        },
        "authorization_filtering": {
            "filter_applied": False,
            "elements_removed_count": 0,
            "filter_reason_summary": [
                "Fine-tuning not authorized at current state"
            ] if not auth.get("fine_tuning", False) else [],
        },
        "promotion_controls": {
            "promotion_to_state1_allowed": bool(lifecycle.get("promotion_to_state1_allowed", False)),
            "new_version_required": True,
            "promotion_event_required": True,
            "promotion_blockers": lifecycle.get("promotion_blockers", []),
        },
        "manual_review": {
            "review_status": "pending" if auth.get("human_review_required", True) else "not_required",
            "reviewed_by": "",
            "review_note": "Awaiting governance review." if auth.get("human_review_required", True) else "",
        },
        "recorded_at_utc": utc_now(),
        "updated_at_utc": utc_now(),
    }
    return routing


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate dataset routing record from passport.")
    parser.add_argument("--passport", required=True, type=Path)
    parser.add_argument("--routing-id", required=True)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    passport = read_json(args.passport)
    routing = route_from_passport(passport, args.routing_id)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(routing, f, indent=2)
        f.write("\n")

    print(f"Wrote routing record: {args.out}")


if __name__ == "__main__":
    main()