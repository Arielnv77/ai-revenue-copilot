"""
Analysis — GET /analysis/{dataset_id} endpoint for EDA results.
"""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from src.data.schemas import AnalysisResponse, ColumnStats

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/analysis/{dataset_id}", response_model=AnalysisResponse)
async def get_analysis(request: Request, dataset_id: str):
    """
    Get exploratory data analysis results for a dataset.

    Returns summary statistics, column profiles, quality report, and correlations.
    """
    # Retrieve dataset
    datasets = request.app.state.datasets
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_id}' not found")

    data = datasets[dataset_id]
    df = data["clean"]

    # Summary
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_columns": len(df.select_dtypes(include=["number"]).columns),
        "categorical_columns": len(df.select_dtypes(include=["object", "category"]).columns),
        "date_columns": len(df.select_dtypes(include=["datetime64"]).columns),
    }

    # Column stats
    column_stats = []
    for col in df.columns:
        stats = ColumnStats(
            name=col,
            dtype=str(df[col].dtype),
            count=int(df[col].count()),
            missing=int(df[col].isnull().sum()),
            missing_pct=round(df[col].isnull().mean() * 100, 2),
            unique=int(df[col].nunique()),
        )

        if df[col].dtype in ["int64", "float64"]:
            desc = df[col].describe()
            stats.mean = round(float(desc["mean"]), 4)
            stats.std = round(float(desc["std"]), 4)
            stats.min = round(float(desc["min"]), 4)
            stats.q25 = round(float(desc["25%"]), 4)
            stats.median = round(float(desc["50%"]), 4)
            stats.q75 = round(float(desc["75%"]), 4)
            stats.max = round(float(desc["max"]), 4)
        elif df[col].dtype in ["object", "category"]:
            top = df[col].value_counts().head(10).to_dict()
            stats.top_values = {str(k): int(v) for k, v in top.items()}

        column_stats.append(stats)

    # Correlations (numeric only)
    numeric_df = df.select_dtypes(include=["number"])
    correlations = None
    if len(numeric_df.columns) >= 2:
        corr_matrix = numeric_df.corr().round(4)
        correlations = {
            col: corr_matrix[col].to_dict()
            for col in corr_matrix.columns
        }

    return AnalysisResponse(
        dataset_id=dataset_id,
        summary=summary,
        column_stats=column_stats,
        quality_report=data["quality_report"],
        correlations=correlations,
    )
