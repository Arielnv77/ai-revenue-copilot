"""
Report — PDF/HTML report generator.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def generate_pdf_report(
    analysis_data: dict[str, Any],
    output_path: str | Path = "report.pdf",
) -> Path:
    """
    Generate a PDF analysis report.

    Args:
        analysis_data: Dict with summary, quality_report, key metrics.
        output_path: Where to save the PDF.

    Returns:
        Path to the generated PDF.
    """
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 20, "AI Revenue Copilot", ln=True, align="C")
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 10, "Revenue Analysis Report", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
    pdf.ln(20)

    # Summary section
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Dataset Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)

    summary = analysis_data.get("summary", {})
    for key, value in summary.items():
        pdf.cell(0, 8, f"  {key}: {value}", ln=True)
    pdf.ln(10)

    # Quality report
    quality = analysis_data.get("quality_report", {})
    if quality:
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Data Quality", ln=True)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, f"  Quality Score: {quality.get('quality_score', 'N/A')}/100", ln=True)
        pdf.cell(0, 8, f"  Duplicate Rows: {quality.get('duplicate_rows', 0)}", ln=True)

        warnings = quality.get("warnings", [])
        if warnings:
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(0, 8, "  Warnings:", ln=True)
            pdf.set_font("Helvetica", "", 10)
            for w in warnings:
                pdf.cell(0, 7, f"    • {w}", ln=True)
    pdf.ln(10)

    # Key insights (placeholder)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Key Insights", ln=True)
    pdf.set_font("Helvetica", "", 11)

    insights = analysis_data.get("insights", [
        "Revenue trends have been analyzed",
        "Customer segments have been identified",
        "Anomalies detected and flagged",
    ])
    for insight in insights:
        pdf.cell(0, 8, f"  • {insight}", ln=True)

    # Save
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))
    logger.info(f"PDF report generated: {output_path}")
    return output_path
