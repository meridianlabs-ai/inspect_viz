# Contributing to Inspect Viz

Thanks for your interest in contributing to Inspect Viz, a data visualization library for Inspect AI evaluations.

## Development setup

Inspect Viz targets Python 3.10+. Clone the repository and install it in editable mode with the `dev` optional dependencies:

```bash
git clone https://github.com/meridianlabs-ai/inspect_viz
cd inspect_viz
pip install -e ".[dev]"
```

The front-end widgets are built with TypeScript. To work on them, install the JS dependencies with yarn:

```bash
yarn install
```

While developing front-end components, run the following in a separate terminal to automatically rebuild the JavaScript as you make changes:

```bash
yarn dev          # or
yarn dev-sourcemap
```

## Checks and tests

Run linting, formatting, and type checking with:

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
