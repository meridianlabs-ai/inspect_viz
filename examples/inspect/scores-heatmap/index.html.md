# Scores Heatmap – Inspect Viz

This example illustrates the code behind the [scores_heatmap()](../../../view-scores-heatmap.html.md) pre-built view function. If you want to include this plot in your notebooks or websites you should start with that function rather than the lower-level code below.

    Code

``` python
from inspect_viz import Data
from inspect_viz.plot import plot
from inspect_viz.mark import cell, text

evals_data = Data.from_file("evals.parquet")

plot(
1    cell(
        evals_data,                                                         
        x="task_name",                                                      
        y="model",
2        fill="score_headline_value",
        tip=True,
3        inset=1,
4        sort={
            "y": {"value": "fill", "reduce": "sum", "reverse": True},
            "x": {"value": "fill", "reduce": "sum", "reverse": False},
        },
    ),
5    text(
        evals_data,
        x="task_name",
        y="model",
        text="score_headline_value",
        fill="white",
        styles={"font_weight": 600},
    ),
6    padding=0,
    color_scheme="viridis",
    height=250,
    margin_left=150,
    x_label=None,
    y_label=None
)
```

1  
The `cell` mark draws the cells, position each cell along the x and y axis using the fields specified in `x` and `y`.

2  
The cell’s color is determined using the field specified in the `fill`.

3  
The cell inset controls the space between cells.

4  
Sorting of the cells is important in a heatmap to cause colors to be grouped along the x and y axis. In this case, we sort using the sum of the rows and columns, place the highest values at the top righ and lowest values at the bottom left.

5  
Place the value as text centered in the cell.

6  
Remove plot padding so the inset along controls spacing between cells.
