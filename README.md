# Personal Site

<!-- TODO: update URL once Cloudflare Pages project is created -->
**Live site**: [depository.pages.dev](https://depository.pages.dev)

Personal website built with Hugo, styled with Tufte CSS typography.

## Stack

- **Hugo** (extended) — static site generator
- **EB Garamond** — body text
- **JetBrains Mono** — code
- **Tufte CSS** — layout with sidenotes and wide margins
- **KaTeX** — math rendering

## Development

```bash
# Install Hugo (requires Go)
go install -tags extended github.com/gohugoio/hugo@latest

# Dev server with drafts
hugo server -D

# Production build
hugo --minify
```

## Linting

Pre-commit hooks run automatically on `git commit`:

```bash
# Install hooks (first time only)
pre-commit install

# Run all checks manually
pre-commit run --all-files
```

Checks: markdownlint, typos, proselint, stylelint, Hugo build.

## Project Structure

See [AGENTS.md](AGENTS.md) for full project context and architecture decisions.

## Deployment

Deployed to [Cloudflare Pages](https://pages.cloudflare.com/) via native Git integration.
Every push to `main` auto-builds and deploys.

GitHub Actions runs lint checks on all pushes and PRs.
