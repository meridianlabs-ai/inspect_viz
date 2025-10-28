# Sample Heatmap


## Overview

The `sample_heatmap()`function renders a heatmap for viewing individual
sample scores. Each sample is shown along one axis, models are shown
along the other axis.

``` python
from inspect_viz import Data
from inspect_viz.view.beta import sample_heatmap

samples = Data.from_file("writing_bench_samples.parquet")
sample_heatmap(
  samples, 
  score_value="score_multi_scorer_wrapper", 
  height=200
)
```

## Data Preparation

Above we read the data for the plot from a parquet file. This file was
in turn created by:

1.  Reading logs into a dataframe with `samples_df`, specifying the
    SampleSummaryColumns and the EvaalModel columns.

2.  Using the `prepare()` function to `model_info()` and `log_viewer()`
    columns to the data frame.

``` python
from inspect_ai.analysis import samples_df, log_viewer, model_info, prepare, EvalModel, SampleSummary

df = samples_df("logs", columns=SampleSummary + EvalModel)
df = prepare(df, [
    model_info(), 
    log_viewer("sample", {"logs": "https://samples.meridianlabs.ai/"})
  ])
df.to_parquet("writing_bench_samples.parquet")
```

If your samples are using non-numeric values (for example ‘C’ and ‘I’ to
represent correct and incorrect), you can use the `score_to_float`
prepare function in `inspect.analysis` to convert the score values to
floats. For example:

``` python
from inspect_ai.analysis import samples_df, log_viewer, model_info, score_to_float, prepare, EvalModel, SampleSummary

df = samples_df("logs", columns=SampleSummary + EvalModel)
df = prepare(df, [
    model_info(), 
    log_viewer("sample", {"logs": "https://samples.meridianlabs.ai/"}),
    score_to_float("score_includes")
  ])
```

Note that both the log viewer links and model names are optional (the
plot will render without links and use raw model strings if the data
isn’t prepared with `log_viewer()` and `model_info()`).

## Function Reference

Creates a heatmap plot of success rate of eval data.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/43bc7cbad55804123a0150d2f5f083c28b44e0c1/src/inspect_viz/view/beta/_sample_heatmap.py#L15)

``` python
def sample_heatmap(
    data: Data,
    id: str = "id",
    id_label: str | None | NotGiven = None,
    model_name: str = "model_display_name",
    model_label: str | None | NotGiven = None,
    score_value: str | None = None,
    cell: CellOptions | None = None,
    tip: bool = True,
    title: str | Title | None = None,
    marks: Marks | None = None,
    height: float | None = None,
    width: float | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    sort: Literal["ascending", "descending"] | SortOrder | None = "ascending",
    orientation: Literal["horizontal", "vertical"] = "horizontal",
    **attributes: Unpack[PlotAttributes],
) -> Component
```

`data` [Data](reference/inspect_viz.qmd#data)  
Evals data table.

`id` str  
Name of column to use for displaying the sample id.

`id_label` str \| None \| NotGiven  
x-axis label (defaults to None).

`model_name` str  
Name of column to use for rows.

`model_label` str \| None \| NotGiven  
y-axis label (defaults to None).

`score_value` str \| None  
Name of the column to use as values to determine cell color.

`cell` [CellOptions](reference/inspect_viz.view.qmd#celloptions) \| None  
Options for the cell marks.

`tip` bool  
Whether to show a tooltip with the value when hovering over a cell
(defaults to True).

`title` str \| [Title](reference/inspect_viz.mark.qmd#title) \| None  
Title for plot (`str` or mark created with the `title()` function)

`marks` [Marks](reference/inspect_viz.mark.qmd#marks) \| None  
Additional marks to include in the plot.

`height` float \| None  
The outer height of the plot in pixels, including margins. The default
is width / 1.618 (the [golden
ratio](https://en.wikipedia.org/wiki/Golden_ratio)).

`width` float \| None  
The outer width of the plot in pixels, including margins. Defaults to
700.

`legend` [Legend](reference/inspect_viz.plot.qmd#legend) \| NotGiven \| None  
Options for the legend. Pass None to disable the legend.

`sort` Literal\['ascending', 'descending'\] \| SortOrder \| None  
Sort order for the x and y axes. If ascending, the highest values will
be sorted to the top right. If descending, the highest values will
appear in the bottom left. If None, no sorting is applied. If a
SortOrder is provided, it will be used to sort the x and y axes.

`orientation` Literal\['horizontal', 'vertical'\]  
The orientation of the heatmap. If “horizontal”, the tasks will be on
the x-axis and models on the y-axis. If “vertical”, the tasks will be on
the y-axis and models on the x-axis.

`**attributes` Unpack\[[PlotAttributes](reference/inspect_viz.plot.qmd#plotattributes)\]  
Additional \`PlotAttributes

## Implementation

The [Sample Heatmap](examples/inspect/sample-heatmap/index.qmd) example
demonstrates how this view was implemented using lower level plotting
components.
