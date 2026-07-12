"""Chart theme for this notebook, matching the CLO Atlas project's house
style (white background, Arial, one red accent, warm-gray categorical ramp)
so this desk research reads as one visual system with the rest of the
presentation deck.

House rules (same as clo-atlas/src/common/style.py):
  - White background (#FFFFFF), horizontal-only gridlines, no top/right spines.
  - Arial (falls back to Helvetica/DejaVu Sans if Arial isn't installed).
  - One accent color against a warm-gray categorical ramp; color means
    something (the thing the chart is about) or it isn't used at all.
  - Headline is a full declarative sentence in bold; subtitle carries the
    technical description; source line bottom-left; byline+date bottom-right.
  - ILLUSTRATIVE / TO-VERIFY / VERIFIED tags stay in the headline or subtitle
    text itself — the theme doesn't hide that provenance discipline, it just
    standardizes how the chart looks.
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

BG = "#FFFFFF"
INK = "#1A1A1A"
INK_MUTED = "#5C5652"
GRID = "#DAD5CE"
ACCENT = "#D0021B"
ACCENT_SOFT = "#F2A6AE"
WARM_GRAY = ["#4A4540", "#8C8579", "#B8B0A4", "#D8D2C6"]
EVENT_SPAN = "#C7C0B4"

BYLINE = "Credit: Ashley Shi"

_FONT_CANDIDATES = ["Arial", "Helvetica", "Helvetica Neue", "DejaVu Sans"]


def apply_theme() -> None:
    available = {f.name for f in mpl.font_manager.fontManager.ttflist}
    body_font = next((f for f in _FONT_CANDIDATES if f in available), "DejaVu Sans")
    mpl.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "savefig.bbox": "tight",
        "font.family": body_font,
        "text.color": INK,
        "axes.edgecolor": INK_MUTED,
        "axes.labelcolor": INK_MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.frameon": False,
        "lines.linewidth": 2.0,
        "figure.dpi": 150,
    })


def categorical_color(index: int) -> str:
    if index == 0:
        return ACCENT
    return WARM_GRAY[(index - 1) % len(WARM_GRAY)]


def warm_gray_ramp(n: int) -> list:
    """n evenly-spaced grays along the warm-gray ramp, light -> dark. Use for an
    *ordinal* series (e.g. seniority stack) where a continuous ramp reads better
    than wrapping the 4-stop categorical ramp and colliding two categories."""
    from matplotlib.colors import LinearSegmentedColormap
    if n <= 1:
        return [WARM_GRAY[1]]
    cmap = LinearSegmentedColormap.from_list("nomura_warm_gray", list(reversed(WARM_GRAY)))
    return [cmap(x) for x in np.linspace(0, 1, n)]


def sequential_cmap():
    """Single-hue (accent) sequential colormap, light -> dark, for magnitude
    encodings (heatmaps, contour fills) — never a rainbow, never diverging
    where the data is one-sided."""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list("nomura_sequential", ["#FBEAEC", ACCENT])


def categorical_cmap(n: int):
    """Discrete colormap over the fixed categorical order, for pcolormesh/imshow
    on categorical (non-magnitude) grids — e.g. 'which agency binds here'."""
    from matplotlib.colors import ListedColormap
    return ListedColormap([categorical_color(i) for i in range(n)])


def save_figure(fig, name: str, headline: str, subtitle: str = "", source: str = "",
                 notes: str = "", fig_dir: Path | None = None,
                 panel_titles: bool = False) -> tuple[Path, Path]:
    """Stamp the headline/subtitle/source/byline scaffold onto `fig` and write
    PNG (@200dpi, notebook-sized) + SVG. Header/footer margins are sized in
    inches from estimated wrapped-line counts (headline, subtitle, and notes
    all scale with their own text length) so neither the x-axis label nor a
    multi-line note collides with the footer, and short-and-wide multi-panel
    figures don't get their titles crushed. Pass `panel_titles=True` when the
    axes themselves carry `ax.set_title(...)` (e.g. small-multiples labels)
    so the reserved header leaves room below the headline/subtitle block for
    those per-axes titles too.
    """
    fig_dir = Path(fig_dir or "figures")
    fig_dir.mkdir(parents=True, exist_ok=True)

    fig_w, fig_h = fig.get_size_inches()
    headline_chars_per_line = max(fig_w * 7.5, 15)
    headline_lines = max(1, -(-len(headline) // headline_chars_per_line))
    subtitle_chars_per_line = max(fig_w * 11, 20)
    subtitle_lines = -(-len(subtitle) // subtitle_chars_per_line) if subtitle else 0
    notes_chars_per_line = max(fig_w * 15, 25)
    notes_lines = -(-len(notes) // notes_chars_per_line) if notes else 0

    headline_block_in = 0.20 * headline_lines + 0.08
    subtitle_block_in = 0.24 * subtitle_lines
    panel_title_in = 0.28 if panel_titles else 0.0
    header_in = 0.18 + headline_block_in + subtitle_block_in + panel_title_in

    source_text = f"SOURCE: {source.upper()}" if source else ""
    dateline = _dt.date.today().isoformat()
    byline_text = f"{BYLINE} · {dateline}"

    xlabel_clear_in = 0.34   # room for the axes' own x-axis label + tick labels
    source_row_in = 0.20
    notes_block_in = 0.17 * notes_lines
    footer_in = xlabel_clear_in + notes_block_in + source_row_in

    top = 1 - header_in / fig_h
    bottom = footer_in / fig_h
    fig.subplots_adjust(top=top, bottom=bottom)

    fig.text(0.02, 1 - (0.18 / fig_h), headline, fontsize=13, fontweight="bold", color=INK, ha="left", va="top", wrap=True)
    if subtitle:
        fig.text(0.02, 1 - ((0.18 + headline_block_in) / fig_h), subtitle, fontsize=9.5, color=INK_MUTED, ha="left", va="top", wrap=True)

    # SOURCE (bottom-left) and byline (bottom-right) normally share one row. A
    # char-count heuristic for whether they'd overlap is fragile (uppercase
    # glyphs run wider than a flat average), so measure the actual rendered
    # text extents after a draw pass and reposition for real if they collide.
    source_y_in = 0.09
    source_artist = None
    if source:
        source_artist = fig.text(0.02, source_y_in / fig_h, source_text, fontsize=7, color=INK_MUTED, ha="left", va="bottom")
    byline_artist = fig.text(0.98, source_y_in / fig_h, byline_text, fontsize=7, color=INK_MUTED, ha="right", va="bottom")

    if source_artist is not None:
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        src_bbox = source_artist.get_window_extent(renderer)
        byl_bbox = byline_artist.get_window_extent(renderer)
        gap_px = byl_bbox.x0 - src_bbox.x1
        if gap_px < 10:  # too close / overlapping — stack byline above source
            byline_artist.set_position((0.98, (source_y_in + 0.16) / fig_h))
            footer_in += 0.16
            fig.subplots_adjust(bottom=footer_in / fig_h)

    if notes:
        notes_y_in = footer_in - xlabel_clear_in - notes_block_in + 0.06
        fig.text(0.02, notes_y_in / fig_h, notes, fontsize=6.5, color=INK_MUTED, ha="left", va="bottom", style="italic", wrap=True)

    png_path = fig_dir / f"{name}.png"
    svg_path = fig_dir / f"{name}.svg"
    fig.savefig(png_path, dpi=200, facecolor=BG)
    fig.savefig(svg_path, facecolor=BG)
    return png_path, svg_path
