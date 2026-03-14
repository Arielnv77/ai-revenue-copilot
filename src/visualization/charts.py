"""
Charts — Plotly chart factories for the dashboard.
"""

from typing import Optional

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# === Color palette ===
COLORS = {
    "primary": "#6366f1",
    "secondary": "#8b5cf6",
    "accent": "#06b6d4",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "dark": "#1e1b4b",
    "light": "#f8fafc",
}

PALETTE = ["#6366f1", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#ec4899", "#14b8a6"]


def revenue_time_series(
    df: pd.DataFrame,
    date_col: str = "date",
    value_col: str = "revenue_sum",
    title: str = "Revenue Over Time",
) -> go.Figure:
    """Create an interactive revenue time-series chart."""
    fig = px.line(
        df, x=date_col, y=value_col,
        title=title,
        labels={date_col: "Date", value_col: "Revenue ($)"},
    )
    fig.update_traces(line_color=COLORS["primary"], line_width=2)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def forecast_chart(
    historical: pd.DataFrame,
    forecast: pd.DataFrame,
    title: str = "Revenue Forecast",
) -> go.Figure:
    """Create forecast chart with confidence interval."""
    fig = go.Figure()

    # Historical data
    fig.add_trace(go.Scatter(
        x=historical["date"], y=historical["revenue_sum"],
        name="Historical", mode="lines",
        line=dict(color=COLORS["primary"], width=2),
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast["date"], y=forecast["predicted"],
        name="Forecast", mode="lines",
        line=dict(color=COLORS["accent"], width=2, dash="dash"),
    ))

    # Confidence interval
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast["date"], forecast["date"][::-1]]),
        y=pd.concat([forecast["upper_bound"], forecast["lower_bound"][::-1]]),
        fill="toself", fillcolor="rgba(6, 182, 212, 0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Confidence Interval",
    ))

    fig.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def anomaly_chart(
    df: pd.DataFrame,
    date_col: str = "date",
    value_col: str = "revenue_sum",
    title: str = "Anomaly Detection",
) -> go.Figure:
    """Revenue chart with anomalies highlighted."""
    fig = go.Figure()

    # Normal points
    normal = df[~df["is_anomaly"]]
    fig.add_trace(go.Scatter(
        x=normal[date_col], y=normal[value_col],
        name="Normal", mode="lines+markers",
        line=dict(color=COLORS["primary"]),
        marker=dict(size=4),
    ))

    # Anomaly points
    anomalies = df[df["is_anomaly"]]
    fig.add_trace(go.Scatter(
        x=anomalies[date_col], y=anomalies[value_col],
        name="Anomaly", mode="markers",
        marker=dict(color=COLORS["danger"], size=12, symbol="diamond"),
    ))

    fig.update_layout(
        title=title,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def segmentation_chart(
    df: pd.DataFrame,
    title: str = "Customer Segments",
) -> go.Figure:
    """Pie/donut chart of customer segments."""
    segment_counts = df["segment_label"].value_counts()

    fig = px.pie(
        values=segment_counts.values,
        names=segment_counts.index,
        title=title,
        color_discrete_sequence=PALETTE,
        hole=0.4,
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def rfm_scatter(
    df: pd.DataFrame,
    title: str = "RFM Customer Map",
) -> go.Figure:
    """3D scatter plot of RFM segments. Samples max 10,000 rows for performance."""
    plot_df = df if len(df) <= 10000 else df.sample(10000, random_state=42)
    fig = px.scatter_3d(
        plot_df, x="recency", y="frequency", z="monetary",
        color="segment_label",
        title=title,
        color_discrete_sequence=PALETTE,
        opacity=0.7,
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def correlation_heatmap(
    df: pd.DataFrame,
    title: str = "Correlation Matrix",
) -> go.Figure:
    """Correlation heatmap for numeric columns."""
    numeric = df.select_dtypes(include=["number"])
    corr = numeric.corr()

    fig = px.imshow(
        corr, text_auto=".2f",
        title=title,
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1,
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
    )
    return fig


def distribution_chart(
    df: pd.DataFrame,
    column: str,
    title: Optional[str] = None,
) -> go.Figure:
    """Histogram with KDE for a numeric column. Samples max 20,000 rows for performance."""
    plot_df = df if len(df) <= 20000 else df.sample(20000, random_state=42)
    fig = px.histogram(
        plot_df, x=column,
        title=title or f"Distribution of {column}",
        nbins=50,
        color_discrete_sequence=[COLORS["primary"]],
        marginal="box",
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
    )
    return fig
