#!/usr/bin/env python3
"""Generate and stage post cards as part of a local pre-commit hook."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATOR = REPO_ROOT / "scripts" / "generate_post_cards.py"


def main() -> int:
    result = subprocess.run([sys.executable, GENERATOR], cwd=REPO_ROOT)
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
