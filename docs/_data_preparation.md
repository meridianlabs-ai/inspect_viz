
Above we read the data for the plot from a parquet file. This file was in turn created by:

1. Reading logs into a data frame with [`evals_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#evals_df).

2. Using the [`prepare()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#prepare) function to add [`model_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) and [`log_viewer()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#model_info) columns to the data frame.

```python
from inspect_ai.analysis import evals_df, log_viewer, model_info, prepare

df = evals_df("logs")
df = prepare(df, [
    model_info(),
    log_viewer("eval", {"logs": "https://samples.meridianlabs.ai/"})
])
df.to_parquet("{{< meta datafile>}}")
```

You can additionally use the [`task_info()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#task_info) operation to map lower-level task names to task display names (e.g. "gpqa_diamond" -> "GPQA Diamond").




