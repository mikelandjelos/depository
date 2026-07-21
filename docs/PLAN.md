# Project Plan

## Task 1: Project Setup [DONE]

- [x] git init
- [x] Install Hugo extended
- [x] Scaffold site with `hugo new site`
- [x] Create AGENTS.md
- [x] Create docs/ structure
- [x] Verify `hugo server` works

## Task 2: Custom Theme [DONE]

Build a minimal custom theme inline (layouts/ + assets/) using:

- Tufte CSS for layout (sidenotes, wide margins, responsive)
- EB Garamond (Google Fonts) for body text
- JetBrains Mono (Google Fonts) for code
- KaTeX for math rendering

### Subtasks

- [x] Research reference sites for specific design choices
- [x] Create base layout (baseof.html) — fonts, KaTeX CDN, CSS, nav, footer
- [x] Create single post template (single.html) — title, subtitle, date, tags
- [x] Create list/index template (list.html, index.html) — chronological post list
- [x] Add CSS (Tufte CSS adapted for EB Garamond + JetBrains Mono)
- [x] Add KaTeX includes (auto-render, inline `$…$` and display `$$…$$`)
- [x] Add sample content (hello-world.md with all features, about.md placeholder)
- [x] Document theme decisions in docs/THEME.md
- [x] Fix timezone config (Europe/Belgrade) for correct date handling
- [x] Add Chroma syntax highlighting CSS (monokailight + monokai for dark mode)
- [x] Fix KaTeX (upgraded to v0.16.33, added Hugo passthrough extension)
- [x] Fix code block contrast and remove border-left
- [x] Center display math with `.katex-display` CSS

### Files Created

- `layouts/_default/baseof.html`
- `layouts/_default/single.html`
- `layouts/_default/list.html`
- `layouts/index.html`
- `assets/css/tufte.css`
- `assets/css/syntax-light.css` (Chroma monokailight)
- `assets/css/syntax-dark.css` (Chroma monokai)
- `content/posts/hello-world.md`
- `content/about.md`

## Task 3: Linters & Pre-commit [DONE]

- [x] Install pre-commit framework
- [x] Configure pre-commit hooks (.pre-commit-config.yaml)
- [x] Markdown linting (markdownlint-cli2)
- [x] Spell checking (typos)
- [x] Prose linting (proselint)
- [x] CSS linting (stylelint)
- [x] General file hygiene (trailing whitespace, EOF, TOML/YAML, line endings)
- [x] Hugo build check (runs on every commit)
- [x] Fix all existing lint errors across docs
- [x] All hooks passing on full codebase

### Files Created

- `.pre-commit-config.yaml`
- `.markdownlint-cli2.yaml`
- `.stylelintrc.json`
- `.proselintrc.json`
- `_typos.toml`

## Task 4: Deployment [DONE]

- [x] Research hosting options and costs (Cloudflare chosen — free, unlimited BW)
- [x] Create GitHub Actions workflow — lint only (.github/workflows/deploy.yml)
- [x] Add cross-links: site footer → repo, README → live site
- [x] Document deployment in docs/DEPLOY.md
- [x] Create Cloudflare project via dashboard (native Git integration)
- [x] Add wrangler.toml for static asset deployment
- [x] Verify first deploy — live at depository.mihajlo-madic.workers.dev
- [x] Update baseURL in hugo.toml
- [x] Add favicon (from GitHub profile picture)
- [x] Add homepage avatar (64px circular, from same profile picture)
- [x] Configure main-branch-only deploys (no non-production builds)

### Deployment Model

Cloudflare builds and deploys via native Git integration on push to main.
`wrangler.toml` configures static asset serving from `public/` directory.
GitHub Actions runs lint checks independently.

### Files Created

- `.github/workflows/deploy.yml` (lint only)
- `docs/DEPLOY.md`
- `wrangler.toml`
- `static/favicon.ico`
- `static/favicon.png`

## Task 5: GitHub-issue-driven fixes/features [IN PROGRESS]

Working through <https://github.com/mikelandjelos/depository/issues> in
sequence, skipping issue #5 (Graph indexing) for last/brainstorm.

- [x] **#1 Mobile view issues** [CLOSED] — code blocks and KaTeX math were
      clipped/squeezed on mobile and at non-100% browser zoom.
  - Mobile media query widened `pre > code` but missed `.highlight
    pre.chroma` and `.katex-display`, so they stayed at desktop widths on
    small screens.
  - Real root cause of the persistent zoom-triggered scrollbar/clipping bug:
    a CSS selector collision double-shrinking the `<code>` inside
    chroma-highlighted blocks (see docs/THEME.md → "Code blocks — width/scroll
    architecture").
  - Added themed thin scrollbars for code/table horizontal overflow.
- [x] **#2 Page/post enhancement** [CLOSED] — auto TOC + drop cap.
  - Auto-generated numbered-outline TOC (gwern-inspired), shown for posts
    with 2+ headings.
  - Illuminated-manuscript-style drop cap on a post's first letter.
  - Metadata (tags/category/date/draft) split into sub-issue #8, design
    still being brainstormed.
- [x] **#3 About Me page** [CV part shipped in 32038e2; About part still open]
  - Originally asked for CV content to live on the About page — split
    instead, since About (personal/site-philosophy, gwern.net/about-style)
    and CV (professional résumé) serve different purposes.
  - Shipped: `/cv/` page, data-driven from Mihajlo's separate
    curriculum-vitae repo's `cv.tex` via `scripts/sync_cv.py` →
    `data/cv.yaml` → `layouts/_default/cv.html`. See docs/THEME.md →
    "Curriculum Vitae" for the full pipeline.
  - **Confirmed working end-to-end**: a real push to `cv.tex` on
    curriculum-vitae now auto-syncs to `/cv/` with no manual step — verified
    live (notify workflow → `repository_dispatch` → sync-cv.yml →
    `data/cv.yaml` commit → Cloudflare auto-deploy). Needed two secrets:
    `DEPOSITORY_DISPATCH_TOKEN` in curriculum-vitae (dispatch permission on
    depository) and `CURRICULUM_VITAE_READ_TOKEN` in depository
    (Contents:Read on curriculum-vitae, since it's a *private* repo — the
    original design assumed public and had to be fixed after the first
    real test 404'd). Also fixed a parser bug found in the same test pass:
    LaTeX comments (`% ...`) weren't stripped, so a commented-out `\item`
    still rendered.
  - Scaffolded `content/about.md`: a `p.wip-notice` marker (small, italic,
    excluded from the drop-cap selector so it doesn't get the illuminated
    first-letter treatment meant for real opening prose — see docs/THEME.md
    → Typography), plus two placeholder section headers ("Who I am", "Why
    this site") and a link to `/cv/` for the professional side. The
    headers auto-trigger the TOC feature from #2 (2+ headings).
  - **Still open**: filling in the actual personal/philosophical content
    under those headers — intentionally left to Mihajlo to write himself,
    not something to fabricate on his behalf. `about.md` also needed a
    `date` front-matter field added (was missing entirely, which rendered
    as "January 1, 0001" via `single.html`'s `.Date.Format` once the page
    had real content to look at).
- [x] **#8 Post metadata** [CLOSED, sub-issue of #2]
  - Tags and categories are real Hugo taxonomies now (`/tags/`,
    `/categories/`, and per-term pages), linked from post-meta instead of
    plain text.
  - Date created: kept as the existing `date` field, no separate field
    added.
  - Maturity badge: new `status` front-matter field, rendered as a small
    bordered pill when present, omitted otherwise. Vocabulary still open
    beyond the `hello-world.md` demo (`status: "seedling"`).
  - See docs/THEME.md → "Metadata: tags, categories, status" for the full
    design.
- [x] **#9 ToC layout refinement** [CLOSED] — tightened line-height
      (1.7 → 1.35), font-size (1.2rem → 1.15rem), and margins around
      `#TableOfContents`/`p.toc-label`; ~26% shorter block for a 7-item
      list. See docs/THEME.md → "Table of contents".
- [ ] **#10 Manual light/dark mode toggle** [OPEN] — gwern-style mode
      switcher, not just `prefers-color-scheme`.
- [ ] **#4 Integrate Quarto Scientific publishing** [OPEN]
- [ ] **#6 Articles** [OPEN]
- [ ] **#7 Github interop** [OPEN]
- [ ] **#5 Graph indexing** [OPEN] — deliberately last; needs a brainstorming
      pass before implementation.

### Notes

- Every fix in this task is verified in-browser (via claude-in-chrome) before
  being committed, not just by `hugo build` succeeding.
- Each closed issue gets a comment summarizing what shipped, before closing.
