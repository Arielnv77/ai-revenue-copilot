"""Tests for anomaly detector module."""

import pytest
import pandas as pd
import numpy as np
from src.models.anomaly_detector import RevenueAnomalyDetector, detect_revenue_anomalies


class TestRevenueAnomalyDetector:

    def test_fit_predict(self):
        """Test basic fit and predict."""
        np.random.seed(42)
        df = pd.DataFrame({
            "revenue_sum": np.random.normal(1000, 100, 100),
            "transaction_count": np.random.randint(10, 100, 100),
        })
        # Add some anomalies
        df.loc[5, "revenue_sum"] = 5000
        df.loc[50, "revenue_sum"] = 50

        detector = RevenueAnomalyDetector(contamination=0.05)
        detector.fit(df)
        result = detector.predict(df)

        assert "is_anomaly" in result.columns
        assert "anomaly_score" in result.columns
        assert result["is_anomaly"].sum() > 0

    def test_not_fitted_error(self):
        """Test error when predicting without fitting."""
        detector = RevenueAnomalyDetector()
        df = pd.DataFrame({"a": [1, 2, 3]})
        with pytest.raises(RuntimeError):
            detector.predict(df)

    def test_evaluate_after_predict(self):
        """Test metrics available after prediction."""
        df = pd.DataFrame({"revenue": np.random.normal(100, 10, 50)})
        detector = RevenueAnomalyDetector()
        detector.fit(df)
        detector.predict(df)
        metrics = detector.evaluate()
        assert "n_anomalies" in metrics
        assert "anomaly_pct" in metrics


class TestDetectRevenueAnomalies:

    def test_convenience_function(self):
        """Test the convenience function."""
        np.random.seed(42)
        df = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=100),
            "revenue_sum": np.random.normal(1000, 100, 100),
        })
        result = detect_revenue_anomalies(df)
        assert "is_anomaly" in result.columns
