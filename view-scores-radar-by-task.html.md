# Scores Radar By Task


## Overview

The `scores_radar_by_task()`function renders a radar chart for comparing
headline metrics from different tasks across multiple models. This is
useful for comparing the relative performance of models across different
tasks.

``` python
from inspect_viz import Data
from inspect_viz.view import scores_radar_by_task

evals = Data.from_file("radar_by_task.parquet")
scores_radar_by_task(evals)
```

The scores plotted on this radar chart have been normalized using
percentile ranking, which means each score represents the model’s
relative performance compared to all other models in the dataset.
Specifically, a score of 0.5 indicates that the model performed better
than 50% of the other models. Absolute scores are displayed in the
tooltips.

You can use `scores_radar_by_task_df()` to produce data with min-max
normalization, omit normalization entirely, or invert the scores for
tasks where lower scores are better.

## Data Preparation

Above we read the data for the plot from a parquet file. This file was
in turn created by:

1.  Reading evals level data into a data frame with
    [`evals_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df).

2.  Converting the evals dataframe into a dataframe specifically used by
    `scores_radar_by_task()` by using the `scores_radar_by_task_df()`
    function. The output of `scores_radar_by_task_df()` can be directly
    passed to `scores_radar_by_task()`. `scores_radar_by_task_df()`
    expects an optional list of metric names to invert where lower
    scores correspond to better scores, an optional list of model names,
    an optional list of task names, an optional normalization method to
    scale scores, and an optional min-max domain to use for
    normalization on the radar chart.

3.  Using the
    [`prepare()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare)
    function to add
    [`model_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info),
    [`task_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#task_info)
    and
    [`log_viewer()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info)
    columns to the data frame.

Here is the data preparation code end-to-end:

``` python
from inspect_ai.analysis import (
    evals_df,
    log_viewer,
    model_info,
    prepare,
)
from inspect_viz.view import scores_radar_by_task_df


df = evals_df([
    "logs/aime",
    "logs/cybench",
    "logs/gpqa",
    "logs/mmlu-pro",
    "logs/swe-bench",
])

df = scores_radar_by_task_df(
    df,
    models=[
        "openai/o3",
        "anthropic/claude-3-7-sonnet-latest",
    ],
    normalization="min_max",
    domain=(0, 1),
)

df = prepare(df, [
    model_info(),
    log_viewer("eval", { "logs": "https://samples.meridianlabs.ai/" })
    task_info(task_name_mapping={
        "aime2024": "AIME 2024",
        "cybench": "CyBench",
        "gpqa_diamond": "GPQA Diamond",
        "mmlu_pro": "MMLU Pro",
        "swe_bench": "SWE Bench",
    }),
])

df.to_parquet("radar_by_task.parquet")
```

Lines 10-16  
Read the evals data into a dataframe.

Lines 18-19  
Convert the dataframe into a `scores_radar_by_task()` specific
dataframe.

Lines 20-23  
Filter specific models to plot on the radar chart. Each task in the data
should have the same set of models.

Line 24  
Choose an optional normalization method to scale the raw scores.
Available options: `"percentile"` (computes percentile rank, useful for
identifying consistently strong performers), `"min_max"` (scales scores
between min-max values, sensitive to outliers), or `"absolute"`
(default, no normalization, may result in incomprehensible charts if
metrics have different scales).

Line 25  
Specify an optional domain when using min-max normalization. If
unspecified, min-max values are inferred from the data.

Lines 28-30  
Add pretty model names and log links to the dataframe using `prepare()`.

Lines 31-37  
Provide an optional task name mapping for pretty task names in
`prepare()`.

## Function Reference

### scores_radar_by_task

Creates a radar chart showing scores for multiple models across multiple
tasks.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/view/_scores_radar.py#L277)

``` python
def scores_radar_by_task(
    data: Data,
    model: str = "model_display_name",
    label: str = "task_display_name",
    title: str | Title | None = None,
    width: float = 400,
    channels: dict[str, str] | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    label_styles: LabelStyles | None = None,
    **attributes: Unpack[PlotAttributes],
) -> Component
```

`data` [Data](reference/inspect_viz.qmd#data)  
A `Data` object prepared using the `scores_radar_by_task_df` function.

`model` str  
Name of field holding the model (defaults to “model_display_name”).

`label` str  
Name of field holding the axes labels (defaults to “task_display_name”);
use “metric” to plot against metrics.

`title` str \| [Title](reference/inspect_viz.mark.qmd#title) \| None  
Title for plot (`str` or mark created with the `title()` function).

`width` float  
The outer width of the plot in pixels, including margins. Defaults
to 400. Height is automatically set to match width to maintain square
aspect ratio.

`channels` dict\[str, str\] \| None  
Channels for the tooltips. Defaults are “Model”, “Score”, “Scaled
Score”, “Metric”, “Scorer”, and “Task”. Values in the dictionary should
correspond to column names in the data.

`legend` [Legend](reference/inspect_viz.plot.qmd#legend) \| NotGiven \| None  
Options for the legend. Pass None to disable the legend.

`label_styles` LabelStyles \| None  
Label styling options. It accepts `line_width` and `text_overflow`.
Defaults to None.

`**attributes` Unpack\[[PlotAttributes](reference/inspect_viz.plot.qmd#plotattributes)\]  
Additional `PlotAttributes`. Use `margin` to set custom margin (defaults
to max(60, width \* 0.12)).

### scores_radar_by_task_df

Creates a dataframe for a radar chart showing headline metrics across
multiple models and tasks.

This is useful for comparing the headline metrics of multiple models
across multiple tasks.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/view/_scores_radar.py#L33)

``` python
def scores_radar_by_task_df(
    data: pd.DataFrame,
    invert: list[str] | None = None,
    models: list[str] | None = None,
    tasks: list[str] | None = None,
    normalization: Literal["percentile", "min_max", "absolute"] = "absolute",
    domain: tuple[float, float] | None = None,
) -> pd.DataFrame
```

`data` pd.DataFrame  
Evals data table containing model scores. It assumes one row per model
for each task.

`invert` list\[str\] \| None  
Optional list of metrics to invert (where lower scores are better).
These should match the values in the “score_headline_metric” column.

`models` list\[str\] \| None  
Optional list of models to include. If None, all models will be
included. These should match the values in the “model” column. We expect
the same set of models for all tasks.

`tasks` list\[str\] \| None  
Optional list of tasks to include. If None, all tasks will be included.
These should match the values in the “task_name” column.

`normalization` Literal\['percentile', 'min_max', 'absolute'\]  
The normalization method to use for the headline metrics. Can be
“percentile”, “min_max”, or “absolute”. Defaults to “absolute” (no
normalization).

`domain` tuple\[float, float\] \| None  
Optional min-max domain to use for the normalization. Only used if
normalization is “min_max”. Otherwise, the domain is inferred from the
data. Defaults to None.

## Implementation

The [Scores Radar By
Task](examples/inspect/scores-radar-by-task/index.qmd) example
demonstrates how this view was implemented using lower level plotting
components.
