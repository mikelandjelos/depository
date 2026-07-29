---
title: "How This Site Draws Its Post Cards"
subtitle: "A deterministic system for turning text into mathematical social images"
date: 2026-07-29
status: "seedling"
categories: ["meta"]
tags: ["meta", "mathematics", "generative-art"]
---

<span class="newthought">Every post on this site now receives</span> a
mathematical card: the image above the article and the image shown when its
link is shared. It is generated from the post itself, not selected from a
stock library and not drawn by hand. The system treats a post as a compact,
reproducible input to a visual program.

That property matters more than novelty. A social image may be cached,
indexed, or inspected long after it was first rendered. Regenerating a card
from the same committed post must produce the same pixels, while an edit to
the post should be able to change the result. The implementation uses no
external random state, network call, or generation service: it is a
deterministic function of the authored text.

## The two hashes

Let $B$ be a normalized version of the article body and $M$ a normalized
version of its front matter. The generator computes the standard SHA-256
digests {{< cite fips1804 >}}

$$
H_s = \operatorname{SHA256}(B), \qquad H_c = \operatorname{SHA256}(M).
$$

Normalization converts line endings, removes HTML and Markdown punctuation,
collapses whitespace, and lowercases text. This avoids changing a card merely
because a writer chose an equivalent line break or emphasis marker. It does
not attempt to understand meaning; it produces a stable textual source.

The subscript $s$ means shape and $c$ means color. Splitting the input is
intentional. The body digest controls geometry; the title, date, status,
categories, and tags control palette and framing. A prose revision can redraw
the image without quietly changing its editorial treatment. Conversely, a
better title or new tag can recolor the card without changing its drawing.

For a byte $b$, define $u(b) = b / 256$. This maps a digest byte to the
half-open interval $[0, 1)$. The drawing family is

$$
f = H_s[0] \bmod 5.
$$

SHA-256 is designed to distribute arbitrary inputs evenly over its output
space, so each of the five residue classes has the same size. This is a
uniform hash partition, not a claim that the system understands a post's
topic. Similar essays can produce different drawings, and an unrelated edit
can change every parameter. The relationship is provenance, rather than
semantic illustration.

All remaining choices are derived from further digest bytes. When a method
needs pseudo-random points, its generator is seeded from a fixed byte slice of
$H_s$. There is therefore no hidden clock, machine state, or random seed to
record.

## Five drawing families

Each family fills the same 1200 by 630 pixel canvas. The available methods are
deliberately different: continuous vector fields, discrete partitions,
complex-plane iteration, local Boolean dynamics, and a nonlinear orbit. They
share a deterministic interface, but they do not collapse into one visual
style.

### Trigonometric flow fields

For the flow-field family, the plane is sampled over a rectangular grid. Three
digest-derived coefficients $a$, $b$, and $c$ define an angle field

$$
\theta(x,y) = \sin\!\bigl(ax + c\sin(by)\bigr) + \cos\!\bigl(by - c\sin(ax)\bigr).
$$

The vector field is then

$$
\mathbf{v}(x,y) = \left(\cos\theta(x,y), \sin\theta(x,y)\right).
$$

Streamlines follow this field numerically. The hash selects the three
frequencies and a streamline density between 1.6 and 2.8. Since the field is
smooth but not usually integrable to a simple potential, it produces ribbons,
turning channels, and occasional saddle-like regions without a particle
simulation or nondeterministic integration.

### Voronoi regions and local networks

The Voronoi family samples between 18 and 40 sites in a slightly enlarged
canvas rectangle. At every raster point $p$, its assigned cell is

$$
V(p) = \underset{i}{\operatorname{argmin}}\; \lVert p - q_i \rVert^2,
$$

where $q_i$ is site $i$. Coloring this nearest-site index yields a hard
partition of the plane. The sites are not merely decorative: each is connected
to its three nearest neighbours, producing a sparse local graph over the
regions. The graph is intentionally approximate rather than a formal Delaunay
triangulation; it exposes local structure while keeping the method small, fast,
and reproducible.

{{< cite aurenhammer1991 >}}

The hash-seeded sample positions determine both the regions and the network.
Consequently, two cards cannot differ only in palette while retaining the same
accidental point arrangement unless their body digest is also the same.

### Julia sets

The Julia family iterates a quadratic map over the complex plane:

$$
z_{n+1} = z_n^2 + c.
$$

Each pixel starts from $z_0 = x + i y$, with $(x,y)$ spanning
$[-1.8, 1.8] \times [-1.0, 1.0]$. The generator chooses one of several
curated constants, including values near $-0.8 + 0.156i$ and
$-0.7269 + 0.1889i$, then applies a small digest-derived perturbation.
Curating the base constants avoids broad regions of parameter space that are
mathematically valid but visually empty at card scale.

Iteration stops when $\lvert z_n \rvert > 2$, the usual escape radius for
this quadratic map. The number of iterations lies between 96 and 191. Escaped
points receive a smooth escape-time value,

$$
\nu = n + 1 - \log_2\!\left(\log_2\!\max(\lvert z_n \rvert, 2)\right),
$$

which removes harsh bands from the color field. Points which do not escape are
masked to the dark background. This is why the Julia cards retain a strong
silhouette and contrast instead of becoming uniformly bright noise.

{{< cite milnor2006 >}}

### Elementary cellular automata

The cellular family is a one-dimensional binary automaton shown through time.
For a cell with left, centre, and right states $L$, $C$, and $R$, form
the neighbourhood number

$$
n = 4L + 2C + R.
$$

An eight-bit Wolfram rule supplies the next state,

$$
C' = (r \mathbin{\texttt{>>}} n) \mathbin{\&} 1.
$$

The generator selects from a fixed collection of nontrivial rules such as 30,
45, 90, 110, 122, and 150. A hash-seeded sparse first row is combined with one
live central cell, then evolved for 252 rows across 480 columns with periodic
boundary conditions. The result is a space-time diagram: every horizontal row
is a complete state, and every diagonal trace records causal propagation
through the local rule.

{{< cite wolfram2002 >}}

### De Jong dynamical systems

The final family uses a two-dimensional nonlinear recurrence commonly called a
De Jong attractor:

$$
\begin{aligned}
x_{n+1} &= \sin(a y_n) - \cos(b x_n), \\
y_{n+1} &= \sin(c x_n) - \cos(d y_n).
\end{aligned}
$$

The generator chooses one of several vetted coefficient quadruples, then adds
a small digest-derived perturbation to all four values. Starting at
$(0.1, 0.1)$, it discards the first 500 states as a transient and records the
next 150,000. Rather than drawing each point directly, it bins the orbit into
a 900 by 480 two-dimensional histogram and displays $\log(1 + h)$, where
$h$ is the bin count. The logarithm makes both dense attractor cores and faint
outer structure visible. A fixed point or tiny cycle is valid dynamics but
unreadable at card scale, so a deterministic alternate vetted seed is used
when fewer than 1,500 histogram bins are occupied. Empty bins are masked to
the dark canvas background, leaving only the orbit visible across the full
1200 by 630 frame.

{{< cite bourke1991 >}}

## Palette and frame are a second system

The shape digest never chooses a color. Instead, the first byte of $H_c$
selects one of five named palette families, and later bytes perturb its hue,
saturation, and accent values. The palette is generated in HSV space. A dark,
complementary background is paired with three brighter accents at fixed hue
offsets. Those accents define a continuous colormap for scalar images and the
line or point colors for geometric images.

The fourth byte of $H_c$ selects one of four restrained frames:

$$
\operatorname{frame} = H_c[3] \bmod 4.
$$

The choices are a single rule, a double rule, an inset edge, and brackets.
They are CSS, rather than pixels baked into the PNG, so the card preserves its
full 1200 by 630 social-preview dimensions while the article can give it a
classical, responsive presentation. The generated manifest stores the chosen
shape, color name, and frame for every post. Hugo uses it for both the visible
figure and its automatic italic caption.

## From draft to deployment

The author-facing workflow is intentionally ordinary:

1. Write Markdown with normal Hugo front matter. No image field, seed, or
   generator command is required.
2. Stage and commit the post. The `generate-post-cards` pre-commit hook sees
   the changed post and runs `scripts/stage_post_cards.py`.
3. That script invokes `scripts/generate_post_cards.py`, which rereads all
   Markdown posts, writes `static/images/post-cards/<slug>.png`, writes
   `data/post_cards.yaml`, and stages both outputs in the same commit.
4. Push the commit. Cloudflare builds Hugo from the committed files, so it
   needs neither Python nor the scientific rendering stack.
5. Hugo looks up the manifest. It places the card beneath the post metadata,
   emits the explanatory caption, and adds absolute `og:image` and
   `twitter:image` tags for social crawlers.
6. GitHub Actions installs the pinned `matplotlib` and `numpy`
   versions, regenerates the complete card set, and fails if a committed image
   or manifest entry differs. The ordinary lint-and-build workflow runs the
   same hook with those dependencies as well.

The generated assets are committed rather than produced at deploy time. That
choice makes every deployed revision self-contained, lets a review inspect the
actual pixels, and prevents a future renderer upgrade from changing old cards
without a deliberate regeneration commit. The automated caption and manifest
make the process inspectable in the finished site, while the hash functions
make it reproducible from the source.

{{< references >}}
