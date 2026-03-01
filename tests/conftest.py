"""
Test fixtures and sample data generators.
"""

import pandas as pd
import numpy as np
import pytest
from datetime import datetime, timedelta


@pytest.fixture
def sample_sales_df():
    """Generate a sample sales DataFrame for testing."""
    np.random.seed(42)
    n_rows = 500

    dates = pd.date_range("2024-01-01", periods=n_rows, freq="h")
    customer_ids = np.random.choice(range(100, 200), size=n_rows)
    quantities = np.random.randint(1, 20, size=n_rows)
    unit_prices = np.round(np.random.uniform(1.0, 100.0, size=n_rows), 2)

    df = pd.DataFrame({
        "InvoiceNo": [f"INV{i:05d}" for i in range(n_rows)],
        "InvoiceDate": dates,
        "CustomerID": customer_ids,
        "Description": np.random.choice(
            ["Widget A", "Widget B", "Gadget X", "Gadget Y", "Tool Z"],
            size=n_rows,
        ),
        "Quantity": quantities,
        "UnitPrice": unit_prices,
    })
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    return df


@pytest.fixture
def sample_csv_path(tmp_path, sample_sales_df):
    """Save sample data to a CSV and return the path."""
    csv_path = tmp_path / "sample_sales.csv"
    sample_sales_df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_rfm_df():
    """Generate a sample RFM DataFrame for testing."""
    np.random.seed(42)
    n_customers = 50

    return pd.DataFrame({
        "customerid": range(100, 100 + n_customers),
        "recency": np.random.randint(1, 365, size=n_customers),
        "frequency": np.random.randint(1, 50, size=n_customers),
        "monetary": np.round(np.random.uniform(10, 5000, size=n_customers), 2),
        "recency_score": np.random.randint(1, 6, size=n_customers),
        "frequency_score": np.random.randint(1, 6, size=n_customers),
        "monetary_score": np.random.randint(1, 6, size=n_customers),
    })


@pytest.fixture
def sample_time_series_df():
    """Generate a sample time series DataFrame for forecasting."""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=365, freq="D")
    values = (
        1000
        + np.cumsum(np.random.randn(365) * 10)
        + 200 * np.sin(np.arange(365) * 2 * np.pi / 365)
    )
    return pd.DataFrame({
        "ds": dates,
        "y": np.maximum(values, 0),
    })
