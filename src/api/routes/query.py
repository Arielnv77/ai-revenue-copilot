"""
Query — POST /query endpoint for natural language Q&A.
"""

import logging

from fastapi import APIRouter, HTTPException, Request

from src.data.schemas import QueryRequest, QueryResponse
from src.nlp.query_engine import QueryEngine
from src.utils.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def natural_language_query(request: Request, body: QueryRequest):
    """
    Answer a natural-language question about a dataset.

    Uses an LLM to translate the question into pandas operations
    and generate a business-friendly answer.
    """
    datasets = request.app.state.datasets
    if body.dataset_id not in datasets:
        raise HTTPException(status_code=404, detail=f"Dataset '{body.dataset_id}' not found")

    df = datasets[body.dataset_id]["clean"]

    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured. Set OPENAI_API_KEY in .env",
        )

    try:
        engine = QueryEngine(api_key=settings.openai_api_key)
        engine.load_data(df)
        result = engine.ask(body.question)

        return QueryResponse(
            dataset_id=body.dataset_id,
            question=body.question,
            answer=result.get("answer", ""),
            sql_or_code=result.get("code"),
            chart_data=None,
        )

    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
