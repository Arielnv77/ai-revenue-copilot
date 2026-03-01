"""
Upload — POST /upload endpoint for CSV file upload.
"""

import io
import logging
import uuid

from fastapi import APIRouter, File, Request, UploadFile, HTTPException

from src.data.loader import load_csv, get_dataframe_profile
from src.data.validator import validate_dataframe
from src.data.schemas import UploadResponse
from src.preprocessing.cleaner import run_cleaning_pipeline

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_csv(request: Request, file: UploadFile = File(...)):
    """
    Upload a CSV file for analysis.

    The file is loaded, validated, cleaned, and stored in memory.
    Returns dataset metadata and a unique dataset_id for further operations.
    """
    # Validate file type
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    # Read file content
    try:
        content = await file.read()
        buffer = io.BytesIO(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")

    # Load CSV
    try:
        df = load_csv(buffer)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error parsing CSV: {e}")

    # Validate
    quality_report = validate_dataframe(df)

    # Clean
    df_clean = run_cleaning_pipeline(df.copy())

    # Generate unique ID and store
    dataset_id = str(uuid.uuid4())[:8]
    request.app.state.datasets[dataset_id] = {
        "raw": df,
        "clean": df_clean,
        "filename": file.filename,
        "quality_report": quality_report.to_dict(),
    }

    # Profile
    profile = get_dataframe_profile(df_clean)

    logger.info(f"Uploaded dataset '{file.filename}' as {dataset_id}: {df_clean.shape}")

    return UploadResponse(
        dataset_id=dataset_id,
        filename=file.filename,
        rows=profile["rows"],
        columns=profile["columns"],
        column_names=profile["column_names"],
        dtypes=profile["dtypes"],
        memory_mb=profile["memory_mb"],
        quality_score=quality_report.quality_score,
    )
