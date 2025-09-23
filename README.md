Welcome to Inspect Viz, a data visualisation library for Inspect AI. Inspect Viz provides flexible tools for high quality interactive visualisations from Inspect evaluations.

To get started with Inspect Viz, please see the documentation at <https://meridianlabs-ai.github.io/inspect_viz/>.

## Installation

Latest published version:

```bash
pip install inspect-viz
```

Latest development version:

```bash
pip install git+https://github.com/meridianlabs-ai/inspect_viz
```

## Development

To work on development of Inspect Viz, clone the repository and install with the `-e` flag and `[dev]` optional dependencies:

```bash
git clone https://github.com/meridianlabs-ai/inspect_viz
cd inspect_viz
pip install -e ".[dev]"
```

Run linting, formatting, and tests via

```bash
make check
make test
```

For JS / front-end development:

```sh
yarn install
```

While developing front end components, you can run the following in a separate terminal to automatically rebuild JavaScript as you make changes:

```sh
yarn dev # or
yarn dev-sourcemap
```

To build the docs locally and view them in your browser, install the optional doc dependencies and run `quarto preview`.

```sh
pip install -e ".[doc]"
quarto preview inspect_viz/docs/index.qmd
```

If you use VS Code, you should be sure to have installed the recommended extensions (Python, Ruff, MyPy, Inspect AI, Quarto). Note that you'll be prompted to install these when you open the project in VS Code.
