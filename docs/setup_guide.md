# Setup Guide

## Prerequisites
- Python 3.11+
- pip
- (Optional) Docker

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/AI_REVENUE.git
cd AI_REVENUE

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Running

### API Server
```bash
uvicorn src.api.main:app --reload --port 8000
```
Swagger docs: http://localhost:8000/docs

### Streamlit Dashboard
```bash
streamlit run app/streamlit_app.py
```
Dashboard: http://localhost:8501

### Run Tests
```bash
pytest tests/ -v --cov=src
```

## Configuration

All settings are in `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | Required for NL Q&A |
| `API_HOST` | 0.0.0.0 | API host |
| `API_PORT` | 8000 | API port |
| `DEBUG` | true | Debug mode |
| `MAX_UPLOAD_SIZE_MB` | 50 | Max CSV size |
| `FORECAST_HORIZON_DAYS` | 90 | Default forecast |
