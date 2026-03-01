"""
Data Validator — Schema validation, quality checks, and data quality reports.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class QualityReport:
    """Data quality assessment report."""
    total_rows: int = 0
    total_columns: int = 0
    missing_values: dict = field(default_factory=dict)
    missing_pct: dict = field(default_factory=dict)
    duplicate_rows: int = 0
    duplicate_pct: float = 0.0
    constant_columns: list = field(default_factory=list)
    high_cardinality_columns: list = field(default_factory=list)
    outlier_columns: dict = field(default_factory=dict)
    quality_score: float = 0.0
    warnings: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "total_rows": self.total_rows,
            "total_columns": self.total_columns,
            "missing_values": self.missing_values,
            "missing_pct": self.missing_pct,
            "duplicate_rows": self.duplicate_rows,
            "duplicate_pct": round(self.duplicate_pct, 2),
            "constant_columns": self.constant_columns,
            "high_cardinality_columns": self.high_cardinality_columns,
            "outlier_columns": self.outlier_columns,
            "quality_score": round(self.quality_score, 2),
            "warnings": self.warnings,
        }


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: Optional[list[str]] = None,
    min_rows: int = 10,
) -> QualityReport:
    """
    Run comprehensive data quality validation.

    Args:
        df: Input DataFrame.
        required_columns: Columns that must be present.
        min_rows: Minimum number of rows required.

    Returns:
        QualityReport with all findings.
    """
    report = QualityReport()
    report.total_rows = len(df)
    report.total_columns = len(df.columns)

    # Check minimum rows
    if len(df) < min_rows:
        report.warnings.append(f"Dataset has only {len(df)} rows (minimum: {min_rows})")

    # Check required columns
    if required_columns:
        missing_cols = set(required_columns) - set(df.columns)
        if missing_cols:
            report.warnings.append(f"Missing required columns: {missing_cols}")

    # Missing values
    missing = df.isnull().sum()
    report.missing_values = missing[missing > 0].to_dict()
    report.missing_pct = {
        col: round(count / len(df) * 100, 2)
        for col, count in report.missing_values.items()
    }

    # Flag columns with >50% missing
    for col, pct in report.missing_pct.items():
        if pct > 50:
            report.warnings.append(f"Column '{col}' has {pct}% missing values")

    # Duplicates
    report.duplicate_rows = int(df.duplicated().sum())
    report.duplicate_pct = (report.duplicate_rows / len(df) * 100) if len(df) > 0 else 0.0
    if report.duplicate_pct > 10:
        report.warnings.append(f"{report.duplicate_pct:.1f}% of rows are duplicates")

    # Constant columns (only one unique value)
    report.constant_columns = [
        col for col in df.columns if df[col].nunique() <= 1
    ]
    if report.constant_columns:
        report.warnings.append(f"Constant columns detected: {report.constant_columns}")

    # High cardinality (>95% unique in object cols)
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].nunique() / len(df) > 0.95:
            report.high_cardinality_columns.append(col)

    # Outliers (IQR method for numeric columns)
    report.outlier_columns = _detect_outliers(df)

    # Quality score (0-100)
    report.quality_score = _calculate_quality_score(report)

    logger.info(f"Quality report: score={report.quality_score:.1f}, warnings={len(report.warnings)}")
    return report


def _detect_outliers(df: pd.DataFrame, threshold: float = 1.5) -> dict:
    """Detect outliers using IQR method on numeric columns."""
    outliers = {}
    for col in df.select_dtypes(include=["number"]).columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - threshold * iqr
        upper = q3 + threshold * iqr
        n_outliers = int(((df[col] < lower) | (df[col] > upper)).sum())
        if n_outliers > 0:
            outliers[col] = {
                "count": n_outliers,
                "pct": round(n_outliers / len(df) * 100, 2),
                "lower_bound": round(lower, 4),
                "upper_bound": round(upper, 4),
            }
    return outliers


def _calculate_quality_score(report: QualityReport) -> float:
    """Calculate overall data quality score (0-100)."""
    score = 100.0

    # Deduct for missing values
    if report.missing_pct:
        avg_missing = sum(report.missing_pct.values()) / len(report.missing_pct)
        score -= min(avg_missing * 0.5, 30)

    # Deduct for duplicates
    score -= min(report.duplicate_pct * 0.3, 15)

    # Deduct for constant columns
    if report.total_columns > 0:
        const_ratio = len(report.constant_columns) / report.total_columns
        score -= const_ratio * 20

    # Deduct for warnings
    score -= len(report.warnings) * 2

    return max(0.0, min(100.0, score))
