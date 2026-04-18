# Scores by Model – Inspect Viz

This example illustrates the code behind the [scores_by_model()](../../../view-scores-by-model.html.md) pre-built view function. If you want to include this plot in your notebooks or websites you should start with that function rather than the lower-level code below.

The plot summarizes the scores of a single evaluation task, showing performance for 13 different models. Models are ordered based upon their headline score (defaulting to descending).

    Code

``` python
from inspect_viz import Data
from inspect_viz.plot import plot
from inspect_viz.mark import rule_y, baseline
from inspect_viz.transform import ci_bounds

evals = Data.from_file("agi-lsat-ar.parquet")

1ci_lower, ci_upper = ci_bounds(
    score="score_headline_value",
    level=0.95,
    stderr="score_headline_stderr"
)

plot(
2    rule_y(
        evals,
        x="score_headline_value",
        y="model",
        sort={"y": "x", "reverse": True},
        stroke_width=4,
        stroke_linecap="round",
        marker_end="circle",
        tip=True,
        stroke="#416AD0",
    ),
3    rule_y(
        evals,
        x1=ci_lower,
        x2=ci_upper,
        y="model",
        sort={"y": "x", "reverse": True},
        stroke="#416AD020",
        stroke_width=15,
    ),
4    baseline(0.78, label="Human"),
5    margin_left=225,
    y_label=None,
    x_label="Score",
6    x_domain=[0, 1.0]
)
```

1  
Create transforms for upper and lower CI bounds.

2  
This draws the core bar chart, sorting the y-axis by the value of x (descending).

3  
This draws the error bars using the upper and lower bounds.

4  
Add a mark for human baseline.

5  
Ensure there is room for model names in the left margin.

6  
Ensure that the x axis always goes to 1.0 (even if scores are below that).
