""" Upload · Design v4"""
import streamlit as st, pandas as pd, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.data.loader import load_csv, get_dataframe_profile
from src.data.validator import validate_dataframe
from src.preprocessing.cleaner import run_cleaning_pipeline
st.set_page_config(page_title="Upload | RevenueOS", page_icon="", layout="wide")
from _shared_css import SHARED; from _sidebar import render_sidebar
st.markdown(SHARED, unsafe_allow_html=True)
render_sidebar()

st.markdown("""
<div class="rc-topbar">
  <div class="rc-topbar-left">
    <div class="rc-logo-mark">R</div><span class="rc-logo-name">RevenueOS</span>
    <div class="rc-sep"></div><span class="rc-crumb">Upload</span>
  </div>
  <div class="rc-topbar-right"><span class="rc-pill gray">Step 1 of 5</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="rc-page">', unsafe_allow_html=True)
st.markdown("""<div class="rc-page-hd"><div><div class="rc-title">Upload Dataset</div><div class="rc-sub">Import a CSV to begin your revenue analysis · Supports up to 50 MB</div></div><span class="rc-tag green">CSV Import</span></div>""", unsafe_allow_html=True)

col_up, col_info = st.columns([1.7, 1], gap="large")
with col_up:
    st.markdown('<div style="font-size:0.67rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#4a7c59;margin-bottom:0.75rem;">Import file</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drop CSV here", type=["csv"], label_visibility="collapsed")

with col_info:
    st.markdown("""
<div class="rc-card">
  <div class="rc-card-hd"><span class="rc-card-ttl">Sample datasets</span></div>
  <div>
    <div style="border-bottom:1px solid rgba(255,255,255,0.06);padding:1rem 1.5rem;display:flex;gap:12px;align-items:flex-start;">
      <span style="font-size:1rem;flex-shrink:0;">🛒</span>
      <div><div style="font-size:0.83rem;font-weight:600;color:#ffffff;margin-bottom:1px;">Online Retail II (UCI)</div><div style="font-size:0.73rem;color:#4a7c59;">UK e-commerce · 1M+ rows</div></div>
    </div>
    <div style="border-bottom:1px solid rgba(255,255,255,0.06);padding:1rem 1.5rem;display:flex;gap:12px;align-items:flex-start;">
      <span style="font-size:1rem;flex-shrink:0;">🏪</span>
      <div><div style="font-size:0.83rem;font-weight:600;color:#ffffff;margin-bottom:1px;">Superstore Sales</div><div style="font-size:0.73rem;color:#4a7c59;">Clean US retail · ideal for RFM</div></div>
    </div>
    <div style="padding:1rem 1.5rem;display:flex;gap:12px;align-items:flex-start;">
      <span style="font-size:1rem;flex-shrink:0;">📦</span>
      <div><div style="font-size:0.83rem;font-weight:600;color:#ffffff;margin-bottom:1px;">Brazilian E-Commerce</div><div style="font-size:0.73rem;color:#4a7c59;">Olist multi-table orders dataset</div></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if uploaded_file is not None:
    with st.spinner("Profiling and cleaning dataset…"):
        df = load_csv(uploaded_file); st.session_state.dataset = df
        qr = validate_dataframe(df); st.session_state.quality_report = qr
        df_clean = run_cleaning_pipeline(df.copy())
        st.session_state.dataset_clean = df_clean; st.session_state.filename = uploaded_file.name
    profile = get_dataframe_profile(df_clean); score = qr.quality_score

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""<div style="background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.20);border-radius:var(--r-md);padding:0.9rem 1.4rem;display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;"><div style="display:flex;align-items:center;gap:10px;"><span>✅</span><div><div style="font-size:0.85rem;font-weight:600;color:#4ade80;">{uploaded_file.name}</div><div style="font-size:0.75rem;color:#4a7c59;">{profile['rows']:,} rows · {profile['columns']} columns · {profile['memory_mb']} MB</div></div></div><span class="rc-tag green">Loaded</span></div>""", unsafe_allow_html=True)

    k1,k2,k3,k4 = st.columns(4)
    k1.metric("Rows",f"{profile['rows']:,}"); k2.metric("Columns",f"{profile['columns']}")
    k3.metric("Memory",f"{profile['memory_mb']} MB"); k4.metric("Quality Score",f"{score:.0f}/100")

    bc = "#4ade80" if score>=80 else "#facc15" if score>=60 else "#f87171"
    st.markdown(f"""<div style="margin:0.5rem 0 1.75rem;"><div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#4a7c59;margin-bottom:4px;"><span>Data quality</span><span style="color:{bc};font-weight:600;">{score:.0f}%</span></div><div class="rc-bw"><div class="rc-b" style="width:{score}%;background:{bc};"></div></div></div>""", unsafe_allow_html=True)

    t1,t2,t3 = st.tabs(["Data Preview","Column Inspector","Quality Report"])
    with t1:
        n = st.slider("Rows",5,100,20,key="pn")
        st.dataframe(df_clean.head(n),width='stretch')
    with t2:
        for cn in df_clean.columns:
            s=df_clean[cn]; dtype=str(s.dtype); np=s.isnull().mean()*100
            nc="#f87171" if np>20 else "#facc15" if np>5 else "#4ade80"
            tl = "int" if "int" in dtype else "float" if "float" in dtype else "text" if "object" in dtype else "date" if "date" in dtype else dtype[:5]
            tc = "blue" if tl in("int","float") else "green" if tl=="text" else "gold" if tl=="date" else "gray"
            st.markdown(f"""<div style="background:#0c1810;border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:9px 14px;margin-bottom:5px;display:flex;align-items:center;gap:1rem;flex-wrap:wrap;"><div style="flex:2;min-width:120px;font-size:0.83rem;font-weight:600;color:#ffffff;">{cn}</div><span class="rc-tag {tc}">{tl}</span><div style="flex:1;text-align:right;"><div style="font-size:0.62rem;color:#4a7c59;text-transform:uppercase;letter-spacing:0.07em;">Nulls</div><div style="font-size:0.8rem;font-weight:600;color:{nc};">{np:.1f}%</div></div><div style="flex:1;text-align:right;"><div style="font-size:0.62rem;color:#4a7c59;text-transform:uppercase;letter-spacing:0.07em;">Unique</div><div style="font-size:0.8rem;font-weight:600;color:#ffffff;">{s.nunique():,}</div></div></div>""", unsafe_allow_html=True)
    with t3:
        report = qr.to_dict()
        if report["warnings"]:
            for w in report["warnings"]: st.markdown(f"""<div style="background:rgba(234,179,8,0.07);border:1px solid rgba(234,179,8,0.20);border-radius:8px;padding:8px 14px;font-size:0.82rem;color:#facc15;margin-bottom:5px;">⚠ {w}</div>""", unsafe_allow_html=True)
        else: st.markdown("""<div style="background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.20);border-radius:10px;padding:0.9rem 1.25rem;display:flex;align-items:center;gap:10px;"><span>✅</span><span style="font-size:0.85rem;font-weight:600;color:#4ade80;">No quality issues detected</span></div>""", unsafe_allow_html=True)
        if report.get("missing_pct"):
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#4a7c59;margin-bottom:0.75rem;">Missing values</div>',unsafe_allow_html=True)
            for col_name,pct in report["missing_pct"].items():
                clr="#f87171" if pct>20 else "#facc15" if pct>5 else "#4ade80"
                st.markdown(f"""<div style="margin-bottom:8px;"><div style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:3px;"><span style="color:#6da882;">{col_name}</span><span style="color:{clr};font-weight:600;">{pct:.1f}%</span></div><div class="rc-bw"><div class="rc-b" style="width:{min(pct,100)}%;background:{clr};"></div></div></div>""", unsafe_allow_html=True)
        dup=report.get("duplicate_rows",0); dp=report.get("duplicate_pct",0)
        st.markdown(f"""<div style="background:#0c1810;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:0.9rem 1.25rem;display:flex;align-items:center;justify-content:space-between;margin-top:1rem;"><span style="font-size:0.83rem;color:#6da882;">Duplicate rows</span><div><span style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.1rem;font-weight:800;color:{'#facc15' if dp>0 else '#4ade80'};">{dup}</span><span style="font-size:0.72rem;color:#4a7c59;margin-left:6px;">({dp:.1f}%)</span></div></div>""", unsafe_allow_html=True)
    st.markdown(f'<div class="rc-footer"><span>RevenueOS · Upload</span><span>{df_clean.shape[0]:,} rows · {df_clean.shape[1]} cols</span></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)