# API Reference

Base URL: `http://localhost:8000`

## Endpoints

### GET /health
Health check.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-02-28T12:00:00Z"
}
```

### POST /upload
Upload a CSV file for analysis.

**Request:** `multipart/form-data` with `file` field.

**Response:**
```json
{
  "dataset_id": "abc12345",
  "filename": "sales.csv",
  "rows": 500,
  "columns": 7,
  "column_names": ["date", "customer_id", ...],
  "dtypes": {"date": "datetime64[ns]", ...},
  "memory_mb": 1.2,
  "quality_score": 92.5,
  "message": "Dataset uploaded successfully"
}
```

### GET /analysis/{dataset_id}
Get EDA analysis results.

**Response:** Summary stats, column profiles, quality report, correlations.

### GET /forecast/{dataset_id}
Get revenue forecast.

**Query params:**
- `date_column` (default: "invoicedate")
- `value_column` (default: "revenue")
- `horizon_days` (default: 90, range: 7-365)

**Response:** Forecast data points with confidence intervals.

### POST /query
Natural language Q&A.

**Request:**
```json
{
  "dataset_id": "abc12345",
  "question": "What is the total revenue?"
}
```

**Response:** Answer, code, insight.
