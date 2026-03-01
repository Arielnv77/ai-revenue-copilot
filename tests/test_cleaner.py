"""Tests for preprocessing cleaner module."""

import pytest
import pandas as pd
import numpy as np
from src.preprocessing.cleaner import (
    remove_duplicates,
    handle_missing_values,
    cap_outliers,
    clean_column_names,
    drop_constant_columns,
    run_cleaning_pipeline,
)


class TestRemoveDuplicates:

    def test_removes_duplicates(self):
        df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
        result = remove_duplicates(df)
        assert len(result) == 2

    def test_no_duplicates(self):
        df = pd.DataFrame({"a": [1, 2, 3]})
        result = remove_duplicates(df)
        assert len(result) == 3


class TestHandleMissing:

    def test_auto_strategy(self):
        df = pd.DataFrame({"a": [1.0, np.nan, 3.0], "b": ["x", None, "z"]})
        result = handle_missing_values(df, strategy="auto")
        assert result["a"].isnull().sum() == 0
        assert result["b"].isnull().sum() == 0

    def test_drop_strategy(self):
        df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
        result = handle_missing_values(df, strategy="drop")
        assert len(result) == 2

    def test_fill_strategy(self):
        df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
        result = handle_missing_values(df, strategy="fill", fill_value=0)
        assert result["a"].iloc[1] == 0


class TestCapOutliers:

    def test_caps_outliers(self):
        df = pd.DataFrame({"a": [1, 2, 3, 4, 5, 100]})
        result = cap_outliers(df, columns=["a"])
        assert result["a"].max() < 100


class TestCleanColumnNames:

    def test_standardizes_names(self):
        df = pd.DataFrame({"First Name": [1], "Last  Name!": [2]})
        result = clean_column_names(df)
        assert "first_name" in result.columns
        assert "last_name" in result.columns


class TestCleaningPipeline:

    def test_full_pipeline(self, sample_sales_df):
        result = run_cleaning_pipeline(sample_sales_df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        # Column names should be lowercase
        for col in result.columns:
            assert col == col.lower()
