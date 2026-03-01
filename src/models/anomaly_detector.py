"""
Anomaly Detector — Detect revenue anomalies using Isolation Forest.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from src.models.base import BaseModel

logger = logging.getLogger(__name__)


class RevenueAnomalyDetector(BaseModel):
    """
    Detect anomalous revenue periods using Isolation Forest.

    Works on aggregated time-series data to flag unusual spikes or drops.
    """

    def __init__(
        self,
        contamination: float = 0.05,
        n_estimators: int = 100,
        random_state: int = 42,
    ):
        super().__init__(name="RevenueAnomalyDetector")
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        self._model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=random_state,
        )
        self._feature_columns: list[str] = []

    def fit(self, data: pd.DataFrame, **kwargs) -> "RevenueAnomalyDetector":
        """
        Fit the Isolation Forest model.

        Args:
            data: DataFrame with numeric columns to use as features.
                  Typically: revenue_sum, revenue_mean, transaction_count.
        """
        features = self._prepare_features(data)
        self._model.fit(features)
        self._is_fitted = True
        logger.info(f"Anomaly detector fitted on {len(data)} samples, {features.shape[1]} features")
        return self

    def predict(self, data: Optional[pd.DataFrame] = None, **kwargs) -> pd.DataFrame:
        """
        Detect anomalies in the data.

        Returns:
            DataFrame with original data + anomaly_score + is_anomaly columns.
        """
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before predicting")

        features = self._prepare_features(data)

        # Isolation Forest: -1 = anomaly, 1 = normal
        predictions = self._model.predict(features)
        scores = self._model.decision_function(features)

        result = data.copy()
        result["anomaly_score"] = scores
        result["is_anomaly"] = predictions == -1

        n_anomalies = result["is_anomaly"].sum()
        logger.info(f"Detected {n_anomalies} anomalies ({n_anomalies/len(data)*100:.1f}%)")

        self._metrics = {
            "total_samples": len(data),
            "n_anomalies": int(n_anomalies),
            "anomaly_pct": round(n_anomalies / len(data) * 100, 2),
        }

        return result

    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Select and prepare numeric features for the model."""
        numeric_cols = data.select_dtypes(include=["number"]).columns.tolist()

        # Exclude internal columns
        exclude = {"anomaly_score", "is_anomaly"}
        feature_cols = [c for c in numeric_cols if c not in exclude]

        if not feature_cols:
            raise ValueError("No numeric columns found for anomaly detection")

        self._feature_columns = feature_cols
        features = data[feature_cols].fillna(0).values
        return features


def detect_revenue_anomalies(
    df: pd.DataFrame,
    date_col: str = "date",
    value_col: str = "revenue_sum",
    contamination: float = 0.05,
) -> pd.DataFrame:
    """
    Convenience function: detect anomalies on a time-series revenue DataFrame.

    Args:
        df: DataFrame with date and revenue columns.
        date_col: Date column name.
        value_col: Revenue column name.
        contamination: Expected proportion of anomalies.

    Returns:
        DataFrame with anomaly_score and is_anomaly columns added.
    """
    detector = RevenueAnomalyDetector(contamination=contamination)

    # Add derived features for better detection
    features_df = df.copy()
    if value_col in features_df.columns:
        features_df["rolling_mean_7"] = features_df[value_col].rolling(7, min_periods=1).mean()
        features_df["rolling_std_7"] = features_df[value_col].rolling(7, min_periods=1).std().fillna(0)
        features_df["pct_change"] = features_df[value_col].pct_change().fillna(0)

    detector.fit(features_df.select_dtypes(include=["number"]))
    result = detector.predict(features_df)

    # Restore the date column
    if date_col in df.columns:
        result[date_col] = df[date_col].values

    return result
