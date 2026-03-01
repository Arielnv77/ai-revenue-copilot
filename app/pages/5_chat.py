"""💬 Chat · Design v4"""
import streamlit as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.nlp.query_engine import QueryEngine
from src.utils.config import settings
st.set_page_config(page_title="Chat | Revenue Copilot", page_icon="💬", layout="wide")
from _shared_css import SHARED; from _sidebar import render_sidebar
st.markdown(SHARED, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""<div class="sb-brand"><div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;"><div style="width:30px;height:30px;background:linear-gradient(135deg,#22c55e,#10b981);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:14px;box-shadow:0 0 14px rgba(34,197,94,0.38);">⚡</div><div><div style="font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:0.9rem;color:#ffffff;letter-spacing:-0.025em;">Revenue Copilot</div><div style="font-size:0.62rem;color:#2d4a35;font-weight:600;letter-spacing:0.07em;text-transform:uppercase;">Enterprise Analytics</div></div></div></div><div class="sb-nav-lbl">Navigation</div>""",unsafe_allow_html=True)
    st.markdown("<div style='height:0.3rem'></div>",unsafe_allow_html=True)
    if st.session_state.get("dataset_clean") is not None:
        fname=st.session_state.get("filename","dataset.csv"); n=len(st.session_state.dataset_clean); c=st.session_state.dataset_clean.shape[1]
        st.markdown(f"""<div class="sb-ds on"><div style="display:flex;align-items:center;gap:7px;margin-bottom:6px;"><div style="width:6px;height:6px;border-radius:50%;background:#22c55e;box-shadow:0 0 6px #22c55e;"></div><span style="font-size:0.62rem;font-weight:700;color:#4ade80;letter-spacing:0.09em;text-transform:uppercase;">Dataset active</span></div><div style="font-size:0.82rem;font-weight:600;color:#ffffff;margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{fname}</div><div style="font-size:0.72rem;color:#2d4a35;">{n:,} rows · {c} cols</div></div>""",unsafe_allow_html=True)
    else:
        st.markdown("""<div class="sb-ds off"><div style="display:flex;align-items:center;gap:7px;margin-bottom:5px;"><div style="width:6px;height:6px;border-radius:50%;background:#facc15;"></div><span style="font-size:0.62rem;font-weight:700;color:#facc15;letter-spacing:0.09em;text-transform:uppercase;">No dataset</span></div><div style="font-size:0.78rem;color:#2d4a35;">Upload a CSV file to begin</div></div>""",unsafe_allow_html=True)
    st.markdown('<div class="sb-nav-lbl" style="margin-top:0.75rem;">Suggested prompts</div>',unsafe_allow_html=True)
    st.markdown('<div style="height:0.25rem"></div>',unsafe_allow_html=True)
    for ex in ["What is the total revenue?","Top 10 customers by spend","Revenue trend by month","Average order value","Products with highest sales","% orders with negative revenue"]:
        st.markdown(f"""<div style="margin:0.2rem 0.75rem;background:rgba(34,197,94,0.05);border:1px solid rgba(34,197,94,0.12);border-radius:6px;padding:6px 10px;font-size:0.75rem;color:#4a7c59;font-family:'JetBrains Mono',monospace;cursor:pointer;">→ {ex}</div>""",unsafe_allow_html=True)

if st.session_state.get("dataset_clean") is None:
    st.markdown("""<div class="rc-topbar"><div class="rc-topbar-left"><div class="rc-logo-mark">⚡</div><span class="rc-logo-name">Revenue Copilot</span><div class="rc-sep"></div><span class="rc-crumb">Chat</span></div></div><div class="rc-page"><div class="rc-empty"><span class="rc-empty-icon">📂</span><div class="rc-empty-ttl">No dataset loaded</div><div class="rc-empty-sub">Go to Upload first.</div></div></div>""",unsafe_allow_html=True); st.stop()

df=st.session_state.dataset_clean; ok=bool(getattr(settings,"openai_api_key",None))
st.markdown(f"""<div class="rc-topbar"><div class="rc-topbar-left"><div class="rc-logo-mark">⚡</div><span class="rc-logo-name">Revenue Copilot</span><div class="rc-sep"></div><span class="rc-crumb">Ask Your Data</span></div><div class="rc-topbar-right"><span class="rc-pill {'green' if ok else 'amber'}"><span class="rc-dot"></span>{'API connected' if ok else 'API key missing'}</span></div></div>""",unsafe_allow_html=True)
st.markdown('<div class="rc-page">',unsafe_allow_html=True)
st.markdown(f"""<div class="rc-page-hd"><div><div class="rc-title">Ask Your Data</div><div class="rc-sub">Natural language Q&amp;A · powered by GPT-4o</div></div><span class="rc-tag {'green' if ok else 'gold'}">GPT-4o</span></div>""",unsafe_allow_html=True)

fname=st.session_state.get("filename","dataset.csv"); cp=", ".join(df.columns[:7])+("…" if len(df.columns)>7 else "")
st.markdown(f"""<div style="background:#0c1810;border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:0.85rem 1.4rem;display:flex;gap:2.5rem;margin-bottom:1.25rem;flex-wrap:wrap;"><div><div style="font-size:0.62rem;color:#4a7c59;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:2px;">Dataset</div><div style="font-size:0.8rem;font-weight:600;color:#ffffff;font-family:'JetBrains Mono',monospace;">{fname}</div></div><div><div style="font-size:0.62rem;color:#4a7c59;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:2px;">Rows</div><div style="font-size:0.8rem;font-weight:600;color:#ffffff;">{df.shape[0]:,}</div></div><div><div style="font-size:0.62rem;color:#4a7c59;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:2px;">Columns</div><div style="font-size:0.8rem;font-weight:600;color:#ffffff;">{df.shape[1]}</div></div><div style="flex:2"><div style="font-size:0.62rem;color:#4a7c59;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:2px;">Available columns</div><div style="font-size:0.73rem;color:#6da882;font-family:'JetBrains Mono',monospace;">{cp}</div></div></div>""",unsafe_allow_html=True)

if not ok: st.markdown("""<div style="background:rgba(234,179,8,0.07);border:1px solid rgba(234,179,8,0.20);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem;"><div style="font-size:0.85rem;font-weight:600;color:#facc15;margin-bottom:5px;">⚠ OpenAI API key not configured</div><div style="font-size:0.8rem;color:#6da882;">Add <code style="background:rgba(255,255,255,0.06);padding:1px 6px;border-radius:3px;">OPENAI_API_KEY=sk-...</code> to your <code style="background:rgba(255,255,255,0.06);padding:1px 6px;border-radius:3px;">.env</code> file.</div></div>""",unsafe_allow_html=True)

if "chat_history" not in st.session_state or st.session_state.chat_history is None: st.session_state.chat_history=[]
cl2,_=st.columns([1,5])
with cl2:
    if st.button("Clear conversation",key="clr"): st.session_state.chat_history=[]; st.rerun()

if not st.session_state.chat_history:
    st.markdown("""<div class="rc-empty" style="margin:1rem 0 1.5rem;padding:3rem 2rem;"><span class="rc-empty-icon">💬</span><div class="rc-empty-ttl">Start a conversation</div><div class="rc-empty-sub">Ask anything about your data in plain English.<br>Use the suggested prompts in the sidebar to get started.</div></div>""",unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if question:=st.chat_input("Ask a question about your data…"):
    st.session_state.chat_history.append({"role":"user","content":question})
    with st.chat_message("user"): st.markdown(question)
    with st.chat_message("assistant"):
        if not ok:
            ans="⚠️ **API key not configured.** Add `OPENAI_API_KEY` to your `.env` file."
            st.markdown(ans)
        else:
            with st.spinner("Thinking…"):
                try:
                    eng=QueryEngine(api_key=settings.openai_api_key); eng.load_data(df); res=eng.ask(question)
                    ans=res.get("answer","I couldn't generate an answer.")
                    if res.get("code"): st.markdown('<div style="font-size:0.62rem;color:#4a7c59;text-transform:uppercase;letter-spacing:0.09em;margin-bottom:4px;">Code executed</div>',unsafe_allow_html=True); st.code(res["code"],language="python")
                    st.markdown('<div style="font-size:0.62rem;color:#4a7c59;text-transform:uppercase;letter-spacing:0.09em;margin:0.75rem 0 4px;">Answer</div>',unsafe_allow_html=True)
                    st.markdown(ans)
                    if res.get("insight"): st.markdown(f"""<div style="background:rgba(34,197,94,0.06);border:1px solid rgba(34,197,94,0.18);border-radius:8px;padding:0.75rem 1rem;margin-top:0.75rem;font-size:0.82rem;color:#4ade80;">💡 {res['insight']}</div>""",unsafe_allow_html=True)
                    if res.get("execution_result"): st.code(res["execution_result"])
                except Exception as e: ans=f"❌ Error: {e}"; st.error(ans)
        st.session_state.chat_history.append({"role":"assistant","content":ans})

st.markdown(f'<div class="rc-footer"><span>Revenue Copilot · Chat</span><span>{len(st.session_state.chat_history)} messages · GPT-4o</span></div>',unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)