from typing import Literal, Union

import pandas as pd
import pytest
from inspect_viz.view import scores_radar_by_metric_df, scores_radar_by_task_df


@pytest.fixture
def metric_evals_df() -> pd.DataFrame:
    """Sample data for testing scores_radar_by_metric_df."""
    return pd.DataFrame(
        {
            "model": ["model1", "model2"],
            "task_id": ["1", "1"],
            "task_name": ["task1", "task1"],
            "log": ["path1", "path2"],
            "score_myscorer_metric": [1, 2],
        }
    )


@pytest.fixture
def task_evals_df() -> pd.DataFrame:
    """Sample data for testing scores_radar_by_task_df."""
    return pd.DataFrame(
        {
            "model": ["model1", "model2"],
            "task_id": ["1", "1"],
            "task_name": ["task1", "task1"],
            "log": ["path1", "path2"],
            "score_headline_name": ["myscorer", "myscorer"],
            "score_headline_metric": ["metric", "metric"],
            "score_headline_value": [1, 2],
        }
    )


def test_scores_radar_by_metric_df(metric_evals_df: pd.DataFrame) -> None:
    result = scores_radar_by_metric_df(metric_evals_df, "myscorer")
    expected = _create_expected_df(
        scaled_values=[1.0, 1.0, 2.0, 2.0],
        x_values=[1.0, 1.0, 2.0, 2.0],
    )
    _assert_df_equal(result, expected)


def test_scores_radar_by_task_df(task_evals_df: pd.DataFrame) -> None:
    result = scores_radar_by_task_df(task_evals_df)
    expected = _create_expected_df(
        scaled_values=[1.0, 1.0, 2.0, 2.0],
        x_values=[1.0, 1.0, 2.0, 2.0],
    )
    _assert_df_equal(result, expected)


def test_scores_radar_by_metric_df_invert(metric_evals_df: pd.DataFrame) -> None:
    """Test scores_radar_by_metric_df with invert functionality."""
    result = scores_radar_by_metric_df(
        metric_evals_df,
        scorer="myscorer",
        invert=["metric"],
    )
    expected = _create_expected_df(
        scaled_values=[1.0, 1.0, 0.0, 0.0],
        x_values=[1.0, 1.0, 0.0, 0.0],
    )
    _assert_df_equal(result, expected)


@pytest.mark.parametrize(
    "normalization,expected_scaled,expected_x",
    [
        ("percentile", [0.5, 0.5, 1.0, 1.0], [0.5, 0.5, 1.0, 1.0]),
        ("min_max", [0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]),
        ("absolute", [1.0, 1.0, 2.0, 2.0], [1.0, 1.0, 2.0, 2.0]),
    ],
)
def test_scores_radar_by_metric_df_normalization(
    metric_evals_df: pd.DataFrame,
    normalization: Literal["percentile", "min_max", "absolute"],
    expected_scaled: list[float],
    expected_x: list[float],
) -> None:
    """Test scores_radar_by_metric_df with different normalizations."""
    result = scores_radar_by_metric_df(
        metric_evals_df, scorer="myscorer", normalization=normalization
    )
    expected = _create_expected_df(
        scaled_values=expected_scaled,
        x_values=expected_x,
    )
    _assert_df_equal(result, expected)


def test_scores_radar_by_task_df_invert(task_evals_df: pd.DataFrame) -> None:
    """Test scores_radar_by_task_df with invert functionality."""
    result = scores_radar_by_task_df(
        task_evals_df,
        invert=["metric"],
    )
    expected = _create_expected_df(
        scaled_values=[1.0, 1.0, 0.0, 0.0],
        x_values=[1.0, 1.0, 0.0, 0.0],
    )
    _assert_df_equal(result, expected)


@pytest.mark.parametrize(
    "normalization,expected_scaled,expected_x",
    [
        ("percentile", [0.5, 0.5, 1.0, 1.0], [0.5, 0.5, 1.0, 1.0]),
        ("min_max", [0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 1.0]),
        ("absolute", [1.0, 1.0, 2.0, 2.0], [1.0, 1.0, 2.0, 2.0]),
    ],
)
def test_scores_radar_by_task_df_normalization(
    task_evals_df: pd.DataFrame,
    normalization: Literal["percentile", "min_max", "absolute"],
    expected_scaled: list[float],
    expected_x: list[float],
) -> None:
    """Test scores_radar_by_task_df with different normalizations."""
    result = scores_radar_by_task_df(task_evals_df, normalization=normalization)
    expected = _create_expected_df(
        scaled_values=expected_scaled,
        x_values=expected_x,
    )
    _assert_df_equal(result, expected)


def _create_expected_df(
    scaled_values: list[float],
    x_values: list[float],
    values: list[Union[int, float]] | None = None,
    y_values: list[float] | None = None,
    task_id: str = "1",
    task_name: str = "task1",
    model1: str = "model1",
    model2: str = "model2",
    log1: str = "path1",
    log2: str = "path2",
    metric: str = "metric",
    scorer: str = "myscorer",
) -> pd.DataFrame:
    if values is None:
        values = [1.0, 1.0, 2.0, 2.0]
    if y_values is None:
        y_values = [0.0, 0.0, 0.0, 0.0]

    return pd.DataFrame(
        {
            "task_id": [task_id] * len(values),
            "task_name": [task_name] * len(values),
            "model": [model1, model1, model2, model2],
            "log": [log1, log1, log2, log2],
            "metric": [metric] * len(values),
            "scorer": [scorer] * len(values),
            "value": values,
            "value_scaled": scaled_values,
            "x": x_values,
            "y": y_values,
        }
    )


def _assert_df_equal(
    result_df: pd.DataFrame,
    expected_df: pd.DataFrame,
    rtol: float = 1e-10,
    atol: float = 1e-10,
) -> None:
    pd.testing.assert_frame_equal(
        result_df,
        expected_df,
        rtol=rtol,
        atol=atol,
    )
