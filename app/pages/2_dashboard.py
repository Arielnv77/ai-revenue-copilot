""" Dashboard · Design v4"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.visualization.charts import revenue_time_series, correlation_heatmap, distribution_chart
from src.preprocessing.feature_engineering import aggregate_revenue_by_period
st.set_page_config(page_title="Dashboard | RevenueOS", page_icon="", layout="wide")
from _shared_css import SHARED; from _sidebar import render_sidebar
st.markdown(SHARED, unsafe_allow_html=True); render_sidebar()

if st.session_state.get("dataset_clean") is None:
    st.markdown("""<div class="rc-topbar"><div class="rc-topbar-left"><div class="rc-logo-mark">R</div><span class="rc-logo-name">RevenueOS</span><div class="rc-sep"></div><span class="rc-crumb">Dashboard</span></div></div><div class="rc-page"><div class="rc-empty"><span class="rc-empty-icon"></span><div class="rc-empty-ttl">No dataset loaded</div><div class="rc-empty-sub">Go to Upload first.</div></div></div>""",unsafe_allow_html=True); st.stop()

df=st.session_state.dataset_clean; fname=st.session_state.get("filename","dataset.csv")
nc=df.select_dtypes(include=["number"]).columns.tolist()
dc=df.select_dtypes(include=["datetime64"]).columns.tolist()
cc=df.select_dtypes(include=["object","category"]).columns.tolist()

st.markdown(f"""<div class="rc-topbar"><div class="rc-topbar-left"><div class="rc-logo-mark">R</div><span class="rc-logo-name">RevenueOS</span><div class="rc-sep"></div><span class="rc-crumb">Dashboard</span></div><div class="rc-topbar-right"><span class="rc-pill green"><span class="rc-dot"></span>Live</span><span style="font-size:0.72rem;color:#4a7c59;padding:3px 8px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);border-radius:4px;font-family:'JetBrains Mono',monospace;">{fname}</span></div></div>""",unsafe_allow_html=True)
st.markdown('<div class="rc-page">',unsafe_allow_html=True)
st.markdown(f"""<div class="rc-page-hd"><div><div class="rc-title">Analysis Dashboard</div><div class="rc-sub">{df.shape[0]:,} rows · {df.shape[1]} columns · {df.memory_usage(deep=True).sum()/1024**2:.1f} MB</div></div><span class="rc-tag green">Auto-EDA</span></div>""",unsafe_allow_html=True)

if nc:
    st.markdown('<div style="font-size:0.67rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#4a7c59;margin-bottom:0.75rem;">Key metrics</div>',unsafe_allow_html=True)
    kc=st.columns(min(4,len(nc)))
    for i,cn in enumerate(nc[:4]):
        s=df[cn]; tot=s.sum(); h=len(s)//2; dl=None
        if h>0:
            h1,h2=s.iloc[:h].mean(),s.iloc[h:].mean()
            if h1: dl=f"{(h2-h1)/abs(h1)*100:+.1f}% vs prior"
        with kc[i]: st.metric(cn.replace("_"," ").title(),f"{tot:,.0f}" if abs(tot)<1e9 else f"{tot/1e6:.1f}M",delta=dl or f"avg {s.mean():,.1f}")
st.markdown("<br>",unsafe_allow_html=True)

PL=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_family="DM Sans",margin=dict(l=0,r=0,t=20,b=0),xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),legend=dict(bgcolor="rgba(0,0,0,0)"))
t1,t2,t3,t4=st.tabs(["Time Series","Distributions","Correlations","Summary Stats"])

with t1:
    if not dc: st.markdown('<div class="rc-empty"><span class="rc-empty-icon">📅</span><div class="rc-empty-ttl">No date columns</div></div>',unsafe_allow_html=True)
    else:
        st.markdown('<div class="rc-ctrl"><div class="rc-ctrl-ttl">Configuration</div>',unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1: sd=st.selectbox("Date column",dc,key="ts_d")
        with c2: sv=st.selectbox("Value column",nc,key="ts_v")
        with c3: sp=st.selectbox("Aggregate by",["D","W","M"],index=1,format_func=lambda x:{"D":"Day","W":"Week","M":"Month"}[x],key="ts_p")
        st.markdown('</div>',unsafe_allow_html=True)
        try:
            ts=aggregate_revenue_by_period(df,sd,sv,sp); pl={"D":"days","W":"weeks","M":"months"}[sp]
            st.markdown(f"""<div class="rc-strip"><div class="rc-scell"><div class="rc-slbl">Total</div><div class="rc-sval">{ts['revenue_sum'].sum():,.0f}</div></div><div class="rc-scell"><div class="rc-slbl">Peak</div><div class="rc-sval">{ts['revenue_sum'].max():,.0f}</div></div><div class="rc-scell"><div class="rc-slbl">Avg</div><div class="rc-sval">{ts['revenue_sum'].mean():,.0f}</div></div><div class="rc-scell"><div class="rc-slbl">Periods</div><div class="rc-sval">{len(ts)} {pl}</div></div></div>""",unsafe_allow_html=True)
            fig=revenue_time_series(ts,"date","revenue_sum"); fig.update_layout(**PL); st.plotly_chart(fig,width='stretch',theme=None)
        except Exception as e: st.markdown(f'<div class="rc-err"><div class="rc-err-ttl">Chart error</div><div class="rc-err-body">{e}</div></div>',unsafe_allow_html=True)

with t2:
    if not nc: st.info("No numeric columns.")
    else:
        cl,cr=st.columns([1,3],gap="large")
        with cl:
            sc=st.selectbox("Column",nc,key="dist_c"); s=df[sc].dropna()
            for lbl,val in [("Count",f"{len(s):,}"),("Mean",f"{s.mean():,.2f}"),("Median",f"{s.median():,.2f}"),("Std",f"{s.std():,.2f}"),("Min",f"{s.min():,.2f}"),("Max",f"{s.max():,.2f}")]:
                st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.06);font-size:0.8rem;"><span style="color:#4a7c59;">{lbl}</span><span style="color:#ffffff;font-weight:500;">{val}</span></div>""",unsafe_allow_html=True)
        with cr:
            try: fig=distribution_chart(df,sc); fig.update_layout(**PL); st.plotly_chart(fig,width='stretch',theme=None)
            except Exception as e: st.markdown(f'<div class="rc-err"><div class="rc-err-body">{e}</div></div>',unsafe_allow_html=True)

with t3:
    if len(nc)<2: st.markdown('<div class="rc-empty"><span class="rc-empty-icon">🔗</span><div class="rc-empty-ttl">Need 2+ numeric columns</div></div>',unsafe_allow_html=True)
    else:
        cl,cr=st.columns([1,3],gap="large")
        with cl: cs=st.multiselect("Columns",nc,default=nc[:min(8,len(nc))],key="corr_c")
        with cr:
            if len(cs)>=2:
                try: fig=correlation_heatmap(df[cs]); fig.update_layout(**PL); st.plotly_chart(fig,width='stretch',theme=None)
                except Exception as e: st.markdown(f'<div class="rc-err"><div class="rc-err-body">{e}</div></div>',unsafe_allow_html=True)

with t4:
    it1,it2,it3=st.tabs(["Numeric","Categorical","Raw data"])
    with it1:
        if nc: st.dataframe(df[nc].describe().round(3),width='stretch')
    with it2:
        for c in cc[:5]:
            with st.expander(f"{c} — {df[c].nunique()} unique values"):
                vc=df[c].value_counts().reset_index(); vc.columns=[c,"count"]; vc["pct"]=(vc["count"]/len(df)*100).round(1)
                st.dataframe(vc.head(20),width='stretch')
    with it3:
        n=st.slider("Rows",5,200,25,key="raw_n"); st.dataframe(df.head(n),width='stretch')

st.markdown(f'<div class="rc-footer"><span>RevenueOS · Dashboard</span><span>{df.shape[0]:,} rows · {df.shape[1]} cols</span></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)