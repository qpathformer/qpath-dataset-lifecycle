#!/usr/bin/env python3
"""Check tracked JSON syntax without changing files or asserting schema validity.

The repository uses UTF-8 without a byte-order mark. Object keys must be
unique, and the JavaScript extensions NaN and Infinity are not JSON.
Numbers are kept as tokens: this checks JSON syntax, not numeric ranges.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def reject_constant(token: str) -> None:
    raise ValueError(f"{token} is not a JSON number")


def check_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if text.startswith("\ufeff"):
        raise ValueError("UTF-8 byte-order mark is not allowed; use UTF-8 without BOM")
    json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
        parse_int=str,
        parse_float=str,
    )


def tracked_json_files(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "-z"],
        check=True,
        capture_output=True,
    )
    return sorted(
        {
            name.decode("utf-8")
            for name in completed.stdout.split(b"\0")
            if name and name.lower().endswith(b".json")
        }
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2],
        help="repository root (defaults to this script's repository)",
    )
    root = parser.parse_args(argv).root.resolve()
    try:
        paths = tracked_json_files(root)
    except (OSError, UnicodeError, subprocess.CalledProcessError) as error:
        print(f"FAIL: cannot list tracked JSON files: {error}", file=sys.stderr)
        return 1
    if not paths:
        print("FAIL: no tracked JSON files found", file=sys.stderr)
        return 1

    failures = 0
    for name in paths:
        try:
            if not (root / name).resolve().is_relative_to(root):
                raise ValueError("JSON path resolves outside the repository")
            check_file(root / name)
        except (OSError, ValueError, RecursionError) as error:
            failures += 1
            print(f"FAIL: {name}: {error}", file=sys.stderr)
    if failures:
        print(f"FAIL: {failures} of {len(paths)} tracked JSON files failed", file=sys.stderr)
        return 1
    print(
        f"PASS: {len(paths)} tracked JSON files have valid UTF-8 JSON syntax, "
        "unique object keys, and no NaN/Infinity literals."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
