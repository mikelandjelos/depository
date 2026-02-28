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
- `content/posts/hello-world.md` (draft)
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

## Task 4: Deployment [IN PROGRESS]

- [x] Research hosting options and costs (Cloudflare Pages chosen — free, unlimited BW)
- [x] Create GitHub Actions workflow — lint only (.github/workflows/deploy.yml)
- [x] Add cross-links: site footer → repo, README → live site
- [x] Document deployment in docs/DEPLOY.md
- [ ] Push latest changes to GitHub
- [ ] Create Cloudflare Pages project via dashboard (native Git integration)
- [ ] Verify first deploy
- [ ] Update baseURL and live site URL once confirmed
- [ ] Configure custom domain (if applicable)

### Deployment Model

Cloudflare Pages connects directly to GitHub (native Git integration).
No API tokens or GitHub secrets needed. Cloudflare auto-builds on push to main.
GitHub Actions runs lint checks independently.

### Files Created

- `.github/workflows/deploy.yml` (lint only)
- `docs/DEPLOY.md`
