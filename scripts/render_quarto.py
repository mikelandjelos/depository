#!/usr/bin/env python3
"""Render Quarto (.qmd/.ipynb) posts into Hugo-native Markdown.

Wraps `quarto render` with two fixups the `hugo-md` writer doesn't handle
on its own, both stemming from Quarto not knowing Hugo's URL scheme:

- Root-relative links (`/stats/`) get rewritten by Quarto to be relative to
  the *source file's* location on disk (`../../../stats/`), since Quarto
  assumes it's the one serving the output. But Hugo serves every post in
  `content/posts/<slug>/index.md` at the flat URL `/posts/<slug>/` --
  disk depth and URL depth don't match, so Quarto's math is wrong for us.
  Since every post bundle sits at the same fixed depth (content/posts/
  <slug>/index.qmd), the walk-up prefix Quarto emits is always the same
  three levels, and always meant a project-root-relative link -- so it's
  safe to deterministically undo.
- Requires QUARTO_PYTHON pointed at the repo's .venv so `jupyter`/
  `matplotlib` etc. are found regardless of the caller's shell state
  (e.g. a pre-commit hook running outside an activated venv).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python3"

# Quarto rewrites a root-relative link/src to a path relative to the source
# file's directory. Every post bundle lives at content/posts/<slug>/index.qmd,
# a fixed three levels below the repo root, so the walk-up is always "../../../".
ROOT_LINK_PREFIX = "../../../"


def fix_root_relative_links(text: str) -> str:
    text = re.sub(r'(\]\()' + re.escape(ROOT_LINK_PREFIX), r"\1/", text)
    text = re.sub(r'(src="|href=")' + re.escape(ROOT_LINK_PREFIX), r"\1/", text)
    return text


# A code-cell's figure output is a bare <img> on its own line. Wrap it so it
# can be aligned to the code block's column (see .quarto-figure in tufte.css)
# instead of centering on the full article width.
FIGURE_IMG_RE = re.compile(r"^(<img [^\n>]*/>)[ \t]*$", re.MULTILINE)

# Collapses any pre-existing wrapper(s) back to a bare <img> line first, so
# re-running this script on an already-wrapped file (e.g. a second manual
# invocation before the source changed) can't nest the div repeatedly.
FIGURE_WRAPPER_RE = re.compile(
    r'(?:<div class="quarto-figure">\n)+(<img [^\n>]*/>)\n(?:</div>\n?)+',
)


def wrap_figures(text: str) -> str:
    text = FIGURE_WRAPPER_RE.sub("\\1\n", text)
    return FIGURE_IMG_RE.sub('<div class="quarto-figure">\n\\1\n</div>', text)


def rendered_output_paths(targets: list[str]) -> set[Path]:
    """Every index.md whose index.qmd/index.ipynb source falls under one of
    the given targets -- so post-processing only ever touches files this
    invocation actually rendered, not every post that happens to exist."""
    paths = set()
    for t in targets:
        p = (REPO_ROOT / t).resolve()
        sources = [p] if p.is_file() else [*p.rglob("index.qmd"), *p.rglob("index.ipynb")]
        for src in sources:
            md_path = src.parent / "index.md"
            if md_path.exists():
                paths.add(md_path)
    return paths


def main() -> int:
    if not VENV_PYTHON.exists():
        print(f"error: {VENV_PYTHON} not found -- run:", file=sys.stderr)
        print("  python3 -m venv .venv && .venv/bin/pip install jupyter matplotlib", file=sys.stderr)
        return 1

    targets = sys.argv[1:] or ["content/posts"]

    env = os.environ.copy()
    env["QUARTO_PYTHON"] = str(VENV_PYTHON)
    env["MATPLOTLIBRC"] = str(REPO_ROOT / "matplotlibrc")

    result = subprocess.run(
        ["quarto", "render", *targets],
        cwd=REPO_ROOT,
        env=env,
    )
    if result.returncode != 0:
        return result.returncode

    for md_path in rendered_output_paths(targets):
        original = md_path.read_text()
        fixed = wrap_figures(fix_root_relative_links(original))
        if fixed != original:
            md_path.write_text(fixed)
            print(f"post-processed {md_path.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
