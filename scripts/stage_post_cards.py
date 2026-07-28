#!/usr/bin/env python3
"""Generate and stage post cards as part of a local pre-commit hook."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATOR = REPO_ROOT / "scripts" / "generate_post_cards.py"
VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python3"


def main() -> int:
    # Prefer the project's pinned local environment; CI uses its configured Python.
    renderer = VENV_PYTHON if VENV_PYTHON.is_file() else Path(sys.executable)
    result = subprocess.run([renderer, GENERATOR], cwd=REPO_ROOT)
    if result.returncode:
        return result.returncode

    subprocess.run(
        ["git", "add", "data/post_cards.yaml", "static/images/post-cards"],
        cwd=REPO_ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
