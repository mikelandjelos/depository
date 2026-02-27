# AGENTS.md — Project Context for AI Agents

## Project Overview

Personal website/blog with a clean, academic, CS-oriented aesthetic.
Inspired by: gwern.net, distill.pub, ciechanow.ski, Andy Matuschak's notes.

## Tech Stack

- **Static site generator**: Hugo (extended edition, v0.157.0+)
- **Typography**: EB Garamond (body text), JetBrains Mono (code)
- **Layout/CSS**: Tufte CSS (sidenotes, wide margins, clean layout)
- **Math rendering**: KaTeX
- **Deployment**: Cloudflare Pages

## Project Structure

```
site/
├── archetypes/       # Content templates
├── assets/           # CSS/JS processed by Hugo Pipes
├── content/          # Markdown content (posts, pages)
├── data/             # Data files (JSON/YAML/TOML)
├── docs/             # Project documentation (plan, todos, specs)
│   ├── PLAN.md       # High-level plan and task tracking
│   └── THEME.md      # Theme implementation details
├── i18n/             # Translations
├── layouts/          # HTML templates
├── static/           # Static files (fonts, images, etc.)
├── themes/           # (unused — custom theme lives in layouts/ + assets/)
├── hugo.toml         # Hugo configuration
└── AGENTS.md         # This file
```

## Key Decisions

- **No external theme**: Custom minimal theme built from Tufte CSS, living in
  `layouts/` and `assets/` directly (not under `themes/`).
- **Fonts via Google Fonts**: EB Garamond + JetBrains Mono loaded from CDN.
- **KaTeX via CDN**: Client-side math rendering.

## Task Sequence

1. [DONE] Project setup — Hugo install, scaffold, git init, docs
2. [TODO] Custom theme — Tufte CSS + fonts + KaTeX, inspired by reference sites
3. [TODO] Linters/pre-commit — HTML/CSS/MD linting, formatting
4. [TODO] Deployment — Cloudflare Pages setup + alternatives research

## Development

```bash
# Dev server with drafts
hugo server -D

# Build for production
hugo --minify
```

## Notes for Continuing Agents

- User prefers step-by-step workflow: finish one task fully before starting next.
- Keep this file and docs/ updated as you make progress.
- User will explicitly say a task is "done" before moving on.
