#!/bin/bash
# start.sh - Runs FastAPI and Streamlit concurrently
# Exit on error
set -e

# Render gives us a $PORT environment variable for the public web entry.
# We will run Streamlit on that $PORT so the user sees the UI.
# FastAPI will run internally on 8000 for Streamlit to talk to.
WEB_PORT=${PORT:-8501}
API_PORT=8000

echo " Starting RevenueOS Backend (FastAPI) on port $API_PORT..."
# Start the FastAPI backend in the background.
uvicorn src.api.main:app --host 0.0.0.0 --port $API_PORT &
# Save the PID of the background process
API_PID=$!

echo " Waiting for API to start..."
sleep 3

echo " Starting RevenueOS Frontend (Streamlit) on port $WEB_PORT..."
# Start Streamlit in the foreground taking the dynamic Render port
streamlit run app/streamlit_app.py --server.port $WEB_PORT --server.address 0.0.0.0 &
STREAMLIT_PID=$!

# Wait for both processes
wait $API_PID $STREAMLIT_PID
