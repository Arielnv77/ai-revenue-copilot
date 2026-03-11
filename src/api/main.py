"""
FastAPI Main — Application entry point with CORS, exception handlers, and route registration.
"""

import logging
import time
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.routes import analysis, forecast, health, query, upload
from src.utils.config import settings
from src.utils.logger import setup_logging

logger = logging.getLogger(__name__)

# --- In-memory rate limiter (sliding window per IP) ---
_request_log: dict[str, list[float]] = defaultdict(list)
_WINDOW = 60.0  # seconds
_LIMITS: dict[str, int] = {
    "/upload": 10,
    "/query": 20,
}
_DEFAULT_LIMIT = 60


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

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host if request.client else "unknown"
    path = request.url.path
    limit = next((v for k, v in _LIMITS.items() if path.startswith(k)), _DEFAULT_LIMIT)
    now = time.time()
    window_start = now - _WINDOW

    log = _request_log[ip]
    _request_log[ip] = [t for t in log if t > window_start]

    if len(_request_log[ip]) >= limit:
        logger.warning(f"Rate limit hit: ip={ip} path={path}")
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please slow down."},
            headers={"Retry-After": "60"},
        )

    _request_log[ip].append(now)
    return await call_next(request)


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
