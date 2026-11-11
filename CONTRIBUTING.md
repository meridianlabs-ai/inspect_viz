# Contributing to Inspect Viz

Thanks for your interest in contributing to Inspect Viz, a data visualization library for Inspect AI evaluations.

## Development setup

Inspect Viz targets Python 3.11+ and needs [uv](https://docs.astral.sh/uv/) 0.13.4 or later. Clone the repository and install it in editable mode with the `dev` optional dependencies:

```bash
git clone https://github.com/meridianlabs-ai/inspect_viz
cd inspect_viz
uv sync --locked --extra dev
```

`uv sync --locked` creates `.venv` with the exact versions in `uv.lock`, the `dev` extra included, and installs Inspect Viz editable. It fails if `uv.lock` is out of date with `pyproject.toml`. Run Python commands from the environment: `uv run <command>`, `.venv/bin/<command>`, or `source .venv/bin/activate`. `uv sync --locked` without `--extra dev` removes the dev tools again. To also install the `doc` extra, run `uv sync --locked --extra dev --extra doc`.

The front-end widgets are built with TypeScript. To work on them, install the JS dependencies with yarn 1:

```bash
yarn install --frozen-lockfile
```

`--frozen-lockfile` installs the exact versions in `yarn.lock` and fails if `package.json` asks for a version that `yarn.lock` doesn't have. After you change `package.json`, run `yarn install` and commit `yarn.lock`. yarn 1 has no cooldown setting, so `yarn install` and `yarn add` take the newest matching releases.

While developing front-end components, run the following in a separate terminal to automatically rebuild the JavaScript as you make changes:

```bash
yarn dev          # or
yarn dev-sourcemap
```

### Dependencies

[DEPENDENCIES.md](https://github.com/meridianlabs-ai/actions/blob/main/DEPENDENCIES.md) in meridianlabs-ai/actions tells how the Inspect repositories install and change dependencies. It covers the lock file, the cooldown, Dependabot, the canaries, the release build tools, and the procedures to add or update a dependency. Follow it. It is the same for every Inspect repository, so this file does not repeat it.

For this repository:

- inspect_viz does not depend on inspect-ai.
- No package has the 6-hour cooldown, so `pyproject.toml` has no `[tool.uv.exclude-newer-package]` table. If you add the first 6-hour entry, put the `six-hour-cooldown` group before `python-packages` in `.github/dependabot.yml`.
- Dependabot also bumps `yarn.lock`, weekly, with the same 7-day cooldown.
- When you change the `hatchling` requirement in `[build-system]`, make the same change in `scripts/build-dist/requirements.in` and compile `requirements.txt` again. A test checks that the two agree.

## Checks and tests

Run the commands below in the activated `.venv`, or prefix them with `uv run`. Run linting, formatting, and type checking with:

```bash
make check
```

This runs `ruff check --fix`, `ruff format`, and `mypy src`. Run the Python test suite with:

```bash
make test
```

For the TypeScript front end, check types and formatting with:

```bash
yarn typecheck
yarn format:check   # or `yarn format` to apply formatting
```

## Commit messages and releases

We use [Conventional Commits](https://www.conventionalcommits.org/). Because we
squash-merge, **the PR title becomes the commit message** — so the title is what
matters. Format it as `<type>: <description>`.

Releases are automated with [Release Please](https://github.com/googleapis/release-please):
**don't edit `CHANGELOG.md` or bump the version by hand.** Release Please reads the
merged commit types, opens a release PR that updates the changelog and version, and
merging that PR tags the release; the publish then runs once a maintainer approves
the deployment.

Choose the type deliberately — `feat:` and `fix:` drive the version bump and
headline the release notes:

| Type | Effect |
| --- | --- |
| `feat:` | a user-facing feature — bumps the patch version (pre-1.0 policy) |
| `fix:` | a user-facing bug fix — bumps the patch version |
| `perf:`, `revert:` | appear in the release notes (no bump on their own) |
| `docs:`, `refactor:`, `chore:`, `build:`, `ci:`, `test:`, `style:` | hidden from the release notes |

Anything that isn't a user-facing feature or fix should avoid `feat:`/`fix:` so it
stays out of the headline sections.

## Reporting issues

Found a bug or have a feature request? Please open an issue on the [GitHub issue tracker](https://github.com/meridianlabs-ai/inspect_viz/issues).
