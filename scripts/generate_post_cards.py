#!/usr/bin/env python3
"""Generate deterministic mathematical social cards for Hugo posts.

Each card separates shape from color. A SHA-256 digest of the post body
uniformly selects one of five mathematical drawing families and parameterizes
it. A second digest of the title and front-matter metadata uniformly selects
the color family and its palette variation.
Generated image files are committed static assets, so Hugo and Cloudflare never need
the scientific Python stack to build or deploy the site.
"""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import colors

matplotlib.use("Agg")
from matplotlib import pyplot as plt

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"
FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)
HTML_RE = re.compile(r"<[^>]+>")
MARKDOWN_RE = re.compile(r"[`*_#>[\](){}|]")
WHITESPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class Post:
    source: Path
    slug: str
    shape_digest: bytes
    color_digest: bytes
    body_text: str


def byte_float(digest: bytes, index: int) -> float:
    """Map one digest byte to the half-open unit interval."""
    return digest[index] / 256


def normalized_source(text: str) -> str:
    """Keep the authored data while removing markup-only variation."""
    text = text.replace("\r\n", "\n")
    text = HTML_RE.sub(" ", text)
    text = MARKDOWN_RE.sub(" ", text)
    return WHITESPACE_RE.sub(" ", text).strip().lower()


def post_sources() -> list[Path]:
    return sorted([*POSTS_DIR.glob("*.md"), *POSTS_DIR.glob("*/index.md")])


def read_post(source: Path) -> Post:
    raw = source.read_text()
    slug = source.stem if source.parent == POSTS_DIR else source.parent.name
    front_matter = FRONT_MATTER_RE.match(raw)
    if not front_matter:
        raise ValueError(f"{source.relative_to(REPO_ROOT)} is missing YAML front matter")

    metadata, body = front_matter.groups()
    body_text = normalized_source(body)
    metadata_text = normalized_source(metadata)
    color_digest = hashlib.sha256(metadata_text.encode()).digest()
    return Post(
        source,
        slug,
        hashlib.sha256(body_text.encode()).digest(),
        color_digest,
        body_text,
    )


COLOR_HUES = (0.52, 0.08, 0.76, 0.25, 0.60)
COLOR_NAMES = ("flow", "voronoi", "julia", "cellular", "contour")
FRAME_NAMES = ("rule", "double", "inset", "bracket")


def palette(digest: bytes, color_index: int) -> tuple[str, list[str], colors.Colormap]:
    hue = (COLOR_HUES[color_index] + (byte_float(digest, 3) - 0.5) * 0.14) % 1
    background = colorsys.hsv_to_rgb((hue + 0.62) % 1, 0.45, 0.10)
    values = [0.55, 0.74, 0.92]
    accents = [
        colorsys.hsv_to_rgb((hue + offset) % 1, 0.56 + byte_float(digest, i) * 0.28, value)
        for i, (offset, value) in enumerate(zip((0.00, 0.17, 0.52), values), start=4)
    ]
    hex_colors = [colors.to_hex(color) for color in accents]
    return colors.to_hex(background), hex_colors, colors.LinearSegmentedColormap.from_list("card", hex_colors)


def feature_values(post: Post) -> tuple[int, float, int, int]:
    words = re.findall(r"[a-z0-9]+", post.body_text)
    word_count = len(words)
    diversity = len(set(words)) / max(word_count, 1)
    code_blocks = post.body_text.count("python") + post.body_text.count(" r ")
    math_markers = post.body_text.count("math") + post.body_text.count("pi") + post.body_text.count("$")
    return word_count, diversity, code_blocks, math_markers


def card_axes(background: str) -> tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=(12, 6.3), dpi=100, facecolor=background)
    ax = fig.add_axes((0, 0, 1, 1), facecolor=background)
    ax.set_axis_off()
    return fig, ax


def flow_field(ax: plt.Axes, digest: bytes, palette_map: colors.Colormap) -> None:
    x, y = np.meshgrid(np.linspace(-3, 3, 160), np.linspace(-1.6, 1.6, 96))
    a, b, c = 1.2 + 3 * byte_float(digest, 8), 1.2 + 3 * byte_float(digest, 9), 0.4 + byte_float(digest, 10)
    angle = np.sin(a * x + c * np.sin(b * y)) + np.cos(b * y - c * np.sin(a * x))
    u, v = np.cos(angle), np.sin(angle)
    density = 1.6 + byte_float(digest, 11) * 1.2
    ax.streamplot(
        x,
        y,
        u,
        v,
        color=angle,
        cmap=palette_map,
        density=density,
        linewidth=1.1,
        arrowsize=0.01,
    )
    ax.set_xlim(-3, 3)
    ax.set_ylim(-1.6, 1.6)


def cellular_automaton(
    ax: plt.Axes,
    digest: bytes,
    palette_map: colors.Colormap,
    background: str,
    accent: str,
) -> None:
    width, height = 480, 252
    rules = (30, 45, 54, 60, 73, 90, 94, 105, 110, 122, 126, 129, 137, 150, 161, 182)
    rule = rules[digest[8] % len(rules)]
    cells = np.zeros((height, width), dtype=np.uint8)
    rng = np.random.default_rng(int.from_bytes(digest[9:17], "big"))
    cells[0] = rng.random(width) < (0.006 + 0.018 * byte_float(digest, 17))
    center = width // 2
    cells[0, center] = 1

    for row in range(1, height):
        previous = cells[row - 1]
        neighborhoods = np.roll(previous, 1) * 4 + previous * 2 + np.roll(previous, -1)
        cells[row] = (rule >> neighborhoods) & 1

    cmap = colors.ListedColormap([background, accent])
    ax.imshow(cells, extent=(-1, 1, -0.525, 0.525), origin="upper", cmap=cmap, interpolation="nearest", aspect="auto")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-0.525, 0.525)


def voronoi_geometry(ax: plt.Axes, digest: bytes, palette_map: colors.Colormap, accent: str) -> None:
    rng = np.random.default_rng(int.from_bytes(digest[8:16], "big"))
    count = 18 + digest[16] % 23
    points = rng.uniform((-1.1, -0.68), (1.1, 0.68), size=(count, 2))
    x, y = np.meshgrid(np.linspace(-1.1, 1.1, 960), np.linspace(-0.68, 0.68, 570))
    distances = (x[..., None] - points[:, 0]) ** 2 + (y[..., None] - points[:, 1]) ** 2
    nearest = np.argmin(distances, axis=-1)
    ax.imshow(
        nearest,
        extent=(-1.1, 1.1, -0.68, 0.68),
        origin="lower",
        cmap=palette_map,
        interpolation="nearest",
    )
    for index, point in enumerate(points):
        nearest_points = np.argsort(np.sum((points - point) ** 2, axis=1))[1:4]
        for neighbor in nearest_points:
            ax.plot((point[0], points[neighbor, 0]), (point[1], points[neighbor, 1]), color="white", alpha=0.20, linewidth=0.45)
    ax.scatter(points[:, 0], points[:, 1], s=8, color=accent, alpha=0.86)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-0.68, 0.68)


def julia_set(
    ax: plt.Axes,
    digest: bytes,
    palette_map: colors.Colormap,
    background: str,
    accents: list[str],
) -> None:
    x, y = np.meshgrid(np.linspace(-1.8, 1.8, 960), np.linspace(-1.0, 1.0, 540))
    z = x + 1j * y
    constants = (
        complex(-0.800, 0.156),
        complex(-0.7269, 0.1889),
        complex(-0.70176, -0.3842),
        complex(-0.835, -0.2321),
        complex(-0.74543, 0.11301),
        complex(-0.4, 0.6),
        complex(0.285, 0.01),
    )
    base = constants[digest[8] % len(constants)]
    c = base + complex((byte_float(digest, 9) - 0.5) * 0.025, (byte_float(digest, 10) - 0.5) * 0.025)
    escaped = np.zeros(z.shape, dtype=int)
    active = np.ones(z.shape, dtype=bool)
    iterations = 96 + digest[10] % 96
    for iteration in range(iterations):
        z[active] = z[active] * z[active] + c
        escaped_now = active & (np.abs(z) > 2)
        escaped[escaped_now] = iteration
        active &= ~escaped_now
    smooth = escaped + 1 - np.log2(np.log2(np.maximum(np.abs(z), 2)))
    smooth = np.ma.masked_where(active, smooth)
    cmap = colors.LinearSegmentedColormap.from_list("julia", [background, *accents])
    ax.imshow(
        smooth,
        extent=(-1.8, 1.8, -1.0, 1.0),
        origin="lower",
        cmap=cmap,
        interpolation="bilinear",
        vmin=0,
        vmax=iterations,
    )
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-1.0, 1.0)


def potential_contours(
    ax: plt.Axes,
    digest: bytes,
    palette_map: colors.Colormap,
) -> None:
    """Draw level curves of a deterministic anisotropic radial basis field."""
    rng = np.random.default_rng(int.from_bytes(digest[8:16], "big"))
    x, y = np.meshgrid(np.linspace(-1.5, 1.5, 960), np.linspace(-0.8, 0.8, 540))
    field = np.zeros_like(x)
    source_count = 3 + digest[16] % 4
    for _ in range(source_count):
        center_x, center_y = rng.uniform((-1.15, -0.55), (1.15, 0.55))
        scale_x, scale_y = rng.uniform(0.20, 0.60), rng.uniform(0.12, 0.38)
        angle = rng.uniform(0, np.pi)
        amplitude = rng.choice((-1, 1)) * rng.uniform(0.65, 1.35)
        dx, dy = x - center_x, y - center_y
        major = np.cos(angle) * dx + np.sin(angle) * dy
        minor = -np.sin(angle) * dx + np.cos(angle) * dy
        field += amplitude * np.exp(-0.5 * ((major / scale_x) ** 2 + (minor / scale_y) ** 2))

    low, high = np.quantile(field, (0.10, 0.92))
    levels = np.linspace(low, high, 13)
    line_colors = [palette_map(index / (len(levels) - 1)) for index in range(len(levels))]
    ax.contour(x, y, field, levels=levels, colors=line_colors, linewidths=1.25, antialiased=True)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.8, 0.8)


FAMILIES = (flow_field, voronoi_geometry, julia_set, cellular_automaton, potential_contours)
FAMILY_NAMES = ("flow", "voronoi", "julia", "cellular", "contour")


def render(post: Post) -> tuple[str, str]:
    family_index = post.shape_digest[0] % len(FAMILIES)
    color_index = post.color_digest[0] % len(COLOR_HUES)
    background, accents, palette_map = palette(post.color_digest, color_index)
    figure, ax = card_axes(background)
    family = FAMILIES[family_index]
    if family is voronoi_geometry:
        family(ax, post.shape_digest, palette_map, accents[-1])
    elif family is julia_set:
        family(ax, post.shape_digest, palette_map, background, accents)
    elif family is cellular_automaton:
        family(ax, post.shape_digest, palette_map, background, accents[-1])
    else:
        family(ax, post.shape_digest, palette_map)

    output = REPO_ROOT / "static" / "images" / "post-cards" / f"{post.slug}.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=100, facecolor=background, edgecolor="none")
    plt.close(figure)
    return FAMILY_NAMES[family_index], COLOR_NAMES[color_index], FRAME_NAMES[color_digest_byte(post)]


def color_digest_byte(post: Post) -> int:
    return post.color_digest[3] % len(FRAME_NAMES)


def write_manifest(cards: dict[str, tuple[str, str, str]]) -> None:
    lines = ["# Generated by scripts/generate_post_cards.py; do not edit by hand.", ""]
    for slug in sorted(cards):
        shape, color, frame = cards[slug]
        lines.extend(
            [
                f"{slug}:",
                f"  frame: {frame}",
                f"  shape: {shape}",
                f"  color: {color}",
            ]
        )
    (REPO_ROOT / "data" / "post_cards.yaml").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    sources = post_sources()
    cards = {}

    for source in sources:
        post = read_post(source)
        word_count, diversity, code_blocks, math_markers = feature_values(post)
        shape, color, frame = render(post)
        cards[post.slug] = (shape, color, frame)
        print(
            f"{post.slug}: {shape} shape, {color} color, {frame} frame "
            f"({word_count} words, {diversity:.0%} unique, "
            f"{code_blocks} code markers, {math_markers} math markers)"
        )
    write_manifest(cards)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
