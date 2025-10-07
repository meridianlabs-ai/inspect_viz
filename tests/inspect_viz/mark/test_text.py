import pandas as pd
from inspect_viz import Data
from inspect_viz.mark._text import resolve_text_inputs
from inspect_viz.transform._aggregate import first
from inspect_viz.transform._transform import Transform


class TestResolveTextInputs:
    """Test suite for the resolve_text_inputs function."""

    def test_with_data_and_all_columns_exist(self) -> None:
        """Test when data is provided and all columns exist in the data."""
        df = pd.DataFrame(
            {"x": [1, 2, 3], "y": [4, 5, 6], "z": [7, 8, 9], "text": ["a", "b", "c"]}
        )
        data = Data.from_dataframe(df)

        result_data, x_col, y_col, z_col, text_col = resolve_text_inputs(
            data, "x", "y", "z", "text"
        )

        assert result_data is data
        assert x_col == "x"
        assert y_col == "y"
        assert z_col == "z"
        assert text_col == "text"

    def test_with_data_and_some_columns_missing(self) -> None:
        """Test when data is provided but some columns don't exist."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        data = Data.from_dataframe(df)

        result_data, x_col, y_col, z_col, text_col = resolve_text_inputs(
            data, "x", "y", "z", "text"
        )

        assert result_data is data
        assert x_col == "x"
        assert y_col == "y"
        assert z_col is None  # column doesn't exist
        assert text_col is None  # column doesn't exist

    def test_with_data_and_none_parameters(self) -> None:
        """Test when data is provided but some parameters are None."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        data = Data.from_dataframe(df)

        result_data, x_col, y_col, z_col, text_col = resolve_text_inputs(
            data, "x", None, None, None
        )

        assert result_data is data
        assert x_col == "x"
        assert y_col is None  # None stays None
        assert z_col is None
        assert text_col is None

    def test_with_none_data_creates_data_from_sequences(self) -> None:
        """Test when data is None, it creates data from provided sequences."""
        x_seq = [1, 2, 3]
        y_seq = [4, 5, 6]
        z_seq = [7, 8, 9]
        text_seq = ["a", "b", "c"]

        result_data, x_col, y_col, z_col, text_col = resolve_text_inputs(
            None, x_seq, y_seq, z_seq, text_seq
        )

        assert result_data is not None
        assert "x" in result_data.columns
        assert "y" in result_data.columns
        assert "z" in result_data.columns
        assert "text" in result_data.columns
        assert x_col == "x"
        assert y_col == "y"
        assert z_col == "z"
        assert text_col == "text"

    def test_with_none_data_and_partial_sequences(self) -> None:
        """Test when data is None with only some sequences provided."""
        x_seq = [1, 2, 3]
        y_seq = [4, 5, 6]

        result_data, x_col, y_col, z_col, text_col = resolve_text_inputs(
            None, x_seq, y_seq, None, None
        )

        assert result_data is not None
        assert "x" in result_data.columns
        assert "y" in result_data.columns
        assert x_col == "x"
        assert y_col == "y"
        assert z_col is None
        assert text_col is None

    def test_with_dict_channel_spec(self) -> None:
        """Test when text parameter is a dictionary (ChannelWithScale/ChannelWithInterval)."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "limit": ["A", "B", "C"]})
        data = Data.from_dataframe(df)

        text_dict: Transform = first("limit")

        result_data, x_col, y_col, z_col, text_col = resolve_text_inputs(
            data, "x", "y", None, text_dict
        )

        assert result_data is data
        assert x_col == "x"
        assert y_col == "y"
        assert z_col is None
        # Transform should be returned as-is (not converted to column name)
        assert text_col is text_dict
