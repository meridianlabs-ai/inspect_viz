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
from inspect_viz.view.beta import scores_radar_by_task_df


df = evals_df([  # <1>
    "logs/aime",  # <1>
    "logs/cybench",  # <1>
    "logs/gpqa",  # <1>
    "logs/mmlu-pro",  # <1>
    "logs/swe-bench",  # <1>
])  # <1>

models = [  # <2>
    "openai/o3",  # <2>
    "anthropic/claude-3-7-sonnet-latest",  # <2>
]  # <2>
normalization = "percentile"  # <2>

df = scores_radar_by_task_df(  # <2>
    df,  # <2>
    models=models,  # <2>
    normalization=normalization,  # <2>
)  # <2>

task_name_mapping = {  # <3>
    "aime2024": "AIME 2024",  # <3>
    "cybench": "CyBench",  # <3>
    "gpqa_diamond": "GPQA Diamond",  # <3>
    "mmlu_pro": "MMLU Pro",  # <3>
    "swe_bench": "SWE Bench",  # <3>
}  # <3>

df = prepare(df, [  # <3>
    model_info(),  # <3>
    task_info(task_name_mapping),  # <3>
    log_viewer("eval", { "logs": "https://samples.meridianlabs.ai/" })  # <3>
])  # <3>

df.to_parquet("{{< meta datafile>}}")
```

1. Read the evals data info a dataframe.

2. Convert the dataframe into a `scores_radar_by_task()` specific dataframe.

3. Add pretty model names, task names and log links to the dataframe using `prepare()`.
