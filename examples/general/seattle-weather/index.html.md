# Seattle Weather – Inspect Viz

Select a horizontal range on the dot pot to filter the contents of the bar plot. Click the legend or the bar plot to filter by weather conditions.

    Code

``` python
from inspect_viz import Data, Selection
from inspect_viz.interactor import Brush, highlight, interval_x, toggle_y
from inspect_viz.plot import legend, plot, plot_defaults
from inspect_viz.mark import bar_x, dot
from inspect_viz.layout import vconcat
from inspect_viz.transform import count, date_month_day

# data
seattle = Data.from_file("seattle-weather.parquet")

# plot defaults for domain and range
weather = ["sun", "fog", "drizzle", "rain", "snow"]
plot_defaults(
    color_domain=weather,
    color_range=["#e7ba52", "#a7a7a7", "#aec7e8", "#1f77b4", "#9467bd"]
)

# selections (scatter x-range and bar/legend click)
range = Selection("intersect")
click = Selection("single")

vconcat(
    plot(
        dot(
            data=seattle,
            filter_by=click,
            x=date_month_day("date"),
            y="temp_max",
            fill="weather",
            fill_opacity=0.7,
            r="precipitation",
        ),
        interval_x(target=range, brush=Brush(fill="none", stroke="#888")),
        highlight(by=range, fill="#ccc", fill_opacity=0.2),
        legend=legend("color", target=click),
        xy_domain="fixed",
        x_tick_format="%b",
        r_domain="fixed",
        r_range=[2, 10]
    ),
    plot(
        bar_x(seattle, x=count(), y="weather", fill="#ccc", fill_opacity=0.2),
        bar_x(seattle, filter_by=range, x=count(), y="weather", fill="weather"),
        toggle_y(target=click),
        highlight(by=click),
        x_domain="fixed",
        y_domain=weather,
        y_label=None,
        height=200
    )
)
```
