# Architecture

## System Overview

AI Revenue Copilot follows a layered architecture:

```
┌─────────────────────────────────┐
│        Streamlit Frontend       │
│    (app/streamlit_app.py)       │
├─────────────────────────────────┤
│         FastAPI Backend         │
│      (src/api/main.py)          │
├──────────┬──────────┬───────────┤
│ Data     │ ML       │ NLP       │
│ Pipeline │ Models   │ Engine    │
├──────────┴──────────┴───────────┤
│       Utilities & Config        │
└─────────────────────────────────┘
```

## Components

### Data Pipeline (`src/data/`)
- **loader.py** — CSV loading with encoding/separator auto-detection
- **validator.py** — Data quality assessment and reporting
- **schemas.py** — Pydantic models for all API contracts

### Preprocessing (`src/preprocessing/`)
- **cleaner.py** — Missing values, duplicates, outliers
- **transformer.py** — Type casting, normalization
- **feature_engineering.py** — RFM scores, time features, revenue aggregation

### ML Models (`src/models/`)
- **forecaster.py** — Revenue forecasting with Prophet
- **anomaly_detector.py** — Anomaly detection with Isolation Forest
- **segmentation.py** — Customer segmentation with KMeans + RFM

### NLP Engine (`src/nlp/`)
- **query_engine.py** — NL → pandas via GPT-4o-mini
- **prompts.py** — System prompts and templates

### API (`src/api/`)
- **main.py** — FastAPI app with CORS and lifespan
- **routes/** — Upload, analysis, forecast, query, health

### Visualization (`src/visualization/`)
- **charts.py** — Plotly chart factories
- **report.py** — PDF report generator
