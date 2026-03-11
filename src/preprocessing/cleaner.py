"""
Cleaner — Handle missing values, duplicates, and outliers.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df: pd.DataFrame, subset: Optional[list[str]] = None) -> pd.DataFrame:
    """Remove duplicate rows."""
    n_before = len(df)
    df = df.drop_duplicates(subset=subset).reset_index(drop=True)
    n_removed = n_before - len(df)
    if n_removed > 0:
        logger.info(f"Removed {n_removed} duplicate rows")
    return df


def handle_missing_values(
    df: pd.DataFrame,
    strategy: str = "auto",
    fill_value: Optional[float] = None,
) -> pd.DataFrame:
    """
    Handle missing values with configurable strategy.

    Args:
        df: Input DataFrame.
        strategy: One of 'auto', 'drop', 'mean', 'median', 'mode', 'fill'.
        fill_value: Value to use when strategy='fill'.

    Returns:
        DataFrame with missing values handled.
    """
    if strategy == "drop":
        df = df.dropna().reset_index(drop=True)
        logger.info("Dropped all rows with missing values")

    elif strategy == "fill":
        df = df.fillna(fill_value)
        logger.info(f"Filled missing values with {fill_value}")

    elif strategy == "auto":
        # Numeric: fill with median
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                logger.info(f"Filled '{col}' missing values with median ({median_val:.2f})")

        # Categorical: fill with mode
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in cat_cols:
            if df[col].isnull().any():
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col] = df[col].fillna(mode_val.iloc[0])
                    logger.info(f"Filled '{col}' missing values with mode ({mode_val.iloc[0]})")
                else:
                    logger.warning(f"Column '{col}' has all-NaN values; skipping mode imputation")

        # Datetime: forward fill
        date_cols = df.select_dtypes(include=["datetime64"]).columns
        for col in date_cols:
            if df[col].isnull().any():
                df[col] = df[col].ffill()
                logger.info(f"Forward-filled '{col}' missing dates")

    elif strategy in ("mean", "median", "mode"):
        numeric_cols = df.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                if strategy == "mean":
                    val = df[col].mean()
                elif strategy == "median":
                    val = df[col].median()
                else:
                    mode_series = df[col].mode()
                    if len(mode_series) == 0:
                        logger.warning(f"Column '{col}' has all-NaN values; skipping mode imputation")
                        continue
                    val = mode_series.iloc[0]
                df[col] = df[col].fillna(val)

    return df


def cap_outliers(
    df: pd.DataFrame,
    columns: Optional[list[str]] = None,
    method: str = "iqr",
    threshold: float = 1.5,
) -> pd.DataFrame:
    """
    Cap outliers in numeric columns using IQR method.

    Args:
        df: Input DataFrame.
        columns: Columns to process. If None, all numeric columns.
        method: Currently supports 'iqr'.
        threshold: IQR multiplier for bounds.

    Returns:
        DataFrame with outliers capped.
    """
    if columns is None:
        columns = df.select_dtypes(include=["number"]).columns.tolist()

    for col in columns:
        if col not in df.columns:
            continue
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        n_capped = int(((df[col] < lower) | (df[col] > upper)).sum())
        if n_capped > 0:
            df[col] = df[col].clip(lower=lower, upper=upper)
            logger.info(f"Capped {n_capped} outliers in '{col}' [{lower:.2f}, {upper:.2f}]")

    return df


def drop_constant_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove columns with only one unique value."""
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if constant_cols:
        df = df.drop(columns=constant_cols)
        logger.info(f"Dropped constant columns: {constant_cols}")
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names: lowercase, underscores, no special chars."""
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)
        .str.replace(r"\s+", "_", regex=True)
    )
    logger.info(f"Cleaned column names: {list(df.columns)}")
    return df


def run_cleaning_pipeline(
    df: pd.DataFrame,
    remove_dupes: bool = True,
    handle_missing: str = "auto",
    cap_outlier: bool = False,
    clean_names: bool = True,
    drop_constant: bool = True,
) -> pd.DataFrame:
    """
    Run the full cleaning pipeline.

    Args:
        df: Raw DataFrame.
        remove_dupes: Remove duplicate rows.
        handle_missing: Missing value strategy.
        cap_outlier: Whether to cap outliers.
        clean_names: Standardize column names.
        drop_constant: Remove constant columns.

    Returns:
        Cleaned DataFrame.
    """
    logger.info(f"Starting cleaning pipeline: {df.shape}")

    if clean_names:
        df = clean_column_names(df)
    if remove_dupes:
        df = remove_duplicates(df)
    df = handle_missing_values(df, strategy=handle_missing)
    if cap_outlier:
        df = cap_outliers(df)
    if drop_constant:
        df = drop_constant_columns(df)

    logger.info(f"Cleaning complete: {df.shape}")
    return df
