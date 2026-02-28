# Project Plan

## Task 1: Project Setup [DONE]

- [x] git init
- [x] Install Hugo extended
- [x] Scaffold site with `hugo new site`
- [x] Create AGENTS.md
- [x] Create docs/ structure
- [x] Verify `hugo server` works

## Task 2: Custom Theme [IN PROGRESS]

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
- [x] Add KaTeX includes (auto-render, inline $...$ and display $$...$$)
- [x] Add sample content (hello-world.md with all features, about.md placeholder)
- [x] Document theme decisions in docs/THEME.md
- [x] Fix timezone config (Europe/Belgrade) for correct date handling
- [ ] Add Chroma syntax highlighting CSS theme
- [ ] Awaiting user review and confirmation

### Files Created
- `layouts/_default/baseof.html`
- `layouts/_default/single.html`
- `layouts/_default/list.html`
- `layouts/index.html`
- `assets/css/tufte.css`
- `content/posts/hello-world.md` (draft)
- `content/about.md`

## Task 3: Linters & Pre-commit

- [ ] Set up pre-commit framework
- [ ] HTML linting (htmlhint or similar)
- [ ] CSS linting (stylelint)
- [ ] Markdown linting (markdownlint)
- [ ] Hugo-specific checks

## Task 4: Deployment

- [ ] Research hosting options and costs
- [ ] Set up Cloudflare Pages
- [ ] Configure custom domain (if applicable)
- [ ] Document deployment process
