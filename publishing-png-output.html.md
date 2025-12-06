# PNG Output


## Overview

When publishing a [notebook](publishing-notebooks.qmd),
[website](publishing-websites.qmd), or
[dashboard](publishing-dashboards.qmd), Inspect Viz plots are rendered
by default as Jupyter Widgets that use JavaScript to provide various
interactive features (tooltips, filtering, brushing, etc.). While this
is the recommended way to publish Inspect Viz content, you can also
choose to render content as static PNG images.

You might want do this if you are creating an Office or PDF document
from a notebook, or want plots in a dashboard to be available even when
disconnected from the Internet. Note however that rendering plots as PNG
images does take longer than the native JavaScript output format, and
that interactive features are not available in this mode.

#### Prerequisites

To create PNG output with Inspect Viz, first install the
[playwright](https://playwright.dev/python/) Python package, which
enables taking screenshots of web graphics using an embedded version of
the Chromium web browser. You can do this as follows:

``` bash
pip install playwright
playwright install
```

## Standalone

Use the `write_png()` function to save a stanalone PNG version of any
plot. For example:

``` python
from inspect_viz import Data
from inspect_viz.mark import dot
from inspect_viz.plot import plot, write_png

penguins = Data.from_file("penguins.parquet")

pl = plot(
    dot(penguins, x="body_mass", y="flipper_length",  
        stroke="species", symbol="species"),
    legend="symbol",
    grid=True
)

write_png("penguins.png", pl)
```

## Embedded

When your plots are embedded in a notebook or website, use the global
`output_format` option to specify that you’d like to render them in PNG
format. For example, the plot below is rendered as a static PNG graphic:

``` python
from inspect_viz import Data, options
from inspect_viz.view import scores_by_factor

# set 'png' as default output format
options.output_format = "png"

# render plot
evals = Data.from_file("evals-hint.parquet")
scores_by_factor(evals, "task_arg_hint", ("No hint", "Hint"))
```

Lines 4-5  
Set the global `options.output_format` option to render all plots in a
notebook or Quarto document as static PNG images.

You can also do this for a single plot or set of plots using
`options_context()`:

``` python
from inspect_viz import options_context

with options_context(output_format="png"):
    # plot code here
```

Note that when rendering a PDF document with Quarto, the output format
is automatically set to “png” (as PDFs can’t ever include interactive
JavaScript content).
