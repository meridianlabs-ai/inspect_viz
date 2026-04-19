"""Regenerate the static PNG view-tile shown at the top of `docs/index.qmd`.

Run once to produce three thumbnails under `docs/images/`. Re-run if any of
the underlying view defaults change visually. Quarto skips this file at
render time (leading underscore).

Usage:
    python docs/_generate_index_images.py
"""

from pathlib import Path

import pandas as pd
from PIL import Image, ImageOps

from inspect_viz import Data
from inspect_viz.plot import legend, plot_defaults, write_png
from inspect_viz.view import scores_by_model, scores_by_task, scores_timeline

DOCS = Path(__file__).parent
IMAGES = DOCS / "images"
IMAGES.mkdir(exist_ok=True)

# Tile-sized; Quarto scales these via `layout-ncol=3` to column width, so
# native 600x400 (1200x800 at scale=2) gives crisp display on retina.
plot_defaults(width=600, height=400)

# Each view captures a slightly different widget shape (varying legend
# placement, faceting, etc.) so write_png returns PNGs at different aspect
# ratios. We render at native shape, then pad each to a common 3:2 canvas
# so the three thumbnails tile cleanly under `layout-ncol=3` with uniform
# heights instead of a ragged row.
TILE_CANVAS = (1500, 1000)  # 3:2 aspect, fits all three native dimensions


def _render_and_pad(filename: str, component) -> None:
    path = IMAGES / filename
    write_png(path, component)
    with Image.open(path) as img:
        padded = ImageOps.pad(img.convert("RGB"), TILE_CANVAS, color="white")
    padded.save(path)


_render_and_pad(
    "scores_by_model.png",
    scores_by_model(Data.from_file(DOCS / "agi-lsat-ar.parquet")),
)
_render_and_pad(
    "scores_by_task.png",
    scores_by_task(Data.from_file(DOCS / "evals.parquet")),
)

# scores_timeline filtered to GPQA Diamond only, with no filter UI — gives
# us a static timeline image for the hero tile (the interactive version
# with filter controls appears in the Interactive Plots section).
_bench = pd.read_parquet(DOCS / "benchmarks.parquet")
_gpqa = _bench[_bench["task_name"] == "GPQA Diamond"]
_render_and_pad(
    "scores_timeline_gpqa.png",
    scores_timeline(
        Data.from_dataframe(_gpqa),
        filters=False,
        legend=legend("color", frame_anchor="top-left", inset=20),
    ),
)
