#!/usr/bin/env python3
"""Fetch cv.tex from the curriculum-vitae repo and convert it into
data/cv.yaml for the Hugo CV page (layouts/cv/single.html).

This is a targeted parser for the specific LaTeX template used in
mikelandjelos/curriculum-vitae (custom `onecolentry`/`twocolentry`/
`highlights`/`header` environments) -- not a general LaTeX-to-anything
converter. If the template's structure changes significantly, this will
need updating alongside it.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

import yaml

RAW_URL = (
    "https://raw.githubusercontent.com/mikelandjelos/"
    "curriculum-vitae/main/cv.tex"
)

ICON_MAP = {
    "faMapMarker": "map-marker",
    "faEnvelope": "envelope",
    "faPhone": "phone",
    "faLinkedinIn": "linkedin",
    "faGithub": "github",
    "faGlobe": "globe",
}

SUPERSCRIPT_MAP = {
    "st": "ˢᵗ",
    "nd": "ⁿᵈ",
    "rd": "ʳᵈ",
    "th": "ᵗʰ",
}


def find_matching_brace(s: str, open_idx: int) -> int:
    assert s[open_idx] == "{"
    depth = 0
    for i in range(open_idx, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError("unmatched brace in LaTeX source")


def extract_blocks(s: str, env: str, has_arg: bool) -> list[dict]:
    """Find non-self-nesting \\begin{env}...\\end{env} blocks in s."""
    blocks = []
    for m in re.finditer(r"\\begin\{" + re.escape(env) + r"\}", s):
        pos = m.end()
        arg = None
        if has_arg and pos < len(s) and s[pos] == "{":
            close = find_matching_brace(s, pos)
            arg = s[pos + 1 : close]
            pos = close + 1
        end_m = re.search(r"\\end\{" + re.escape(env) + r"\}", s[pos:])
        if not end_m:
            continue
        content = s[pos : pos + end_m.start()]
        blocks.append({"start": m.start(), "end": pos + end_m.end(), "arg": arg, "content": content})
    return blocks


def clean_latex(text: str) -> str:
    if text is None:
        return ""
    t = text

    # Strip layout/spacing commands with no textual meaning.
    t = re.sub(r"\\vspace\{[^}]*\}", "", t)
    t = re.sub(r"\\kern[^%\n]*%?", "", t)
    t = re.sub(r"\\hspace\*?\{[^}]*\}", "", t)
    t = re.sub(r"\\needspace\{[^}]*\}", "", t)

    # href variants -> markdown links. Run repeatedly to unwind nesting.
    href_re = re.compile(r"\\(?:hrefWithoutArrow|href)\{([^{}]*)\}\{")
    while True:
        m = href_re.search(t)
        if not m:
            break
        close = find_matching_brace(t, m.end() - 1)
        label = clean_latex(t[m.end() : close])
        url = m.group(1)
        t = t[: m.start()] + f"[{label}]({url})" + t[close + 1 :]

    # Simple text-formatting commands -> markdown, unwound repeatedly to
    # handle nesting (e.g. \textbf{\textit{x}}).
    simple_cmds = {
        "textbf": "**{}**",
        "textit": "*{}*",
        "texttt": "`{}`",
        "emph": "*{}*",
    }
    changed = True
    while changed:
        changed = False
        for cmd, fmt in simple_cmds.items():
            m = re.search(r"\\" + cmd + r"\{", t)
            if not m:
                continue
            open_idx = m.end() - 1
            close = find_matching_brace(t, open_idx)
            inner = clean_latex(t[open_idx + 1 : close])
            t = t[: m.start()] + fmt.format(inner) + t[close + 1 :]
            changed = True

    # Superscript ordinals: $2^{nd}$ -> 2ⁿᵈ
    def sup_repl(m: re.Match) -> str:
        base, suffix = m.group(1), m.group(2)
        return base + SUPERSCRIPT_MAP.get(suffix, "^" + suffix)

    t = re.sub(r"\$(\w+)\^\{(\w+)\}\$", sup_repl, t)
    t = re.sub(r"\$(\w+)\$", r"\1", t)

    # Remaining icon/color/font noise.
    t = re.sub(r"\\color\{[^}]*\}", "", t)
    t = re.sub(r"\\(footnotesize|small|normalsize|selectfont)\b", "", t)
    t = re.sub(r"\\fa[A-Za-z]+(\[[a-z]*\])?\*?", "", t)
    t = re.sub(r"\{\s*\}", "", t)  # empty braces left behind by stripped commands

    # Escapes and dashes.
    t = t.replace(r"\%", "%").replace(r"\#", "#").replace(r"\$", "$").replace(r"\&", "&")
    t = re.sub(r"(?<!-)--(?!-)", "–", t)  # -- -> en dash
    t = t.replace("``", "“").replace("''", "”")

    # Whitespace / leftover LaTeX line-continuation noise.
    t = t.replace("\\\\", "\n")
    t = re.sub(r"%\s*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    t = "\n".join(line.strip() for line in t.split("\n"))
    t = t.strip()
    return t


def parse_header(doc: str) -> dict:
    blocks = extract_blocks(doc, "header", has_arg=False)
    if not blocks:
        raise ValueError("no header block found")
    header_src = blocks[0]["content"]

    name = ""
    name_cmd_m = re.search(r"\\textbf\{", header_src)
    if name_cmd_m:
        open_idx = name_cmd_m.end() - 1
        close = find_matching_brace(header_src, open_idx)
        inner = header_src[open_idx + 1 : close]
        inner = re.sub(r"\\fontsize\{[^}]*\}\{[^}]*\}", "", inner)
        inner = inner.replace("\\selectfont", "")
        name = clean_latex(inner).strip()

    contact = []
    for item in header_src.split("\\AND"):
        mbox_m = re.search(r"\\mbox\{", item)
        if not mbox_m:
            continue
        open_idx = mbox_m.end() - 1
        close = find_matching_brace(item, open_idx)
        inner = item[open_idx + 1 : close]

        icon_m = re.search(r"\\(fa[A-Za-z]+)", inner)
        icon = ICON_MAP.get(icon_m.group(1), "") if icon_m else ""

        href = None
        href_m = re.search(r"\\hrefWithoutArrow\{([^{}]*)\}\{", inner)
        if href_m:
            href = href_m.group(1).replace("\\%", "%")
            label_open = href_m.end() - 1
            label_close = find_matching_brace(inner, label_open)
            label_src = inner[label_open + 1 : label_close]
            inner = inner[: href_m.start()] + label_src + inner[label_close + 1 :]

        # Strip the leading icon/color/size wrapper, e.g.
        # `{\color{black}\footnotesize\faMapMarker*}`.
        inner = re.sub(r"\{\\color\{[^}]*\}[^{}]*\\fa[A-Za-z]+(\[[a-z]*\])?\*?\}", "", inner)
        inner = re.sub(r"\\hspace\*?\{[^}]*\}", "", inner)

        text = clean_latex(inner)
        if text:
            contact.append({"icon": icon, "text": text, "href": href})

    return {"name": name, "contact": contact}


def parse_section_body(body: str) -> list[dict]:
    twocol = extract_blocks(body, "twocolentry", has_arg=True)
    onecol = extract_blocks(body, "onecolentry", has_arg=False)

    entries: list[dict] = []
    for b in sorted(twocol + onecol, key=lambda x: x["start"]):
        is_twocol = b in twocol
        if is_twocol:
            left = clean_latex(b["content"])
            right = clean_latex(b["arg"])
            title, _, subtitle = left.partition("\n")
            meta_lines = [line.strip() for line in right.split("\n") if line.strip()]
            entries.append(
                {
                    "kind": "entry",
                    "title": title.strip(),
                    "subtitle": subtitle.strip(),
                    "meta": meta_lines,
                    "highlights": [],
                    "text": "",
                }
            )
        else:
            hl_blocks = extract_blocks(b["content"], "highlights", has_arg=False)
            if hl_blocks:
                items = [clean_latex(i) for i in hl_blocks[0]["content"].split("\\item") if i.strip()]
                if entries and entries[-1]["kind"] == "entry" and not entries[-1]["highlights"]:
                    entries[-1]["highlights"] = items
                else:
                    entries.append({"kind": "highlights", "highlights": items})
            else:
                text = clean_latex(b["content"])
                if text:
                    entries.append({"kind": "text", "text": text})
    return entries


def parse_sections(doc: str) -> list[dict]:
    doc_end = len(doc)
    matches = list(re.finditer(r"\\section\{([^}]*)\}", doc))
    sections = []
    for i, m in enumerate(matches):
        title = clean_latex(m.group(1))
        content_start = m.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else doc_end
        body = doc[content_start:content_end]
        body = re.sub(r"\\newpage", "", body)
        sections.append({"title": title, "entries": parse_section_body(body)})
    return sections


def parse_cv(tex: str) -> dict:
    doc_m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", tex, re.DOTALL)
    doc = doc_m.group(1) if doc_m else tex

    last_updated_m = re.search(r"Last updated in ([A-Za-z]+ \d{4})", tex)

    return {
        "name": parse_header(doc)["name"],
        "contact": parse_header(doc)["contact"],
        "last_updated": last_updated_m.group(1) if last_updated_m else "",
        "sections": parse_sections(doc),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, help="local cv.tex path (skips network fetch)")
    ap.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "cv.yaml",
    )
    args = ap.parse_args()

    if args.input:
        tex = args.input.read_text()
    else:
        with urllib.request.urlopen(RAW_URL, timeout=30) as resp:
            tex = resp.read().decode("utf-8")

    cv = parse_cv(tex)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        yaml.safe_dump(cv, f, sort_keys=False, allow_unicode=True, width=100)

    print(f"Wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
