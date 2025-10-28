# Scores Timeline


## Overview

The `scores_timeline()` function plots eval scores by model,
organization, and release date[^1]:

``` python
from inspect_viz import Data
from inspect_viz.view.beta import scores_timeline

evals = Data.from_file("benchmarks.parquet")
scores_timeline(evals)
```

## Data Preparation

Above we read the data for the plot from a parquet file. This file was
in turn created by:

1.  Reading logs into a data frame with
    [`evals_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df).

2.  Using the
    [`prepare()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare)
    function to add
    [`model_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info),
    [`frontier()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#frontier)
    and
    [`log_viewer()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info)
    columns to the data frame.

``` python
from inspect_ai.analysis import (
    evals_df, frontier, log_viewer, model_info, prepare
)

df = evals_df("logs")
df = prepare(df, [
    model_info(),
    frontier(),
    log_viewer("eval", {"logs": "https://samples.meridianlabs.ai/"})
])
df.to_parquet("benchmarks.parquet")
```

## Filtering

A `select()` input for tasks is automatically provided if more than one
task exists in the `data`. A `checkbox_group()` is automatically
provided for organizations if more than one organization exists (you can
disable this with `organizations_filter=False`).

When multiple organizations exist, clicking on the legend for an
organization will filter the plot by that organization.

## Function Reference

Eval scores by model, organization, and release date.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/view/beta/_scores_timeline.py#L29)

``` python
def scores_timeline(
    data: Data,
    task_name: str = "task_display_name",
    model_name: str = "model_display_name",
    model_organization: str = "model_organization_name",
    model_release_date: str = "model_release_date",
    score_name: str = "score_headline_name",
    score_value: str = "score_headline_value",
    score_stderr: str = "score_headline_stderr",
    organizations: list[str] | None = None,
    filters: bool | list[Literal["task", "organization"]] = True,
    ci: float | bool | NotGiven = NOT_GIVEN,
    time_label: str = "Release Date",
    score_label: str = "Score",
    eval_label: str = "Eval",
    title: str | Title | None = None,
    marks: Marks | None = None,
    width: float | Param | None = None,
    height: float | Param | None = None,
    regression: bool = False,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component
```

`data` [Data](reference/inspect_viz.qmd#data)  
Data read using `evals_df()` and amended with model metadata using the
`model_info()` prepare operation (see [Data
Preparation](https://inspect.aisi.org.uk/dataframe.html#data-preparation)
for details).

`task_name` str  
Column for task name (defaults to “task_display_name”).

`model_name` str  
Column for model name (defaults to “model_display_name”).

`model_organization` str  
Column for model organization (defaults to “model_organization_name”).

`model_release_date` str  
Column for model release date (defaults to “model_release_date”).

`score_name` str  
Column for scorer name (defaults to “score_headline_name”).

`score_value` str  
Column for score value (defaults to “score_headline_value”).

`score_stderr` str  
Column for score stderr (defaults to “score_headline_stderr”)

`organizations` list\[str\] \| None  
List of organizations to include (in order of desired presentation).

`filters` bool \| list\[Literal\['task', 'organization'\]\]  
Provide UI to filter plot by task and organization(s).

`ci` float \| bool \| NotGiven  
Confidence interval (defaults to 0.95, pass `False` for no confidence
intervals)

`time_label` str  
Label for time (x-axis).

`score_label` str  
Label for score (y-axis).

`eval_label` str  
Label for eval select input.

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

`regression` bool  
If `True`, adds a regression line to the plot (uses the confidence
interval passed using ci). Defaults to False.

`legend` [Legend](reference/inspect_viz.plot.qmd#legend) \| NotGiven \| None  
Legend to use for the plot (defaults to `None`, which uses the default
legend).

`**attributes` Unpack\[[PlotAttributes](reference/inspect_viz.plot.qmd#plotattributes)\]  
Additional `PlotAttributes`. By default, the `x_domain` is set to
“fixed”, the `y_domain` is set to `[0,1.0]`, `color_label` is set to
“Organizations”, and `color_domain` is set to `organizations`.

## Implementation

The [Scores Timeline](examples/inspect/scores-timeline/index.qmd)
example demonstrates how this view was implemented using lower level
plotting components.

[^1]: This plot was inspired by and includes data from the [Epoch
    AI](https://epoch.ai/data/ai-benchmarking-dashboard) Benchmarking
    Hub
