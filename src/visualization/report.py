"""
Report — Full PDF report generator (fpdf2).

Sections:
  1. Cover page  — title, filename, timestamp, quality score gauge
  2. EDA Summary — shape, dtypes breakdown, top missing columns
  3. Column stats — numeric describe table
  4. Forecast     — horizon, MAPE, predicted range (if provided)
  5. Segments     — segment profile table (if provided)
  6. Quality      — score, warnings list
"""

import logging
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Colour palette (RGB tuples)
# ──────────────────────────────────────────────────────────────────────────────
_C_BG      = (5,  12, 10)    # deep black
_C_PRIMARY = (52, 211, 153)  # emerald #34d399
_C_WHITE   = (255, 255, 255)
_C_MUTED   = (140, 160, 150)
_C_WARN    = (250, 204, 21)  # yellow
_C_ERR     = (248, 113, 113) # red
_C_OK      = (74, 222, 128)  # green


def _score_color(score: float):
    if score >= 80:
        return _C_OK
    if score >= 60:
        return _C_WARN
    return _C_ERR


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────
def _section(pdf, title: str):
    """Render a section header bar."""
    pdf.set_fill_color(*_C_PRIMARY)
    pdf.set_text_color(*_C_BG)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, f"  {title}", ln=True, fill=True)
    pdf.set_text_color(*_C_WHITE)
    pdf.ln(3)


def _kv(pdf, key: str, value: str, muted_key: bool = True):
    """Render a key: value row."""
    pdf.set_font("Helvetica", "B" if not muted_key else "", 9)
    pdf.set_text_color(*(_C_MUTED if muted_key else _C_WHITE))
    pdf.cell(55, 6, key, ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*_C_WHITE)
    pdf.cell(0, 6, str(value), ln=True)


def _table_header(pdf, cols: list[tuple[str, int]]):
    """Render a table header row. cols = [(label, width_mm), ...]"""
    pdf.set_fill_color(*_C_PRIMARY)
    pdf.set_text_color(*_C_BG)
    pdf.set_font("Helvetica", "B", 8)
    for label, w in cols:
        pdf.cell(w, 7, label, border=0, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(*_C_WHITE)


def _table_row(pdf, values: list[str], widths: list[int], even: bool):
    """Render a table data row."""
    bg = (15, 28, 22) if even else (10, 20, 16)
    pdf.set_fill_color(*bg)
    pdf.set_font("Helvetica", "", 8)
    for val, w in zip(values, widths):
        pdf.cell(w, 6, str(val)[:22], border=0, fill=True, align="C")
    pdf.ln()


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────
def generate_pdf_report(
    analysis_data: dict[str, Any],
    forecast_data: Optional[dict[str, Any]] = None,
    segment_data: Optional[dict[str, Any]] = None,
    output_path: Optional[str | Path] = None,
) -> bytes:
    """
    Generate a full PDF analysis report and return it as bytes.

    Args:
        analysis_data: Dict from the /analysis endpoint (summary, column_stats,
                       quality_report, correlations).
        forecast_data: Optional dict from the /forecast endpoint.
        segment_data:  Optional dict with segment profiles DataFrame rows.
        output_path:   If given, also saves the PDF to disk.

    Returns:
        Raw PDF bytes (suitable for st.download_button).
    """
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)

    # ── 1. Cover page ─────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*_C_BG)
    pdf.rect(0, 0, 210, 297, style="F")

    # Logo-like accent bar at top
    pdf.set_fill_color(*_C_PRIMARY)
    pdf.rect(0, 0, 210, 4, style="F")

    pdf.ln(18)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*_C_PRIMARY)
    pdf.cell(0, 14, "RevenueOS", ln=True, align="C")

    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(*_C_WHITE)
    pdf.cell(0, 8, "Revenue Intelligence Report", ln=True, align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*_C_MUTED)
    filename = analysis_data.get("filename", "dataset")
    pdf.cell(0, 6, f"Dataset: {filename}", ln=True, align="C")
    pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}", ln=True, align="C")

    # Quality score badge
    quality = analysis_data.get("quality_report", {})
    score = float(quality.get("quality_score", 0))
    pdf.ln(10)
    sc = _score_color(score)
    pdf.set_fill_color(*sc)
    pdf.set_text_color(*_C_BG)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 14, f"Quality Score: {score:.0f} / 100", ln=True, align="C", fill=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*sc)
    label = "Excellent" if score >= 80 else "Needs Attention" if score >= 60 else "Poor"
    pdf.cell(0, 6, label, ln=True, align="C")

    # Accent bar at bottom
    pdf.set_fill_color(*_C_PRIMARY)
    pdf.rect(0, 293, 210, 4, style="F")

    # ── 2. EDA Summary ────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.set_fill_color(*_C_BG)
    pdf.rect(0, 0, 210, 297, style="F")
    pdf.set_fill_color(*_C_PRIMARY)
    pdf.rect(0, 0, 210, 4, style="F")
    pdf.ln(6)

    _section(pdf, "Dataset Overview")
    summary = analysis_data.get("summary", {})
    _kv(pdf, "Total Rows",    f"{summary.get('total_rows', 'N/A'):,}" if isinstance(summary.get('total_rows'), int) else str(summary.get('total_rows', 'N/A')))
    _kv(pdf, "Total Columns", str(summary.get('total_columns', 'N/A')))
    _kv(pdf, "Numeric Cols",  str(summary.get('numeric_columns', 'N/A')))
    _kv(pdf, "Categorical",   str(summary.get('categorical_columns', 'N/A')))
    _kv(pdf, "Date Columns",  str(summary.get('date_columns', 'N/A')))
    memory = summary.get('memory_mb', summary.get('memory', 'N/A'))
    _kv(pdf, "Memory (MB)",   str(memory))
    pdf.ln(6)

    # ── 3. Column stats table ────────────────────────────────────────────────
    col_stats = analysis_data.get("column_stats", [])
    numeric_stats = [c for c in col_stats if c.get("dtype", "").startswith(("int", "float"))]
    if numeric_stats:
        _section(pdf, "Numeric Column Statistics")
        cols = [("Column", 38), ("Mean", 22), ("Std", 22), ("Min", 20), ("Median", 22), ("Max", 20), ("Missing%", 26)]
        widths = [w for _, w in cols]
        _table_header(pdf, cols)
        for i, c in enumerate(numeric_stats[:18]):
            _table_row(pdf, [
                c.get("name", "")[:18],
                f"{c.get('mean', 0):.2f}"    if c.get('mean')    is not None else "–",
                f"{c.get('std',  0):.2f}"    if c.get('std')     is not None else "–",
                f"{c.get('min',  0):.2f}"    if c.get('min')     is not None else "–",
                f"{c.get('median', 0):.2f}"  if c.get('median')  is not None else "–",
                f"{c.get('max',  0):.2f}"    if c.get('max')     is not None else "–",
                f"{c.get('missing_pct', 0):.1f}%",
            ], widths, even=(i % 2 == 0))
        pdf.ln(6)

    # Missing data summary
    missing_pct = quality.get("missing_pct", {})
    high_missing = {k: v for k, v in missing_pct.items() if v > 5}
    if high_missing:
        _section(pdf, "Columns with High Missing Data (> 5%)")
        for col_name, pct in list(high_missing.items())[:15]:
            clr = _C_ERR if pct > 20 else _C_WARN
            pdf.set_fill_color(*clr)
            pdf.set_text_color(*_C_BG)
            pdf.set_font("Helvetica", "B", 8)
            bar_w = min(int(pct * 1.5), 90)
            pdf.cell(55, 6, f"  {col_name[:22]}", fill=False)
            pdf.set_text_color(*clr)
            pdf.set_font("Helvetica", "", 8)
            pdf.cell(0, 6, f"{pct:.1f}%", ln=True)
        pdf.set_text_color(*_C_WHITE)
        pdf.ln(4)

    # ── 4. Forecast section ───────────────────────────────────────────────────
    if forecast_data:
        pdf.add_page()
        pdf.set_fill_color(*_C_BG)
        pdf.rect(0, 0, 210, 297, style="F")
        pdf.set_fill_color(*_C_PRIMARY)
        pdf.rect(0, 0, 210, 4, style="F")
        pdf.ln(6)

        _section(pdf, "Revenue Forecast")
        horizon = forecast_data.get("horizon_days", "N/A")
        metrics = forecast_data.get("model_metrics", {})
        _kv(pdf, "Forecast Horizon", f"{horizon} days")
        _kv(pdf, "MAPE",  f"{metrics.get('mape', 'N/A')}")
        _kv(pdf, "MAE",   f"{metrics.get('mae',  'N/A')}")
        _kv(pdf, "RMSE",  f"{metrics.get('rmse', 'N/A')}")
        pdf.ln(4)

        points = forecast_data.get("forecast", [])
        if points:
            _kv(pdf, "Forecast Start", str(points[0].get("date", "")[:10]))
            _kv(pdf, "Forecast End",   str(points[-1].get("date", "")[:10]))
            predicted_vals = [p.get("predicted", 0) for p in points if p.get("predicted")]
            if predicted_vals:
                _kv(pdf, "Avg Predicted", f"{sum(predicted_vals)/len(predicted_vals):,.0f}")
                _kv(pdf, "Peak Predicted",f"{max(predicted_vals):,.0f}")
            pdf.ln(6)

            # Sample table: first 10 + last 5 rows
            _section(pdf, "Forecast Sample (first 10 / last 5 days)")
            tcols = [("Date", 45), ("Predicted", 40), ("Lower Bound", 42), ("Upper Bound", 43)]
            twidths = [w for _, w in tcols]
            _table_header(pdf, tcols)
            sample = points[:10] + points[-5:]
            for i, p in enumerate(sample):
                _table_row(pdf, [
                    str(p.get("date", ""))[:10],
                    f"{p.get('predicted', 0):,.0f}",
                    f"{p.get('lower_bound', 0):,.0f}",
                    f"{p.get('upper_bound', 0):,.0f}",
                ], twidths, even=(i % 2 == 0))

    # ── 5. Segment profiles ───────────────────────────────────────────────────
    if segment_data:
        pdf.add_page()
        pdf.set_fill_color(*_C_BG)
        pdf.rect(0, 0, 210, 297, style="F")
        pdf.set_fill_color(*_C_PRIMARY)
        pdf.rect(0, 0, 210, 4, style="F")
        pdf.ln(6)

        _section(pdf, "Customer Segments (RFM + KMeans)")
        n_seg = segment_data.get("n_segments", "N/A")
        total_cust = segment_data.get("total_customers", "N/A")
        _kv(pdf, "Total Segments",   str(n_seg))
        _kv(pdf, "Total Customers",  str(total_cust))
        pdf.ln(4)

        profiles = segment_data.get("profiles", [])
        if profiles:
            scols = [("Segment", 52), ("Customers", 28), ("%", 18), ("Avg Recency", 30), ("Avg Freq", 24), ("Avg Monetary", 28)]
            swidths = [w for _, w in scols]
            _table_header(pdf, scols)
            for i, seg in enumerate(profiles):
                _table_row(pdf, [
                    str(seg.get("label", seg.get("segment_label", f"Segment {i}")))[:24],
                    str(seg.get("size",        seg.get("customers", "–"))),
                    f"{seg.get('pct_of_total', 0):.1f}%",
                    f"{seg.get('avg_recency',  0):.0f}d",
                    f"{seg.get('avg_frequency',seg.get('avg_freq', 0)):.1f}",
                    f"${seg.get('avg_monetary',0):,.0f}",
                ], swidths, even=(i % 2 == 0))

    # ── 6. Data quality detail ────────────────────────────────────────────────
    warnings = quality.get("warnings", [])
    if warnings:
        if pdf.get_y() > 220:
            pdf.add_page()
            pdf.set_fill_color(*_C_BG)
            pdf.rect(0, 0, 210, 297, style="F")
            pdf.set_fill_color(*_C_PRIMARY)
            pdf.rect(0, 0, 210, 4, style="F")
            pdf.ln(6)
        else:
            pdf.ln(8)

        _section(pdf, "Data Quality Warnings")
        pdf.set_font("Helvetica", "", 9)
        for w in warnings:
            pdf.set_text_color(*_C_WARN)
            pdf.cell(6, 6, "!")
            pdf.set_text_color(*_C_WHITE)
            pdf.cell(0, 6, str(w)[:100], ln=True)

    # ── Footer on every page ─────────────────────────────────────────────────
    pdf.set_fill_color(*_C_PRIMARY)
    pdf.rect(0, 293, 210, 4, style="F")

    # ── Output ────────────────────────────────────────────────────────────────
    raw = pdf.output()
    pdf_bytes = bytes(raw) if not isinstance(raw, bytes) else raw

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(pdf_bytes)
        logger.info(f"PDF report saved: {out}")

    logger.info("PDF report generated in memory (%d bytes)", len(pdf_bytes))
    return pdf_bytes
