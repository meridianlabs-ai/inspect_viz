#!/bin/bash

files=("index" "components-plots" "components-marks" "components-links" "components-tables" "components-inputs" "components-interactivity" "view-scores-by-task" "view-scores-by-model" "view-scores-by-factor" "view-scores-timeline" "view-scores-heatmap" "view-sample-tool-calls" "view-sample-heatmap" "view-scores-radar" "examples/inspect/scores-by-task/index" "examples/inspect/scores-by-model/index" "examples/inspect/scores-by-factor/index" "examples/inspect/scores-timeline/index" "examples/inspect/scores-heatmap/index" "examples/inspect/sample-tool-calls/index" "examples/inspect/sample-heatmap/index" "examples/general/penguins/index" "examples/general/bias-parameter/index"  "examples/general/seattle-weather/index" "examples/general/athletes-regression/index" "examples/general/athletes-errorbars/index" "publishing-plots" "publishing-notebooks" "publishing-websites" "publishing-dashboards" "publishing-png-output" "reference/inspect_viz" "reference/inspect_viz.view" "reference/inspect_viz.plot" "reference/inspect_viz.mark" "reference/inspect_viz.interactor" "reference/inspect_viz.transform" "reference/inspect_viz.table" "reference/inspect_viz.input" "reference/inspect_viz.layout") 


if [ "$QUARTO_PROJECT_RENDER_ALL" = "1" ]; then
    llms_guide="_site/llms-guide.txt"
    rm -f "${llms_guide}"
    llms_full="_site/llms-full.txt"
    rm -f "${llms_full}"
    mv _quarto.yml _quarto.yml.bak
    for file in "${files[@]}"; do
        echo "llms: ${file}.qmd"
        quarto render "${file}.qmd" --to gfm-raw_html --quiet --no-execute
        output_file="${file}.md"
        cat "${output_file}" >> "${llms_full}"
        echo "" >> "${llms_full}"
        if [[ ! "${file}" == reference/* ]]; then
            cat "${output_file}" >> "${llms_guide}"
            echo "" >> "${llms_guide}"
        fi
        mv $output_file "_site/${file}.html.md"
    done
    mv _quarto.yml.bak _quarto.yml
fi


