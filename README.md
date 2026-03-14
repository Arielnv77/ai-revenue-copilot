# RevenueOS

[![CI — Tests](https://github.com/yourusername/revenueos/actions/workflows/tests.yml/badge.svg)](https://github.com/yourusername/revenueos/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41.0-FF4B4B.svg)
![Prophet](https://img.shields.io/badge/Prophet-1.1.6-brightgreen.svg)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?logo=render)](https://revenueos.onrender.com)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> Transforms raw sales CSV data into actionable revenue intelligence in under 60 seconds — no code required.

RevenueOS combines classical ML (time-series forecasting, clustering, anomaly detection) with Generative AI to deliver a complete "Analyst-in-a-box" experience directly in the browser.

---

## Key Features

1. **Upload & Auto-EDA** — Drop any sales CSV. Auto-detects encoding (multi-fallback), infers schemas, runs data quality checks, and generates a Quality Score (0-100).
2. **Interactive Dashboard** — Auto-generated Plotly visualizations: distributions, correlation heatmaps, time-series, and category breakdowns.
3. **Revenue Forecasting** — Facebook Prophet with weekly/yearly seasonality. Projects revenue up to 365 days ahead with 95% confidence intervals.
4. **Customer Segmentation** — RFM Analysis (Recency, Frequency, Monetary) combined with KMeans Clustering. Produces business-friendly segment labels (Champions, At-Risk, Loyal, etc.).
5. **Ask Your Data (GenAI Q&A)** — Natural language query engine via GPT-4o-mini or Groq (LLaMA 3.1-70b). Generates and safely executes Pandas code. Supports BYOK (Bring Your Own Key).
6. **PDF Export** — Full analysis report: Quality Score, EDA summary, forecast results, and segment profiles — downloadable in one click.

---

## Architecture

```
                              ┌─────────────────────────────────┐
                              │         Streamlit Frontend        │
                              │           app/pages/              │
                              │  1_upload  2_dashboard  3_forecast│
                              │  4_segments  5_chat  6_report     │
                              └────────────┬────────────────────┘
                                           │  direct Python calls
                              ┌────────────▼────────────────────┐
                              │         FastAPI Backend           │
                              │           src/api/                │
                              │  POST /upload   GET /analysis     │
                              │  GET /forecast  POST /query       │
                              └──┬─────────┬──────────┬─────────┘
                                 │         │          │
                    ┌────────────▼──┐  ┌───▼──────┐  ┌▼──────────────┐
                    │  src/data/    │  │src/models│  │  src/nlp/     │
                    │  loader.py    │  │forecaster│  │  query_engine │
                    │  validator.py │  │segmentat.│  │  (OpenAI/Groq)│
                    │  schemas.py   │  │anomaly   │  └───────────────┘
                    └───────────────┘  └──────────┘
                                 │
                    ┌────────────▼─────────────────┐
                    │      src/preprocessing/       │
                    │  cleaner · feature_eng · xform│
                    └──────────────────────────────┘
                                 │
                    ┌────────────▼─────────────────┐
                    │    src/visualization/         │
                    │  charts.py (Plotly)           │
                    │  report.py (fpdf2 PDF export) │
                    └──────────────────────────────┘
```

### BYOK (Bring Your Own Key) LLM Strategy

The **Ask Your Data** feature supports two LLM providers, selectable from the sidebar:

| Provider | Model | Cost |
|----------|-------|------|
| OpenAI | gpt-4o-mini | ~$0.001/query |
| Groq | llama-3.1-70b-versatile | Free tier available |

Both providers share the same `QueryEngine` interface. Users supply their API key via `.env`.

---

## Quickstart (Local Development)

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/revenueos.git
cd revenueos

python3.11 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Add OPENAI_API_KEY or GROQ_API_KEY to activate Q&A
```

### 3. Run the complete stack

**Terminal 1 — Backend:**
```bash
uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 — Frontend:**
```bash
streamlit run app/streamlit_app.py --server.port 8501
```

Open **http://localhost:8501** — or use the **Load demo dataset** button on the Upload page to start immediately without uploading a file.

---

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=src   # with coverage
```

CI runs automatically on every push to `main` and on all pull requests via GitHub Actions.

---

## Deployment (Render)

The app is containerized with Docker (Python 3.11-slim). `start.sh` launches both services:

```bash
# Backend (port 8000)
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
# Frontend (PORT env var from Render)
streamlit run app/streamlit_app.py --server.port $WEB_PORT --server.address 0.0.0.0
```

Required environment variables on Render:
- `OPENAI_API_KEY` *(optional — activates OpenAI Q&A)*
- `GROQ_API_KEY` *(optional — activates Groq Q&A)*
- `WEB_PORT` *(set automatically by Render)*

---

## Roadmap

The following features are planned but not yet implemented:

- [ ] **Authentication** — User login / multi-tenant isolation (Auth0 or Supabase)
- [ ] **Persistent storage** — PostgreSQL / S3 for datasets and reports (currently in-memory)
- [ ] **Scheduled forecasts** — Cron-based auto-refresh of predictions
- [ ] **Anomaly alerts** — Email/Slack notifications when anomalies are detected
- [ ] **Multi-file joins** — Upload and join multiple CSVs before analysis
- [ ] **Custom segment labels** — User-defined business labels for clusters

---

## License

MIT License. See `LICENSE` for details.
