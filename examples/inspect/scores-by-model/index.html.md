# Scores by Model

Dataset: [agi-lsat-ar.parquet](agi-lsat-ar.parquet)

This example illustrates the code behind the [`scores_by_model()`](../../../view-scores-by-model.html.md) pre-built view function. If you want to include this plot in your notebooks or websites you should start with that function rather than the lower-level code below.

The plot summarizes the scores of a single evaluation task, showing performance for 13 different models. Models are ordered based upon their headline score (defaulting to descending).

``` python
from inspect_viz import Data
from inspect_viz.plot import plot
from inspect_viz.mark import rule_y, baseline
from inspect_viz.transform import ci_bounds

evals = Data.from_file("agi-lsat-ar.parquet")

ci_lower, ci_upper = ci_bounds( # <1>
    score="score_headline_value",  # <1>
    level=0.95, # <1>
    stderr="score_headline_stderr"  # <1>
)  # <1>

plot(
    rule_y( # <2>
        evals, # <2>
        x="score_headline_value", # <2>
        y="model", # <2>
        sort={"y": "x", "reverse": True}, # <2>
        stroke_width=4, # <2>
        stroke_linecap="round", # <2>
        marker_end="circle", # <2>
        tip=True, # <2>
        stroke="#416AD0", # <2>
    ), # <2>
    rule_y( # <3>
        evals, # <3>
        x1=ci_lower, # <3>
        x2=ci_upper, # <3>
        y="model", # <3>
        sort={"y": "x", "reverse": True}, # <3>
        stroke="#416AD020", # <3>
        stroke_width=15, # <3>
    ), # <3>
    baseline(0.78, label="Human"), # <4>
    margin_left=225, # <5>
    y_label=None,
    x_label="Score",
    x_domain=[0, 1.0] # <6>
)
```

1.  Create transforms for upper and lower CI bounds.
2.  This draws the core bar chart, sorting the y-axis by the value of x (descending).
3.  This draws the error bars using the upper and lower bounds.
4.  Add a mark for human baseline.
5.  Ensure there is room for model names in the left margin.
6.  Ensure that the x axis always goes to 1.0 (even if scores are below that).
