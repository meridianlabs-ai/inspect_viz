# Scores by Model


## Overview

The `scores_by_model()` function creates a horizontal bar plot for
comparing the scores of different models on a single evaluation, with
one or more baselines overlaid as vertical lines.

``` python
from inspect_viz import Data
from inspect_viz.view.beta import scores_by_model
from inspect_viz.mark import baseline

evals = Data.from_file("agi-lsat-ar.parquet")
scores_by_model(evals, marks=baseline(0.697, label="Human"))
```

## Data Preparation

Above we read the data for the plot from a parquet file. This file was
in turn created by:

1.  Reading logs into a data frame with
    [`evals_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df).

2.  Using the
    [`prepare()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare)
    function to add
    [`model_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info)
    and
    [`log_viewer()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info)
    columns to the data frame.

``` python
from inspect_ai.analysis import evals_df, log_viewer, model_info, prepare

df = evals_df("logs")
df = prepare(df, [
    model_info(),
    log_viewer("eval", {"logs": "https://samples.meridianlabs.ai/"})
])
df.to_parquet("agi-lsat-ar.parquet")
```

You can additionally use the
[`task_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#task_info)
operation to map lower-level task names to task display names
(e.g. “gpqa_diamond” -\> “GPQA Diamond”).

Note that both the log viewer links and model names are optional (the
plot will render without links and use raw model strings if the data
isn’t prepared with `log_viewer()` and `model_info()`).

## Function Reference

Bar plot for comparing the scores of different models on a single
evaluation.

Summarize eval scores using a bar plot. By default, scores (`y`) are
plotted by “model_display_name” (`y`). By default, confidence intervals
are also plotted (disable this with `y_ci=False`).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/view/beta/_scores_by_model.py#L19)

``` python
def scores_by_model(
    data: Data,
    *,
    model_name: str = "model_display_name",
    score_value: str = "score_headline_value",
    score_stderr: str = "score_headline_stderr",
    ci: float = 0.95,
    sort: Literal["asc", "desc"] | None = None,
    score_label: str | None | NotGiven = None,
    model_label: str | None | NotGiven = None,
    color: str | None = None,
    title: str | Title | None = None,
    marks: Marks | None = None,
    width: float | None = None,
    height: float | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component
```

`data` [Data](reference/inspect_viz.qmd#data)  
Evals data table. This is typically created using a data frame read with
the inspect `evals_df()` function.

`model_name` str  
Column containing the model name (defaults to “model_display_name”)

`score_value` str  
Column containing the score value (defaults to “score_headline_value”).

`score_stderr` str  
Column containing the score standard error (defaults to
“score_headline_stderr”).

`ci` float  
Confidence interval (e.g. 0.80, 0.90, 0.95, etc.). Defaults to 0.95.

`sort` Literal\['asc', 'desc'\] \| None  
Sort order for the bars (sorts using the ‘x’ value). Can be “asc” or
“desc”. Defaults to “asc”.

`score_label` str \| None \| NotGiven  
x-axis label (defaults to None).

`model_label` str \| None \| NotGiven  
x-axis label (defaults to None).

`color` str \| None  
The color for the bars. Defaults to “\#416AD0”. Pass any valid hex color
value.

`title` str \| [Title](reference/inspect_viz.mark.qmd#title) \| None  
Title for plot (`str` or mark created with the `title()` function)

`marks` [Marks](reference/inspect_viz.mark.qmd#marks) \| None  
Additional marks to include in the plot.

`width` float \| None  
The outer width of the plot in pixels, including margins. Defaults to
700.

`height` float \| None  
The outer height of the plot in pixels, including margins. The default
is width / 1.618 (the [golden
ratio](https://en.wikipedia.org/wiki/Golden_ratio))

`legend` [Legend](reference/inspect_viz.plot.qmd#legend) \| NotGiven \| None  
Options for the legend. Pass None to disable the legend.

`**attributes` Unpack\[[PlotAttributes](reference/inspect_viz.plot.qmd#plotattributes)\]  
Additional `PlotAttributes`. By default, the `y_inset_top` and
`margin_bottom` are set to 10 pixels and `x_ticks` is set to `[]`.

## Implementation

The [Scores by Model](examples/inspect/scores-by-model/index.qmd)
example demonstrates how this view was implemented using lower level
plotting components.
