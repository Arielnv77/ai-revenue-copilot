"""
Forecaster — Revenue forecasting using Facebook Prophet.
"""

import logging
from typing import Optional

import pandas as pd

from src.models.base import BaseModel

logger = logging.getLogger(__name__)


class RevenueForecaster(BaseModel):
    """
    Time-series revenue forecasting using Facebook Prophet.

    Expects a DataFrame with columns: 'ds' (date) and 'y' (revenue).
    """

    def __init__(
        self,
        yearly_seasonality: bool = True,
        weekly_seasonality: bool = True,
        daily_seasonality: bool = False,
        changepoint_prior_scale: float = 0.05,
    ):
        super().__init__(name="RevenueForecaster")
        self.yearly_seasonality = yearly_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.daily_seasonality = daily_seasonality
        self.changepoint_prior_scale = changepoint_prior_scale
        self._model = None
        self._forecast_df: Optional[pd.DataFrame] = None

    def fit(self, data: pd.DataFrame, **kwargs) -> "RevenueForecaster":
        """
        Fit Prophet model on time-series data.

        Args:
            data: DataFrame with 'ds' (date) and 'y' (revenue) columns.
        """
        from prophet import Prophet

        self._validate_input(data)

        logger.info(f"Fitting Prophet on {len(data)} data points...")
        self._model = Prophet(
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality,
            changepoint_prior_scale=self.changepoint_prior_scale,
        )
        self._model.fit(data[["ds", "y"]])
        self._is_fitted = True
        logger.info("Prophet model fitted successfully")
        return self

    def predict(
        self,
        data: Optional[pd.DataFrame] = None,
        horizon_days: int = 90,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Generate revenue forecast.

        Args:
            data: Not used (Prophet generates future dates internally).
            horizon_days: Number of days to forecast.

        Returns:
            DataFrame with columns: ds, yhat, yhat_lower, yhat_upper.
        """
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before predicting")

        future = self._model.make_future_dataframe(periods=horizon_days, freq="D")
        forecast = self._model.predict(future)

        self._forecast_df = forecast
        logger.info(f"Generated {horizon_days}-day forecast")

        # Return only forecast columns
        result = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
        result.columns = ["date", "predicted", "lower_bound", "upper_bound"]
        return result

    def get_components(self) -> Optional[pd.DataFrame]:
        """Get forecast components (trend, seasonality)."""
        if self._forecast_df is None:
            return None
        return self._forecast_df[["ds", "trend", "yearly", "weekly"]].copy()

    def _validate_input(self, data: pd.DataFrame) -> None:
        """Validate input data format."""
        if "ds" not in data.columns or "y" not in data.columns:
            raise ValueError("Data must have 'ds' (date) and 'y' (value) columns")
        if len(data) < 14:
            raise ValueError("Need at least 14 data points for forecasting")


def prepare_forecast_data(
    df: pd.DataFrame,
    date_col: str,
    value_col: str,
    freq: str = "D",
) -> pd.DataFrame:
    """
    Prepare a DataFrame for Prophet by renaming and resampling.

    Args:
        df: Input DataFrame.
        date_col: Name of the date column.
        value_col: Name of the value column.
        freq: Resample frequency.

    Returns:
        DataFrame with 'ds' and 'y' columns, resampled.
    """
    ts = df[[date_col, value_col]].copy()
    ts.columns = ["ds", "y"]
    ts["ds"] = pd.to_datetime(ts["ds"])

    # Resample to fill gaps
    ts = ts.set_index("ds").resample(freq).sum().reset_index()
    ts = ts[ts["y"] > 0]  # Remove zero-revenue periods

    logger.info(f"Prepared forecast data: {len(ts)} periods ({freq})")
    return ts
