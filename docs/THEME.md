# Theme Implementation Details

## Architecture

Custom theme built inline (no `themes/` directory). All templates live in
`layouts/`, all styles in `assets/css/`.

## Files

| File | Purpose |
|---|---|
| `layouts/_default/baseof.html` | Base template: `<head>` with favicon, fonts, KaTeX, CSS; site header nav; footer |
| `layouts/_default/single.html` | Article/post page: title, status badge, subtitle, date, category, tags, content |
| `layouts/_default/list.html` | Section list page: title, content, chronological post list |
| `layouts/_default/taxonomy.html` | Tag/category index page: alphabetical list of terms with post counts |
| `layouts/_default/term.html` | Single tag/category page: chronological list of posts with that term |
| `layouts/index.html` | Homepage: site title, description, recent 10 posts from `posts/` section |
| `layouts/_default/cv.html` | Curriculum Vitae page: renders `data/cv.yaml` (see "Curriculum Vitae" below) |
| `assets/css/tufte.css` | All styles — adapted Tufte CSS + site header/nav/footer/post-list/avatar |
| `assets/css/syntax-light.css` | Chroma syntax highlighting — monokailight (light mode) |
| `assets/css/syntax-dark.css` | Chroma syntax highlighting — monokai (dark mode) |

## Design Decisions

### Typography

- **Body**: EB Garamond (Google Fonts) — serif, 15px base, 1.4rem paragraph size
- **Code**: JetBrains Mono (Google Fonts) — 1rem inline, 0.9rem in blocks
- **Headings**: h1 normal weight 3.2rem; h2/h3 italic weight 400
- **New thought**: `span.newthought` — small-caps opener for topic shifts
- **Drop cap**: `article section > p:first-child::first-letter` — first letter of a
  post's first paragraph rendered large (4.2rem) in UnifrakturMaguntia (Google
  Fonts), an illuminated-manuscript-style blackletter face

### Layout

- Tufte-style: 87.5% body width, 12.5% left padding, 55% main content column
- Right margin reserved for sidenotes/margin notes (floated right, -60% margin)
- Max-width 1400px to prevent over-stretching on ultrawide monitors

### Colors

- Background: `#fffff8` (off-white), text: `#111` (off-black)
- Dark mode via `prefers-color-scheme: dark` — bg `#151515`, text `#ddd`
- Inline code: `#e8e8e0` background (light), `#303030` with `#e0e0e0` text (dark)
- Code blocks: transparent background, styled by Chroma syntax CSS
- Links: inherit color, subtle underline (0.05em thickness, 0.15em offset)

### Table of contents

- Auto-generated via Hugo's built-in `.TableOfContents` (from goldmark), shown
  in `single.html` only when a post has 2+ headings
  (`len (findRE "<h[2-6][^>]*>" .Content) >= 2`)
- Hugo emits `<nav id="TableOfContents"><ul>...</ul></nav>` — the `id` is
  hardcoded by Hugo itself, hence the `selector-id-pattern` stylelint-disable
  around that block in `tufte.css`
- Styled as a numbered decimal outline (1, 1.1, 1.1.1 …) purely with CSS
  counters (`counter-reset`/`counter-increment`/`counters()`), no box or
  background — inspired by gwern.net's TOC treatment, adapted into this site's
  existing single-column flow rather than copying gwern's separate left-rail
  column layout
- Nested levels shrink slightly in size/opacity (selector targets any nested
  `ul` inside `#TableOfContents`)
- "Contents" label above it: `p.toc-label`, small-caps, matches other
  small-caps accents on the site

### Metadata: tags, categories, status

Resolved from GitHub issue #8's brainstorm (tags, singular category, date
created, draft/"digital garden" maturity system):

- **Tags** and **categories** are real Hugo taxonomies (`[taxonomies]` in
  hugo.toml: `tag = 'tags'`, `category = 'categories'`), not plain front
  matter strings — this gets `/tags/`, `/tags/<term>/`, `/categories/`, and
  `/categories/<term>/` index pages automatically. `layouts/_default/taxonomy.html`
  renders the "all terms" index (alphabetical, with post counts);
  `layouts/_default/term.html` renders a single term's post list (same
  markup/CSS as the post-list on `/posts/`). Front matter: `tags: [...]`
  (multiple) and `categories: [...]` (Hugo taxonomies are inherently
  multi-value, but the convention here is one category per post — just
  keep the list to a single item).
- In `single.html`, both render as links (via `.GetTerms "tags"` /
  `.GetTerms "categories"`, not raw `.Params` strings) in the post-meta
  line: `date — category — tag, tag`.
- **Date created** is still just the existing `date` front-matter field —
  no separate field was added, "created" is implicit/conventional rather
  than an explicit UI label.
- **Maturity/draft badge**: decided in the #8 brainstorm to publish
  everything (not hide via Hugo's own `draft: true`) and show a visible
  badge on unfinished posts instead. New front-matter field `status` (any
  string; the CSS doesn't hardcode specific values), rendered as a small
  bordered small-caps pill (`p.status-badge`) right under the title when
  present, omitted entirely otherwise. `content/posts/hello-world.md`
  demos this with `status: "seedling"`. Exact vocabulary/levels beyond that
  one demo value are still open — could grow into a seedling/budding/
  evergreen spectrum later if wanted.

### Sidenotes (from Tufte CSS)

- Uses checkbox toggle pattern: `<label>` + `<input type="checkbox">` + `<span>`
- Numbered sidenotes: class `sidenote-number` on label, `sidenote` on span
- Margin notes: no number, `marginnote` on span, `⊕` toggle symbol
- On mobile (<760px): hidden by default, tap number/symbol to expand inline

### Math (KaTeX)

- KaTeX v0.16.33 loaded from jsDelivr CDN with SRI hashes
- Auto-render extension: `$…$` for inline, `$$…$$` for display
- Hugo passthrough extension (`markup.goldmark.extensions.passthrough`) preserves
  LaTeX delimiters so Goldmark does not mangle backslashes
- Display math centered via `.katex-display` CSS (width: 55%, text-align: center)
- Deferred loading — does not block page render

### Syntax Highlighting

- Hugo's built-in Chroma highlighter with `noClasses = false`
- Uses CSS classes (not inline styles) for theme-ability
- Two Chroma CSS files generated via `hugo gen chromastyles`:
  - `syntax-light.css` (monokailight) — loaded with `media="(prefers-color-scheme: light)"`
  - `syntax-dark.css` (monokai) — loaded with `media="(prefers-color-scheme: dark)"`

### Code blocks — width/scroll architecture (important gotcha)

Chroma's highlighted output nests `<code class="language-...">` directly
inside `<pre class="chroma">`. The generic `pre > code` selector (meant for
*plain*, non-highlighted fences) also matches that nested `<code>`. Giving
both the outer `pre.chroma` and the inner `code` their own `width: 52.5%`
double-shrinks the actual text column (52.5% of an already 52.5%-wide box,
~27.5% of the container) while the visible background box stays full width —
and gives the inner `code` its own independent `overflow-x: auto` scrollbar
nested inside the outer one. Most lines fit inside that hidden narrower
column so it went unnoticed, but a longer line (or browser zoom, which
shrinks available CSS pixels) would overflow it, producing a
scrollbar/clipped text sitting mid-box, well short of the box's visible right
edge.

Fix (`tufte.css`): scope the width/margin/scroll box rule to
`pre:not(.chroma) > code` (plain fences only); `.highlight pre.chroma` owns
sizing/scrolling for highlighted blocks, and its inner `code` just fills it
(`display: block; width: 100%; overflow-x: visible`). Same split applies in
the mobile media query. Also: a `calc(<pct> + 2px)` buffer on the outer boxes
plus explicit `overflow-y: hidden` guards against subpixel-rounding
false-positive scrollbars at non-100% zoom (setting only `overflow-x` lets
the browser compute `overflow-y` as an ambiguous auto-like value per spec).
Horizontal scrollbars (on code blocks and `div.table-wrapper`) are styled
thin/theme-colored via `scrollbar-width`/`scrollbar-color` +
`::-webkit-scrollbar*`, instead of the bulky OS-default one.

### Navigation

- Minimal top bar: site name (small-caps, left) + nav links (right, flexbox)
- Links from `[menus.main]` in hugo.toml
- Current pages: Posts, About, Curriculum Vitae

### Curriculum Vitae

The `/cv/` page renders live from Mihajlo's separate
[curriculum-vitae](https://github.com/mikelandjelos/curriculum-vitae) repo
(source of truth: `cv.tex`), not hand-authored content. Split out from
GitHub issue #3 (which originally asked for CV content to live on the About
page) — About and CV serve different purposes: About is a personal/site-
philosophy page (à la [gwern.net/about](https://gwern.net/about)), CV is the
professional résumé. About remains a placeholder until that content gets
written.

**Pipeline:**

1. `scripts/sync_cv.py` parses `cv.tex` (from a local path via `--input`, or
   — only useful if the repo ever becomes public — its raw URL) into
   `data/cv.yaml`. This is a **targeted parser for this specific LaTeX
   template**, not a general LaTeX-to-anything converter — the template uses
   custom `onecolentry`/`twocolentry`/`highlights`/`header` environments
   (from a RenderCV-style CV template) that plain `pandoc` cannot render (it
   doesn't know what to do with undefined custom environments). The parser
   does balanced-brace-aware extraction of those environments plus a
   `clean_latex()` pass that converts `\textbf`/`\textit`/`\texttt`/`\href`
   etc. into Markdown, so the resulting YAML holds Markdown strings that
   `layouts/_default/cv.html` renders via Hugo's `markdownify`.
2. `layouts/_default/cv.html` reads `.Site.Data.cv` and renders the header
   (name and contact line — inline SVG icons from
   `layouts/partials/icon.html`, keyed by each contact entry's `icon` field,
   no icon-font dependency), then each section's entries: `kind: entry`
   (title/subtitle left,
   right-aligned `meta` — a list of lines, not a folded string, since YAML
   flow-scalar line-folding collapses blank-line-separated text to a single
   `\n`/space rather than preserving a real line break) with optional
   `highlights` bullets, or `kind: text` for a plain paragraph (used by the
   Summary and Skills sections, which have no title/date row).
3. `.github/workflows/sync-cv.yml` (in this repo) checks out
   **curriculum-vitae — a private repo** — using a
   `CURRICULUM_VITAE_READ_TOKEN` secret (a PAT with Contents:Read on
   curriculum-vitae, added to *this* repo's secrets), then re-runs the
   parser against that checkout and commits `data/cv.yaml` if it changed, on
   a `repository_dispatch` `cv-updated` event or manual `workflow_dispatch`.
   That commit triggers the existing Cloudflare auto-deploy — no separate
   deploy step needed. (Earlier versions of this workflow tried an
   unauthenticated `raw.githubusercontent.com` fetch, which 404s for a
   private repo — first real end-to-end test caught this.)
4. The curriculum-vitae repo has a companion workflow (pushed directly
   there, **not** tracked in this repo) that fires the `cv-updated`
   dispatch on every push to `cv.tex`, using a `DEPOSITORY_DISPATCH_TOKEN`
   secret (a PAT with Contents:Read-and-write on `depository`, added to
   curriculum-vitae's secrets) — confirmed working as of the first real
   sync.

**Styling:** contact icons are minimal inline SVGs (Feather-icons-style,
`layouts/partials/icon.html`, keyed by the `icon` field in `data/cv.yaml`) —
no external icon-font dependency for just six glyphs. Section headings get a
`border-bottom` rule (visual nod to the LaTeX template's `\titlerule`)
rather than the italic `h2` style used elsewhere. Entry rows are a flex row
(title/subtitle left, date/location right), stacking to a single column on
mobile (`<760px`).

**Width, twice fixed:** `article.cv` is capped at `max-width: 850px` —
printed CVs are page-width, not browser-width, and stretching title-left/
date-right rows across the site's full ~1400px container leaves huge dead
gaps in every row. Separately, `section.cv-section`'s direct `p`/`ul`/`ol`/
`dl` children need an explicit `width: 100%` override, because the site's
global blog-prose rules (`section > p { width: 55% }`,
`section > ul { width: 50% }`) silently apply to `.cv-text`/`.cv-highlights`
too otherwise (same-specificity selectors that this page's own rules never
overrode, since a rule that doesn't set `width` doesn't "win" against one
that does) — the mismatch is not obvious until you compare a paragraph's
wrap width against a sibling entry row's date position.

### Favicon & Avatar

- `static/favicon.ico` — 32×32, generated from GitHub profile picture
- `static/favicon.png` — 180×180, used as Apple touch icon and homepage avatar
- Favicon linked in `baseof.html` head
- Homepage avatar: 64px circular, slightly transparent (opacity 0.85), displayed
  inline next to site title via `.home-header` flexbox in `index.html`

### Footer

- Copyright notice + "Source" link to GitHub repo
- Repo URL configured via `params.repoURL` in hugo.toml

### Responsive (<760px)

- Body expands to 84% width, 8% padding each side
- Main content + lists + code blocks + `.katex-display` + `#TableOfContents`
  expand to ~100% width
- Sidenotes/margin notes collapse to toggleable inline blocks
- Images scale to 100% width

## Hugo Configuration Notes

- `baseURL = 'https://depository.mihajlo-madic.workers.dev/'`
- `title = 'Mihajlo Madić'`
- `timeZone = 'Europe/Belgrade'` — prevents today's posts being treated as future
- `markup.goldmark.renderer.unsafe = true` — required for sidenote HTML in markdown
- `markup.goldmark.extensions.passthrough` — preserves `$…$` and `$$…$$` for KaTeX
- `markup.highlight.noClasses = false` — CSS-based syntax highlighting

## Sample Content

- `content/posts/hello-world.md` — demonstrates all features (sidenotes, math, code)
- `content/about.md` — placeholder about page

## Known TODOs

- Consider Hugo shortcodes for sidenotes (cleaner than raw HTML in markdown)
- Add RSS feed customization
- Add Open Graph / meta tags for social sharing
- TOC layout needs refinement — currently inserts too much vertical
  whitespace; should read more like gwern.net's compact TOC treatment
  (tracked in GitHub issue, see docs/PLAN.md)
- Manual light/dark mode toggle (currently `prefers-color-scheme` only, no
  user override) — inspired by gwern.net's mode selector (tracked in GitHub
  issue, see docs/PLAN.md)
- Post metadata: tags, singular category, date-created, and a
  draft/not-draft "digital garden" maturity system — design still being
  brainstormed (tracked as GitHub sub-issue #8 of #2)
