# Contributing to Inspect Viz

Thanks for your interest in contributing to Inspect Viz, a data visualization library for Inspect AI evaluations.

## Development setup

Inspect Viz targets Python 3.11+ and needs [uv](https://docs.astral.sh/uv/) 0.13.4 or later. Clone the repository and install it in editable mode with the `dev` optional dependencies:

```bash
git clone https://github.com/meridianlabs-ai/inspect_viz
cd inspect_viz
uv sync --extra dev
```

`uv sync` creates `.venv` with the exact versions in `uv.lock`, the `dev` extra included, and installs Inspect Viz editable. Run Python commands from it: `uv run <command>`, `.venv/bin/<command>`, or `source .venv/bin/activate`. `uv sync` without `--extra dev` removes the dev tools again. To also install the `doc` extra, run `uv sync --extra dev --extra doc`.

The front-end widgets are built with TypeScript. To work on them, install the JS dependencies with yarn:

```bash
yarn install
```

While developing front-end components, run the following in a separate terminal to automatically rebuild the JavaScript as you make changes:

```bash
yarn dev          # or
yarn dev-sourcemap
```

### Dependencies and the cooldown

`uv.lock` pins every Python dependency except the build toolchain. CI's lint, type-check, test and build jobs install their dependencies from it, and fail when `uv.lock` is out of date with `pyproject.toml`. CI's build job and the release build use the build toolchain (build, hatchling, hatch-vcs) pinned with hashes in `scripts/build-dist/requirements.txt`. For the editable install in the other jobs and on your machine, uv gets hatchling and hatch-vcs from PyPI with the same cooldown. Dependabot updates that file weekly, and `.github/workflows/publish.yaml` gives the command to update it by hand. When you change dependencies in `pyproject.toml`, run `uv lock` and commit both files. When you change the `hatchling` requirement in `[build-system]`, make the same change in `scripts/build-dist/requirements.in` and compile `requirements.txt` again.

`pyproject.toml` sets `exclude-newer = "7 days"` under `[tool.uv]`, so `uv lock`, `uv sync` and `uv pip` only pick releases that have been on PyPI for at least seven days. A compromised release is usually found and removed within that time, before it reaches `uv.lock`, CI or your machine. A direct dependency (a package in `dependencies` or the `dev` extra in `pyproject.toml`) that is a model provider SDK or an Inspect package can wait 6 hours instead, with a `"6 hours"` entry in `[tool.uv.exclude-newer-package]`. No current dependency is one of these, so every package keeps the seven-day cooldown. Dependabot's `uv` entry in `.github/dependabot.yml` repeats the cooldown. When you add a `"6 hours"` entry, also add the package to `cooldown.exclude` there and to a `six-hour-cooldown` group listed before `python-packages`. `tests/test_dependency_cooldown.py` checks that each entry is a direct dependency, that dated entries (below) are less than seven days old, and that the two files match. Whether a package is a provider SDK or an Inspect package is up to review.

Dependabot proposes `uv.lock` updates daily, once a release has cleared its cooldown. To adopt a release sooner, run `uv lock --upgrade-package <package>` and commit `uv.lock`. A release still inside its cooldown can't be locked; wait for it rather than overriding `exclude-newer`, unless it's an emergency (below).

In an emergency, for example a security fix, you can adopt a release that is less than seven days old with a one-time dated entry:

1. Under `[tool.uv.exclude-newer-package]` in `pyproject.toml` (add the table if it is not there), add `<package> = "<timestamp>"`. The package must be a direct dependency. Use an RFC 3339 timestamp just after the upload time of the fixed release. Don't add a dated entry to `.github/dependabot.yml`.
2. Run `uv lock --upgrade-package <package>` and commit both files.
3. Within seven days, once the normal cooldown includes the release, delete the entry, run `uv lock --upgrade-package <package>`, and commit both files. A plain `uv lock` doesn't reliably remove the entry from `uv.lock`, and CI then fails. A test fails when a dated entry is seven days old or older.

Testing against the newest releases of the runtime and `dev` dependencies happens in the nightly canary in [meridianlabs-ai/canaries](https://github.com/meridianlabs-ai/canaries), so Inspect Viz's own CI doesn't need to.

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
