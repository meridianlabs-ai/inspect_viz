# Sample Tool Calls


## Overview

The `sample_tool_calls()` function creates a heat map visualising tool
calls over evaluation turns for each sample.

``` python
from inspect_viz import Data
from inspect_viz.view import sample_tool_calls

tools = Data.from_file("cybench_tools.parquet")
sample_tool_calls(tools)
```

## Data Preparation

To create the plot we read a raw messages data frame from an eval log
using the
[`messages_df()`](https://inspect.aisi.org.uk/reference/inspect_ai.analysis.html#messages_df)
function, then filter down to just the fields we require for
visualization:

``` python
from inspect_ai.analysis import messages_df, log_viewer, model_info, prepare, EvalModel, MessageColumns, SampleSummary

# read messages from log
log = "<path-to-log>.eval"

# Be sure to add EvalModel column so links can be prepared
df = messages_df(log, columns=EvalModel + SampleSummary + MessageColumns)

# trim columns
df = df[[
    "eval_id",
    "sample_id",
    "message_id",
    "model",
    "id",
    "order",
    "tool_call_function",
    "limit",
    "log"
]]

# prepare the data frame with model info and log links
df = prepare(df, [
    model_info(),
    log_viewer("message", url_mappings={
      "logs": "https://samples.meridianlabs.ai/"  
    })
])

# write to parquet
df.to_parquet("cybench_tools.parquet")
```

Note that the trimming of columns is particularly important because
Inspect Viz embeds datasets directly in the web pages that host them (so
we want to minimize their size for page load performance and bandwidth
usage).

## Function Reference

Heat map visualising tool calls over evaluation turns.

[Source](https://github.com/meridianlabs-ai/inspect_viz/blob/b7ff86f26d2b0701b70fdc5c3a024ac7d7f5473e/src/inspect_viz/view/_sample_tool_calls.py#L18)

``` python
def sample_tool_calls(
    data: Data,
    x: str = "order",
    y: str = "id",
    tool: str = "tool_call_function",
    limit: str = "limit",
    tools: list[str] | None = None,
    x_label: str | None = "Message",
    y_label: str | None = "Sample",
    title: str | Title | None = None,
    marks: Marks | None = None,
    width: float | None = None,
    height: float | None = None,
    legend: Legend | NotGiven | None = NOT_GIVEN,
    **attributes: Unpack[PlotAttributes],
) -> Component
```

`data` [Data](reference/inspect_viz.qmd#data)  
Messages data table. This is typically created using a data frame read
with the inspect `messages_df()` function.

`x` str  
Name of field for x axis (defaults to “order”)

`y` str  
Name of field for y axis (defaults to “id”).

`tool` str  
Name of field with tool name (defaults to “tool_call_function”)

`limit` str  
Name of field with sample limit (defaults to “limit”).

`tools` list\[str\] \| None  
Tools to include in plot (and order to include them). Defaults to all
tools found in `data`.

`x_label` str \| None  
x-axis label (defaults to “Message”).

`y_label` str \| None  
y-axis label (defaults to “Sample”).

`title` str \| [Title](reference/inspect_viz.mark.qmd#title) \| None  
Title for plot (`str` or mark created with the `title()` function)

`marks` [Marks](reference/inspect_viz.mark.qmd#marks) \| None  
Additional marks to include in the plot.

`width` float \| None  
The outer width of the plot in pixels, including margins. Defaults to
700.

`height` float \| None  
The outer height of the plot in pixels, including margins. The default
is width / 1.618 (the [golden
ratio](https://en.wikipedia.org/wiki/Golden_ratio))

`legend` [Legend](reference/inspect_viz.plot.qmd#legend) \| NotGiven \| None  
Options for the legend. Pass None to disable the legend.

`**attributes` Unpack\[[PlotAttributes](reference/inspect_viz.plot.qmd#plotattributes)\]  
Additional `PlotAttributes`. By default, the `margin_top` is set to 0,
`margin_left` to 20, `margin_right` to 100, `color_label` is “Tool”,
`y_ticks` is empty, and `x_ticks` and `color_domain` are calculated from
`data`.

## Implementation

The [Sample Tool Calls](examples/inspect/sample-tool-calls/index.qmd)
example demonstrates how this view was implemented using lower level
plotting components.
