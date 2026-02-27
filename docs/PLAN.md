# Project Plan

## Task 1: Project Setup [DONE]

- [x] git init
- [x] Install Hugo extended
- [x] Scaffold site with `hugo new site`
- [x] Create AGENTS.md
- [x] Create docs/ structure
- [x] Verify `hugo server` works

## Task 2: Custom Theme

Build a minimal custom theme inline (layouts/ + assets/) using:
- Tufte CSS for layout (sidenotes, wide margins, responsive)
- EB Garamond (Google Fonts) for body text
- JetBrains Mono (Google Fonts) for code
- KaTeX for math rendering

### Subtasks
- [ ] Research reference sites for specific design choices
- [ ] Create base layout (baseof.html)
- [ ] Create single post template (single.html)
- [ ] Create list/index template (list.html, index.html)
- [ ] Add CSS (Tufte CSS base + custom overrides)
- [ ] Add KaTeX includes
- [ ] Add sample content to verify everything works
- [ ] Document theme decisions in docs/THEME.md

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
