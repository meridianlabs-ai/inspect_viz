# LLM Assistance

## Overview

Inspect Viz is a new library so details on using it are generally not available within the training data of LLMs. Even so, there are a couple of techniques you can use to get assistance:

1.  Inspect Viz makes it’s documentation available in an LLM friendly markdown format ([/llms.txt](https://llmstxt.org/)) which you can register with IDEs or coding agents (or paste into model context windows).

2.  Inspect Viz is built on top of the [Observable Plot](https://observablehq.com/plot/) JavaScript library, so asking an LLM how to do things in Observable Plot will typically yield useful advice.

## llms.txt

There are various versions of LLM friendly documentation available. Use the `llms.txt` variant to register documentation with an IDE or coding agent (details below) or the other variants for pasting into a model context window.

|  |  |
|----|----|
| [llms.txt](https://meridianlabs-ai.github.io/inspect_viz/llms.txt) | Documentation index (links to other docs). |
| [llms-guide.txt](https://meridianlabs-ai.github.io/inspect_viz/llms-guide.txt) | Documentation excluding reference (138k). |
| [llms-full.txt](https://meridianlabs-ai.github.io/inspect_viz/llms-full.txt) | Documentation including reference (529k) |

The `llms-guide.txt` file works well for models with a 128k or 200k context window (e.g. Claude 3/4, GPT 4 or o3/o4). The `llms-full.txt` file requires a model with a larger context window (e.g. GPT 4.1, Gemini 2.5).

Details are provided below on how to register `/llms.txt` for use with [Claude Code](#claude-code), [Claude Desktop](#claude-desktop), and [Cursor](#cursor-ide).

## Observable

Inspect Viz is built on the [Observable Plot](https://observablehq.com/plot/) JavaScript library and consequently it’s Python API maps quite closely to Observable’s JavaScript API. For example, here is an Inspect Viz dot plot and the equivalent Observable dot plot:

``` python
plot(
    dot(
        penguins, 
        x="body_mass", 
        y="flipper_length",
        stroke="species", 
        symbol="species"
    ),
    grid=True,
    legend=legend("symbol")
)
```

``` js
Plot.plot({
  marks: [
    Plot.dot(penguins, {
      x: "body_mass",
      y: "flipper_length", 
      stroke: "species",
      symbol: "species"
    })
  ],
  grid: true,
  symbol: { legend: true }
})
```

If you are looking to refine the appearance of plots or create a custom plot with advanced elements, ask an LLM how to do it in Observable Plot and you can very often translate this into the equivalent Inspect Viz construct.

## Claude Code

You can configure Claude Code with access to the Inspect Viz documentation using an MCP server. To add the documentation for Inspect Viz to the project in the current working directory, execute this:

``` bash
claude mcp add-json inspect-viz-docs '{"type":"stdio","command":"uvx" ,"args":["--from", "mcpdoc", "mcpdoc", "--urls", "inspect_viz:https://meridianlabs-ai.github.io/inspect_viz/llms.txt"]}' -s local
```

Alternatively, configure the following MCP server for your project by editing the Claude Code config file (`~/.claude.json`):

``` json
"mcpServers": {
   "inspect-viz-docs": {
      "type": "stdio",
      "command": "uvx",
      "args": [
      "--from",
      "mcpdoc",
      "mcpdoc",
      "--urls",
      "inspect_viz:https://meridianlabs-ai.github.io/inspect_viz/llms.txt"
      ]
   }
}
```

## Claude Desktop

To register an Inspect Viz MDP server with Claude Desktop, do the following:

1.  Ensure that you have installed the [uv](https://docs.astral.sh/uv/getting-started/installation/) Python package manager.

2.  Note the full path to the `uvx` binary by executing `which uvx` in a terminal (you’ll neded this for configuration below).

3.  Open `Settings/Developer` to update the `claude_desktop_config.json` file. Add the `inspect-viz-docs` MCP server into the config:

    ``` json
    {
      "globalShortcut": "Alt+Ctrl+Space",
      "mcpServers": {
        "inspect-viz-docs": {
          "command": "/full/path/to/uvx",
          "args": [
              "--from",
              "mcpdoc",
              "mcpdoc",
              "--urls",
              "inspect_viz:https://meridianlabs-ai.github.io/inspect_viz/llms.txt",
              "--transport",
              "stdio"
          ]
        }
      }
    }
    ```

    Note that it is critical that you provide the **full path** to `uvx` in the “command” configuration.

4.  Restart Claude Desktop. If you go to `Settings/Developer` you should see something like the following:

    ![](claude-desktop-mcp.png)

## Cursor IDE

You can use `/llms.txt` documentation within Cursor in one of two ways:

1.  Use [@Docs](https://docs.cursor.com/en/context/@-symbols/@-docs) to register the Inspect Viz documentation with Cursor, which will index and retrieve sections of the documentation as required.

2.  Use the [mcpdoc](https://github.com/langchain-ai/mcpdoc) MCP server configured with the Inspect Viz documentation. To do this, register an MCP server within the`~/.cursor/mcp.json` configuration file as follows:

    ``` json
    {
      "mcpServers": {
        "inspect-viz-docs": {
          "command": "uvx",
          "args": [
            "--from",
            "mcpdoc",
            "mcpdoc",
            "--urls",
            "inspect_viz:https://meridianlabs-ai.github.io/inspect_viz/llms.txt",
            "--transport",
            "stdio"
          ]
        }
      }
    }
    ```

    Then, add the followiing to `User Rules` (found within `Settings/Rules`):

    ``` default
    For ANY question about Inspect Viz, use the inspect-viz-docs MCP server to help answer -- 
    call list_doc_sources tool to get the available llms.txt file
    call fetch_docs tool to read it
    reflect on the urls in llms.txt 
    reflect on the input question 
    call fetch_docs on any urls relevant to the question
    use this to answer the question
    ```
