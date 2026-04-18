# Dashboards – Inspect Viz

## Overview

[Quarto Dashboards](https://quarto.org/docs/dashboards/) are a special type of Quarto website optimized for publishing easily navigable sets of plots and tables. Features of Quarto Dashboards include:

1.  Many flexible ways to layout components (row or column based, tabsets, multiple pages, etc.) including responsive layout for mobile devices.

2.  A variety of ways to present inputs for interactivity including toolbars, sidebars, and card-level inputs.

3.  Dozens of available themes including the ability to create your own themes.

## Example

Here is the [Scores Timeline](./examples/inspect/scores-timeline/index.html.md) example from this repository re-written as a dashboard (this is a live dashboard embedded as an iframe):

[Capabilities Timeline](#)

Expand ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgc3R5bGU9ImhlaWdodDoxZW07d2lkdGg6MWVtOyIgYXJpYS1oaWRkZW49InRydWUiIHJvbGU9ImltZyI+PHBhdGggZD0iTTIwIDVDMjAgNC40IDE5LjYgNCAxOSA0SDEzQzEyLjQgNCAxMiAzLjYgMTIgM0MxMiAyLjQgMTIuNCAyIDEzIDJIMjFDMjEuNiAyIDIyIDIuNCAyMiAzVjExQzIyIDExLjYgMjEuNiAxMiAyMSAxMkMyMC40IDEyIDIwIDExLjYgMjAgMTFWNVpNNCAxOUM0IDE5LjYgNC40IDIwIDUgMjBIMTFDMTEuNiAyMCAxMiAyMC40IDEyIDIxQzEyIDIxLjYgMTEuNiAyMiAxMSAyMkgzQzIuNCAyMiAyIDIxLjYgMiAyMVYxM0MyIDEyLjQgMi40IDEyIDMgMTJDMy42IDEyIDQgMTIuNCA0IDEzVjE5WiIgLz48L3N2Zz4=)

Expand ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgc3R5bGU9ImhlaWdodDoxZW07d2lkdGg6MWVtOyIgYXJpYS1oaWRkZW49InRydWUiIHJvbGU9ImltZyI+PHBhdGggZD0iTTIwIDVDMjAgNC40IDE5LjYgNCAxOSA0SDEzQzEyLjQgNCAxMiAzLjYgMTIgM0MxMiAyLjQgMTIuNCAyIDEzIDJIMjFDMjEuNiAyIDIyIDIuNCAyMiAzVjExQzIyIDExLjYgMjEuNiAxMiAyMSAxMkMyMC40IDEyIDIwIDExLjYgMjAgMTFWNVpNNCAxOUM0IDE5LjYgNC40IDIwIDUgMjBIMTFDMTEuNiAyMCAxMiAyMC40IDEyIDIxQzEyIDIxLjYgMTEuNiAyMiAxMSAyMkgzQzIuNCAyMiAyIDIxLjYgMiAyMVYxM0MyIDEyLjQgMi40IDEyIDMgMTJDMy42IDEyIDQgMTIuNCA0IDEzVjE5WiIgLz48L3N2Zz4=)

------------------------------------------------------------------------

Benchmark data from the Epoch AI [Benchmarking Hub](https://epoch.ai/data/ai-benchmarking-dashboard).

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAxNiAxNiIgY2xhc3M9ImJpIGJpLWNoZXZyb24tbGVmdCBjb2xsYXBzZS1pY29uIiBzdHlsZT0iZmlsbDpjdXJyZW50Q29sb3I7IiBhcmlhLWhpZGRlbj0idHJ1ZSIgcm9sZT0iaW1nIj4KICAgICAgPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBkPSJNMTEuMzU0IDEuNjQ2YS41LjUgMCAwIDEgMCAuNzA4TDUuNzA3IDhsNS42NDcgNS42NDZhLjUuNSAwIDAgMS0uNzA4LjcwOGwtNi02YS41LjUgMCAwIDEgMC0uNzA4bDYtNmEuNS41IDAgMCAxIC43MDggMHoiIC8+CiAgICA8L3N2Zz4=)

Below is the source code for this dashboard. You’ll notice that this looks quite similar to the code for any other Quarto document, but level-two headings (`##`) have been added to denote a toolbar and dashboard rows (additional headings could be used to create columns and tabsets).

```` python
---
title: "Capabilities Timeline"
format: dashboard
---

```{python}
from inspect_viz import Data, Param
from inspect_viz.input import select
from inspect_viz.mark import dot
from inspect_viz.plot import plot
from inspect_viz.table import table, column
from inspect_viz.view import scores_timeline
from inspect_viz.input import checkbox_group, select

evals = Data.from_file("benchmarks.parquet")
```

## {.sidebar}

```{python}
select(
    evals,
    column="task_name",
    value="auto",
    label="Benchmark"
)

checkbox_group(
    evals, 
    column="model_organization_name", 
    label="Organization"
)
```

***

Benchmark data from the Epoch AI [Benchmarking Hub](https://epoch.ai/data/ai-benchmarking-dashboard).

## Column

### Row {height=60%}

```{python}
scores_timeline(evals, filters=False)
```

### Row {height=40%}

```{python}
table(
    evals, 
    columns=[
        column("model_organization_name", label="Organization"),
        column("model_display_name", label="Model"),
        column("model_release_date", label="Release Date"),
        column("score_headline_value", label="Score", width=100),
        column("score_headline_stderr", label="StdErr", width=100),
    ]
)
```
````

## Notebook Execution

When using Inspect Viz with Quarto Websites you should always add the following configuration to your `_quarto.yml` to specify that notebooks should be fully executed when rendered:

    _quarto.yml

``` yaml
execute: 
  enabled: true
```

## Learning More

- See the [Quarto Dashboards](https://quarto.org/docs/dashboards/) documentation for additional details on creating dashboards.

- See the [Dashboard Examples](https://quarto.org/docs/gallery/#dashboards) to get an idea for the sorts of layouts and themes that are available and to see the source code for a variety of dashboard types.
