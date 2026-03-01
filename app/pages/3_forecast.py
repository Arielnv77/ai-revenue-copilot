"""📈 Forecast · Design v4"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.models.forecaster import RevenueForecaster, prepare_forecast_data
from src.preprocessing.feature_engineering import aggregate_revenue_by_period
from src.visualization.charts import forecast_chart
st.set_page_config(page_title="Forecast | Revenue Copilot", page_icon="📈", layout="wide")
from _shared_css import SHARED; from _sidebar import render_sidebar
st.markdown(SHARED, unsafe_allow_html=True); render_sidebar()

st.markdown("""<div class="rc-topbar"><div class="rc-topbar-left"><div class="rc-logo-mark">⚡</div><span class="rc-logo-name">Revenue Copilot</span><div class="rc-sep"></div><span class="rc-crumb">Forecast</span></div><div class="rc-topbar-right"><span class="rc-pill blue">Prophet ML</span></div></div>""", unsafe_allow_html=True)
st.markdown('<div class="rc-page">', unsafe_allow_html=True)
st.markdown("""<div class="rc-page-hd"><div><div class="rc-title">Revenue Forecast</div><div class="rc-sub">Facebook Prophet · time-series prediction with confidence intervals</div></div><span class="rc-tag blue">ML Model</span></div>""", unsafe_allow_html=True)

if st.session_state.get("dataset_clean") is None:
    st.markdown("""<div class="rc-empty"><span class="rc-empty-icon">📂</span><div class="rc-empty-ttl">No dataset loaded</div><div class="rc-empty-sub">Go to Upload in the sidebar first.</div></div>""", unsafe_allow_html=True); st.stop()

df=st.session_state.dataset_clean; dc=df.select_dtypes(include=["datetime64"]).columns.tolist(); nc=df.select_dtypes(include=["number"]).columns.tolist()
if not dc:
    st.markdown("""<div class="rc-empty"><span class="rc-empty-icon">📅</span><div class="rc-empty-ttl">No date columns found</div><div class="rc-empty-sub">Forecasting requires a datetime column.</div></div>""",unsafe_allow_html=True); st.stop()

cc,ch = st.columns([2.2,1],gap="large")
with cc:
    st.markdown('<div class="rc-ctrl"><div class="rc-ctrl-ttl">Model configuration</div>',unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: date_col=st.selectbox("Date column",dc,key="fc_d")
    with c2: val_col=st.selectbox("Value column",nc,key="fc_v")
    horizon=st.slider("Forecast horizon (days)",7,365,90,key="fc_h")
    st.markdown('</div>',unsafe_allow_html=True)
with ch:
    st.markdown(f"""<div class="rc-card" style="height:100%;"><div class="rc-card-hd"><span class="rc-card-ttl">Horizon</span></div><div style="padding:1.5rem;text-align:center;"><div style="font-family:'Bricolage Grotesque',sans-serif;font-size:3.5rem;font-weight:800;color:#ffffff;line-height:1;background:linear-gradient(135deg,#4ade80,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{horizon}</div><div style="font-size:0.68rem;color:#4a7c59;text-transform:uppercase;letter-spacing:0.09em;margin-top:4px;">days ahead</div><div style="margin-top:1.25rem;display:flex;justify-content:center;gap:1.5rem;"><div style="text-align:center;"><div style="font-size:0.95rem;font-weight:700;color:#ffffff;">{horizon//30}</div><div style="font-size:0.65rem;color:#4a7c59;text-transform:uppercase;letter-spacing:0.07em;">months</div></div><div style="text-align:center;"><div style="font-size:0.95rem;font-weight:700;color:#ffffff;">{horizon//7}</div><div style="font-size:0.65rem;color:#4a7c59;text-transform:uppercase;letter-spacing:0.07em;">weeks</div></div></div></div></div>""", unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
bc,_ = st.columns([1,3])
with bc: run=st.button("Generate Forecast →",type="primary",width='stretch')
st.markdown("<br>",unsafe_allow_html=True)

PL=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_family="DM Sans",margin=dict(l=0,r=0,t=20,b=0),xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),legend=dict(bgcolor="rgba(0,0,0,0)"))
if run:
    with st.spinner("Running Prophet model…"):
        try:
            ts=prepare_forecast_data(df,date_col,val_col,freq="D"); fc=RevenueForecaster(); fc.fit(ts); fdf=fc.predict(horizon_days=horizon)
            hist=aggregate_revenue_by_period(df,date_col,val_col,"D"); fut=fdf[fdf["date"]>ts["ds"].max()]
            km1,km2,km3,km4=st.columns(4)
            km1.metric("Predicted Total",f"${fut['predicted'].sum():,.0f}"); km2.metric("Avg Daily",f"${fut['predicted'].mean():,.0f}")
            km3.metric("Peak Day",f"${fut['predicted'].max():,.0f}"); km4.metric("Forecast Period",f"{horizon} days")
            st.markdown("<br>",unsafe_allow_html=True)
            tc,td=st.tabs(["Forecast Chart","Raw Data"])
            with tc:
                fig=forecast_chart(hist,fdf); fig.update_layout(**PL); st.plotly_chart(fig,width='stretch',theme=None)
            with td:
                st.dataframe(fut.round(2).reset_index(drop=True),width='stretch')
                with st.expander("Full forecast table"): st.dataframe(fdf.round(2),width='stretch')
        except Exception as e: st.markdown(f'<div class="rc-err"><div class="rc-err-ttl">Forecast failed</div><div class="rc-err-body">{e}</div></div>',unsafe_allow_html=True)
else: st.markdown("""<div class="rc-empty"><span class="rc-empty-icon">📈</span><div class="rc-empty-ttl">Configure and generate your forecast</div><div class="rc-empty-sub">Select columns above and click Generate Forecast.</div></div>""",unsafe_allow_html=True)
st.markdown('<div class="rc-footer"><span>Revenue Copilot · Forecast</span><span>Powered by Facebook Prophet</span></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)