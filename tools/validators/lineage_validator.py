# SPDX-License-Identifier: QPATHFORMER-PLATFORM-1.0
# Copyright (c) 2026 Anthony Siljeg
# Project: Q-Pathformer Dataset Lifecycle Reference Implementation
# File: lineage_validator.py
# Description: Reference tooling for governed dataset lifecycle workflows

#!/usr/bin/env python3
"""
lineage_validator.py

Minimal validator for dataset lineage records.
This is a lightweight structural validator, not a full JSON Schema engine.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_KEYS = [
    "lineage_id",
    "dataset_id",
    "parent_references"
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a dataset lineage JSON file.")
    parser.add_argument("--input", required=True, help="Path to lineage JSON")
    args = parser.parse_args()

    path = Path(args.input)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    missing = [key for key in REQUIRED_KEYS if key not in data]

    if missing:
        print(f"INVALID: missing required keys: {', '.join(missing)}")
        raise SystemExit(1)

    print(f"VALID: {path}")


if __name__ == "__main__":
    main()