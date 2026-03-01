"""
FastAPI Main — Application entry point with CORS, exception handlers, and route registration.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import analysis, forecast, health, query, upload
from src.utils.config import settings
from src.utils.logger import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    setup_logging(level="DEBUG" if settings.debug else "INFO")
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")

    # Initialize in-memory dataset store
    app.state.datasets = {}

    yield

    logger.info("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered revenue analysis platform",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health.router, tags=["Health"])
app.include_router(upload.router, tags=["Upload"])
app.include_router(analysis.router, tags=["Analysis"])
app.include_router(forecast.router, tags=["Forecast"])
app.include_router(query.router, tags=["Query"])
