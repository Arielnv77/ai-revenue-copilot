"""
Segmentation — Customer segmentation using RFM + KMeans clustering.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.models.base import BaseModel
from src.utils.constants import RFM_SEGMENTS

logger = logging.getLogger(__name__)


class CustomerSegmenter(BaseModel):
    """
    Customer segmentation using KMeans clustering on RFM features.

    Takes an RFM DataFrame (output of compute_rfm) and clusters customers
    into meaningful segments.
    """

    def __init__(
        self,
        n_clusters: int = 4,
        random_state: int = 42,
        max_iter: int = 300,
    ):
        super().__init__(name="CustomerSegmenter")
        self.n_clusters = n_clusters
        self.random_state = random_state
        self._model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            max_iter=max_iter,
            n_init=10,
        )
        self._scaler = StandardScaler()
        self._cluster_profiles: Optional[pd.DataFrame] = None

    def fit(self, data: pd.DataFrame, **kwargs) -> "CustomerSegmenter":
        """
        Fit KMeans on RFM data.

        Args:
            data: DataFrame with recency, frequency, monetary columns.
        """
        features = self._get_features(data)
        scaled = self._scaler.fit_transform(features)
        self._model.fit(scaled)
        self._is_fitted = True
        logger.info(f"KMeans fitted: {self.n_clusters} clusters on {len(data)} customers")
        return self

    def predict(self, data: Optional[pd.DataFrame] = None, **kwargs) -> pd.DataFrame:
        """
        Assign cluster labels to customers.

        Returns:
            DataFrame with segment_id and segment_label columns added.
        """
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before predicting")

        features = self._get_features(data)
        scaled = self._scaler.transform(features)
        labels = self._model.predict(scaled)

        result = data.copy()
        result["segment_id"] = labels

        # Generate cluster profiles
        self._cluster_profiles = self._build_profiles(result)

        # Assign business-friendly labels
        result = self._assign_labels(result)

        self._metrics = {
            "n_clusters": self.n_clusters,
            "inertia": round(self._model.inertia_, 2),
            "n_customers": len(data),
        }

        logger.info(f"Segmented {len(data)} customers into {self.n_clusters} clusters")
        return result

    def get_profiles(self) -> Optional[pd.DataFrame]:
        """Return cluster profiles with summary statistics."""
        return self._cluster_profiles

    def find_optimal_k(
        self,
        data: pd.DataFrame,
        k_range: range = range(2, 9),
    ) -> dict[int, float]:
        """
        Find optimal number of clusters using elbow method.

        Returns:
            Dict mapping k → inertia.
        """
        features = self._get_features(data)
        scaled = self._scaler.fit_transform(features)

        results = {}
        for k in k_range:
            km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            km.fit(scaled)
            results[k] = km.inertia_
            logger.info(f"k={k}, inertia={km.inertia_:.2f}")

        return results

    def _get_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Extract RFM feature columns."""
        rfm_cols = ["recency", "frequency", "monetary"]
        available = [c for c in rfm_cols if c in data.columns]
        if not available:
            raise ValueError(f"Need at least one of {rfm_cols} columns")
        return data[available].fillna(0)

    def _build_profiles(self, data: pd.DataFrame) -> pd.DataFrame:
        """Build summary profile for each cluster."""
        profiles = data.groupby("segment_id").agg(
            size=("segment_id", "count"),
            avg_recency=("recency", "mean"),
            avg_frequency=("frequency", "mean"),
            avg_monetary=("monetary", "mean"),
        ).reset_index()

        profiles["pct_of_total"] = round(profiles["size"] / profiles["size"].sum() * 100, 1)
        return profiles

    def _assign_labels(self, data: pd.DataFrame) -> pd.DataFrame:
        """Assign business-friendly labels based on cluster characteristics."""
        if self._cluster_profiles is None:
            return data

        # Sort clusters by monetary value (descending) and assign labels
        profiles = self._cluster_profiles.sort_values("avg_monetary", ascending=False)
        label_options = [
            "High-Value Customers",
            "Growth Potential",
            "Regular Customers",
            "Low-Engagement",
            "New / Occasional",
            "At Risk",
            "Inactive",
            "Others",
        ]

        label_map = {}
        for i, (_, row) in enumerate(profiles.iterrows()):
            label = label_options[i] if i < len(label_options) else f"Segment {row['segment_id']}"
            label_map[row["segment_id"]] = label

        data["segment_label"] = data["segment_id"].map(label_map)
        return data
