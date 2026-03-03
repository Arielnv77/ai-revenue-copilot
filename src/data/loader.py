"""
CSV Loader — Handles file reading with encoding detection and type inference.
"""

import io
import logging
from pathlib import Path
from typing import Optional

import chardet
import pandas as pd

logger = logging.getLogger(__name__)


def detect_encoding(file_path: str | Path) -> str:
    """Detect file encoding using chardet."""
    with open(file_path, "rb") as f:
        raw = f.read(10_000)
    result = chardet.detect(raw)
    encoding = result.get("encoding", "utf-8") or "utf-8"
    confidence = result.get("confidence", 0) or 0

    # Heuristic: retail CSVs often contain "£" encoded as 0xA3 in cp1252/latin-1.
    # If chardet weakly suggests utf-8, prefer cp1252 to avoid decode failures.
    if encoding.lower() in {"utf-8", "ascii"} and confidence < 0.90 and b"\xa3" in raw:
        encoding = "cp1252"
        logger.info("Adjusted detected encoding to cp1252 based on byte-pattern heuristic")
    logger.info(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
    return encoding


def detect_separator(file_path: str | Path, encoding: str = "utf-8") -> str:
    """Auto-detect CSV separator by inspecting the first few lines."""
    separators = [",", ";", "\t", "|"]
    with open(file_path, "r", encoding=encoding) as f:
        sample = f.read(5_000)

    counts = {sep: sample.count(sep) for sep in separators}
    best_sep = max(counts, key=counts.get)
    logger.info(f"Detected separator: {repr(best_sep)}")
    return best_sep


def load_csv(
    source: str | Path | io.BytesIO,
    encoding: Optional[str] = None,
    separator: Optional[str] = None,
    parse_dates: bool = True,
    sample_rows: Optional[int] = None,
) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame with smart defaults.

    Args:
        source: File path or BytesIO object.
        encoding: Override encoding detection.
        separator: Override separator detection.
        parse_dates: Whether to attempt date parsing.
        sample_rows: If set, only load this many rows (for preview).

    Returns:
        pd.DataFrame with inferred types.
    """
    # Handle file path vs BytesIO
    if isinstance(source, (str, Path)):
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not file_path.suffix.lower() == ".csv":
            raise ValueError(f"Expected a .csv file, got: {file_path.suffix}")

        if encoding is None:
            encoding = detect_encoding(file_path)
        if separator is None:
            separator = detect_separator(file_path, encoding)
    else:
        encoding = encoding or "utf-8"
        separator = separator or ","

    encodings_to_try = [encoding, "utf-8", "iso-8859-1", "cp1252"]

    df = None
    last_err = None

    for enc in dict.fromkeys(encodings_to_try):  # remove dupes while preserving order
        try:
            logger.info(f"Trying to load CSV with encoding={enc}, separator={repr(separator)}")
            # Reset BytesIO pointer if needed
            if isinstance(source, io.BytesIO):
                source.seek(0)
                
            df = pd.read_csv(
                source,
                encoding=enc,
                sep=separator,
                nrows=sample_rows,
                on_bad_lines="warn",
                engine="pyarrow",
                dtype_backend="pyarrow"
            )
            # If successful, break out of loop
            break
        except UnicodeDecodeError as e:
            logger.warning(f"Failed to read with encoding {enc}: {e}")
            last_err = e
            continue

    if df is None:
        raise ValueError(f"Failed to load CSV with all attempted encodings. Last error: {last_err}")

    # Attempt to parse date columns
    if parse_dates:
        df = _infer_dates(df)

    logger.info(f"Loaded DataFrame: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def _infer_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Try to convert object columns that look like dates."""
    date_keywords = ("date", "time", "timestamp", "created", "updated", "invoice")

    for col in df.select_dtypes(include=["object"]).columns:
        col_lower = col.lower()
        if not any(kw in col_lower for kw in date_keywords):
            continue
        try:
            converted = pd.to_datetime(df[col], errors="coerce", format="mixed")
            if converted.notna().mean() > 0.5:
                df[col] = converted
                logger.info(f"Parsed column '{col}' as datetime")
        except Exception:
            continue
    return df


def get_dataframe_profile(df: pd.DataFrame) -> dict:
    """
    Generate a quick profile of the DataFrame.

    Returns:
        Dict with shape, dtypes, memory usage, and column info.
    """
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1_048_576, 2),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "column_names": list(df.columns),
        "date_columns": list(df.select_dtypes(include=["datetime64"]).columns),
        "numeric_columns": list(df.select_dtypes(include=["number"]).columns),
        "categorical_columns": list(df.select_dtypes(include=["object", "category"]).columns),
    }
