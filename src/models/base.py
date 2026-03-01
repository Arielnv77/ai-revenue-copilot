"""
Base — Abstract base class for all ML models.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

import pandas as pd


class BaseModel(ABC):
    """Abstract interface that all RevenueOS models must implement."""

    def __init__(self, name: str = "BaseModel"):
        self.name = name
        self._is_fitted = False
        self._metrics: dict[str, float] = {}

    @abstractmethod
    def fit(self, data: pd.DataFrame, **kwargs) -> "BaseModel":
        """Train the model on the given data."""
        ...

    @abstractmethod
    def predict(self, data: Optional[pd.DataFrame] = None, **kwargs) -> Any:
        """Generate predictions."""
        ...

    def evaluate(self) -> dict[str, float]:
        """Return model evaluation metrics."""
        return self._metrics

    @property
    def is_fitted(self) -> bool:
        return self._is_fitted

    def __repr__(self) -> str:
        status = "fitted" if self._is_fitted else "not fitted"
        return f"<{self.name} ({status})>"
