Above we read the data for the plot from a parquet file. This file was in turn created by:

1. Reading evals level data into a data frame with [`evals_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df).

2. Converting the evals dataframe into a dataframe specifically used by `scores_radar_by_task()` by using the `scores_radar_by_task_df()` function. The output of `scores_radar_by_task_df()` can be directly passed to `scores_radar_by_task()`. `scores_radar_by_task_df()` expects an optional list of metric names to invert where lower scores correspond to better scores, an optional list of model names, an optional list of task names, an optional normalization method to scale scores, and an optional min-max domain to use for normalization on the radar chart.

3. Using the [`prepare()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare) function to add [`model_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info), [`task_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#task_info) and [`log_viewer()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) columns to the data frame.

Here is the data preparation code end-to-end:

```python
from inspect_ai.analysis import (
    evals_df,
    log_viewer,
    model_info,
    prepare,
)
from inspect_viz.view import scores_radar_by_task_df


df = evals_df([  # <1>
    "logs/aime",  # <1>
    "logs/cybench",  # <1>
    "logs/gpqa",  # <1>
    "logs/mmlu-pro",  # <1>
    "logs/swe-bench",  # <1>
])  # <1>

df = scores_radar_by_task_df(  # <2>
    df,  # <2>
    models=[  # <3>
        "openai/o3",  # <3>
        "anthropic/claude-3-7-sonnet-latest",  # <3>
    ],  # <3>
    normalization="min_max",  # <4>
    domain=(0, 1),  # <5>
)

df = prepare(df, [  # <6>
    model_info(),  # <6>
    log_viewer("eval", { "logs": "https://samples.meridianlabs.ai/" })  # <6>
    task_info(task_name_mapping={  # <7>
        "aime2024": "AIME 2024",  # <7>
        "cybench": "CyBench",  # <7>
        "gpqa_diamond": "GPQA Diamond",  # <7>
        "mmlu_pro": "MMLU Pro",  # <7>
        "swe_bench": "SWE Bench",  # <7>
    }),  # <7>
])

df.to_parquet("{{< meta datafile>}}")
```

1. Read the evals data into a dataframe.

2. Convert the dataframe into a `scores_radar_by_task()` specific dataframe.

3. Filter specific models to plot on the radar chart. Each task in the data should have the same set of models.

4. Choose an optional normalization method to scale the raw scores. Available options: `"percentile"` (computes percentile rank, useful for identifying consistently strong performers), `"min_max"` (scales scores between min-max values, sensitive to outliers), or `"absolute"` (default, no normalization, may result in incomprehensible charts if metrics have different scales).

5. Specify an optional domain when using min-max normalization. If unspecified, min-max values are inferred from the data.

6. Add pretty model names and log links to the dataframe using `prepare()`.

7. Provide an optional task name mapping for pretty task names in `prepare()`.
