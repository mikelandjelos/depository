# Quarto Scientific Publishing (issue #4)

How posts get written as executable `.qmd`/`.ipynb` documents (Python and R
so far) instead of only plain Markdown, and how to reproduce the local
toolchain on a fresh machine. This is genuinely a local build step: Quarto,
Jupyter, and R only need to be installed on the machine that *authors* a
post. Cloudflare only ever builds plain Hugo from the already-rendered
`index.md` + images that get committed alongside the `.qmd`/`.ipynb` source
— nothing about the deploy pipeline changes.

## Fresh-machine setup

### 1. Quarto

Install Quarto 1.8.26 (or newer) from <https://quarto.org/docs/get-started/>.
Verify with `quarto check` — it should report Pandoc, Dart Sass, Deno, and
Typst all OK.

### 2. Python (Jupyter engine)

An isolated venv at the repo root, so this never touches the system/pyenv
Python:

```bash
python3 -m venv .venv
.venv/bin/pip install jupyter matplotlib
```

`scripts/render_quarto.py` points `QUARTO_PYTHON` at `.venv/bin/python3`
itself, so nothing needs to be activated by hand before rendering.

### 3. R (knitr engine)

```bash
mkdir -p ~/R/library
echo 'R_LIBS_USER=~/R/library' >> ~/.Renviron
USE_BUNDLED_LIBUV=1 Rscript -e 'install.packages(c("knitr", "rmarkdown"), repos="https://cloud.r-project.org", lib="~/R/library")'
```

Two things that aren't obvious from a plain `install.packages()`:

- Without `R_LIBS_USER` pointed at a writable directory, installation fails
  because the default site-library isn't writable without sudo.
- `rmarkdown`'s dependency chain pulls in the `fs` package, which needs the
  system `libuv` dev headers to compile. Rather than requiring
  `sudo apt install libuv1-dev`, `USE_BUNDLED_LIBUV=1` tells `fs` to compile
  its own bundled copy of libuv instead — no sudo needed at all.

Verify with `quarto check knitr` — should report both `knitr` and
`rmarkdown` with version numbers, not `(None)`.

### 4. Julia

Not set up yet. Quarto supports a Julia/IJulia engine the same shape as the
Python/R ones; this is future exploration, not implemented (see docs/PLAN.md
→ #4).

## Authoring a post

Every Quarto post is a **Hugo leaf bundle**: the source lives at
`content/posts/<slug>/index.qmd` (or `index.ipynb`), and Quarto renders
`index.md` plus a figures directory right alongside it in the same folder.
That's what makes Hugo pick up the figures automatically as page resources
— no `static/` copying needed.

```bash
mkdir content/posts/my-post
$EDITOR content/posts/my-post/index.qmd   # or hand-build an .ipynb
python3 scripts/render_quarto.py content/posts/my-post/index.qmd
hugo server -D   # check it live, both themes
```

Front matter works exactly like a plain-Markdown post (`title`, `subtitle`,
`date`, `status`, `categories`, `tags` all pass through). One extra optional
table field:

- `tableStyle: "striped"` or `"grid"` — see docs/THEME.md → "Tables" for
  what each looks like. Default (no field) is a plain Tufte rule-table.

Post cards require no additional front matter or local command. The
pre-commit hook detects a changed post, derives its card from the rendered
Markdown, and stages the generated asset and Hugo data manifest in the same
commit. GitHub Actions independently verifies the committed output.

For a hand-authored `.ipynb` (not compiled from `.qmd`), front matter goes
in a **raw cell** (Jupyter cell type "Raw") as the very first cell,
delimited the same way as a `.qmd`'s YAML header (`---` ... `---`).

Commit the source (`index.qmd`/`index.ipynb`) *and* the rendered output
(`index.md` + figure files) together — the rendered output is the actual
build input for Hugo/Cloudflare, so it can't be gitignored.

## `scripts/render_quarto.py`

A thin wrapper around `quarto render` that also fixes up two things the
`hugo-md` writer gets wrong for our setup (see "Known quirks" below):

```bash
python3 scripts/render_quarto.py                          # renders all of content/posts
python3 scripts/render_quarto.py content/posts/my-post/index.qmd   # renders one post
```

It sets `QUARTO_PYTHON` (repo `.venv`) and `MATPLOTLIBRC` (repo
`matplotlibrc`) in the render's environment, then post-processes exactly the
`index.md` files whose source fell under the given target — never every
post in the repo, to avoid re-processing (and corrupting) unrelated files.

## Known quirks and how we work around them

- **`hugo-md`'s "smart" typography flattens Unicode em dashes into ASCII
  `---`.** Fixed via `variant: "-smart"` in `_quarto.yml`'s format config
  (a plain `smart: false` metadata key does *not* work — it has to be a
  variant subtraction).
- **Root-relative links (`/stats/`) get rewritten relative to the source
  file's disk location** (`../../../stats/`), because Quarto assumes it's
  serving the output itself and has no idea Hugo will flatten
  `content/posts/<slug>/index.md` to the URL `/posts/<slug>/`. Since every
  post bundle sits at the same fixed depth, the walk-up prefix Quarto emits
  is always `../../../` — `render_quarto.py` deterministically rewrites it
  back to `/`.
- **A code cell's figure output is a bare `<img>`**, not wrapped in
  anything, so it defaults to centering (or not) against the *entire*
  article width rather than the code block's own (inset, narrower) column.
  `render_quarto.py` wraps it in `<div class="quarto-figure">`, sized in
  CSS to match `.highlight pre.chroma`'s box exactly.
- **`.ipynb` files are not executed by default** — Quarto trusts whatever
  outputs are already stored in the notebook (matching how `nbconvert`
  treats a notebook as "already run"). A hand-built notebook with empty
  `outputs: []` renders code with no output at all unless forced. Fixed
  with `execute: enabled: true` in `_quarto.yml`, so every render actually
  executes the code (still respecting `freeze: auto` caching).
- **knitr (R) and Jupyter (Python) name their figure directories
  differently** for the same `index.qmd`/`index.ipynb` → `index.md`:
  Jupyter produces `index_files/`, knitr produces
  `index.markdown_strict_files/`. Cosmetic only — Hugo copies whatever
  sibling files exist in a leaf bundle regardless of name, so both work
  fine, just don't assume one naming convention when checking output.
- **Matplotlib/R plots default to black text and a white figure
  background**, neither of which survives a theme switch (black text is
  invisible in dark mode; a white box clashes with dark mode). Both are
  fixed project-wide, not per-post:
  - `matplotlibrc` at the repo root sets `savefig.transparent`,
    `figure.facecolor`/`axes.facecolor: none`, and a mid-gray
    (`#888888`) for all text/tick/label/edge colors — legible on both the
    light theme's `#fffff8` background and the dark theme's `#151515`.
  - R's `_quarto.yml` `knitr.opts_chunk.dev.args.bg: transparent` does the
    same for base-R graphics. R plot text color isn't defaulted the same
    way yet since neither demo post currently renders any (both use
    `axes = FALSE`) — worth revisiting via `par()` if a future R post
    needs visible axis labels.
- **Code blocks were already inset 2.5% from the left** relative to
  paragraphs/tables, a leftover from an old scrollbar-rounding fix
  (`margin-left: 2.5%; width: calc(52.5% + 2px)`) that went unnoticed until
  a Quarto post put a table directly under a code block and made the
  misalignment obvious. Fixed by dropping the 2.5% inset entirely
  (`margin-left: 0; width: calc(55% + 2px)`, `box-sizing: border-box` so
  the `1em` padding doesn't push the box wider than the 55% column) — see
  docs/THEME.md → "Code blocks".
