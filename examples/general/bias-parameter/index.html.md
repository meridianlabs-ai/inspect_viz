# Bias Parameter – Inspect Viz

Use the slider to create bias offsets for the y-axis.

    Code

``` python
from inspect_viz import Data, Param
from inspect_viz.input import slider
from inspect_viz.mark import area_y
from inspect_viz.layout import vconcat
from inspect_viz.plot import plot
from inspect_viz.transform import sql

random_walk = Data.from_file("random-walk.parquet")
bias = Param(100)

vconcat(
    slider(label="Bias", target=bias, min=0, max=1000, step=1),
    plot(area_y(random_walk, x="t", y=sql(f"v + {bias}"), fill="steelblue"))
)
```
