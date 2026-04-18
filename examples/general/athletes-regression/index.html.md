# Athletes (Regression) – Inspect Viz

Use the drop downs to filter by sport or sex. Select a range on the plot to filter the table and see the regression lines for the selected range. Hover over the table to highlight the corresponding point on the plot.

    Code

``` python
from inspect_viz import Data, Selection
from inspect_viz.input import search, select
from inspect_viz.interactor import Brush, interval_xy
from inspect_viz.layout import hconcat, vconcat
from inspect_viz.mark import TextStyles, dot, regression_y, text
from inspect_viz.plot import plot
from inspect_viz.table import column, table

athletes = Data.from_file("athletes.parquet")

category = Selection.intersect()
query = Selection.intersect(include=category)
hover = Selection.intersect(empty=True)

vconcat(
    hconcat(
        select(athletes, label="Sport", column="sport", target=category),
        select(athletes, label="Sex", column="sex", target=category),
    ),
    plot(
        text(
            text=["Olympic Athletes"],
            frame_anchor="top",
            styles=TextStyles(font_size=14),
            dy=-20
        ),
        dot(
            athletes,
            filter_by=query,
            x="weight",
            y="height",
            fill="sex",
            r=2,
            opacity=0.1,
        ),
        regression_y(athletes, filter_by=query, x="weight", y="height", stroke="sex"),
        interval_xy(target=query, brush=Brush(fill_opacity=0, stroke="black")),
        dot(
            athletes,
            filter_by=hover,
            x="weight",
            y="height",
            fill="sex",
            stroke="currentColor",
            stroke_width=1,
            r=3
        ),
        xy_domain="fixed",
        r_domain="fixed",
        color_domain="fixed"
    ),
    table(
        athletes, 
        filter_by=query, 
        target=hover, 
        columns=[
            column("name", width=200), 
            "sex", 
            "height", 
            "weight", 
            "sport"
        ],
    )
)
```
