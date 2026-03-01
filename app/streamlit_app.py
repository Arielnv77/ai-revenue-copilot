"""⚡ Revenue Copilot — Home · Design v4 dark emerald SaaS"""
import streamlit as st
st.set_page_config(page_title="Revenue Copilot", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
from _shared_css import SHARED
from _sidebar import render_sidebar
st.markdown(SHARED, unsafe_allow_html=True)
st.markdown("""
<style>
.hero{padding:6rem 3rem 5rem;max-width:1380px;margin:0 auto;}
.hero-ey{display:inline-flex;align-items:center;gap:8px;background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.22);border-radius:99px;padding:5px 14px;font-size:0.72rem;font-weight:700;color:#4ade80;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:2rem;}
.h-dot{width:6px;height:6px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;display:inline-block;}
.hero-h{font-family:'Bricolage Grotesque',sans-serif;font-size:clamp(2.8rem,5vw,5rem);font-weight:800;line-height:1.03;letter-spacing:-0.05em;color:#ffffff;margin-bottom:1.5rem;max-width:800px;}
.hero-h .g{background:linear-gradient(135deg,#4ade80 0%,#22d3ee 40%,#a3e635 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-s{font-size:1.05rem;color:#4a7c59;max-width:560px;line-height:1.72;margin-bottom:3rem;}
.hero-acts{display:flex;align-items:center;gap:14px;margin-bottom:5rem;}
.btn-p{display:inline-flex;align-items:center;gap:8px;background:#22c55e;color:#060e09;border-radius:8px;padding:0.7rem 1.75rem;font-weight:800;font-size:0.88rem;box-shadow:0 0 28px rgba(34,197,94,0.30);}
.btn-s{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.10);color:#6da882;border-radius:8px;padding:0.7rem 1.5rem;font-weight:600;font-size:0.88rem;}
.trust{display:flex;align-items:center;gap:1.75rem;padding:1.1rem 1.6rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;max-width:760px;flex-wrap:wrap;}
.ti{display:flex;align-items:center;gap:7px;font-size:0.78rem;color:#4a7c59;font-weight:500;}
.tc{width:16px;height:16px;border-radius:50%;background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.25);display:inline-flex;align-items:center;justify-content:center;font-size:9px;color:#4ade80;}
.sdiv{height:1px;background:rgba(255,255,255,0.06);}
.sw{padding:0 3rem;max-width:1380px;margin:0 auto;}
.sg{display:flex;gap:1px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.06);border-radius:14px;overflow:hidden;}
.sbl{flex:1;background:#090f0c;padding:1.5rem 2rem;border-right:1px solid rgba(255,255,255,0.06);}
.sbl:last-child{border-right:none;}
.sn{font-family:'Bricolage Grotesque',sans-serif;font-size:2rem;font-weight:800;color:#ffffff;line-height:1;}
.sl{font-size:0.73rem;color:#4a7c59;font-weight:500;margin-top:5px;}
.sbg{display:inline-block;background:rgba(34,197,94,0.10);border:1px solid rgba(34,197,94,0.18);color:#4ade80;border-radius:4px;padding:1px 7px;font-size:0.63rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;margin-top:5px;}
.fw{padding:5rem 3rem;max-width:1380px;margin:0 auto;}
.sec-ey{font-size:0.7rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#22c55e;margin-bottom:0.75rem;}
.sec-h{font-family:'Bricolage Grotesque',sans-serif;font-size:clamp(1.8rem,3vw,2.8rem);font-weight:800;color:#ffffff;letter-spacing:-0.04em;margin-bottom:0.75rem;line-height:1.1;}
.sec-s{font-size:0.95rem;color:#4a7c59;max-width:540px;margin-bottom:3rem;line-height:1.65;}
.fg{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.06);border-radius:20px;overflow:hidden;}
.fi{background:#090f0c;padding:2rem;transition:background 0.2s;position:relative;overflow:hidden;}
.fi::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(34,197,94,0.20),transparent);opacity:0;transition:opacity 0.2s;}
.fi:hover{background:#0c1810;}.fi:hover::before{opacity:1;}
.fic{width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:1.25rem;}
.fic1{background:rgba(34,197,94,0.10);border:1px solid rgba(34,197,94,0.20);}
.fic2{background:rgba(34,211,238,0.08);border:1px solid rgba(34,211,238,0.16);}
.fic3{background:rgba(163,230,53,0.08);border:1px solid rgba(163,230,53,0.16);}
.fic4{background:rgba(234,179,8,0.08);border:1px solid rgba(234,179,8,0.16);}
.fic5{background:rgba(167,139,250,0.08);border:1px solid rgba(167,139,250,0.16);}
.fic6{background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.16);}
.fn{font-family:'Bricolage Grotesque',sans-serif;font-size:1rem;font-weight:700;color:#ffffff;margin-bottom:0.5rem;letter-spacing:-0.02em;}
.fd{font-size:0.82rem;color:#4a7c59;line-height:1.6;}
.wfw{padding:0 3rem 5rem;max-width:1380px;margin:0 auto;}
.wg{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;}
.wc{background:#090f0c;border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:1.75rem;position:relative;overflow:hidden;transition:border-color 0.2s;}
.wc:hover{border-color:rgba(34,197,94,0.22);}
.wc::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#22c55e,#22d3ee);}
.wn{font-family:'Bricolage Grotesque',sans-serif;font-size:3rem;font-weight:800;color:rgba(34,197,94,0.12);line-height:1;margin-bottom:0.75rem;letter-spacing:-0.06em;}
.wt{font-family:'Bricolage Grotesque',sans-serif;font-size:0.95rem;font-weight:700;color:#ffffff;margin-bottom:0.35rem;}
.wd{font-size:0.8rem;color:#4a7c59;line-height:1.58;}
.ctaw{padding:0 3rem 5rem;max-width:1380px;margin:0 auto;}
.cta-box{background:linear-gradient(135deg,#0c1810 0%,#102015 50%,#0c1810 100%);border:1px solid rgba(34,197,94,0.18);border-radius:24px;padding:3.5rem;display:flex;align-items:center;justify-content:space-between;gap:2rem;position:relative;overflow:hidden;}
.cta-box::before{content:'';position:absolute;top:-60%;right:-5%;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(34,197,94,0.07) 0%,transparent 65%);pointer-events:none;}
.cta-ey{font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#22c55e;margin-bottom:0.6rem;}
.cta-h{font-family:'Bricolage Grotesque',sans-serif;font-size:1.9rem;font-weight:800;color:#ffffff;letter-spacing:-0.04em;line-height:1.1;margin-bottom:0.5rem;}
.cta-s{font-size:0.88rem;color:#4a7c59;line-height:1.6;}
.cta-btn{display:inline-flex;align-items:center;gap:10px;background:#22c55e;color:#060e09;border-radius:8px;padding:0.85rem 2rem;font-weight:800;font-size:0.88rem;box-shadow:0 0 32px rgba(34,197,94,0.35);white-space:nowrap;flex-shrink:0;}
</style>
""", unsafe_allow_html=True)

render_sidebar()

st.markdown("""
<div class="rc-topbar">
  <div class="rc-topbar-left">
    <div class="rc-logo-mark">⚡</div>
    <span class="rc-logo-name">Revenue Copilot</span>
    <div class="rc-sep"></div>
    <span class="rc-crumb">Overview</span>
  </div>
  <div class="rc-topbar-right">
    <span class="rc-pill green"><span class="rc-dot"></span>v4.0</span>
    <span class="rc-pill blue">GPT-4o · Prophet · RFM</span>
  </div>
</div>

<div class="hero">
  <div class="hero-ey"><span class="h-dot"></span>&nbsp;AI-Powered Revenue Intelligence</div>
  <div class="hero-h">The modern<br><span class="g">revenue analytics</span><br>platform</div>
  <div class="hero-s">Upload any sales CSV and get automated EDA, 90-day forecasting, RFM segmentation, and natural-language Q&amp;A — in under 60 seconds.</div>
  <div class="hero-acts">
    <span class="btn-p">Get Started &nbsp;→</span>
    <span class="btn-s">View documentation</span>
  </div>
  <div class="trust">
    <div class="ti"><div class="tc">✓</div>No setup required</div>
    <div class="ti"><div class="tc">✓</div>Works with any CSV</div>
    <div class="ti"><div class="tc">✓</div>ML models built-in</div>
    <div class="ti"><div class="tc">✓</div>GPT-4o Q&amp;A</div>
    <div class="ti"><div class="tc">✓</div>Export PDF reports</div>
  </div>
</div>

<div class="sdiv"></div>
<div class="sw" style="padding-top:0;padding-bottom:0;">
  <div class="sg">
    <div class="sbl"><div class="sn">60s</div><div class="sl">Time to first insight</div><div class="sbg">Fast</div></div>
    <div class="sbl"><div class="sn">5</div><div class="sl">Integrated modules</div><div class="sbg">Complete</div></div>
    <div class="sbl"><div class="sn">90d</div><div class="sl">Max forecast horizon</div><div class="sbg">Prophet</div></div>
    <div class="sbl"><div class="sn">RFM</div><div class="sl">Segmentation engine</div><div class="sbg">KMeans</div></div>
    <div class="sbl"><div class="sn">GPT-4o</div><div class="sl">Q&amp;A model</div><div class="sbg">AI</div></div>
  </div>
</div>
<div class="sdiv" style="margin-top:0;"></div>

<div class="fw">
  <div class="sec-ey">Platform capabilities</div>
  <div class="sec-h">Everything you need to<br>understand your revenue</div>
  <div class="sec-s">Six integrated modules that work together from a single CSV. No pipelines. No configuration.</div>
  <div class="fg">
    <div class="fi"><div class="fic fic1">🔍</div><div class="fn">Automated EDA</div><div class="fd">Statistical profiling, null analysis, distributions and correlations — generated instantly on upload.</div></div>
    <div class="fi"><div class="fic fic2">🚨</div><div class="fn">Anomaly Detection</div><div class="fd">Identify unusual revenue spikes, drops and outliers using adaptive statistical thresholds.</div></div>
    <div class="fi"><div class="fic fic3">📈</div><div class="fn">Revenue Forecasting</div><div class="fd">Facebook Prophet delivers 30, 60, or 90-day projections with calibrated confidence intervals.</div></div>
    <div class="fi"><div class="fic fic4">👥</div><div class="fn">Customer Segments</div><div class="fd">RFM scoring + KMeans maps every customer into Champions, At Risk, Lost and more automatically.</div></div>
    <div class="fi"><div class="fic fic5">💬</div><div class="fn">Natural Language Q&amp;A</div><div class="fd">Ask any business question. GPT-4o writes and executes the Python, then explains the result.</div></div>
    <div class="fi"><div class="fic fic6">📄</div><div class="fn">PDF Reports</div><div class="fd">Export a complete analysis report with all charts and insights ready for board decks.</div></div>
  </div>
</div>

<div class="sdiv"></div>

<div class="wfw" style="padding-top:5rem;">
  <div class="sec-ey">How it works</div>
  <div class="sec-h">Faster. Smarter.</div>
  <div class="sec-s">Six steps from raw CSV to actionable intelligence. No setup, no configuration, no waiting.</div>
  <div class="wg">
    <div class="wc"><div class="wn">01</div><div class="wt">Upload CSV</div><div class="wd">Drop any sales, orders, or subscription CSV. Up to 50 MB. Column types detected automatically.</div></div>
    <div class="wc"><div class="wn">02</div><div class="wt">Auto-analyze</div><div class="wd">Quality scoring, EDA, anomaly detection and correlation analysis run instantly on upload.</div></div>
    <div class="wc"><div class="wn">03</div><div class="wt">Forecast revenue</div><div class="wd">Select date and value columns. Prophet generates projections with confidence bands.</div></div>
    <div class="wc"><div class="wn">04</div><div class="wt">Segment customers</div><div class="wd">RFM scoring + KMeans groups your customer base into actionable behavioral segments.</div></div>
    <div class="wc"><div class="wn">05</div><div class="wt">Ask questions</div><div class="wd">Type any business question. The AI writes Python, executes it, and explains the result.</div></div>
    <div class="wc"><div class="wn">06</div><div class="wt">Export report</div><div class="wd">Generate a branded PDF with all charts and insights ready for investors and board decks.</div></div>
  </div>
</div>

<div class="sdiv"></div>

<div class="ctaw" style="padding-top:5rem;">
  <div class="cta-box">
    <div>
      <div class="cta-ey">Get started now</div>
      <div class="cta-h">Ready to unlock<br>your revenue data?</div>
      <div class="cta-s">Navigate to <strong style="color:#4ade80;">Upload</strong> in the left sidebar to load your first dataset.</div>
    </div>
    <div class="cta-btn">Upload CSV &nbsp;→</div>
  </div>
</div>
""", unsafe_allow_html=True)

for k in ("dataset","dataset_clean","quality_report","filename","chat_history"):
    if k not in st.session_state: st.session_state[k] = None