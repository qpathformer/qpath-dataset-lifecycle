# SPDX-License-Identifier: QPATHFORMER-PLATFORM-1.0
# Copyright (c) 2026 Anthony Siljeg
# Project: Q-Pathformer Dataset Lifecycle Reference Implementation
# File: id3_freeze_to_state3_dataset.py
# Description: Reference tooling for governed dataset lifecycle workflows

#!/usr/bin/env python3
"""
id3_freeze_to_state3_dataset.py

Reference converter that transforms ID3 freeze artifacts into a provisional
STATE_3 dataset record for Q-Pathformer-compatible workflows.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def build_state3_dataset(module_record: dict, session_record: dict) -> dict:
    return {
        "dataset_id": "state3-generated-from-id3-freeze",
        "dataset_state": "STATE_3",
        "source_mode": "ID_3",
        "module_source": module_record.get("module_id", "unknown"),
        "session_source": session_record.get("id_session", "unknown"),
        "record_type": "governance_reasoning_capture",
        "status": "reference_stub"
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert ID3 freeze records into a STATE_3 dataset.")
    parser.add_argument("--module", required=True, help="Path to module JSON")
    parser.add_argument("--session", required=True, help="Path to session JSON")
    parser.add_argument("--output", required=True, help="Path to output dataset JSON")
    args = parser.parse_args()

    module_record = load_json(Path(args.module))
    session_record = load_json(Path(args.session))
    output = build_state3_dataset(module_record, session_record)
    write_json(Path(args.output), output)

    print(f"Wrote STATE_3 dataset: {args.output}")


if __name__ == "__main__":
    main()