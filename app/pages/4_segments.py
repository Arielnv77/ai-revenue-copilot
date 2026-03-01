""" Segments · Design v4"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.preprocessing.feature_engineering import compute_rfm, assign_rfm_labels
from src.models.segmentation import CustomerSegmenter
from src.visualization.charts import segmentation_chart, rfm_scatter
st.set_page_config(page_title="Segments | RevenueOS", page_icon="", layout="wide")
from _shared_css import SHARED; from _sidebar import render_sidebar
st.markdown(SHARED, unsafe_allow_html=True); render_sidebar()

st.markdown("""<div class="rc-topbar"><div class="rc-topbar-left"><div class="rc-logo-mark">R</div><span class="rc-logo-name">RevenueOS</span><div class="rc-sep"></div><span class="rc-crumb">Segments</span></div><div class="rc-topbar-right"><span class="rc-pill blue">RFM + KMeans</span></div></div>""",unsafe_allow_html=True)
st.markdown('<div class="rc-page">',unsafe_allow_html=True)
st.markdown("""<div class="rc-page-hd"><div><div class="rc-title">Customer Segmentation</div><div class="rc-sub">RFM analysis · KMeans clustering · behavioral labeling</div></div><span class="rc-tag blue">ML Model</span></div>""",unsafe_allow_html=True)

if st.session_state.get("dataset_clean") is None:
    st.markdown("""<div class="rc-empty"><span class="rc-empty-icon"></span><div class="rc-empty-ttl">No dataset loaded</div><div class="rc-empty-sub">Go to Upload first.</div></div>""",unsafe_allow_html=True); st.stop()

df=st.session_state.dataset_clean; ac=df.columns.tolist()
dcs=df.select_dtypes(include=["datetime64"]).columns.tolist()
ncs=df.select_dtypes(include=["number"]).columns.tolist()

st.markdown("""<div style="display:flex;gap:1px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.06);border-radius:12px;overflow:hidden;margin-bottom:1.5rem;"><div style="flex:1;background:#0c1810;padding:1.1rem 1.4rem;border-right:1px solid rgba(255,255,255,0.06);"><div style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.5rem;font-weight:800;color:#4ade80;margin-bottom:4px;">R</div><div style="font-size:0.83rem;font-weight:700;color:#ffffff;margin-bottom:2px;">Recency</div><div style="font-size:0.75rem;color:#4a7c59;">How recently did the customer purchase?</div></div><div style="flex:1;background:#0c1810;padding:1.1rem 1.4rem;border-right:1px solid rgba(255,255,255,0.06);"><div style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.5rem;font-weight:800;color:#22d3ee;margin-bottom:4px;">F</div><div style="font-size:0.83rem;font-weight:700;color:#ffffff;margin-bottom:2px;">Frequency</div><div style="font-size:0.75rem;color:#4a7c59;">How often do they buy?</div></div><div style="flex:1;background:#0c1810;padding:1.1rem 1.4rem;"><div style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.5rem;font-weight:800;color:#a3e635;margin-bottom:4px;">M</div><div style="font-size:0.83rem;font-weight:700;color:#ffffff;margin-bottom:2px;">Monetary</div><div style="font-size:0.75rem;color:#4a7c59;">How much total revenue do they generate?</div></div></div>""",unsafe_allow_html=True)

cc,cn=st.columns([2.2,1],gap="large")
with cc:
    st.markdown('<div class="rc-ctrl"><div class="rc-ctrl-ttl">Column mapping</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: cust=st.selectbox("Customer ID",ac,key="sg_c")
    with c2: dcol=st.selectbox("Date column",dcs if dcs else ac,key="sg_d")
    with c3: rcol=st.selectbox("Revenue col",ncs if ncs else ac,key="sg_r")
    st.markdown('</div>',unsafe_allow_html=True)
with cn:
    nk=st.slider("Segments",2,8,4,key="sg_n")
    st.markdown(f"""<div class="rc-card" style="text-align:center;"><div style="padding:1.5rem;"><div style="font-size:0.65rem;color:#4a7c59;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:0.4rem;">Clusters</div><div style="font-family:'Bricolage Grotesque',sans-serif;font-size:3.5rem;font-weight:800;line-height:1;background:linear-gradient(135deg,#4ade80,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{nk}</div><div style="font-size:0.72rem;color:#4a7c59;margin-top:4px;">KMeans segments</div></div></div>""",unsafe_allow_html=True)

st.markdown("<br>",unsafe_allow_html=True)
bc,_=st.columns([1,3])
with bc: run=st.button("Run Segmentation →",type="primary",width='stretch')
st.markdown("<br>",unsafe_allow_html=True)

PL=dict(template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_family="DM Sans",margin=dict(l=0,r=0,t=20,b=0),xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),legend=dict(bgcolor="rgba(0,0,0,0)"))
if run:
    with st.spinner("Computing RFM + clustering…"):
        try:
            rfm=compute_rfm(df,cust,dcol,rcol); rfm=assign_rfm_labels(rfm)
            seg=CustomerSegmenter(n_clusters=nk); seg.fit(rfm); rs=seg.predict(rfm)
            km1,km2,km3,km4=st.columns(4)
            km1.metric("Total Customers",f"{len(rs):,}"); km2.metric("Segments",nk)
            km3.metric("Avg Monetary",f"${rs['monetary'].mean():,.0f}"); km4.metric("Avg Frequency",f"{rs['frequency'].mean():.1f}x")
            st.markdown("<br>",unsafe_allow_html=True)
            tv,tp,tl,td=st.tabs(["Visualizations","Segment Profiles","RFM Labels","Full Data"])
            with tv:
                cl2,cr2=st.columns(2,gap="large")
                with cl2: fig=segmentation_chart(rs); fig.update_layout(**PL); st.plotly_chart(fig,width='stretch',theme=None)
                with cr2: fig=rfm_scatter(rs); fig.update_layout(**PL); st.plotly_chart(fig,width='stretch',theme=None)
            with tp:
                p=seg.get_profiles()
                if p is not None: st.dataframe(p.round(2),width='stretch')
                else: st.info("Profile not available.")
            with tl:
                if "segment_label" in rs.columns:
                    lc=rs["segment_label"].value_counts().reset_index(); lc.columns=["Segment","Customers"]; lc["Pct"]=(lc["Customers"]/len(rs)*100).round(1)
                    SC={"Champions":"#4ade80","Loyal Customers":"#22d3ee","Potential Loyalist":"#a3e635","At Risk":"#facc15","Lost":"#f87171"}
                    for _,row in lc.iterrows():
                        clr=SC.get(row["Segment"],"#6da882")
                        st.markdown(f"""<div style="background:#0c1810;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:1rem 1.25rem;margin-bottom:6px;"><div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;"><div style="display:flex;align-items:center;gap:8px;"><div style="width:8px;height:8px;border-radius:50%;background:{clr};"></div><span style="font-weight:600;font-size:0.85rem;color:#ffffff;">{row['Segment']}</span></div><span style="font-family:'Bricolage Grotesque',sans-serif;font-size:1rem;font-weight:800;color:{clr};">{row['Customers']:,}</span></div><div class="rc-bw"><div class="rc-b" style="width:{row['Pct']}%;background:{clr};"></div></div><div style="font-size:0.68rem;color:#4a7c59;margin-top:3px;">{row['Pct']}% of base</div></div>""",unsafe_allow_html=True)
            with td: st.dataframe(rs.round(2).reset_index(drop=True),width='stretch')
        except Exception as e: st.markdown(f'<div class="rc-err"><div class="rc-err-ttl">Failed</div><div class="rc-err-body">{e}</div></div>',unsafe_allow_html=True)
else: st.markdown("""<div class="rc-empty"><span class="rc-empty-icon"></span><div class="rc-empty-ttl">Map your customer segments</div><div class="rc-empty-sub">Configure columns above and click Run Segmentation.</div></div>""",unsafe_allow_html=True)
st.markdown('<div class="rc-footer"><span>RevenueOS · Segments</span><span>RFM · KMeans</span></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)