# Scores by Limit – Inspect Viz

## Overview

The [scores_by_limit()](./reference/inspect_viz.view.html.md#scores_by_limit) function renders a line plot for evaluating how a model’s **success rate** changes as the **compute budget** increases (e.g., token limit or time). It helps answer “*Will performance keep improving if I spend more?*”. The shaded band displays the confidence interval derived from the standard error.

This visualization requires that you run your evaluation wiht a very high time or token limit, allowing the model a large amount of the resource to complete each sample in the evaluation. Then, use the [scores_by_limit_df()](./reference/inspect_viz.view.html.md#scores_by_limit_df) function will to prepare the dataframe for visualization, computing the amount of the time or tokens required to solve each sample.

``` python
from inspect_viz import Data
from inspect_viz.view import scores_by_limit

evals = Data.from_file("swebench_token_limit.parquet")
scores_by_limit(evals)
```

## Data Preparation

Above we read the data for the plot from a parquet file. This file was in turn created by:

1.  Reading sample level data into a data frame with [samples_df()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df). In addition to the base sample information, we also read eval specific columns using [EvalInfo](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evalinfo) and [EvalModel](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evalmodel).

2.  Converting the samples dataframe into a dataframe specifically used by [scores_by_limit()](./reference/inspect_viz.view.html.md#scores_by_limit) by using the [scores_by_limit_df()](./reference/inspect_viz.view.html.md#scores_by_limit_df) function.

3.  Using the [prepare()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare) function to add [model_info()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) and [log_viewer()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) columns to the data frame.

Here is the data preparation code end-to-end:

``` python
from inspect_ai.analysis import (
    EvalInfo, EvalModel, SampleSummary,
    log_viewer, model_info, prepare, samples_df
)
from inspect_viz.view import scores_by_limit_df

1df = samples_df(
    [
    "logs/swe-bench/"],
2    columns=SampleSummary + EvalInfo + EvalModel,
)

3df = scores_by_limit_df(
    df,
    score="score_swe_bench_scorer",
)

4df = prepare(df, [
  model_info(),
  log_viewer("eval", { "logs": "https://samples.meridianlabs.ai/" })
])

df.to_parquet("swebench_token_limit.parquet")
```

1  
Read the samples data info a dataframe.

2  
Be sure to specify the [SampleSummary](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#samplesummary), [EvalInfo](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evalinfo), and [EvalModel](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evalmodel) columns.

3  
Convert the base dataframe into a [scores_by_limit()](./reference/inspect_viz.view.html.md#scores_by_limit) specific dataframe.

4  
Add pretty model names and log links to the dataframe.

Note that both the log viewer links and model names are optional (the plot will render without links and use raw model strings if the data isn’t prepared with [log_viewer()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#log_viewer) and [model_info()](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info)).

## Function Reference

### scores_by_limit

Visualizes success rate as a function of a resource limit (time, tokens).

Model success rate is plotted as a function of the time, tokens, or other resource limit.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/view/_scores_by_limit.py#L157)

``` python
def scores_by_limit(
    data: Data,
    model: str = "model_display_name",
    success: str = "success_rate",
    stderr: str | None = "standard_error",
    facet: str | None = None,
    other_termination_rate: str | bool = False,
    limit: str | None = None,
    limit_label: str | NotGiven = NOT_GIVEN,
    scale: Literal["log", "linear", "auto"] = "auto",
    title: str | Title | None = None,
    marks: Marks | None = None,
    height: float | None = None,
    width: float | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    ci: float = 0.95,
    **attributes: Unpack[PlotAttributes],
) -> Component
```

`data` [Data](./reference/inspect_viz.html.md#data)  
A dataframe prepared using the `prepare_limit_dataframe` function.

`model` str  
Name of field holding the model (defaults to “model_display_name”).

`success` str  
Name of field containing the success rate (defaults to “success_rate”).

`stderr` str \| None  
Name of field containing the standard_error (defaults to “standard_error”).

`facet` str \| None  
Name of field to use for faceting (defaults to None).

`other_termination_rate` str \| bool  
Name of field containing the other termination rate (defaults to “other_termination_rate”).

`limit` str \| None  
Name of field for x axis (by default, will detect limit type using the columns present in the data frame).

`limit_label` str \| NotGiven  
The limit label (by default, will select limit label using the columns present in the data frame). Pass None for no label.

`scale` Literal\['log', 'linear', 'auto'\]  
The scale type for the limit access. If ‘auto’, will use log scale if the range is 2 or more orders of magnitude (defaults to ‘auto’).

`title` str \| [Title](./reference/inspect_viz.mark.html.md#title) \| None  
Title for plot (`str` or mark created with the [title()](./reference/inspect_viz.mark.html.md#title) function)

`marks` [Marks](./reference/inspect_viz.mark.html.md#marks) \| None  
Additional marks to include in the plot.

`height` float \| None  
The outer height of the plot in pixels, including margins. The default is width / 1.618 (the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio))

`width` float \| None  
The outer width of the plot in pixels, including margins. Defaults to 700.

`legend` [Legend](./reference/inspect_viz.plot.html.md#legend) \| NotGiven \| None  
Options for the legend. Pass None to disable the legend.

`ci` float  
Confidence interval (e.g. 0.80, 0.90, 0.95, etc.). Defaults to 0.95.

`**attributes` Unpack\[[PlotAttributes](./reference/inspect_viz.plot.html.md#plotattributes)\]  
Additional [PlotAttributes](./reference/inspect_viz.plot.html.md#plotattributes).

### scores_by_limit_df

Prepares a dataframe for plotting success rate as a function of a resource limit (time, tokens).

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/f2f2eff657128a6418485a6eabd9462f979cb727/src/inspect_viz/view/_scores_by_limit.py#L27)

``` python
def scores_by_limit_df(
    df: pd.DataFrame,
    score: str,
    limit: Literal["total_tokens", "total_time", "working_time"] = "total_tokens",
    scale: Literal["log", "linear", "auto"] = "auto",
    steps: int = 100,
) -> pd.DataFrame
```

`df` pd.DataFrame  
A dataframe containing sample summaries and eval information.

`score` str  
Name of field containing the score (0 = fail, 1 = success).

`limit` Literal\['total_tokens', 'total_time', 'working_time'\]  
The resource limit to use (one of ‘total_tokens’, ‘total_time’, ‘working_time’). Defaults to ‘total_tokens’.

`scale` Literal\['log', 'linear', 'auto'\]  
The scale type for the limit access. If ‘auto’, will use log scale if the range is 2 or more orders of magnitude (defaults to ‘auto’).

`steps` int  
The number of points to use when sampling the limit range (defaults to 100).

## Implementation

The [Scores by Limit](./examples/inspect/scores-by-limit/index.html.md) example demonstrates how this view was implemented using lower level plotting components.
