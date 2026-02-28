# Deployment

## Architecture

```text
push to main → Cloudflare auto-builds (hugo --minify) and deploys via wrangler
push to main → GitHub Actions runs lint checks (independent of deploy)
PR to main   → GitHub Actions runs lint checks
```

Cloudflare handles building and deploying directly from the GitHub repo.
GitHub Actions runs pre-commit linting as a separate quality gate.

## Live URLs

- **Production**: <https://depository.mihajlo-madic.workers.dev/>
- **Workers subdomain**: mihajlo-madic.workers.dev

## Cloudflare Project Configuration

- **Provider**: GitHub (native Git integration)
- **Repository**: mikelandjelos/depository
- **Project name**: depository
- **Build command**: `hugo --minify`
- **Deploy command**: `npx wrangler deploy`
- **Build output directory**: `public`
- **Environment variable**: `HUGO_VERSION` = `0.157.0`
- **Account ID**: `a273338e34e03b4d8e5418336b53adb2`
- **Non-production builds**: disabled (main branch only)

## wrangler.toml

The repo includes a `wrangler.toml` that tells wrangler to deploy `public/`
as static assets, preventing it from trying to re-run Hugo as an npm package.

## How Deploys Work

1. Push to `main` triggers Cloudflare to pull the repo
2. Cloudflare runs `hugo --minify` to build into `public/`
3. Wrangler deploys `public/` as static assets
4. Site is live at depository.mihajlo-madic.workers.dev
5. Simultaneously, GitHub Actions runs lint checks (independent pipeline)

No manual API tokens or GitHub secrets needed — Cloudflare connects directly
to GitHub via its native Git integration.

## GitHub Actions (.github/workflows/deploy.yml)

Lint-only workflow that runs `pre-commit run --all-files` on every push and PR.
Installs Python, Node, Hugo, and all linters. Does not deploy — Cloudflare
handles that.

## Cross-links

- **Site footer → Repo**: "Source" link, configured via `params.repoURL` in hugo.toml
- **Repo README → Site**: live site link at the top of README.md

## Custom Domain (optional)

1. In Cloudflare project → Custom domains → Add
2. Enter your domain
3. If domain is on Cloudflare DNS, the CNAME is added automatically
4. Update `baseURL` in hugo.toml to match
