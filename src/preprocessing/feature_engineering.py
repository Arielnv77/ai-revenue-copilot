"""
Feature Engineering — RFM scores, time-based features, and aggregations.
"""

import logging
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def compute_rfm(
    df: pd.DataFrame,
    customer_col: str = "customerid",
    date_col: str = "invoicedate",
    revenue_col: str = "revenue",
    reference_date: Optional[datetime] = None,
) -> pd.DataFrame:
    """
    Compute RFM (Recency, Frequency, Monetary) scores per customer.

    Args:
        df: Transaction-level DataFrame.
        customer_col: Column with customer identifiers.
        date_col: Column with transaction dates.
        revenue_col: Column with transaction revenue.
        reference_date: Date to calculate recency from (default: max date + 1 day).

    Returns:
        DataFrame with one row per customer: recency, frequency, monetary, rfm_score.
    """
    required = [customer_col, date_col, revenue_col]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for RFM: {missing}")

    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    if reference_date is None:
        reference_date = df[date_col].max() + pd.Timedelta(days=1)

    # Aggregate per customer
    rfm = df.groupby(customer_col).agg(
        recency=(date_col, lambda x: (reference_date - x.max()).days),
        frequency=(date_col, "count"),
        monetary=(revenue_col, "sum"),
    ).reset_index()

    # Score each dimension (1-5, using quantiles)
    for col in ["recency", "frequency", "monetary"]:
        ascending = col == "recency"  # Lower recency = better
        rfm[f"{col}_score"] = pd.qcut(
            rfm[col].rank(method="first", ascending=ascending),
            q=5,
            labels=[1, 2, 3, 4, 5],
        ).astype(int)

    # Composite RFM score
    rfm["rfm_score"] = (
        rfm["recency_score"] * 100
        + rfm["frequency_score"] * 10
        + rfm["monetary_score"]
    )

    logger.info(f"Computed RFM for {len(rfm)} customers")
    return rfm


def assign_rfm_labels(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Assign business-friendly labels to RFM segments.

    Uses recency_score and frequency_score to create labels like
    'Champions', 'Loyal Customers', 'At Risk', etc.
    """
    def _label(row):
        r, f = row["recency_score"], row["frequency_score"]
        if r >= 4 and f >= 4:
            return "Champions"
        elif r >= 3 and f >= 3:
            return "Loyal Customers"
        elif r >= 4 and f <= 2:
            return "New Customers"
        elif r >= 3 and f <= 2:
            return "Promising"
        elif r <= 2 and f >= 3:
            return "At Risk"
        elif r <= 2 and f >= 4:
            return "Can't Lose Them"
        elif r <= 2 and f <= 2:
            return "Lost"
        else:
            return "Need Attention"

    rfm["segment_label"] = rfm.apply(_label, axis=1)
    logger.info(f"Assigned RFM labels: {rfm['segment_label'].value_counts().to_dict()}")
    return rfm


def add_time_features(
    df: pd.DataFrame,
    date_col: str = "invoicedate",
) -> pd.DataFrame:
    """
    Extract time-based features from a date column.

    Adds: year, month, day_of_week, hour, is_weekend, quarter.
    """
    if date_col not in df.columns:
        logger.warning(f"Date column '{date_col}' not found")
        return df

    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    df["day_of_week"] = df[date_col].dt.dayofweek
    df["hour"] = df[date_col].dt.hour
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["quarter"] = df[date_col].dt.quarter

    logger.info("Added time features: year, month, day_of_week, hour, is_weekend, quarter")
    return df


def aggregate_revenue_by_period(
    df: pd.DataFrame,
    date_col: str = "invoicedate",
    revenue_col: str = "revenue",
    period: str = "D",
) -> pd.DataFrame:
    """
    Aggregate revenue by time period.

    Args:
        df: Transaction DataFrame.
        date_col: Date column.
        revenue_col: Revenue column.
        period: Pandas frequency string ('D'=daily, 'W'=weekly, 'M'=monthly).

    Returns:
        DataFrame with date index and aggregated revenue.
    """
    if date_col not in df.columns or revenue_col not in df.columns:
        raise ValueError(f"Required columns not found: {date_col}, {revenue_col}")

    ts = df.set_index(date_col)[[revenue_col]].resample(period).agg(
        revenue_sum=(revenue_col, "sum"),
        revenue_mean=(revenue_col, "mean"),
        transaction_count=(revenue_col, "count"),
    ).reset_index()

    ts.columns = ["date", "revenue_sum", "revenue_mean", "transaction_count"]
    logger.info(f"Aggregated revenue by '{period}': {len(ts)} periods")
    return ts
