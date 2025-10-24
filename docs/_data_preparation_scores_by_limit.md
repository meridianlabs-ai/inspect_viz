Above we read the data for the plot from a parquet file. This file was in turn created by:

1. Reading sample level data into a data frame with [`samples_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df). In addition to the base sample information, we also read eval specific columns using `EvalInfo` and `EvalModel`.

2. Converting the samples dataframe into a dataframe specifically used by `scores_by_limit()` by using the `scores_by_limit_df()` function.

3. Using the [`prepare()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare) function to add [`model_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) and [`log_viewer()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) columns to the data frame.

Here is the data preparation code end-to-end:

```python
from inspect_ai.analysis import (
    EvalInfo, EvalModel, SampleSummary,
    log_viewer, model_info, prepare, samples_df
)
from inspect_viz.view.beta import scores_by_limit_df

df = samples_df(  # <1>
    [
    "logs/swe-bench/"],
    columns=SampleSummary + EvalInfo + EvalModel,  # <2>
)

df = scores_by_limit_df(                          # <3>
    df,                                           # <3>
    score="score_swe_bench_scorer",        # <3>
)

df = prepare(df, [                                                   #<4>
  model_info(),                                                      #<4>
  log_viewer("eval", { "logs": "https://samples.meridianlabs.ai/" }) #<4>
])                                                                  #<4>

df.to_parquet("{{< meta datafile>}}")
```

1. Read the samples data info a dataframe.

2. Be sure to specify the `SampleSummary`, `EvalInfo`, and `EvalModel` columns.

3. Convert the base dataframe into a `scores_by_limit()` specific dataframe.

4. Add pretty model names and log links to the dataframe.

