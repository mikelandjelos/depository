# Theme Implementation Details

## Architecture

Custom theme built inline (no `themes/` directory). All templates live in
`layouts/`, all styles in `assets/css/`.

## Files

| File | Purpose |
|---|---|
| `layouts/_default/baseof.html` | Base template: `<head>` with fonts, KaTeX, CSS; site header nav; footer |
| `layouts/_default/single.html` | Article/post page: title, subtitle, date, tags, content |
| `layouts/_default/list.html` | Section list page: title, content, chronological post list |
| `layouts/index.html` | Homepage: site title, description, recent 10 posts from `posts/` section |
| `assets/css/tufte.css` | All styles — adapted Tufte CSS + site header/nav/footer/post-list |
| `assets/css/syntax-light.css` | Chroma syntax highlighting — monokailight (light mode) |
| `assets/css/syntax-dark.css` | Chroma syntax highlighting — monokai (dark mode) |

## Design Decisions

### Typography

- **Body**: EB Garamond (Google Fonts) — serif, 15px base, 1.4rem paragraph size
- **Code**: JetBrains Mono (Google Fonts) — 1rem inline, 0.9rem in blocks
- **Headings**: h1 normal weight 3.2rem; h2/h3 italic weight 400
- **New thought**: `span.newthought` — small-caps opener for topic shifts

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

### Navigation

- Minimal top bar: site name (small-caps, left) + nav links (right, flexbox)
- Links from `[menus.main]` in hugo.toml
- Current pages: Posts, About

### Responsive (<760px)

- Body expands to 84% width, 8% padding each side
- Main content + lists + code blocks expand to ~100% width
- Sidenotes/margin notes collapse to toggleable inline blocks
- Images scale to 100% width

## Hugo Configuration Notes

- `timeZone = 'Europe/Belgrade'` — prevents today's posts being treated as future
- `markup.goldmark.renderer.unsafe = true` — required for sidenote HTML in markdown
- `markup.goldmark.extensions.passthrough` — preserves `$…$` and `$$…$$` for KaTeX
- `markup.highlight.noClasses = false` — CSS-based syntax highlighting

## Sample Content

- `content/posts/hello-world.md` — demonstrates all features (draft)
- `content/about.md` — placeholder about page

## Known TODOs

- Consider Hugo shortcodes for sidenotes (cleaner than raw HTML in markdown)
- Add RSS feed customization
- Add favicon
- Add Open Graph / meta tags for social sharing
