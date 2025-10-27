Above we read the data for the plot from a parquet file. This file was in turn created by:

1. Reading evals level data into a data frame with [`evals_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df).

2. Converting the evals dataframe into a dataframe specifically used by `scores_radar_by_metric()` by using the `scores_radar_by_metric_df()` function. The output of `scores_radar_by_metric_df()` can be directly passed to `scores_radar_by_metric()`. `scores_radar_by_metric_df()` expects a scorer name, an optional list of metric names to visualize, an optional list of metric names to invert where lower scores correspond to better scores, an optional normalization method to scale scores, and an optional min-max domain to use for normalization on the radar chart.

3. Using the [`prepare()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare) function to add [`model_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) and [`log_viewer()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) columns to the data frame.

Here is the data preparation code end-to-end:

```python
from inspect_ai.analysis import (
    evals_df,
    log_viewer,
    model_info,
    prepare,
)
from inspect_viz.view.beta import scores_radar_by_metric_df


df = evals_df("logs/writing_bench/")  # <1>

df = scores_radar_by_metric_df(  # <2>
    df,  # <2>
    scorer="multi_scorer_wrapper",  # <3>
    metrics=[  # <4>
        "Abstract",  # <4>
        "Introduction",  # <4>
        "Experiments",  # <4>
        "Literature Review",  # <4>
        "Paper Outline",  # <4>
    ],  # <4>
    normalization="percentile",  # <5>
)

df = prepare(df, [  # <6>
    model_info(),  # <6>
    log_viewer("eval", { "logs": "https://samples.meridianlabs.ai/" })  # <6>
])  # <6>

df.to_parquet("{{< meta datafile>}}")
```

1. Read the evals data into a dataframe.

2. Convert the dataframe into a `scores_radar_by_metric()` specific dataframe.

3. A task might have multiple scorers, specify the scorer which you want to plot. The function only supports plotting one scorer at a time. The scorer name should correspond to columns in `df` named `score_{scorer}_{metric}`.

4. Specify a list of metrics to plot on the radar chart. If unspecified, all metrics from a scorer will be plotted. Metric names in the list should correspond to columns in `df` named `score_{scorer}_{metric}`.

5. Choose an optional normalization method to scale the raw scores. Available options: `"percentile"` (computes percentile rank, useful for identifying consistently strong performers), `"min_max"` (scales scores between min-max values, sensitive to outliers), or `"absolute"` (default, no normalization, may result in incomprehensible charts if metrics have different scales).

6. Add pretty model names and log links to the dataframe using `prepare()`.
