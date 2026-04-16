"""Report · Design v4 — Full PDF export page."""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.visualization.report import generate_pdf_report
from _i18n import t
st.set_page_config(page_title="Report | RevenueOS", page_icon="app/assets/logo.png", layout="wide")
from _shared_css import SHARED; from _sidebar import render_sidebar
st.markdown(SHARED, unsafe_allow_html=True); render_sidebar()

st.markdown('<div class="rc-page">',unsafe_allow_html=True)
st.markdown("""<div class="rc-page-hd"><div><div class="rc-title>{t("report_title")}</div><div class="rc-sub">{t("report_sub")}</div></div><span class="rc-tag blue">PDF</span></div>""",unsafe_allow_html=True)

df   = st.session_state.get("dataset_clean")
qr   = st.session_state.get("quality_report")
fname= st.session_state.get("filename","dataset.csv")

if df is None:
    st.markdown(f"""<div class="rc-empty"><span class="rc-empty-icon">–</span><div class="rc-empty-ttl">{t("no_dataset_loaded")}</div><div class="rc-empty-sub">{t("report_upload_first")}</div></div>""",unsafe_allow_html=True)
else:
    from src.data.validator import validate_dataframe
    from src.data.loader import get_dataframe_profile
    from src.utils.constants import REVENUE_PATTERNS, DATE_PATTERNS

    profile  = get_dataframe_profile(df)
    qr_obj   = qr if qr is not None else validate_dataframe(df)
    quality  = qr_obj.to_dict()
    score    = qr_obj.quality_score

    # Build column_stats (lightweight — mean/std/min/max for numeric)
    col_stats = []
    for col in df.columns:
        s = df[col]; dtype = str(s.dtype)
        entry = {"name": col, "dtype": dtype,
                 "missing_pct": round(s.isnull().mean()*100, 1)}
        if "int" in dtype or "float" in dtype:
            d = s.describe()
            entry.update({"mean": round(float(d["mean"]),2),
                          "std":  round(float(d["std"]),2),
                          "min":  round(float(d["min"]),2),
                          "median": round(float(d["50%"]),2),
                          "max":  round(float(d["max"]),2)})
        col_stats.append(entry)

    analysis_data = {
        "filename": fname,
        "summary": {
            "total_rows":         profile["rows"],
            "total_columns":      profile["columns"],
            "numeric_columns":    profile.get("numeric_cols", len([c for c in col_stats if "int" in c["dtype"] or "float" in c["dtype"]])),
            "categorical_columns":profile.get("categorical_cols", len([c for c in col_stats if "object" in c["dtype"]])),
            "date_columns":       profile.get("date_cols", 0),
            "memory_mb":          profile["memory_mb"],
        },
        "column_stats":   col_stats,
        "quality_report": quality,
    }

    # ── UI ────────────────────────────────────────────────────────────────────
    bc = "#4ade80" if score>=80 else "#facc15" if score>=60 else "#f87171"
    c1, c2, c3 = st.columns(3)
    c1.metric(t("rows"),          f"{profile['rows']:,}")
    c2.metric(t("columns"),       f"{profile['columns']}")
    c3.metric(t("quality_score"), f"{score:.0f}/100")

    st.markdown("<br>",unsafe_allow_html=True)

    # Optional sections info
    st.markdown(f"""<div class="rc-card"><div class="rc-card-hd"><span class="rc-card-ttl">{t("report_contents")}</span></div>
<div style="padding:1.25rem 1.5rem;color:#a0aec0;font-size:0.85rem;line-height:1.9;">
  <b style="color:#fff">{t("always_included")}</b><br>
  &nbsp;· &nbsp;Cover page — filename, timestamp, quality score badge<br>
  &nbsp;· &nbsp;Dataset overview — shape, dtypes, memory<br>
  &nbsp;· &nbsp;Numeric column statistics table<br>
  &nbsp;· &nbsp;Missing data breakdown<br>
  &nbsp;· &nbsp;Quality warnings list<br>
  <br><b style="color:#fff">{t("if_available")}</b><br>
  &nbsp;· &nbsp;Forecast summary + sample table (run Forecast page)<br>
  &nbsp;· &nbsp;Segment profile table (run Segments page)<br>
</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    # Forecast data from session state
    forecast_data = st.session_state.get("forecast_result")

    # Segment data from session state
    seg_raw = st.session_state.get("segment_result")
    segment_data = None
    if seg_raw is not None:
        try:
            profiles = []
            for _, row in seg_raw.iterrows():
                profiles.append({
                    "label":         row.get("segment_label", f"Segment {row.get('segment_id','')}"),
                    "size":          int(seg_raw[seg_raw.get("segment_label","x")==row.get("segment_label","x")].shape[0]) if "segment_label" in seg_raw.columns else "–",
                    "pct_of_total":  0,
                    "avg_recency":   float(row.get("recency",0)),
                    "avg_frequency": float(row.get("frequency",0)),
                    "avg_monetary":  float(row.get("monetary",0)),
                })
            # Aggregate by label
            import pandas as pd
            grp = seg_raw.groupby("segment_label").agg(
                size=("recency","count"),
                avg_recency=("recency","mean"),
                avg_frequency=("frequency","mean"),
                avg_monetary=("monetary","mean"),
            ).reset_index()
            grp["pct_of_total"] = (grp["size"] / grp["size"].sum() * 100).round(1)
            profiles = grp.rename(columns={"segment_label":"label"}).to_dict("records")
            segment_data = {"n_segments": len(profiles),
                            "total_customers": len(seg_raw),
                            "profiles": profiles}
        except Exception:
            pass

    # Generate button
    if st.button(t("generate_pdf"), type="primary", use_container_width=True):
        with st.spinner(t("building_pdf")):
            try:
                pdf_bytes = generate_pdf_report(
                    analysis_data=analysis_data,
                    forecast_data=forecast_data,
                    segment_data=segment_data,
                )
                ts = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M")
                st.download_button(
                    label=t("download_pdf"),
                    data=pdf_bytes,
                    file_name=f"revenueos_report_{ts}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.success(f"Report ready — {len(pdf_bytes):,} bytes")
            except Exception as e:
                st.error(f"PDF generation failed: {e}")

st.markdown('<div class="rc-footer"><span>RevenueOS · Report</span><span>fpdf2</span></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)
