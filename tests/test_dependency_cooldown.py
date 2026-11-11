"""Tests for the dependency cooldown in pyproject.toml and the CI jobs around it.

pyproject.toml holds back releases younger than seven days. A model provider
SDK or Inspect package that is a direct dependency can get six hours instead;
no package has that entry now. Dependabot applies the seven days to its
uv.lock bumps and leaves the six-hour list to uv. CI installs from uv.lock,
and the build toolchain from scripts/build-dist/requirements.txt, pinned with
hashes. The JS jobs install pnpm-lock.yaml. pnpm resolves only releases at
least seven days old, and Dependabot bumps the lock with the same cooldown.
Testing against the newest releases happens in
meridianlabs-ai/canaries, outside this repository.
"""

import pathlib
import re
import tomllib
from datetime import UTC, datetime, timedelta
from typing import Any, cast

import pytest
import yaml

REPO = pathlib.Path(__file__).parents[1]
GITHUB = REPO / ".github"
WORKFLOWS = GITHUB / "workflows"
SHARED_ACTIONS = "meridianlabs-ai/actions/"
SHARED_INSTALLERS = ("setup-uv@", "install-python-dependencies@")
EXEMPT_COOLDOWN = "6 hours"
BUILD_REQUIREMENTS = "scripts/build-dist/requirements.txt"
SHARED_BUILD = SHARED_ACTIONS + ".github/workflows/build-python-dist.yml@"
PUBLISH_STEPS = ("actions/download-artifact@", "pypa/gh-action-pypi-publish@")
DOWNLOAD_INPUTS = {
    "artifact-ids": "${{ needs.build.outputs.artifact-id }}",
    "path": "dist/",
}


def uv_config() -> dict[str, Any]:
    config: dict[str, Any] = tomllib.loads((REPO / "pyproject.toml").read_text())[
        "tool"
    ]["uv"]
    config.setdefault("exclude-newer-package", {})
    return config


def normalize(package: str) -> str:
    return re.sub(r"[-_.]+", "-", package).lower()


def direct_dependencies() -> set[str]:
    """Packages in the pyproject.toml `dependencies` or the `dev` extra."""
    project = tomllib.loads((REPO / "pyproject.toml").read_text())["project"]
    requirements = project["dependencies"] + project["optional-dependencies"]["dev"]
    return {
        normalize(re.split(r"[^A-Za-z0-9._-]", requirement, maxsplit=1)[0])
        for requirement in requirements
    }


def exempt_packages(config: dict[str, Any]) -> list[str]:
    return sorted(
        package
        for package, cooldown in config["exclude-newer-package"].items()
        if cooldown == EXEMPT_COOLDOWN
    )


def dependabot_uv() -> dict[str, Any]:
    updates = yaml.safe_load((GITHUB / "dependabot.yml").read_text())["updates"]
    root = [
        u for u in updates if u["package-ecosystem"] == "uv" and u["directory"] == "/"
    ]
    assert len(root) == 1, "expected one uv entry for directory / in dependabot.yml"
    entry: dict[str, Any] = root[0]
    return entry


def jobs() -> list[tuple[str, dict[str, Any], Any]]:
    """Every job of every workflow, with its location and its permissions."""
    return [
        (
            f"{path.name}:{name}",
            job,
            job.get("permissions", workflow.get("permissions")),
        )
        for path in sorted([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])
        for workflow in [yaml.safe_load(path.read_text())]
        for name, job in workflow["jobs"].items()
    ]


def steps() -> list[tuple[str, dict[str, Any]]]:
    """Every step of every workflow, with its location."""
    return [(where, step) for where, job, _ in jobs() for step in job.get("steps", [])]


def run_lines() -> list[tuple[str, str]]:
    # Joins backslash continuations so a command's flags stay on one line.
    return [
        (where, line.strip())
        for where, step in steps()
        for line in step.get("run", "").replace("\\\n", " ").splitlines()
        if line.strip()
    ]


def verify_exclude_newer_package(
    config: dict[str, Any], direct: set[str], now: datetime
) -> None:
    assert config["exclude-newer"] == "7 days", config["exclude-newer"]
    # Each entry is "6 hours" or a dated entry younger than the cooldown.
    for package, cooldown in config["exclude-newer-package"].items():
        assert normalize(package) in direct, f"{package} is not a direct dependency"
        if cooldown != EXEMPT_COOLDOWN:
            age = now - datetime.fromisoformat(cooldown)
            assert timedelta(0) <= age < timedelta(days=7), (
                f'dated entry {package} = "{cooldown}" is in the future or stale'
            )


def test_exclude_newer_package_entries() -> None:
    verify_exclude_newer_package(uv_config(), direct_dependencies(), datetime.now(UTC))


def test_non_direct_entry_is_caught() -> None:
    config = uv_config()
    config["exclude-newer-package"]["certifi"] = EXEMPT_COOLDOWN
    with pytest.raises(AssertionError, match="not a direct dependency"):
        verify_exclude_newer_package(config, direct_dependencies(), datetime.now(UTC))


@pytest.mark.parametrize(
    "age,caught",
    [(timedelta(days=6), False), (timedelta(days=7), True), (-timedelta(days=1), True)],
    ids=["fresh", "stale", "future"],
)
def test_dated_entry_age(age: timedelta, caught: bool) -> None:
    config = uv_config()
    now = datetime.now(UTC)
    config["exclude-newer-package"]["pandas"] = (now - age).isoformat()
    if caught:
        with pytest.raises(AssertionError, match="dated entry"):
            verify_exclude_newer_package(config, direct_dependencies(), now)
    else:
        verify_exclude_newer_package(config, direct_dependencies(), now)


def test_dependabot_cooldown_matches_pyproject() -> None:
    dependabot = dependabot_uv()
    assert dependabot["cooldown"]["default-days"] == 7
    # Dependabot's cooldown counts whole days, so it leaves the "6 hours"
    # entries to uv. Dated entries are locked by hand.
    exempt = exempt_packages(uv_config())
    assert sorted(dependabot["cooldown"].get("exclude", [])) == exempt
    # The exempt packages, if any, have their own group, listed before the
    # catch-all.
    groups = dependabot["groups"]
    assert list(groups) == ["six-hour-cooldown"] * bool(exempt) + ["python-packages"]
    if exempt:
        assert sorted(groups["six-hour-cooldown"]["patterns"]) == exempt
    assert groups["python-packages"]["patterns"] == ["*"]


def test_python_comes_from_the_shared_actions() -> None:
    direct = [
        (where, step["uses"])
        for where, step in steps()
        if step.get("uses", "").startswith(
            ("astral-sh/setup-uv@", "actions/setup-python@")
        )
    ]
    assert direct == [], "use meridianlabs-ai/actions/install-python-dependencies"


def test_shared_actions_share_one_pinned_commit_and_pin_versions() -> None:
    # One commit for every shared action means one uv.
    shared = [
        (where, step)
        for where, step in steps()
        if step.get("uses", "").startswith(
            tuple(SHARED_ACTIONS + name for name in SHARED_INSTALLERS)
        )
    ]
    assert shared, "no workflow uses the shared install actions"
    refs = {step["uses"].split("@")[1].split()[0] for _, step in shared}
    assert len(refs) == 1, f"shared actions pin different commits: {refs}"
    assert re.fullmatch(r"[0-9a-f]{40}", refs.pop()), "pin a 40-character SHA"
    unlocked = [
        where
        for where, step in shared
        if "install-python-dependencies@" in step["uses"]
        and step["with"]["versions"] not in ("locked", "hashed-requirements")
    ]
    assert unlocked == [], f"use versions: locked or hashed-requirements in {unlocked}"


def test_jobs_that_can_write_use_no_cache() -> None:
    # A cache that a write-capable job restores could run code from a less
    # trusted run. Jobs without permissions get the read-only repo default.
    cached = [
        where
        for where, job, permissions in jobs()
        if permissions == "write-all"
        or "write" in (permissions.values() if isinstance(permissions, dict) else [])
        for step in job.get("steps", [])
        if step.get("uses", "").startswith(
            SHARED_ACTIONS + "install-python-dependencies@"
        )
        and step["with"].get("actions-cache") != "none"
    ]
    assert cached == [], f"use actions-cache: none in {cached}"


def test_ruff_comes_from_uv_lock() -> None:
    # ruff-action installs its own ruff, outside the shared action.
    ruff = [
        w for w, s in steps() if s.get("uses", "").startswith("astral-sh/ruff-action@")
    ]
    assert ruff == [], f"run ruff with uv run --no-sync in {ruff}"


def test_build_toolchain_is_hashed_wheels() -> None:
    hashed = [
        (where, step["with"])
        for where, step in steps()
        if step.get("uses", "").startswith(
            SHARED_ACTIONS + "install-python-dependencies@"
        )
        and step["with"]["versions"] == "hashed-requirements"
    ]
    assert hashed, "no workflow installs the hashed build toolchain"
    wrong = [
        where
        for where, inputs in hashed
        if inputs.get("package-format") != "wheels-only"
        or inputs.get("requirements-file") != BUILD_REQUIREMENTS
    ]
    assert wrong == [], f"use wheels-only and {BUILD_REQUIREMENTS} in {wrong}"


def test_builds_use_the_installed_toolchain() -> None:
    # An isolated build resolves its own build backend, outside the hashes.
    builds = [(w, line) for w, line in run_lines() if re.search(r"-m build\b", line)]
    assert builds, "no workflow builds the package"
    isolated = [(w, line) for w, line in builds if "--no-isolation" not in line.split()]
    assert isolated == [], f"build with --no-isolation in {isolated}"
    uv_build = [
        (w, line) for w, line in run_lines() if re.search(r"\buv build\b", line)
    ]
    assert uv_build == [], f"uv build resolves the build backend in {uv_build}"


def test_publish_jobs_only_upload_the_shared_build() -> None:
    """A job with `id-token: write` only downloads the dist and publishes it.

    The build runs in the shared workflow, in a job with no publishing
    credential. A job that calls a shared workflow, such as a docs deploy, has no
    steps here.
    """
    publishers = [
        (where, job)
        for where, job, permissions in jobs()
        if isinstance(permissions, dict)
        and cast(dict[str, str], permissions).get("id-token") == "write"
        and "uses" not in job
    ]
    assert publishers, "no job holds id-token: write"
    wrong = [
        where
        for where, job in publishers
        if len(job["steps"]) != len(PUBLISH_STEPS)
        or not all(
            step.get("uses", "").startswith(prefix)
            for step, prefix in zip(job["steps"], PUBLISH_STEPS, strict=True)
        )
    ]
    assert wrong == [], f"only download the dist and publish it in {wrong}"
    unlinked = [
        where
        for where, job in publishers
        for needs in [job.get("needs", [])]
        if "build" not in ([needs] if isinstance(needs, str) else needs)
        or job["steps"][0].get("with") != DOWNLOAD_INPUTS
    ]
    assert unlinked == [], f"download only the shared build artifact in {unlinked}"
    build = yaml.safe_load((WORKFLOWS / "publish.yaml").read_text())["jobs"]["build"]
    assert build["uses"].startswith(SHARED_BUILD), build["uses"]
    ref = build["uses"].split("@")[1].split()[0]
    assert re.fullmatch(r"[0-9a-f]{40}", ref), "pin a 40-character SHA"


def test_build_toolchain_matches_build_system() -> None:
    def hatchling(requirements: list[str]) -> str:
        [requirement] = [
            r for r in requirements if normalize(r).startswith("hatchling")
        ]
        return requirement

    pinned = (REPO / "scripts/build-dist/requirements.in").read_text().splitlines()
    build_system = tomllib.loads((REPO / "pyproject.toml").read_text())["build-system"]
    assert hatchling(pinned) == hatchling(build_system["requires"])


# pip installs skip uv.lock; installs go through the shared action.
def test_no_workflow_runs_pip_install() -> None:
    pip = [
        (where, line)
        for where, line in run_lines()
        if re.search(r"\bpip3? install\b", line)
    ]
    assert pip == [], "pip installs skip uv.lock; use the shared action"


def pnpm_installs(line: str) -> list[list[str]]:
    """The pnpm install commands in a run line, each as the words after pnpm."""
    line = re.sub(r"(^|\s)#.*", "", line)
    installs = []
    for command in re.split(r"&&|\|\||;|\|", line):
        words = command.split()
        if "pnpm" in words:
            args = words[words.index("pnpm") + 1 :]
            if {"install", "i"} & set(args):
                installs.append(args)
    return installs


def frozen(args: list[str]) -> bool:
    return "--frozen-lockfile" in args


def test_pnpm_installs_use_the_lockfile() -> None:
    # pnpm turns on --frozen-lockfile when it detects CI. Passing the flag
    # keeps that from depending on the detection.
    installs = [
        (where, line, args)
        for where, line in run_lines()
        for args in pnpm_installs(line)
    ]
    assert installs, "no workflow installs the JS dependencies"
    unlocked = [(where, line) for where, line, args in installs if not frozen(args)]
    assert unlocked == [], f"use pnpm install --frozen-lockfile in {unlocked}"


# npm and yarn ignore pnpm-lock.yaml and minimumReleaseAge.
def test_no_workflow_runs_npm_or_yarn() -> None:
    other = [
        (where, line)
        for where, line in run_lines()
        if re.search(r"\b(yarn|npx|npm\s+(install|i|ci|add|update))\b", line)
    ]
    assert other == [], "install the JS dependencies with pnpm"


@pytest.mark.parametrize(
    "line,locked",
    [
        ("pnpm install", [False]),
        ("pnpm i", [False]),
        ("pnpm install --frozen-lockfile", [True]),
        ("pnpm --frozen-lockfile install", [True]),
        ("pnpm install --frozen-lockfile=false", [False]),
        ("pnpm install --prefer-offline", [False]),
        ("pnpm install # deps", [False]),
        ("pnpm install --frozen-lockfile && pnpm build", [True]),
        ("pnpm install && pnpm build", [False]),
        ("cd js && pnpm --dir js install", [False]),
        ("pnpm build", []),
        ("pnpm typecheck", []),
    ],
)
def test_pnpm_install_detection(line: str, locked: list[bool]) -> None:
    assert [frozen(args) for args in pnpm_installs(line)] == locked


def test_pnpm_minimum_release_age() -> None:
    workspace = yaml.safe_load((REPO / "pnpm-workspace.yaml").read_text())
    assert workspace["minimumReleaseAge"] == 7 * 24 * 60
    assert "minimumReleaseAgeExclude" not in workspace


def test_dependabot_npm_cooldown() -> None:
    updates = yaml.safe_load((GITHUB / "dependabot.yml").read_text())["updates"]
    [npm] = [u for u in updates if u["package-ecosystem"] == "npm"]
    assert npm["directory"] == "/"
    assert npm["versioning-strategy"] == "lockfile-only"
    assert npm["cooldown"]["default-days"] == 7


def test_no_workflow_opts_out_of_the_cooldown() -> None:
    floating = [
        (where, line)
        for where, line in run_lines()
        if re.search(r"--exclude-newer(=|\s+)false", line)
    ]
    assert floating == []
