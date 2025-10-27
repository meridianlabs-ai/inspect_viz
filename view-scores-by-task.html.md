# Scores by Task


## Overview

The `scores_by_task()` function renders a bar plot for comparing eval
scores.

``` python
from inspect_viz import Data
from inspect_viz.view.beta import scores_by_task

evals = Data.from_file("evals.parquet")
scores_by_task(evals)
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
df.to_parquet("evals.parquet")
```

You can additionally use the
[`task_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#task_info)
operation to map lower-level task names to task display names
(e.g. “gpqa_diamond” -\> “GPQA Diamond”).

Note that both the log viewer links and model names are optional (the
plot will render without links and use raw model strings if the data
isn’t prepared with `log_viewer()` and `model_info()`).

## Function Reference

Bar plot for comparing eval scores.

Summarize eval scores using a bar plot. By default, scores (`y`) are
plotted by “task_display_name” (`fx`) and “model_display_name” (`x`). By
default, confidence intervals are also plotted (disable this with
`y_ci=False`).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/7e6c5188a59ac33eeb78737db9b1979fd2867a4a/src/inspect_viz/view/beta/_scores_by_task.py#L20)

``` python
def scores_by_task(
    data: Data,
    model_name: str = "model_display_name",
    task_name: str = "task_display_name",
    score_value: str = "score_headline_value",
    score_stderr: str = "score_headline_stderr",
    score_label: str | None | NotGiven = NOT_GIVEN,
    ci: bool | float = 0.95,
    title: str | Title | None = None,
    marks: Marks | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component
```

`data` [Data](reference/inspect_viz.qmd#data)  
Evals data table. This is typically created using a data frame read with
the inspect `evals_df()` function.

`model_name` str  
Name of field for the model name (defaults to “model_display_name”)

`task_name` str  
Name of field for the task name (defaults to “task_display_name”)

`score_value` str  
Name of field for the score value (defaults to “score_headline_value”).

`score_stderr` str  
Name of field for stderr (defaults to “score_headline_metric”).

`score_label` str \| None \| NotGiven  
Score axis label (pass None for no label).

`ci` bool \| float  
Confidence interval (e.g. 0.80, 0.90, 0.95, etc.). Defaults to 0.95.

`title` str \| [Title](reference/inspect_viz.mark.qmd#title) \| None  
Title for plot (`str` or mark created with the `title()` function).

`marks` [Marks](reference/inspect_viz.mark.qmd#marks) \| None  
Additional marks to include in the plot.

`width` float \| [Param](reference/inspect_viz.qmd#param) \| None  
The outer width of the plot in pixels, including margins. Defaults to
700.

`height` float \| [Param](reference/inspect_viz.qmd#param) \| None  
The outer height of the plot in pixels, including margins. The default
is width / 1.618 (the [golden
ratio](https://en.wikipedia.org/wiki/Golden_ratio))

`legend` [Legend](reference/inspect_viz.plot.qmd#legend) \| NotGiven \| None  
Options for the legend. Pass None to disable the legend.

`**attributes` Unpack\[[PlotAttributes](reference/inspect_viz.plot.qmd#plotattributes)\]  
Additional `PlotAttributes`. By default, the `margin_bottom` are is set
to 10 pixels and `x_ticks` is set to `[]`.

## Implementation

The [Scores by Task](examples/inspect/scores-by-task/index.qmd) example
demonstrates how this view was implemented using lower level plotting
components.
