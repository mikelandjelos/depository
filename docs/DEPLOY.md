# Deployment

## Architecture

```text
push to main → Cloudflare Pages auto-builds and deploys (native Git integration)
push to main → GitHub Actions runs lint checks (independent of deploy)
PR to main   → GitHub Actions runs lint checks
```

Cloudflare Pages handles building and deploying directly from the GitHub repo.
GitHub Actions runs pre-commit linting as a separate quality gate.

## Cloudflare Pages Setup

### Project Configuration

- **Provider**: GitHub (native Git integration)
- **Repository**: mikelandjelos/depository
- **Project name**: depository
- **Build command**: `hugo --minify`
- **Build output directory**: `public`
- **Environment variable**: `HUGO_VERSION` = `0.157.0`
- **Account ID**: `a273338e34e03b4d8e5418336b53adb2`
- **Subdomain**: `mihajlo-madic.workers.dev`

### How Deploys Work

1. Push to `main` triggers Cloudflare Pages to pull the repo, build with Hugo,
   and deploy to `depository.pages.dev`
2. Simultaneously, GitHub Actions runs lint checks
3. PRs get preview deploys (if enabled) at unique URLs

No API tokens or GitHub secrets needed — Cloudflare connects directly to GitHub.

## GitHub Actions (.github/workflows/deploy.yml)

Lint-only workflow that runs `pre-commit run --all-files` on every push and PR.
Installs Python, Node, Hugo, and all linters. Does not deploy — Cloudflare
handles that natively.

## Cross-links

- **Site footer → Repo**: "Source" link, configured via `params.repoURL` in hugo.toml
- **Repo README → Site**: live site URL at the top of README.md

## Custom Domain (optional)

1. In Cloudflare Pages project → Custom domains → Add
2. Enter your domain
3. If domain is on Cloudflare DNS, the CNAME is added automatically
4. Update `baseURL` in hugo.toml to match

## Updating the Live Site URL

Once deployed, update these locations with the actual URL:

1. `hugo.toml` — `baseURL`
2. `README.md` — live site link at top
