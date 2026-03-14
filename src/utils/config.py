"""
Config — Application settings via pydantic-settings.
"""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # General
    app_name: str = "RevenueOS"
    app_version: str = "0.1.0"
    debug: bool = True

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # LLM providers
    openai_api_key: Optional[str] = None
    groq_api_key:   Optional[str] = None

    # Data
    max_upload_size_mb: int = 50
    allowed_extensions: str = "csv"
    data_dir: Path = Path("data")

    # Forecast
    forecast_horizon_days: int = 90

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

    @property
    def upload_dir(self) -> Path:
        path = self.data_dir / "raw"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def processed_dir(self) -> Path:
        path = self.data_dir / "processed"
        path.mkdir(parents=True, exist_ok=True)
        return path


# Singleton
settings = Settings()
