"""
Transformer — Type casting, date parsing, normalization, and encoding.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def cast_numeric_columns(df: pd.DataFrame, columns: Optional[list[str]] = None) -> pd.DataFrame:
    """Force-cast columns to numeric, coercing errors to NaN."""
    if columns is None:
        columns = df.select_dtypes(include=["object"]).columns.tolist()

    for col in columns:
        if col not in df.columns:
            continue
        try:
            converted = pd.to_numeric(df[col], errors="coerce")
            valid_pct = converted.notna().mean()
            if valid_pct > 0.5:
                df[col] = converted
                logger.info(f"Cast '{col}' to numeric ({valid_pct:.0%} valid)")
        except Exception:
            continue
    return df


def parse_dates(df: pd.DataFrame, date_columns: Optional[list[str]] = None) -> pd.DataFrame:
    """Parse date columns to datetime."""
    if date_columns is None:
        date_columns = _detect_date_columns(df)

    for col in date_columns:
        if col not in df.columns:
            continue
        try:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            logger.info(f"Parsed '{col}' as datetime")
        except Exception as e:
            logger.warning(f"Could not parse '{col}' as date: {e}")
    return df


def _detect_date_columns(df: pd.DataFrame) -> list[str]:
    """Heuristically detect columns that look like dates."""
    date_keywords = ["date", "time", "timestamp", "created", "updated", "day", "month", "year"]
    candidates = []
    for col in df.select_dtypes(include=["object"]).columns:
        if any(kw in col.lower() for kw in date_keywords):
            candidates.append(col)
    return candidates


def normalize_column(
    df: pd.DataFrame,
    column: str,
    method: str = "minmax",
) -> pd.DataFrame:
    """
    Normalize a numeric column.

    Args:
        df: Input DataFrame.
        column: Column to normalize.
        method: 'minmax' (0-1) or 'zscore' (mean=0, std=1).
    """
    if column not in df.columns:
        return df

    if method == "minmax":
        col_min = df[column].min()
        col_max = df[column].max()
        if col_max != col_min:
            df[column] = (df[column] - col_min) / (col_max - col_min)
    elif method == "zscore":
        col_mean = df[column].mean()
        col_std = df[column].std()
        if col_std != 0:
            df[column] = (df[column] - col_mean) / col_std

    logger.info(f"Normalized '{column}' using {method}")
    return df


def encode_categorical(
    df: pd.DataFrame,
    columns: Optional[list[str]] = None,
    method: str = "label",
    max_categories: int = 20,
) -> pd.DataFrame:
    """
    Encode categorical columns.

    Args:
        df: Input DataFrame.
        columns: Columns to encode. If None, auto-detect.
        method: 'label' or 'onehot'.
        max_categories: Max unique values to encode (skip high cardinality).
    """
    if columns is None:
        columns = df.select_dtypes(include=["object", "category"]).columns.tolist()

    for col in columns:
        if col not in df.columns:
            continue
        n_unique = df[col].nunique()
        if n_unique > max_categories:
            logger.info(f"Skipping '{col}': too many categories ({n_unique})")
            continue

        if method == "label":
            df[col] = df[col].astype("category").cat.codes
            logger.info(f"Label-encoded '{col}' ({n_unique} categories)")
        elif method == "onehot":
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
            df = pd.concat([df.drop(columns=[col]), dummies], axis=1)
            logger.info(f"One-hot encoded '{col}' ({n_unique} categories)")

    return df


def add_revenue_column(
    df: pd.DataFrame,
    quantity_col: str = "quantity",
    price_col: str = "unitprice",
    revenue_col: str = "revenue",
) -> pd.DataFrame:
    """Calculate revenue = quantity × price."""
    if quantity_col in df.columns and price_col in df.columns:
        df[revenue_col] = df[quantity_col] * df[price_col]
        logger.info(f"Added '{revenue_col}' column = {quantity_col} × {price_col}")
    return df
