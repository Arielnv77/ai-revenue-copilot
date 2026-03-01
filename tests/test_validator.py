"""Tests for data validator module."""

import pytest
import pandas as pd
import numpy as np
from src.data.validator import validate_dataframe, QualityReport


class TestValidateDataframe:
    """Test data validation and quality report generation."""

    def test_basic_validation(self, sample_sales_df):
        """Test basic validation produces a QualityReport."""
        report = validate_dataframe(sample_sales_df)
        assert isinstance(report, QualityReport)
        assert report.total_rows == 500
        assert report.total_columns >= 7

    def test_quality_score_range(self, sample_sales_df):
        """Test quality score is between 0 and 100."""
        report = validate_dataframe(sample_sales_df)
        assert 0 <= report.quality_score <= 100

    def test_no_missing_clean_data(self, sample_sales_df):
        """Test no missing values in clean sample data."""
        report = validate_dataframe(sample_sales_df)
        assert len(report.missing_values) == 0

    def test_detects_missing_values(self):
        """Test detection of missing values."""
        df = pd.DataFrame({
            "a": [1, 2, None, 4],
            "b": ["x", None, "z", None],
        })
        report = validate_dataframe(df, min_rows=1)
        assert "a" in report.missing_values
        assert "b" in report.missing_values

    def test_detects_duplicates(self):
        """Test detection of duplicate rows."""
        df = pd.DataFrame({
            "a": [1, 1, 2, 2],
            "b": ["x", "x", "y", "y"],
        })
        report = validate_dataframe(df, min_rows=1)
        assert report.duplicate_rows == 2

    def test_detects_constant_columns(self):
        """Test detection of constant columns."""
        df = pd.DataFrame({
            "a": [1, 1, 1, 1],
            "b": [1, 2, 3, 4],
        })
        report = validate_dataframe(df, min_rows=1)
        assert "a" in report.constant_columns

    def test_min_rows_warning(self):
        """Test warning when dataset is too small."""
        df = pd.DataFrame({"a": [1, 2]})
        report = validate_dataframe(df, min_rows=10)
        assert any("only 2 rows" in w for w in report.warnings)

    def test_required_columns_warning(self):
        """Test warning when required columns are missing."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        report = validate_dataframe(df, required_columns=["a", "b"], min_rows=1)
        assert any("Missing required columns" in w for w in report.warnings)

    def test_to_dict(self, sample_sales_df):
        """Test serialization to dict."""
        report = validate_dataframe(sample_sales_df)
        d = report.to_dict()
        assert isinstance(d, dict)
        assert "quality_score" in d
