# Interactivty

## Overview

Inspect Viz supports interactive filtering and cross-filtering of plot data based based on [Inputs](components-inputs.html.md) and [Interactors](#interactors). Filtering is done based on *Selections*: each [Data](reference/inspect_viz.html.md#data) table has a built-in selection and you can also create [Selection](reference/inspect_viz.html.md#selection) instances for more sophisticated behaviors.

## Filtering

The most straightforward usage of selections is adding inputs which filter the data displayed in a plot. This filtering uses the *built in* selection of [Data](reference/inspect_viz.html.md#data) instances. For example, here we add a [select()](reference/inspect_viz.input.html.md#select) input to enable filtering by species:

``` python
from inspect_viz import Data
from inspect_viz.plot import plot
from inspect_viz.mark import dot
from inspect_viz.input import select
from inspect_viz.layout import vconcat

penguins = Data.from_file("penguins.parquet")

vconcat( # <1> 
   select(penguins, label="Species", column="species"),  # <2>
   plot(
      dot(penguins, x="body_mass", y="flipper_length",  # <3> 
          stroke="species", symbol="species"),
      legend="symbol",
      color_domain="fixed"       # <4>
   )
)
```

1.  [vconcat()](reference/inspect_viz.layout.html.md#vconcat) function stacks the select input on top of the plot.
2.  Select input bound to “species” column.
3.  Use of `penguins` in both [select()](reference/inspect_viz.input.html.md#select) and [plot()](reference/inspect_viz.plot.html.md#plot) automatically binds to default selection for the penguins [Data](reference/inspect_viz.html.md#data) object.
4.  Fixed color domain ensures that species colors remain the same even when filtered.

### Fixed Domain

The example agove introduces an important concept when dealing with selections and filtering: `"fixed"` scale domains (in this case `color_domain="fixed"`). Fixed scale domains instruct a plot to first calculate a scale domain in a data-driven manner, but then keep that domain fixed across subsequent updates.

Fixed domains enable stable configurations without requiring a hard-wired domain to be known in advance, preventing disorienting scale domain “jumps” that hamper comparison across filter interactions. Several of the examples below will use `"fixed"` domains to provide this stability across interactions.

## Params

As illustrated above, inputs can be used to filter dataset selections. Inputs can also be used to set [Param](reference/inspect_viz.html.md#param) values that make various aspects of plots dynamic. For example, here is a density plot of flight delays which uses a [slider()](reference/inspect_viz.input.html.md#slider) input to vary the amount of smooth ing by setting the kernel bandwidth:

``` python
from inspect_viz import Param
from inspect_viz.input import slider
from inspect_viz.mark import density_y

flights = Data.from_file("flights.parquet")

bandwidth = Param(0.1) # <1> 

vconcat(
   slider(
      label="Bandwidth (σ)", target=bandwidth, # <2>
      min=0.1, max=100, step=0.1
   ),
   plot(
      density_y(
         flights, x="delay", fill="steelblue", bandwidth=bandwidth # <3>
      ),
      x_domain="fixed",
      y_axis=None,
      height=250,
   )
)
```

1.  Create a `bandwidth` parameter with a default value of 0.1.
2.  Bind the [slider()](reference/inspect_viz.input.html.md#slider) to the `bandwidth` parameter.
3.  Apply the `bandwidth` to the plot (plot automatically redraws when the bandwidth changes).

## Interactors

*Interactors* imbue plots with interactive behavior. Most interactors listen to input events from rendered plot SVG elements to update bound [*selections*](reference/inspect_viz.html.md#selection). Interactors take facets into account to properly handle input events across subplots.

### Interval

The [interval_x()](reference/inspect_viz.interactor.html.md#interval_x) and [interval_y()](reference/inspect_viz.interactor.html.md#interval_y) interactors create 1D interval brushes. The [interval_xy()](reference/inspect_viz.interactor.html.md#interval_xy) interactor creates a 2D brush. Interval interactors accept a `pixel_size` parameter that sets the brush resolution: values may snap to a grid whose bins are larger than screen pixels and this can be leveraged to optimize query latency.

For example, below we stack two plots vertically, a [dot()](reference/inspect_viz.mark.html.md#dot) plot along with a [bar_x()](reference/inspect_viz.mark.html.md#bar_x) plot that counts the `sex` column. We then add an [interval_x()](reference/inspect_viz.interactor.html.md#interval_x) interactor that enables us to filter the dataset using selections on the dot plot.

``` python
from inspect_viz import Data, Selection
from inspect_viz.interactor import Brush, interval_x
from inspect_viz.plot import plot
from inspect_viz.mark import bar_x, dot, regression_y
from inspect_viz.transform import count

athletes = Data.from_file("athletes.parquet")

range = Selection.intersect() # <1>

vconcat(
   plot(
      dot(athletes, x="weight", y="height", fill="sex", opacity=0.1),
      regression_y(athletes, x="weight", y="height", stroke="sex"),
      interval_x(
         target=range, # <2>
         brush=Brush(fill="none", stroke="#888") # <3>
      ),
      legend="color"
   ),
   plot(
      bar_x(
         athletes, filter_by=range,  # <4>
         x=count(), y="sex", fill="sex"
      ), 
      y_label=None,
      height=150,
      x_domain="fixed" # <5>
   )
)
```

1.  A [Selection](reference/inspect_viz.html.md#selection) is a means of filtering datasets based on interactions. Here we use an “intersect” selection for application of a simple filter from dot plot to bar plot.
2.  The `range` selection is set via the [interval_x()](reference/inspect_viz.interactor.html.md#interval_x) interactor (which enables using the mouse to select an x-range).
3.  The [Brush](reference/inspect_viz.interactor.html.md#brush) defines the color of the interactor (in this case `#888`, a medium-gray).
4.  The `range` selection is consumed using the `filter_by` parameter.
5.  We set the `x_domain` for the bar plot to “fixed” so that the scale doesn’t change as the dataset is filtered.

Try using the mouse to brush over regions on the dot plot—the bar plot will update accordingly.

### Toggle

The [toggle()](reference/inspect_viz.interactor.html.md#toggle) interactor selects individual points (e.g., by click or shift-click) and generates a selection clause over specified fields of those points. Directives such as [toggle_color()](reference/inspect_viz.interactor.html.md#toggle_color), [toggle_x()](reference/inspect_viz.interactor.html.md#toggle_x), and [toggle_y()](reference/inspect_viz.interactor.html.md#toggle_y) simplify specification of which channel fields are included in the resulting predicates.

The [highlight()](reference/inspect_viz.interactor.html.md#highlight) interactor updates the rendered state of a visualization in response to a Selection. Non-selected points are set to translucent, neutral gray, or other specified visual properties. Selected points maintain normal encodings.

This example demonstrates using the [toggle_y()](reference/inspect_viz.interactor.html.md#toggle_y) and [highlight()](reference/inspect_viz.interactor.html.md#highlight) interactors to render a bar chart that can be clicked to select a subset of points on the dot plot above it. The dot plot legend also targets the same the selection to make itself interactive.

``` python
from inspect_viz import Data, Selection
from inspect_viz.interactor import highlight, toggle_y
from inspect_viz.plot import legend, plot
from inspect_viz.mark import bar_x, dot
from inspect_viz.layout import vconcat
from inspect_viz.transform import count, date_month_day

seattle = Data.from_file("seattle-weather.parquet")

weather = Selection.single() # <1> 

vconcat(
    plot(
        dot(
            data=seattle,
            filter_by=weather, # <2> 
            x=date_month_day("date"),
            y="temp_max",
            fill="weather",
            fill_opacity=0.7,
            r="precipitation", # <3> 
        ),
        legend=legend("color", target=weather), # <4>
        x_tick_format="%b",
        color_domain="fixed",
        r_domain="fixed", 
        r_range=[2, 10]
    ),
    plot(
        bar_x(seattle, x=count(), y="weather", fill="weather"),
        toggle_y(target=weather),  # <5> 
        highlight(by=weather), # <6>
        x_domain="fixed",
        y_label=None,
        height=200
    )
)
```

1.  Single selection (filter out all other points).
2.  Dot plot should filter by the selection.
3.  Show precipitation level using dot radius.
4.  Clicks on the legend target the same selection
5.  [toggle_y()](reference/inspect_viz.interactor.html.md#toggle_y) interactor to filter by weather.
6.  [highlight()](reference/inspect_viz.interactor.html.md#highlight) interactor to fade out unselected bars.

Try clicking either the legend or the bar plot elements to filter the dot plot.

## Crossfilter

In many cases you’ll want to have an input or interactor that both consumes and produces the same selection (i.e. filtered based on interactions with other inputs or interactors, but also able to provide its own filtering).

### Inputs

This example demonstrates crossfiltering across [inputs](reference/inspect_viz.input.html.md). We plot shot types taken during the 2023 WNBA season, providing a [select()](reference/inspect_viz.input.html.md#select) input that filters by team, and another [select()](reference/inspect_viz.input.html.md#select) input that filters by player (which in turn is also filtered by the currently selected team). Click on the numbers at right for additional explanation of the code.

``` python
from inspect_viz import Data, Selection
from inspect_viz.input import select
from inspect_viz.layout import vconcat, hconcat
from inspect_viz.mark import bar_x 
from inspect_viz.plot import plot
from inspect_viz.transform import count

shots = Data.from_file("wnba-shots-2023.parquet")

filter = Selection.crossfilter()            # <1>

vconcat(
   hconcat(
      select(
         shots, label="Team", column="team_name", 
         target=filter                      # <2>
      ),
      select(
         shots, label="Athlete", column="athlete_name", 
         filter_by=filter, target=filter    # <3>
      )
   ),
   plot(
      bar_x(
         shots, filter_by=filter,
         x=count(), y="category", fill="category"
      ),
      y_label=None,
      color_domain="fixed",                # <4>
      y_domain=["Jump", "Layup", "Hook"],  # <4>
      height=200,
      margin_left=60
   )
)
```

1.  Create a crossfilter selection, which enables inputs to both consume and produce the same selection (conditioning their available choices on other inputs).
2.  The team select box targets the `filter` selection (filtering both the choices in the athelte select box and what is displayed in the plot).
3.  The athlete select box is both *filtered by* and targets the `filter` selection, enabling it to both confine itself to the selected team as well as filter what is displayed in the plot.
4.  As different teams and players are selected, the y-axis may take on differnet values and ordering. These options ensure that the y-axis remains stable across selections.

### Interactors

This example demonstrates crossfiltering across plot [interactors](reference/inspect_viz.interactor.html.md). We plot histograms showing arrival delay and departure time for flights. When you select a range in one plot, the other plot updates to show only the data within that selection—and vice versa. This bidirectional filtering is achieved using `Selection.crossfilter()`, which ensures each plot’s selection affects all other plots except itself. Click on the numbers at right for additional explanation of the code.

``` python
from inspect_viz import Data, Selection
from inspect_viz.mark import rect_y
from inspect_viz.layout import vconcat
from inspect_viz.plot import plot
from inspect_viz.transform import count, bin
from inspect_viz.interactor import interval_x

flights = Data.from_file("flights.parquet")

brush = Selection.crossfilter() # <1>

def flights_plot(x, label):    # <2>
   return plot(
      rect_y(
         flights, filter_by=brush, 
         x=bin(x), y=count(), fill="steelblue"
      ),
      interval_x(target=brush),   # <3>
      height=200,
      x_label=label,
      x_domain="fixed",   # <4>
      y_tick_format="s"
   )

vconcat(
   flights_plot("delay", "Arrival Delay (min)"),
   flights_plot("time", "Departure Time (hour)")
)
```

1.  Create a crossfilter selection, which ensures each plot’s selection affects all other plots except itself.
2.  Our two plots are identical save for the `x` value and the `x_label` so factor out into a function.
3.  The [interval_x()](reference/inspect_viz.interactor.html.md#interval_x) interactor enables horizontal selection (targeting the crossfiltering `brush`).
4.  Use a `"fixed"` domain so that the x-axis remains stable even when being filtered.

Try selecting a horizontal range on either or both of the bar plots.
