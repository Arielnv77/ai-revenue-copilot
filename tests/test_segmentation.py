"""Tests for segmentation module."""

import pytest
import pandas as pd
import numpy as np
from src.models.segmentation import CustomerSegmenter


class TestCustomerSegmenter:

    def test_fit_predict(self, sample_rfm_df):
        """Test basic fit and predict."""
        segmenter = CustomerSegmenter(n_clusters=3)
        segmenter.fit(sample_rfm_df)
        result = segmenter.predict(sample_rfm_df)

        assert "segment_id" in result.columns
        assert "segment_label" in result.columns
        assert result["segment_id"].nunique() == 3

    def test_profiles(self, sample_rfm_df):
        """Test cluster profiles generation."""
        segmenter = CustomerSegmenter(n_clusters=3)
        segmenter.fit(sample_rfm_df)
        segmenter.predict(sample_rfm_df)

        profiles = segmenter.get_profiles()
        assert profiles is not None
        assert len(profiles) == 3
        assert "avg_monetary" in profiles.columns

    def test_not_fitted_error(self, sample_rfm_df):
        """Test error when predicting without fitting."""
        segmenter = CustomerSegmenter()
        with pytest.raises(RuntimeError):
            segmenter.predict(sample_rfm_df)

    def test_find_optimal_k(self, sample_rfm_df):
        """Test elbow method for optimal k."""
        segmenter = CustomerSegmenter()
        results = segmenter.find_optimal_k(sample_rfm_df, k_range=range(2, 5))
        assert len(results) == 3
        assert all(v > 0 for v in results.values())

    def test_evaluate_metrics(self, sample_rfm_df):
        """Test metrics after prediction."""
        segmenter = CustomerSegmenter(n_clusters=4)
        segmenter.fit(sample_rfm_df)
        segmenter.predict(sample_rfm_df)
        metrics = segmenter.evaluate()
        assert "n_clusters" in metrics
        assert "inertia" in metrics
