#!/bin/bash
# start.sh - Runs FastAPI and Streamlit concurrently
# Exit on error
set -e

echo " Starting RevenueOS Backend (FastAPI)..."
# Start the FastAPI backend in the background. Address 0.0.0.0 is needed for Docker port mapping.
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &
# Save the PID of the background process
API_PID=$!

echo " Waiting for API to start..."
sleep 3

echo " Starting RevenueOS Frontend (Streamlit)..."
# Start Streamlit in the foreground so the container doesn't exit.
streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
STREAMLIT_PID=$!

# Wait for both processes
wait $API_PID $STREAMLIT_PID
