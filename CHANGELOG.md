## Unreleased

- Quarto: Write plot data to content-addressed `site_data/immutable/*.arrow` assets and fetch via the browser Cache API.
- Quarto: Bypass the ~3.5 MB ipywidgets loader in favor of a small inline bootstrap.
- Quarto: Placeholder loading shimmer so that plots occupy their full size even before loading.

## 0.3.5 (December 5, 2025)

- Views: Take view functions out of beta.

## 0.3.4 (October 27, 2025)

- Radar: Fill selected polygons only, correct quadrant angles for labels, default to `task_name`.

## 0.3.3 (October 27, 2025)

- Views: Add `scores_radar`, `scores_radar_by_task`, and `scores_radar_by_metric` views.
- Views: Improvements to `scores_by_limit`.
- Plots: Improve heatmap defaults.
- Marks: Position radar labels using pixel offset with angle-quadrant awareness.
- Packaging: Export `__version__`.

## 0.3.2 (August 16, 2025)

- Views: Add `samples_heatmap` view.
- Views: Add custom legend support to all views; add `title` and `marks` to `scores_by_limit`.
- Legend: Improved appearance for `top` / `bottom` frame anchors.
- Compatibility: Adapt correctly to JupyterLab themes.

## 0.3.1 (August 12, 2025)

- Views: Add `scores_by_limit` view.
- Plots: Add `orientation` option to heatmap; allow container to grow to content.
- Marks: Improved support for date-based regression lines.
- Legend: Various improvements; remove bottom margin.
- Quarto: Format detection updated for Quarto 1.8.
- Testing: Add test suite and build workflow.

## 0.3.0 (August 3, 2025)

- Views: Add `scores_by_factor` view.
- Views: Rename `scores_with_baseline` to `scores_by_model`.
- Views: Add `title` and `marks` arguments to built-in views.
- Plots: PNG output with `"auto"` detection for Quarto.
- Plots: Dashboard layout support.
- Marks: Add `baseline` mark; `rule_y` no longer requires data.
- Tooltips: Support boolean value filtering; pass user channels through.
- Tool calls: Add log-link support.
- Transforms: More flexible `ci_bounds` with distinct channels for lower and upper bounds.
- Docs: Add citation, Twitter card, and `llms.txt`.

## 0.2.8 (July 25, 2025)

- Views: Add frontier support to `scores_timeline`.
- Views: `scores_timeline` supports data transformed with `model_info`.
- Plots: Heatmap accepts `Legend` directly; add sorting option.
- Plots: Switch built-in views to use `model_display_name`.
- Marks: Text collision handling, opt-in per plot.
- Tooltips: Dismiss on scroll; improved initialization; set min-width.
- Legend: Allow `False` to disable legend on any view.
- Docs: Add data preparation documentation.

## 0.2.7 (July 18, 2025)

- Views: Fix color domain for `scores_timeline`.
- Tables: Tweak column width behavior.

## 0.2.6 (July 18, 2025)

- Packaging: Improve publish workflow.

## 0.2.5 (July 18, 2025)

Initial release.