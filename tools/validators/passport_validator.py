# SPDX-License-Identifier: QPATHFORMER-PLATFORM-1.0
# Copyright (c) 2026 Anthony Siljeg
# Project: Q-Pathformer Dataset Lifecycle Reference Implementation
# File: passport_validator.py
# Description: Reference tooling for governed dataset lifecycle workflows

#!/usr/bin/env python3
"""
Validate a dataset passport JSON against its JSON Schema.

Requires:
    pip install jsonschema
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    print("Missing dependency: jsonschema", file=sys.stderr)
    raise exc


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate dataset passport against schema.")
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()

    schema = read_json(args.schema)
    instance = read_json(args.input)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))

    if not errors:
        print(f"VALID: {args.input}")
        return

    print(f"INVALID: {args.input}")
    for idx, error in enumerate(errors, start=1):
        path = ".".join(str(p) for p in error.absolute_path) or "<root>"
        print(f"{idx}. Path: {path}")
        print(f"   Message: {error.message}")

    sys.exit(1)


if __name__ == "__main__":
    main()