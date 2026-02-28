# AGENTS.md — Project Context for AI Agents

## Project Overview

Personal website/blog with a clean, academic, CS-oriented aesthetic.
Inspired by: gwern.net, distill.pub, ciechanow.ski, Andy Matuschak's notes.

## Tech Stack

- **Static site generator**: Hugo (extended edition, v0.157.0+)
- **Typography**: EB Garamond (body text), JetBrains Mono (code)
- **Layout/CSS**: Tufte CSS (sidenotes, wide margins, clean layout)
- **Math rendering**: KaTeX v0.16.33 (CDN, with Hugo passthrough extension)
- **Deployment**: Cloudflare Pages
- **Linting**: pre-commit with markdownlint, typos, proselint, stylelint

## Project Structure

```text
site/
├── archetypes/                    # Content templates (Hugo default)
├── assets/
│   └── css/
│       ├── tufte.css              # All styles — adapted Tufte CSS
│       ├── syntax-light.css       # Chroma monokailight (light mode)
│       └── syntax-dark.css        # Chroma monokai (dark mode)
├── content/
│   ├── about.md                   # About page
│   └── posts/
│       └── hello-world.md         # Sample post (draft) with all features
├── data/                          # Data files (JSON/YAML/TOML)
├── docs/
│   ├── PLAN.md                    # High-level plan and task tracking
│   └── THEME.md                   # Theme implementation details
├── i18n/                          # Translations
├── layouts/
│   ├── _default/
│   │   ├── baseof.html            # Base template (head, nav, footer)
│   │   ├── list.html              # Section list template
│   │   └── single.html            # Article/post template
│   └── index.html                 # Homepage template
├── static/                        # Static files (fonts, images, etc.)
├── themes/                        # (unused — custom theme in layouts/ + assets/)
├── .gitignore
├── .markdownlint-cli2.yaml        # Markdownlint config
├── .pre-commit-config.yaml        # Pre-commit hooks config
├── .proselintrc.json              # Proselint config
├── .stylelintrc.json              # Stylelint config
├── _typos.toml                    # Typos spell checker config
├── hugo.toml                      # Hugo configuration
├── README.md                      # Project README
└── AGENTS.md                      # This file
```

## Key Decisions

- **No external theme**: Custom minimal theme built from Tufte CSS, living in
  `layouts/` and `assets/` directly (not under `themes/`).
- **Fonts via Google Fonts**: EB Garamond + JetBrains Mono loaded from CDN.
- **KaTeX via CDN**: Client-side math rendering with auto-render extension.
  Hugo passthrough extension preserves LaTeX delimiters in Markdown.
- **Pre-commit hooks**: All commits are checked for markdown lint, spelling,
  prose quality, CSS lint, and Hugo build correctness.

## Task Sequence

1. [DONE] Project setup — Hugo install, scaffold, git init, docs
2. [DONE] Custom theme — Tufte CSS + fonts + KaTeX, inspired by reference sites
3. [DONE] Linters/pre-commit — markdownlint, typos, proselint, stylelint, hugo build
4. [TODO] Deployment — Cloudflare Pages setup + alternatives research

## Development

```bash
# Dev server with drafts
hugo server -D

# Build for production
hugo --minify

# Run all linters manually
pre-commit run --all-files
```

## Pre-commit Hooks

| Hook | What it checks |
|---|---|
| trailing-whitespace | Trailing spaces |
| end-of-file-fixer | Missing final newline |
| check-toml / check-yaml | Config file syntax |
| check-merge-conflict | Leftover merge markers |
| mixed-line-ending | Enforces LF |
| markdownlint-cli2 | Markdown formatting (config: .markdownlint-cli2.yaml) |
| typos | Spelling (config: _typos.toml) |
| proselint | Prose quality (config: .proselintrc.json) |
| stylelint | CSS lint (config: .stylelintrc.json, ignores generated syntax CSS) |
| hugo build | Verifies site builds without errors |

## Notes for Continuing Agents

- User prefers step-by-step workflow: finish one task fully before starting next.
- User will explicitly say a task is "done" before moving on.
- **CRITICAL: Keep all documentation tightly updated.** Every change to code,
  config, or architecture MUST be reflected in AGENTS.md, docs/PLAN.md, and
  docs/THEME.md. No information should be dropped or left stale. If you add a
  file, update the project structure. If you make a design decision, document it.
  Another agent must be able to pick up exactly where you left off.
- Run `pre-commit run --all-files` before considering any task complete.
