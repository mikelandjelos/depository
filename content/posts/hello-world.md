---
title: "Hello World: A Sample Post"
subtitle: "Testing the theme with all its features"
date: 2026-02-28
draft: true
tags: ["meta", "test"]
---

<span class="newthought">This is a sample post</span> to demonstrate the theme's
typography and features. The body text is set in EB Garamond, a revival of
Claude Garamont's sixteenth-century typefaces — elegant, readable, and well
suited to long-form writing on the web.

## Sidenotes

Tufte CSS provides sidenotes as an alternative to footnotes.
<label for="sn-example" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-example" class="margin-toggle">
<span class="sidenote">This is a sidenote. On wide screens it appears in the
margin; on narrow screens, tap the number to reveal it inline.</span>
They allow the reader to glance at supplementary information without losing
their place in the main text.

## Margin notes

These are sidenotes without numbers.
<label for="mn-example" class="margin-toggle">&#8853;</label>
<input type="checkbox" id="mn-example" class="margin-toggle">
<span class="marginnote">This is a margin note. Notice it lacks a number — it
provides context rather than citation.</span>
They work well for brief asides, definitions, or contextual information.

## Code

Inline code uses JetBrains Mono: `fn main() { println!("hello"); }`.

A code block:

```python
def fibonacci(n: int) -> int:
    """Compute the n-th Fibonacci number."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

## Mathematics

KaTeX renders math inline like $e^{i\pi} + 1 = 0$ and in display mode:

$$
\int_{-\infty}^{\infty} e^{-x^2} \, dx = \sqrt{\pi}
$$

The Cauchy–Schwarz inequality:

$$
\left( \sum_{k=1}^{n} a_k b_k \right)^2 \leq \left( \sum_{k=1}^{n} a_k^2 \right) \left( \sum_{k=1}^{n} b_k^2 \right)
$$

## Block quotes

> The purpose of computing is insight, not numbers.
>
> <footer>Richard Hamming</footer>

## Lists

Some things worth reading:

- Gwern's writings on spaced repetition
- Bartosz Ciechanowski's interactive explanations
- Anything by Edward Tufte

## New thought

<span class="newthought">In his later work,</span> Tufte advocated for
information-dense graphics that respect the reader's intelligence. This
paragraph demonstrates the `newthought` small-caps opener used to signal a
shift in topic without a full section heading.
