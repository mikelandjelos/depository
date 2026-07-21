---
title: "About"
date: 2026-07-21
---

<p class="wip-notice">Work in progress — this page is still being written.</p>

## Who I am

## Why this site

For a professional overview, see the [Curriculum Vitae](/cv/).

## Technical aspects

This site is built with [Hugo](https://gohugo.io/), a static site
generator, using a small custom theme (no third-party theme) living
directly in the site's repository rather than as a separate package. The
design draws on [Tufte CSS](https://edwardtufte.github.io/tufte-css/) —
generous margins, sidenotes and margin notes instead of footnotes, and
a restrained, text-first layout. Body text is set in EB Garamond;
code in JetBrains Mono. Math is rendered client-side with
[KaTeX](https://katex.org/). Long posts get an automatically generated
table of contents (a numbered outline, styled after
[gwern.net](https://gwern.net/)'s), and each post opens with an
illuminated-manuscript-style drop cap. The site respects your system's
light/dark preference; there's no manual toggle yet.

The [Curriculum Vitae](/cv/) page is not hand-written here — it's
generated from the LaTeX source of a separate, private CV repository.
A small parser converts that LaTeX into structured data, which this
site renders natively in its own style. A GitHub Actions pipeline keeps
the two in sync automatically: pushing a change to the CV repository
triggers a rebuild of this page within about a minute, with no manual
step in between.

The site deploys to [Cloudflare](https://www.cloudflare.com/) automatically
on every push to the main branch. Source is public on
[GitHub](https://github.com/mikelandjelos/depository); pre-commit hooks
enforce markdown linting, spell-checking, prose-quality checks, CSS linting,
and a full build check on every commit.
