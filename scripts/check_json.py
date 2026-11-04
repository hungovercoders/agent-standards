#!/usr/bin/env python3
"""Check that every committed JSON file parses.

Rulesets, settings templates and the plugin manifest are imported by hand
into GitHub or copied onto machines; a trailing comma found there costs an
admin's time. Catch it here instead. Run via `task check:json`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", ".task"}


def main() -> int:
    errors: list[str] = []
    count = 0
    for path in sorted(REPO_ROOT.rglob("*.json")):
        rel = path.relative_to(REPO_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        # local change: a file reached through a symlinked directory (.claude/skills ->
        # ../skills) is the same file again; Python 3.12's rglob follows
        # directory symlinks, 3.13's does not, so skip them explicitly.
        if path.is_symlink() or any(
            (REPO_ROOT / Path(*rel.parts[:i])).is_symlink() for i in range(1, len(rel.parts))
        ):
            continue
        count += 1
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(REPO_ROOT)}: {exc}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"\ncheck_json: {len(errors)} of {count} file(s) invalid.")
        return 1
    print(f"check_json: {count} JSON file(s) parse.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
