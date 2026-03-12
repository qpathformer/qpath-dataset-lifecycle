# SPDX-License-Identifier: QPATHFORMER-PLATFORM-1.0
# Copyright (c) 2026 Anthony Siljeg
# Project: Q-Pathformer Dataset Lifecycle Reference Implementation
# File: authorized_dataset_filter.py
# Description: Reference tooling for governed dataset lifecycle workflows

#!/usr/bin/env python3
"""
authorized_dataset_filter.py

Filters dataset records according to authorization scope.
Reference implementation for Q-Pathformer governed dataset workflows.
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


def filter_dataset(dataset: dict, allowed_scopes: list[str]) -> dict:
    filtered = dict(dataset)
    filtered["authorized_scopes_applied"] = allowed_scopes
    filtered["filter_status"] = "reference_stub"
    return filtered


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter a dataset by authorized scopes.")
    parser.add_argument("--input", required=True, help="Path to input dataset JSON")
    parser.add_argument("--output", required=True, help="Path to output dataset JSON")
    parser.add_argument(
        "--scope",
        action="append",
        default=[],
        help="Authorized scope to preserve. Repeat as needed."
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    dataset = load_json(input_path)
    filtered = filter_dataset(dataset, args.scope)
    write_json(output_path, filtered)

    print(f"Wrote authorized dataset: {output_path}")


if __name__ == "__main__":
    main()