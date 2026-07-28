# Theme Implementation Details

## Architecture

Custom theme built inline (no `themes/` directory). All templates live in
`layouts/`, all styles in `assets/css/`.

## Files

| File | Purpose |
|---|---|
| `layouts/_default/baseof.html` | Base template: `<head>` with favicon, fonts, KaTeX, CSS; site header nav; footer |
| `layouts/_default/single.html` | Article/post page: title, status badge, subtitle, date, category, tags, content |
| `layouts/_default/list.html` | Section list page: title, content, chronological post list, "Unresolved Promises" on `/posts/` (see below) |
| `layouts/_default/taxonomy.html` | Tag/category index page: alphabetical list of terms with post counts |
| `layouts/_default/term.html` | Single tag/category page: chronological list of posts with that term |
| `layouts/index.html` | Homepage: site title, description, recent 10 posts from `posts/` section |
| `layouts/_default/cv.html` | Curriculum Vitae page: renders `data/cv.yaml` (see "Curriculum Vitae" below) |
| `layouts/_default/stats.html` | Statistics page: writing/tag/repo-activity numbers (see "Statistics" below) |
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
- Dark mode: bg `#151515`, text `#ddd`
- Inline code: `#e8e8e0` background (light), `#303030` with `#e0e0e0` text (dark)
- Code blocks: transparent background, styled by Chroma syntax CSS
- Links: inherit color, subtle underline (0.05em thickness, 0.15em offset)
- All theme-dependent colors are CSS custom properties (`--color-bg`,
  `--color-text`, `--color-border`, `--color-code-bg`, `--color-code-text`,
  `--color-scrollbar-thumb`) defined once at the top of `tufte.css` — see
  "Light/dark/auto theme toggle" below for why (a manual override needs to
  win over the system's `prefers-color-scheme`, which a scattered
  per-component `@media` block can't do cleanly).

### Light/dark/auto theme toggle

Resolved GitHub issue #10 (gwern-style manual override, not just following
the OS setting):

- **CSS**: `:root` defines the light values for the `--color-*` custom
  properties above; `@media (prefers-color-scheme: dark)` overrides them at
  `:root` for the system-follows-dark case; `:root[data-theme="light"]` and
  `:root[data-theme="dark"]` override them again for an explicit visitor
  choice. The attribute-selector rules always win over the media query
  regardless of source order, because an attribute selector on `:root` has
  higher specificity than a bare `:root` inside `@media` — this is *why*
  the custom-property approach was worth the refactor: the old scattered
  `@media (prefers-color-scheme: dark) { body {...} hr {...} code {...} }`
  pattern had no clean way to be overridden by a `data-theme` attribute
  without duplicating every rule three times (base/media/override).
- **Toggle**: `.theme-toggle` is a standalone `position: fixed` icon button
  in the top-right corner — deliberately *not* inside `.nav-links`; an
  early version put it there as a text label ("Auto"/"Light"/"Dark") and it
  read as a stray nav item, not a control, and didn't match gwern.net's
  actual corner-icon treatment (checked live — gwern uses small monochrome
  sun/moon/half-circle icons in a floating corner toolbar, not text).
  Contains two inline SVGs (`.icon-sun`, `.icon-moon`, both Feather-style
  line icons matching the CV page's contact icons) absolutely stacked on
  top of each other; CSS `transition` on `opacity`/`transform` (rotate +
  scale) cross-fades between them, giving the sun/moon "morph" animation.
  `data-theme-state="auto"` shows *both* icons simultaneously at reduced
  opacity and opposing tilt (a distinct third look, since a two-icon morph
  can't otherwise represent a three-state control); `"light"`/`"dark"`
  resolve to one icon fully shown. Click cycles auto → light → dark → auto;
  `aria-label` is updated on each state change to describe the *next*
  action (screen-reader users get no benefit from the visual animation).
- **Persistence**: `localStorage["theme"]` — `"light"`/`"dark"` for an
  explicit choice, absent entirely for "auto" (so removing the override
  cleanly falls back to `prefers-color-scheme` with no leftover state).
- **Anti-FOUC**: two small inline `<script>` blocks in `baseof.html`'s
  `<head>` (before the CSS `<link>` tags render anything) read
  `localStorage` synchronously and set `data-theme` on `<html>` before
  first paint, so a returning visitor with an override never sees a flash
  of the wrong theme. A third script (wiring the click handler, setting
  the button's initial `data-theme-state`/`aria-label`) runs at the end of
  `<body>` — that one can wait, since it doesn't affect paint.
- **Syntax highlighting is a separate problem**: `syntax-light.css` and
  `syntax-dark.css` are loaded via `<link media="(prefers-color-scheme:
  ...)">`, which only ever reflects the *system* preference — the
  `data-theme` attribute has no effect on a `<link>`'s own `media`
  attribute. Both scripts also give each `<link>` an `id`
  (`syntax-light-css`/`syntax-dark-css`) and, when an override is active,
  directly set `.media = "all"` on the matching one and `"not all"` on the
  other (reverting to the original `prefers-color-scheme` query strings
  when back in "auto"). Without this, forcing dark mode while the OS is in
  light mode would keep code blocks in the light Chroma theme — same bug
  class as the page-background FOUC, just for a `<link>` instead of CSS
  variables.

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
- Vertical rhythm deliberately tighter than body prose (line-height 1.35 at
  1.15rem, vs. body's ~1.43 at 1.4rem) — issue #9 flagged the original
  values (1.7 line-height, 1.2rem, 2.5rem bottom margin) as reading like a
  big empty block before the article started. This is a reference list, not
  flowing prose, so it should read compact rather than matching paragraph
  spacing.

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

### Unresolved Promises (GitHub interop, #7)

`/posts/` fetches this repo's own open, `article`-labeled GitHub issues at
**Hugo build time** (`resources.GetRemote` on the public GitHub REST API —
no auth needed, unlike the CV pipeline, since `depository` is public) and
renders them as a teaser list below the real posts, under the heading
"Unresolved Promises" — article ideas that exist as a GitHub issue but
haven't become an actual post yet. Each entry links straight to the GitHub
issue, with its number and opened date.

- Scoped to `{{ if eq .Section "posts" }}` in `layouts/_default/list.html`
  so it doesn't render on other list-kind pages.
- Fetch failure (rate limit, network blip during a CI build) is handled
  with Hugo's `try` keyword — logs a `warnf` and simply omits the section,
  rather than failing the whole build. (`resources.Err` was removed in
  Hugo v0.141 in favor of `try`.)
- **Freshness caveat**: this only re-fetches on an actual Hugo build, i.e.
  whenever `depository` itself gets pushed to (triggering the existing
  Cloudflare auto-deploy) — filing/closing an `article` issue doesn't
  itself trigger a rebuild the way the CV repo's push does (no
  `repository_dispatch` wiring was added for this, unlike the CV pipeline;
  wasn't judged worth the extra cross-repo complexity for a low-frequency,
  same-repo teaser list). Same freshness caveat applies to the Statistics
  page below; #16 tracks adding a nightly scheduled rebuild to keep both
  fresh even with no pushes.

### Statistics (#12)

`/stats/` — "see how actively I'm writing on this site." Three sections:

- **Writing**: post count, total/average word count (`.WordCount` summed
  over `where .Site.RegularPages "Section" "posts"`), first/latest post
  date — all computed from Hugo's own page data, no external fetch.
- **Tags**: every tag with its post count, via `.Site.Taxonomies.tags`
  (alphabetical; reuses the taxonomy system from #8).
- **Repository activity**: total commit count and repo age (from GitHub's
  repo-info endpoint's `created_at`), plus a **sparkline** — literally
  Tufte's own term/invention, a nice fit for this site's lineage — of
  monthly commit counts using Unicode block-element characters (`▁▂▃▄▅▆▇█`,
  U+2581–U+2588), each scaled to the max month's count and set in
  JetBrains Mono (block glyphs need a font that renders partial-height
  fills correctly; the body serif font doesn't). A plain-text table below
  gives the same data in numbers, newest month first.
- Deliberately used the direct `/commits` endpoint, not GitHub's
  `/stats/participation` endpoint — the latter is asynchronously computed
  and cache-lagged (confirmed live: it reported 19 total commits when the
  real count was already past 30), unsuitable for something whose whole
  point is "how actively am I working on this." `/commits?per_page=100`
  is a direct, always-accurate query; this repo will need pagination once
  it passes 100 commits (currently ~30).
- Grouping-by-month uses `newScratch`'s `.Add` for counts and slice-append
  (`(slice $month)` accumulates into a list of month keys, deduplicated
  with `uniq` — first-occurrence order, so this list comes out
  newest-first since the API returns commits newest-first; `sort` on that
  gives the chronological order the sparkline needs instead).

### Quarto posts (#4)

Posts can be written as executable Quarto documents (`.qmd`, Python via
Jupyter or R via knitr) or as hand-authored Jupyter notebooks (`.ipynb`),
not just plain Markdown. Full toolchain setup and authoring workflow lives
in docs/QUARTO.md — this section is the design rationale.

**Compile to Hugo-native Markdown, not an embedded/iframed HTML document.**
Quarto's `hugo-md` output format renders a `.qmd`/`.ipynb` straight to
Markdown (code, executed output, and figures included), which lands in the
exact same `content/posts/<slug>/index.md` shape as a hand-written post —
same `single.html` template, same ToC/tags/status-badge/theme-toggle
treatment. The alternative (render to standalone HTML, embed via iframe)
would preserve true JS interactivity (plotly, ipywidgets) but the iframed
document wouldn't inherit the site's fonts or dark-mode sync, and would sit
outside the ToC/sidenote/drop-cap system built for every other post. Given
this site's whole identity is the Tufte-native typography, consistency won
over interactivity; nothing built so far (static plots, tables) needed a
JS widget anyway.

**Page bundle convention:** every Quarto post's source lives at
`content/posts/<slug>/index.qmd` (or `index.ipynb`), and Quarto renders
`index.md` plus a figures directory as siblings in that same folder — a
Hugo leaf bundle, so figures are picked up as page resources automatically,
no `static/` copying required. `hugo.toml`'s `ignoreFiles` excludes the raw
`.qmd`/`.ipynb` source from being published as a static file.

Three demo posts (mirroring `hello-world.md`'s role as the plain-Markdown
feature demo): `quarto-python-demo` (Jupyter engine — numpy/matplotlib),
`quarto-r-demo` (knitr engine — base R plotting + a `knitr::kable` table),
`quarto-ipynb-demo` (a notebook that was never a `.qmd` at all, front
matter in a raw cell instead of a YAML header).

Several `hugo-md` quirks needed fixing up in `scripts/render_quarto.py`
(the wrapper every render goes through) rather than working around them
per-post — see docs/QUARTO.md → "Known quirks" for the full list: smart
punctuation flattening em dashes, root-relative links resolving against
disk depth instead of Hugo's URL depth, bare figure `<img>` tags needing a
wrapper div to align with their code block's column, `.ipynb` not
executing by default, and non-theme-adaptive plot colors (fixed via
`matplotlibrc` + `_quarto.yml`'s knitr `dev.args`, both defaulting to
transparent backgrounds and mid-gray `#888888` text/ticks that read on
both the light and dark theme's background).

Julia isn't wired up — explored as an option per #4's original ask, but
not started; would need a separate IJulia engine install following the
same shape as Python/R.

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

**Left-edge alignment (found via #4's Quarto posts):** the boxes above used
to be `width: calc(52.5% + 2px); margin-left: 2.5%` — inset from the left
edge by 2.5%, with a matching width reduction so the *right* edge still
lined up with paragraphs (`width: 55%`, no margin). This went unnoticed for
a long time because nothing sat directly under a code block closely enough
to expose it. The R Quarto demo post (`knitr::kable` table right under a
code block) made the misalignment obvious: the code block visibly started
and ended shifted right of the table beneath it. Fixed by dropping the
2.5% inset (`margin-left: 0; width: calc(55% + 2px)`) so code blocks are
flush with paragraphs/tables on both edges. Also added
`box-sizing: border-box` to both rules — without it, the `1em` padding
added *on top of* the specified width (default `content-box` sizing),
pushing the box's right edge out past the 55% column by `2 × 1em`; this
was a separate, previously-invisible overflow that only became visible
once the left edge was fixed and the right-edge mismatch was the one thing
left to spot.

### Tables

No table styling existed beyond the browser default (and an unused
`div.table-wrapper { overflow-x: auto }` rule with nothing to wrap) until
issue #4's Quarto R demo put a real `knitr::kable` table on the page and
made "plain browser default" look obviously unfinished next to the rest of
the site's typography.

Default look (no front matter needed) is a classic Tufte rule-table: bold
header with a rule underneath, a closing rule under the last row, no
vertical lines. Two opt-in alternates via front matter:

```yaml
tableStyle: "striped"   # zebra-striped rows (var(--color-code-bg))
tableStyle: "grid"      # full bordered grid, for dense/wide data
```

`single.html` turns the field into a class on the content `<section>`
(`table-style-striped` / `table-style-grid`), so the CSS scoping is
per-post, not per-table — every table in a post shares the same style.
All colors are theme-variable-based (`--color-text`, `--color-border`,
`--color-code-bg`), so they follow the light/dark toggle automatically.

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

- Copyright notice, context-aware "RSS feed" link, and "Source" link to
  GitHub repo
- Repo URL configured via `params.repoURL` in hugo.toml

### Social metadata (#14)

`baseof.html` emits sharing metadata from a single description-resolution
path, so the ordinary HTML description and social previews cannot drift:

1. an explicit page `description`,
2. a cleaned, plain-text page summary (truncated to 200 characters), then
3. `params.description` for pages with neither.

Every page receives a canonical URL plus `og:type`, `og:url`, `og:title`,
`og:description`, `og:site_name`, `og:locale`, and Twitter/X's equivalent
text-card tags (`twitter:card`, `twitter:title`, and `twitter:description`).
Post pages use `og:type=article` and add `article:author` from the configured
GitHub profile; all other pages use `og:type=website`. `authorURL` and
`ogLocale` in `hugo.toml` keep the public identity and Open Graph locale out
of the template.

When a post appears in the generated `data/post_cards.yaml` manifest,
`baseof.html` adds absolute `og:image` and `twitter:image` tags, plus Open
Graph's explicit 1200×630 dimensions. Non-post pages remain text-only cards
instead of inheriting a generic fallback.

### Mathematical post cards (#33)

`scripts/generate_post_cards.py` reads every `content/posts/*.md` and
`content/posts/*/index.md`, renders an opaque 1200×630 PNG at
`static/images/post-cards/<post-slug>.png`, and writes the selected shape,
color, and frame to `data/post_cards.yaml`. Hugo uses that manifest to render
the figure immediately under post metadata, before the table of contents and
article body. Keeping the assets and manifest under version control means the
deployed Hugo build needs no Python rendering runtime.

The body is normalized (line endings, markup-only variation, and whitespace
are removed) and SHA-256 hashed. `shape_digest[0] % 5` chooses one of five
mathematical drawing families, making each equally probable across the hash
space:

- streamlines through a trigonometric flow field,
- nearest-site Voronoi regions plus local network connections,
- escape-time Julia sets, or
- elementary cellular automata, or
- histograms of a De Jong dynamical system.

The remaining body-digest bytes derive all drawing coefficients, initial
points, densities, and iteration counts. Separately, a hash of the title and
front-matter metadata chooses a color family, palette variation, and one of
four restrained print-like frames. Consequently prose changes reshape a card,
while title or metadata changes recolor and reframe it. The generator prints
those selections and basic body statistics each run. Every visible card also
has a small italic caption that states this body-versus-metadata split using
its actual selected drawing, palette, and frame.

Authors only write and commit posts. The local `generate-post-cards`
pre-commit hook runs `scripts/stage_post_cards.py` whenever a staged post
changes; it invokes the generator and stages the PNG files and manifest into that
same commit. `.github/workflows/generate-post-cards.yml` pins the renderer
versions, regenerates the cards in CI, and fails if the committed assets are
stale. Cloudflare therefore receives posts and cards in one deploy, with no
card front matter, manual generation command, or follow-up commit.
The hook prefers `.venv/bin/python3` on a developer machine and falls back to
the active Python interpreter in CI; both CI workflows install the same pinned
`matplotlib` and `numpy` versions.

### Syndication (#13)

The site uses Hugo's built-in RSS 2.0 template rather than a hand-maintained
feed template. `hugo.toml` explicitly enables the `RSS` output format for:

- the home page (`/index.xml`),
- sections, including the post stream (`/posts/index.xml`),
- taxonomy indexes (`/tags/index.xml` and `/categories/index.xml`), and
- individual taxonomy terms (for example, `/tags/quarto/index.xml`).

The same configuration yields the standard RSS 2.0 feed with an Atom
self-reference that Hugo emits by default. No separate Atom document is
maintained: readers that support RSS can subscribe directly, and browsers or
feed readers can discover the appropriate scoped feed through the
`rel="alternate"` link in the page head. The footer also presents an `RSS
feed` link only on pages that have an RSS output, avoiding a dead control on
individual posts.

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
- `ignoreFiles = ['\.qmd$', '\.ipynb$']` — Quarto source files live alongside
  their rendered `index.md` in a page bundle; this keeps Hugo from
  publishing the raw source as a static file (see docs/QUARTO.md)
- `outputs` — explicitly retains Hugo's native RSS 2.0 generation for home,
  section, taxonomy, and taxonomy-term pages (see "Syndication (#13)")

## Sample Content

- `content/posts/hello-world.md` — demonstrates all features (sidenotes, math, code)
- `content/posts/quarto-python-demo/`, `quarto-r-demo/`, `quarto-ipynb-demo/`
  — demonstrate Quarto/notebook-authored posts (see "Quarto posts (#4)" above)
- `content/about.md` — placeholder about page

## Known TODOs

- Consider Hugo shortcodes for sidenotes (cleaner than raw HTML in markdown)
- Add Open Graph / meta tags for social sharing
