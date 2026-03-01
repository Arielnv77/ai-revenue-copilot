"""
Forecast — GET /forecast/{dataset_id} endpoint for revenue predictions.
"""

import logging

from fastapi import APIRouter, HTTPException, Query, Request

from src.data.schemas import ForecastPoint, ForecastResponse
from src.models.forecaster import RevenueForecaster, prepare_forecast_data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/forecast/{dataset_id}", response_model=ForecastResponse)
async def get_forecast(
    request: Request,
    dataset_id: str,
    date_column: str = Query("invoicedate", description="Name of date column"),
    value_column: str = Query("revenue", description="Name of value column"),
    horizon_days: int = Query(90, ge=7, le=365, description="Forecast horizon in days"),
):
    """
    Generate revenue forecast for a dataset.

    Uses Facebook Prophet to forecast revenue over the specified horizon.
    """
    datasets = request.app.state.datasets
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found")

    df = datasets[dataset_id]["clean"]

    # Check columns exist
    if date_column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Date column '{date_column}' not found")
    if value_column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Value column '{value_column}' not found")

    try:
        # Prepare data for Prophet
        ts_data = prepare_forecast_data(df, date_column, value_column, freq="D")

        # Fit and predict
        forecaster = RevenueForecaster()
        forecaster.fit(ts_data)
        forecast_df = forecaster.predict(horizon_days=horizon_days)

        # Convert to response
        forecast_points = [
            ForecastPoint(
                date=row["date"].strftime("%Y-%m-%d"),
                predicted=round(row["predicted"], 2),
                lower_bound=round(row["lower_bound"], 2),
                upper_bound=round(row["upper_bound"], 2),
            )
            for _, row in forecast_df.iterrows()
        ]

        return ForecastResponse(
            dataset_id=dataset_id,
            horizon_days=horizon_days,
            forecast=forecast_points,
            model_metrics=forecaster.evaluate(),
        )

    except Exception as e:
        logger.error(f"Forecast error: {e}")
        raise HTTPException(status_code=500, detail=f"Forecast failed: {e}")
