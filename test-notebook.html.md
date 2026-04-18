# test-notebook

# Notebook smoke test[¶](#Notebook-smoke-test)

Renders a few plots through the standard anywidget (non-Quarto) path so the Jupyter/nbconvert output can be compared against the Quarto path. None of the recent placeholder / shimmer / `mosaic-widget` class changes should affect this path.

In \[1\]:

    from inspect_viz import Data
    from inspect_viz.plot import plot_defaults, legend
    from inspect_viz.view import scores_timeline

    plot_defaults(width=800, height=500)
    evals = Data.from_file("benchmarks.parquet")

## Scores timeline (mirrors `index.qmd`'s first plot)[¶](#Scores-timeline-(mirrors-index.qmd's-first-plot))

In \[2\]:

    scores_timeline(
        evals,
        legend=legend("color", frame_anchor="top-left", inset=20),
    )

Out\[2\]:

## Plain plot (no inputs, no legend)[¶](#Plain-plot-(no-inputs,-no-legend))

In \[3\]:

    from inspect_viz.plot import plot
    from inspect_viz.mark import dot

    plot(dot(evals, x="model_release_date", y="score_headline_value", r=3, fill="model_organization_name"))

Out\[3\]:
