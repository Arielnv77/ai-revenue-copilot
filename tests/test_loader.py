"""Tests for data loader module."""

import pytest
import pandas as pd
from src.data.loader import load_csv, get_dataframe_profile, detect_encoding


class TestLoadCSV:
    """Test CSV loading functionality."""

    def test_load_csv_from_path(self, sample_csv_path):
        """Test loading a CSV from a file path."""
        df = load_csv(sample_csv_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_load_csv_shape(self, sample_csv_path):
        """Test correct shape after loading."""
        df = load_csv(sample_csv_path)
        assert df.shape[0] == 500
        assert df.shape[1] >= 7

    def test_load_csv_sample_rows(self, sample_csv_path):
        """Test loading only a sample of rows."""
        df = load_csv(sample_csv_path, sample_rows=10)
        assert len(df) == 10

    def test_load_csv_file_not_found(self):
        """Test error on missing file."""
        with pytest.raises(FileNotFoundError):
            load_csv("/nonexistent/file.csv")

    def test_load_csv_wrong_extension(self, tmp_path):
        """Test error on wrong file extension."""
        wrong_file = tmp_path / "test.txt"
        wrong_file.write_text("hello")
        with pytest.raises(ValueError, match="Expected a .csv file"):
            load_csv(wrong_file)


class TestDetectEncoding:
    """Test encoding detection."""

    def test_detect_encoding(self, sample_csv_path):
        """Test encoding is detected as a string."""
        encoding = detect_encoding(sample_csv_path)
        assert isinstance(encoding, str)
        assert len(encoding) > 0


class TestGetProfile:
    """Test DataFrame profiling."""

    def test_profile_keys(self, sample_sales_df):
        """Test that profile contains expected keys."""
        profile = get_dataframe_profile(sample_sales_df)
        assert "rows" in profile
        assert "columns" in profile
        assert "memory_mb" in profile
        assert "dtypes" in profile
        assert "column_names" in profile

    def test_profile_values(self, sample_sales_df):
        """Test profile values are correct."""
        profile = get_dataframe_profile(sample_sales_df)
        assert profile["rows"] == 500
        assert profile["columns"] >= 7
