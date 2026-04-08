# Inspect Viz

Data visualization for [Inspect AI](https://inspect.aisi.org.uk/) large language model evalutions.

## Welcome

Welcome to Inspect Viz, a data visualisation library for [Inspect AI](https://inspect.aisi.org.uk/). Inspect Viz provides flexible tools for creating high quality interactive visualisations from Inspect evaluations.

Here’s an Inspect Viz plot created with the [scores_timeline()](view-scores-timeline.html.md) function that compares benchmarks scores over time[^1]:

Use the filters to switch benchmarks and restrict to models from various organization(s). Hover over the points to get additional details on them or view the underlying Inspect log for the evals.

## Installation

First, install the `inspect_viz` package as follows:

``` bash
pip install inspect-viz
```

Inspect Viz plots are interactive Jupyter Widgets and can be authored in variety of ways:

1.  In any [Jupyter Notebook](https://jupyter.org/) (JupyterLab, VS Code, Colab, etc.)

2.  In VS Code with the **Jupyter: Run Current File in Interactive Window** command.

3.  In VS Code within a [Quarto](https://quarto.org) executable markdown document.

See the article on [LLM Assistance](llm-assistance.html.md) for best practices on using language models to help with creating plots. See the articles on [Publishing](publishing.html.md) for details on including plots in documents as static images or within websites and dashboards as interactive widgets.

## Views

Inspect Viz [Views](views.html.md) are pre-built plots that work with data created by the Inspect log [data frame](https://inspect.aisi.org.uk/dataframe.html) reading functions. For example, the [scores_by_factor()](view-scores-by-factor.html.md) view enables you to compare scores across models and a boolean factor:

``` python
from inspect_viz import Data
from inspect_viz.view import scores_by_factor
from inspect_viz.plot import legend

evals = Data.from_file("evals-hint.parquet")
scores_by_factor(
    evals,
    "task_arg_hint",
    ("No hint", "Hint"),
    legend=legend("color", frame_anchor="bottom-right", border=False, inset=20),
)
```

The [sample_tool_calls()](view-sample-tool-calls.html.md) view enables you to visualize tool calls by sample:

``` python
from inspect_viz.view import sample_tool_calls

tools = Data.from_file("cybench_tools.parquet")
sample_tool_calls(tools, legend=legend("color", frame_anchor="bottom", border=False))
```

\` Available views include:

| View | Description |
|----|----|
| [scores_by_task()](view-scores-by-task.html.md) | Bar plot for comparing eval scores (with confidence intervals) across models and tasks. |
| [scores_by_factor()](view-scores-by-factor.html.md) | Bar bar plot for comparing eval scores by model and a boolean factor (e.g. no hint vs. hint). |
| [scores_by_limit()](view-scores-by-limit.html.md) | Line plot showing success rate by token limit. |
| [scores_timeline()](view-scores-timeline.html.md) | Scatter plot with eval scores by model, organization, and release date. Filterable by evaluation and organization. |
| [scores_heatmap()](view-scores-heatmap.html.md) | Heatmap with values for comparing scores across model and task. |
| [scores_by_model()](view-scores-by-model.html.md) | Bar plot for comparing model scores on a single eval. |
| [`scores_radar_by_task()`](view-scores-radar-by-task.html.md) | Radar plot comparing multiple models across headline metrics from different evals. |
| [`scores_radar_by_metric()`](view-scores-radar-by-metric.html.md) | Radar plot for comparing model scores across multiple metrics from a single eval. |
| [sample_tool_calls()](view-sample-tool-calls.html.md) | Heat map visualising tool calls over evaluation turns. |
| [sample_heatmap()](view-sample-heatmap.html.md) | Heat map visualising sample scores. |

## Plots

While pre-built views are useful, you also may want to create your own custom plots. Plots in `inspect_viz` are composed of one or more [marks](reference/inspect_viz.mark.html.md), which can do either higher level plotting (e.g. [dot()](reference/inspect_viz.mark.html.md#dot), [bar_x()](reference/inspect_viz.mark.html.md#bar_x), [bar_y()](reference/inspect_viz.mark.html.md#bar_y), [area()](reference/inspect_viz.mark.html.md#area), [heatmap()](reference/inspect_viz.view.html.md#heatmap), etc.) or lower level drawing on tπhe plot canvas (e.g. [text()](reference/inspect_viz.mark.html.md#text), [image()](reference/inspect_viz.mark.html.md#image), [arrow()](reference/inspect_viz.mark.html.md#arrow), etc.)

### Dot Plot

Here is an example of a simple dot plot using a dataset of [GPQA Diamond](https://huggingface.co/datasets/fingertap/GPQA-Diamond) results:

``` python
from inspect_viz import Data
from inspect_viz.plot import plot
from inspect_viz.mark import dot

gpqa = Data.from_file("gpqa.parquet") # <1>

plot(
    dot( # <2>
        gpqa, 
        x="model_release_date", 
        y="score_headline_value",
        fill="model_organization_name", # <3>
        channels= {   # <4>
            "Model": "model_display_name", 
            "Score": "score_headline_value",
            "Stderr": "score_headline_stderr",
        } # <4>
    ),
    title="GPQA Diamond",
    legend="color", # <5>
    grid=True,
    x_label="Release Date",
    y_label="Score",
    y_domain=[0,1.0],  # <6>
)
```

1.  Read the dataset from a parquet file. You can can also use `Data.from_dataframe()` to read data from any Pandas, Polars, or PyArrow data frame.
2.  Plot using a [dot()](reference/inspect_viz.mark.html.md#dot) mark. The [plot()](reference/inspect_viz.plot.html.md#plot) function takes one or more marks or interactors.
3.  Map the “model_organization_name” column to the `fill` scale of the plot (causing each orgnization to have its own color).
4.  Show tooltip with defined channels.
5.  Add a `legend` to the plot as a key to our color mappings.
6.  Ensure that the y-axis goes from 0 to 1.

### Bar Plot

Here is a simple horizontal bar plot that counts the number of each species:

``` python
from inspect_viz.mark import bar_x

evals = Data.from_file("agi-lsat-ar.parquet")

plot(
    bar_x(
        evals, 
        x="score_headline_value", 
        y="model_display_name",
        sort={"y": "x", "reverse": True},  # <1>
        fill="#3266ae"
    ),
    title="AR-LSAT",
    x_label="Score",
    y_label=None,     # <2>
    margin_left=120.  # <2>
)
```

1.  Sort the bars by score (descending).
2.  Y-axis is labeled with model names so remove default label and ensure it has enough margin.

## Links

Inspect Viz supports creating direct links from visualizations to published Inspect log transcripts. Links can be made at the eval level, or to individual samples, messages, or events. For example, this plot produced with [scores_by_model()](reference/inspect_viz.view.html.md#scores_by_model) includes a link to the underlying logs in its tooltips:

``` python
from inspect_viz.view import scores_by_model
scores_by_model(evals) # baseline=0.91
```

The pre-built [Views](views.html.md) all support linking when a `log_viewer` column is available in the dataset. To learn more about ammending datasets with viewer URLs as well as adding linking support to your own plots see the article on [Links](components-links.html.md).

## Filters

Use [inputs](reference/inspect_viz.input.html.md) to enable filtering datasets and dynamically updating plots. For example, if we had multiple benchmarks available for a scores timeline, we could add a [select()](reference/inspect_viz.input.html.md#select) input for choosing between them:

``` python
from inspect_viz.input import select
from inspect_viz.layout import vconcat

benchmarks = Data.from_file("benchmarks.parquet")

vconcat(
    select(
        benchmarks, 
        label="Benchmark", 
        column="task_name", 
        value="auto"
    ),
    plot(
        dot( 
            benchmarks, 
            x="model_release_date", 
            y="score_headline_value",
            fill="model_organization_name",
        ),
        legend="color", 
        grid=True,
        x_label="Release Date",
        y_label="Score",
        y_domain=[0,1.0],  
        color_domain="fixed"
    )
)
```

We’ve introduced a few new things here:

1.  The [vconcat()](reference/inspect_viz.layout.html.md#vconcat) function from the [layout](reference/inspect_viz.layout.html.md) module lets us stack inputs on top of our plot.

2.  The [select()](reference/inspect_viz.input.html.md#select) function from the [input](reference/inspect_viz.input.html.md) module binds a select box to the `task_name` column.

3.  The `color_domain="fixed"` argument to [plot()](reference/inspect_viz.plot.html.md#plot) indicates that we want to preserve model organization colors even when the plot is filtered.

## Marks

So far the plots we’ve created include only a single [mark](reference/inspect_viz.mark.html.md), however many of the more interesting plots you’ll create will include multiple marks.

For example, here we create a heatmap of evaluation scores by model. There is a [cell()](reference/inspect_viz.mark.html.md#cell) mark which provides the heatmap background color and a [text()](reference/inspect_viz.mark.html.md#text) mark which displays the value.

``` python
from inspect_viz.mark import cell, text

scores = Data.from_file("scores.parquet")

plot(
    cell(
        scores,                                                     
        x="task_name",
        y="model",
        fill="score_headline_value",
    ),
    text(
        scores,
        x="task_name",
        y="model",
        text="score_headline_value",
        fill="white",
    ),
    padding=0,
    color_scheme="viridis",
    height=250,
    margin_left=150,
    x_label=None,
    y_label=None
)
```

Marks can be used to draw dots, lines, bars, cells, arrows, text, and images on a plot.

## Data

In the examples above we made [Data](reference/inspect_viz.html.md#data) available by reading from a parquet file. We can also read data from any Python Data Frame (e.g. Pandas, Polars, PyArrow, etc.). For example:

``` python
import pandas as pd
from inspect_viz import Data

# read directly from file
penguins = Data.from_file("penguins.parquet")

# read from Pandas DF (i.e. to preprocess first)
df = pd.read_parquet("penguins.parquet")
penguins = Data.from_dataframe(df)
```

You might wonder why is there a special [Data](reference/inspect_viz.html.md#data) class in Inspect Viz rather than using data frames directly? This is because Inpsect Viz is an interactive system where data can be dynamically filtered and transformed as part of plotting—the [Data](reference/inspect_viz.html.md#data) therefore needs to be sent to the web browser rather than remaining only in the Python session. This has a couple of important implications:

1.  Data transformations should be done using standard Python Data Frame operations *prior* to reading into [Data](reference/inspect_viz.html.md#data) for Inspect Viz.

2.  Since [Data](reference/inspect_viz.html.md#data) is embedded in the web page, you will want to filter it down to only the columns required for plotting (as you don’t want the additional columns making the web page larger than is necessary).

### Selections

One other important thing to understand is that [Data](reference/inspect_viz.html.md#data) has a built in *selection* which is used in filtering operations on the client. This means that if you want your inputs and plots to stay synchoronized, you should pass the same [Data](reference/inspect_viz.html.md#data) instance to all of them (i.e. import into [Data](reference/inspect_viz.html.md#data) once and then share that reference). For example:

``` python
from inspect_viz import Data
from inspect_viz.plot import plot
from inspect_viz.mark import dot
from inspect_viz.input import select
from inspect_viz.layout import vconcat

# we import penguins once and then pass it to select() and dot()
penguins = Data.from_file("penguins.parquet")

vconcat( 
   select(penguins, label="Species", column="species"),
   plot(
      dot(penguins, x="body_mass", y="flipper_length",
          stroke="species", symbol="species"),
      legend="symbol",
      color_domain="fixed"  
   )
)
```

## Tables

You can also display data in a tabular layout using the [table()](reference/inspect_viz.table.html.md#table) function:

``` python
from inspect_viz.table import column, table

benchmarks = Data.from_file("benchmarks.parquet")

table(
    benchmarks, 
    columns=[
        column("model_organization_name", label="Organization"),
        column("model_display_name", label="Model"),
        column("model_release_date", label="Release Date"),
        column("score_headline_value", label="Score", width=100),
        column("score_headline_stderr", label="StdErr", width=100),
    ]
)
```

You can sort and filter tables by column, use a scrolling or paginated display, and customize several other aspects of table appearance and behavior.

## Learning More

Use these resources to learn more about using Inspect Viz:

- [Views](views.html.md) describes the various available pre-built views and how to customize them.

- [Plots](components-plots.html.md) goes into further depth on plotting options and how to create custom plots.

- Articles on [Marks](components-marks.html.md), [Links](components-links.html.md), [Tables](components-tables.html.md), [Inputs](components-inputs.html.md), and [Interactivity](components-interactivity.html.md) explore other components commonly used in visualizations.

- [Publishing](publishing.html.md) covers publishing Inspect Viz content as standalone plots, notebooks, websites, and dashboards.

- [Reference](reference/index.html.md) provides details on the available marks, interactors, transforms, and inputs.

- [Examples](examples/index.html.md) demonstrates more advanced plotting and interactivity features.

## Footnotes

## Citation

BibTeX citation:

``` quarto-appendix-bibtex
@software{Meridan_Labs_Inspect_Viz_2025,
  author = {Labs, Meridian},
  title = {Inspect {Viz:} {Data} {Visualization} for {Inspect} {AI}
    {Large} {Language} {Model} {Evalutions}},
  date = {2025-08},
  url = {https://github.com/meridianlabs-ai/inspect_viz},
  langid = {en}
}
```

For attribution, please cite this work as:

Labs, Meridian. 2025. *Inspect Viz: Data Visualization for Inspect AI Large Language Model Evalutions*. Released August. <https://github.com/meridianlabs-ai/inspect_viz>.

[^1]: This plot was inspired by and includes data from the [Epoch AI](https://epoch.ai/data/ai-benchmarking-dashboard) Benchmarking Hub
