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
- Code blocks: `#f5f5f0` background, `#1e1e1e` in dark mode
- Links: inherit color, subtle underline (0.05em thickness, 0.15em offset)

### Sidenotes (from Tufte CSS)

- Uses checkbox toggle pattern: `<label>` + `<input type="checkbox">` + `<span>`
- Numbered sidenotes: class `sidenote-number` on label, `sidenote` on span
- Margin notes: no number, `marginnote` on span, `⊕` toggle symbol
- On mobile (<760px): hidden by default, tap number/symbol to expand inline

### Math (KaTeX)

- Loaded from jsDelivr CDN (v0.16.11) with SRI hashes
- Auto-render extension: `$...$` for inline, `$$...$$` for display
- Deferred loading — does not block page render

### Syntax Highlighting

- Hugo's built-in Chroma highlighter with `noClasses = false`
- Uses CSS classes (not inline styles) for theme-ability
- Note: no Chroma CSS is currently included — Hugo generates class-based
  markup but we rely on browser defaults. TODO: Add a Chroma CSS theme file.

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
- `markup.highlight.noClasses = false` — CSS-based syntax highlighting

## Sample Content

- `content/posts/hello-world.md` — demonstrates all features (draft)
- `content/about.md` — placeholder about page

## Known TODOs

- Add Chroma syntax highlighting CSS theme
- Consider Hugo shortcodes for sidenotes (cleaner than raw HTML in markdown)
- Add RSS feed customization
- Add favicon
- Add Open Graph / meta tags for social sharing
