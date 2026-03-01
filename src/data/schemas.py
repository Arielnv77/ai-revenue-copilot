"""
Pydantic Schemas — Data contracts for API requests and responses.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# === Upload ===

class UploadResponse(BaseModel):
    """Response after successful CSV upload."""
    dataset_id: str
    filename: str
    rows: int
    columns: int
    column_names: list[str]
    dtypes: dict[str, str]
    memory_mb: float
    quality_score: float
    message: str = "Dataset uploaded successfully"


# === Analysis / EDA ===

class ColumnStats(BaseModel):
    """Statistics for a single column."""
    name: str
    dtype: str
    count: int
    missing: int
    missing_pct: float
    unique: int
    # Numeric fields
    mean: Optional[float] = None
    std: Optional[float] = None
    min: Optional[float] = None
    q25: Optional[float] = None
    median: Optional[float] = None
    q75: Optional[float] = None
    max: Optional[float] = None
    # Categorical fields
    top_values: Optional[dict[str, int]] = None


class AnalysisResponse(BaseModel):
    """Full EDA analysis response."""
    dataset_id: str
    summary: dict[str, Any]
    column_stats: list[ColumnStats]
    quality_report: dict[str, Any]
    correlations: Optional[dict[str, dict[str, float]]] = None


# === Forecast ===

class ForecastRequest(BaseModel):
    """Request for revenue forecast."""
    dataset_id: str
    date_column: str
    value_column: str
    horizon_days: int = Field(default=90, ge=7, le=365)


class ForecastPoint(BaseModel):
    """Single forecast data point."""
    date: str
    predicted: float
    lower_bound: float
    upper_bound: float


class ForecastResponse(BaseModel):
    """Revenue forecast response."""
    dataset_id: str
    horizon_days: int
    forecast: list[ForecastPoint]
    model_metrics: Optional[dict[str, float]] = None


# === Anomaly Detection ===

class AnomalyPoint(BaseModel):
    """Single anomaly data point."""
    index: int
    date: Optional[str] = None
    value: float
    anomaly_score: float
    is_anomaly: bool


class AnomalyResponse(BaseModel):
    """Anomaly detection response."""
    dataset_id: str
    total_anomalies: int
    anomaly_pct: float
    anomalies: list[AnomalyPoint]


# === Segmentation ===

class SegmentProfile(BaseModel):
    """Profile for a customer segment."""
    segment_id: int
    label: str
    size: int
    pct_of_total: float
    avg_recency: Optional[float] = None
    avg_frequency: Optional[float] = None
    avg_monetary: Optional[float] = None
    description: str = ""


class SegmentationResponse(BaseModel):
    """Customer segmentation response."""
    dataset_id: str
    n_segments: int
    segments: list[SegmentProfile]


# === NL Query ===

class QueryRequest(BaseModel):
    """Natural language query request."""
    dataset_id: str
    question: str = Field(..., min_length=3, max_length=1000)


class QueryResponse(BaseModel):
    """Natural language query response."""
    dataset_id: str
    question: str
    answer: str
    chart_data: Optional[dict[str, Any]] = None
    sql_or_code: Optional[str] = None


# === Health ===

class HealthResponse(BaseModel):
    """API health check response."""
    status: str = "healthy"
    version: str = "0.1.0"
    timestamp: datetime
