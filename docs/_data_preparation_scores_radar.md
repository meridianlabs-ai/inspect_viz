Above we read the data for the plot from a parquet file. This file was in turn created by:

1. Reading evals level data into a data frame with [`evals_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df).

2. Converting the evals dataframe into a dataframe specifically used by `scores_radar()` by using the `scores_radar_df()` function. The output of `scores_radar_df()` can be directly passed to `scores_radar()`. `scores_radar_df()` expects a scorer name and an optional list of metric names to visualize on the radar chart.

3. Using the [`prepare()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare) function to add [`model_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) and [`log_viewer()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) columns to the data frame.

Here is the data preparation code end-to-end:

```python
from inspect_ai.analysis import (
    evals_df,
    log_viewer,
    model_info,
    prepare,
)
from inspect_viz.view.beta import scores_radar_df


df = evals_df("logs/writing_bench/")  # <1>

scorer = "multi_scorer_wrapper"  # <2>
metrics = [  # <2>
    "Abstract",  # <2>
    "Introduction",  # <2>
    "Experiments",  # <2>
    "Literature Review",  # <2>
    "Paper Outline",  # <2>
]

data = scores_radar_df(  # <2>
    df,  # <2>
    scorer,  # <2>
    metrics,  # <2>
)

df = prepare(df, [  # <3>
    model_info(),  # <3>
    log_viewer("eval", { "logs": "https://samples.meridianlabs.ai/" })  # <3>
])  # <3>

df.to_parquet("{{< meta datafile>}}")
```

1. Read the evals data info a dataframe.

2. Convert the dataframe into a `scores_radar()` specific dataframe.

3. Add pretty model names and log links to the dataframe using `prepare()`.
