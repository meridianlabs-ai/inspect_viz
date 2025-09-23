import pandas as pd
from inspect_viz.view.beta import scores_radar_df


def test_scores_radar_df() -> None:
    # row 3 is expected to be ignored as scores_radar_df processes the first row per model
    evals_df = pd.DataFrame(
        {
            "model": ["model1", "model2", "model1"],
            "task_id": ["task1", "task2", "task3"],
            "log": ["path1", "path2", "path3"],
            "score_myscorer_mymetric1": [1, 2, 3],
            "score_myscorer_mymetric2": [2, 1, 3],
        }
    )

    result = scores_radar_df(evals_df, "myscorer")

    # expected coordinates:
    # model1: ranks [0.5, 1.0] -> x=[0.5*1, 1.0*(-1), 0.5*1]=[0.5, -1, 0.5], y=[0.5*0, 1.0*0, 0.5*0]=[0, 0, 0]
    # model2: ranks [1.0, 0.5] -> x=[1.0*1, 0.5*(-1), 1.0*1]=[1, -0.5, 1], y=[1.0*0, 0.5*0, 1.0*0]=[0, 0, 0]
    expected_df = pd.DataFrame(
        {
            "task_id": ["task1", "task1", "task1", "task2", "task2", "task2"],
            "model": ["model1", "model1", "model1", "model2", "model2", "model2"],
            "log": ["path1", "path1", "path1", "path2", "path2", "path2"],
            "metric": [
                "mymetric1",
                "mymetric2",
                "mymetric1",
                "mymetric1",
                "mymetric2",
                "mymetric1",
            ],
            "value": [1.0, 2.0, 1.0, 2.0, 1.0, 2.0],
            "x": [0.5, -1, 0.5, 1, -0.5, 1],
            "y": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        }
    )

    # compare DataFrames with tolerance for floating point precision
    pd.testing.assert_frame_equal(
        result, expected_df, check_exact=False, rtol=1e-10, atol=1e-10
    )
