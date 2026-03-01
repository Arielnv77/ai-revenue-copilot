# === AI Revenue Copilot — Dockerfile ===
FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose ports (FastAPI + Streamlit)
EXPOSE 8000 8501

# Copy the start script and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Run the start script
CMD ["./start.sh"]
