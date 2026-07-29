# Mihajlo Madić's Depository

Personal site for research notes, essays, and technical experiments.

**Live site**: <https://depository.mihajlo-madic.workers.dev/>

## Features

- Tufte-inspired, responsive reading layout with sidenotes and margin notes
- Light, dark, and system-following color modes
- KaTeX math, Chroma syntax highlighting, and responsive tables/code blocks
- Post table of contents, drop caps, tags, categories, and maturity badges
- Tag and category archive pages, each with an RSS feed; the site and posts
  indexes also have feeds
- Canonical, Open Graph, and Twitter/X text metadata for useful shared-link
  previews
- Deterministic 1200×630 mathematical post cards for social previews
- A daily public-domain Met artwork, locally cached and framed on the homepage
- Statistics page for writing, tags, and repository activity
- "Unresolved Promises" on the post index, sourced from open article issues
- Data-driven Curriculum Vitae, synchronized from the separate
  `curriculum-vitae` repository
- Executable Quarto posts in Python and R, plus directly authored Jupyter
  notebooks

## Stack

- [Hugo](https://gohugo.io/) extended v0.157.0+ for the static site
- Custom templates and Tufte CSS, with EB Garamond and JetBrains Mono
- [KaTeX](https://katex.org/) for browser-side math rendering
- [Quarto](https://quarto.org/) for optional scientific-post authoring
- Cloudflare Workers with native GitHub integration for deployment
- GitHub Actions and pre-commit for linting and build verification

## Write a Post

Plain Markdown posts live in `content/posts/`. Hugo front matter supports
`title`, `subtitle`, `date`, `tags`, `categories`, `status`, and optional
`tableStyle` (`"striped"` or `"grid"`).

Quarto posts use a Hugo page bundle at `content/posts/<slug>/`. Render a
`.qmd` or `.ipynb` source file before committing it:

```bash
python3 scripts/render_quarto.py content/posts/my-post/index.qmd
```

Commit the source, generated `index.md`, and any generated figures together.
Post cards need no author action: the local pre-commit hook generates and
stages them in the same commit, while GitHub Actions verifies that committed
cards are current.
See [docs/QUARTO.md](docs/QUARTO.md) for the full Python, R, and notebook
workflow.

Use `{{< cite key >}}` in Markdown, Quarto, or notebook posts for an
author-year citation, then place `{{< references >}}` at the end. Add the
keyed record to `data/references.yaml`; the bibliography includes only cited
works.

Use `{{< post slug="post-slug" >}}` to reference another post while writing,
or add `text="Label"` to supply link text. Hugo resolves the post title and
URL at build time; internal post links receive a local hover/focus preview
automatically.

## Development

```bash
# Build the production site
hugo --minify

# Serve drafts locally at http://localhost:1313/
hugo server -D

# Run all formatting, prose, style, and build checks
pre-commit run --all-files
```

Hugo extended v0.157.0+ is required. For Quarto authoring, install the
additional tools described in [docs/QUARTO.md](docs/QUARTO.md).

## Deployment

Pushing to `main` triggers Cloudflare's native Git integration: it runs
`hugo --minify` and deploys the generated `public/` directory through
Wrangler. GitHub Actions independently runs `pre-commit run --all-files` on
pushes and pull requests.

See [docs/DEPLOY.md](docs/DEPLOY.md) for the configuration and deployment
flow.

## Documentation

- [AGENTS.md](AGENTS.md): project structure, decisions, and agent workflow
- [docs/THEME.md](docs/THEME.md): templates, styling, and site features
- [docs/QUARTO.md](docs/QUARTO.md): executable-post toolchain and workflow
- [docs/DEPLOY.md](docs/DEPLOY.md): deployment architecture
- [docs/PLAN.md](docs/PLAN.md): issue-driven implementation status
