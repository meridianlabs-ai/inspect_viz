# Scores by Factor

Dataset: [evals.csv](evals.csv)

This example illustrates the code behind the [`scores_by_factor()`](../../../view-scores-by-factor.html.md) pre-built view function. If you want to include this plot in your notebooks or websites you should start with that function rather than the lower-level code below.

``` python
from inspect_viz import Data
from inspect_viz.mark import frame, rule_y
from inspect_viz.plot import legend, plot
from inspect_viz.transform import ci_bounds, sql

evals = Data.from_file("evals.csv")

# factor colors/labels
fx_colors = ["#3266ae", "#a6c0e5"] # <1>
fx_labels = ["No hint", "Hint"] # <1>

# confidence interval tranforms
ci_lower, ci_upper = ci_bounds(
    score="score_headline_value", 
    level=0.95,
    stderr="score_headline_stderr"
)

# compute plot height (65 pixels per model)
height = 65 * len(evals.column_unique("model_display_name")) # <2>

plot(
    frame("left", inset_top=5, inset_bottom=5),  # <3>
    rule_y(
        evals,
        x="score_headline_value",
        y="task_arg_hint",
        fy="model_display_name",
        sort={"fy": "-x"}, # <4>
        stroke=sql(f"IF(NOT task_arg_hint, '{fx_labels[0]}', '{fx_labels[1]}')"), 
        stroke_width=3,
        stroke_linecap="round",
        marker_end="circle",
        tip=True,
        channels={
            "Model": "model_display_name", 
            "Hint": "task_arg_hint",
            "Score": "score_headline_value", 
            "Stderr": "score_headline_stderr"
        },
    ),
    rule_y(
        evals,
        x1=ci_lower,  # <5>
        x2=ci_upper,  # <5>
        y="task_arg_hint",
        fy="model_display_name",
        stroke=f"{fx_colors[0]}20",
        stroke_width=15,
    ),
    legend=legend("color", target=evals.selection),  # <6>
    x_label="Score",
    y_label=None, # <7>
    y_ticks=[],  # <7>
    y_tick_size=0, # <7>
    fy_label=None,
    fy_axis="left",
    color_domain=fx_labels,  # <8>
    color_range=fx_colors,   # <8>
    margin_top=0,
    margin_left=100, # <9>
    height=height
)
```

1.  Factors need to define a dark/light color and labels for the their `False` and `True` states.
2.  Compute plot height based on number of unique models.
3.  Sets off each model with their own horizonal axis line.
4.  Order models on y axis from highest to lowest score.
5.  Confidence interval using specified stderr column.
6.  Clickable legend to filter view by factor value.
7.  Y-axis labels and ticks already covered by factor and `frame()`.
8.  Map legend and colors map to factor.
9.  Leave room for model names.
