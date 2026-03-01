#  RevenueOS

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)
![Prophet](https://img.shields.io/badge/Prophet-1.1.5-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> **Enterprise-grade SaaS for Automated Revenue Intelligence, ML Forecasting, and Natural Language Data Querying.**

RevenueOS transforms raw sales data (CSV) into strategic intelligence in under 60 seconds without requiring any code or complex pipelines. It combines classical Machine Learning (time-series forecasting & clustering) with Generative AI to provide a complete "Analyst-in-a-box" experience.

---

##  Key Features

1. **Upload & Auto-EDA **: Drop any sales CSV. The system auto-detects encoding (with multi-fallback support), infers schemas, runs data quality checks, and generates a Quality Score.
2. **Interactive Dashboard **: Auto-generated Plotly visualizations. Explores distributions, correlation heatmaps, and aggregations automatically.
3. **Revenue Forecasting **: Powered by **Facebook Prophet**. Automatically handles trends and weekly/yearly seasonality to project revenue up to 90 days ahead with confidence intervals.
4. **Customer Segments **: Mathematical profiling combining **RFM Analysis** (Recency, Frequency, Monetary) with **KMeans Clustering** to build behavioral customer segments (Champions, At-Risk, Loyalists).
5. **Ask Your Data (GenAI Q&A) **: A natural language query engine using GPT-4o. The AI dynamically generates Pandas Python code to answer plain-English business questions and executes it securely.

---

##  Architecture

The project is decoupled into a robust backend and a modern frontend:

- **Backend / API engine (`src/`)**: Built on **FastAPI**. Exposes REST endpoints for model inference, data processing, and AI queries.
- **Frontend (`app/`)**: Built on **Streamlit** but radically styled with a custom CSS design system to mirror premium SaaS aesthetics (Dark mode, glassmorphism, responsive grids).

### The "BYOK" (Bring Your Own Key) LLM Strategy
For the **Ask Your Data** feature, the system implements a **BYOK** architecture. Since LLM queries incur token costs, users must provide their own `OPENAI_API_KEY` via the `.env` file to activate the Q&A feature. 
> *Future Scalability Note: The `QueryEngine` interface in `src/nlp` is designed to be model-agnostic. It can be easily swapped from OpenAI to open-source alternatives like LLaMA 3 via Groq for cost-free production deployment.*

---

##  Quickstart (Local Development)

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/revenueos.git
cd revenueos

# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
```
*(Optional)* Add your `OPENAI_API_KEY` inside `.env` if you want to use the Chat features.

### 3. Run the complete stack
You need two terminal instances (one for the Backend API, one for the Frontend Web App).

**Terminal 1 (Backend):**
```bash
source venv/bin/activate
uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

**Terminal 2 (Frontend):**
```bash
source venv/bin/activate
streamlit run app/streamlit_app.py --server.port 8501
```

> **Note:** Open your browser at `http://localhost:8501` to use the application. A sample dataset script is provided: run `python scripts/generate_sample_data.py` to generate a 5k row dataset for testing.

---

##  Testing
The codebase has 100% core test coverage using `pytest`, testing everything from the data cleaning pipeline and ML model instantiation to API endpoints.
```bash
pytest tests/ -v
```

##  License
MIT License. See `LICENSE` for details.
