"""
AI Revenue Copilot — Design System
Aesthetic: Astra-inspired · Deep black + Emerald gradients
"""

SHARED = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
  --bg:   #050c0a;  --bg1: #071110;  --bg2: #0a1815;
  --bg3:  #0d1e1a;  --bg4: #102320;
  --br:   rgba(255,255,255,0.07);
  --br2:  rgba(255,255,255,0.12);
  --br-em:rgba(52,211,153,0.25);
  --em:   #34d399;  --em2: #6ee7b7;
  --em-dim: rgba(52,211,153,0.1);
  --em-glow:rgba(52,211,153,0.18);
  --teal: #2dd4bf;
  --warn: #fbbf24;  --err: #f87171;  --blue: #60a5fa;
  --t1: #e8f5f0;  --t2: #6db89a;  --t3: #2e6650;  --t4: #163d2a;
  --r1: 6px;  --r2: 10px;  --r3: 14px;  --r4: 20px;
  --sh1: 0 1px 3px rgba(0,0,0,0.7);
  --sh2: 0 4px 20px rgba(0,0,0,0.8);
  --glow: 0 0 30px rgba(52,211,153,0.12);
}

#MainMenu, footer, header { visibility: hidden !important; }
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
  font-family: 'DM Sans', -apple-system, sans-serif !important;
  color: var(--t1) !important;
  -webkit-font-smoothing: antialiased !important;
}

.stApp {
  background-color: var(--bg) !important;
  background-image:
    radial-gradient(ellipse 80% 55% at 12% 0%, rgba(52,211,153,0.11) 0%, transparent 55%),
    radial-gradient(ellipse 65% 50% at 88% 100%, rgba(45,212,191,0.07) 0%, transparent 55%) !important;
}

[data-testid="stSidebar"] {
  background: #040a08 !important;
  border-right: 1px solid var(--br) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }
[data-testid="stSidebar"] .block-container   { padding: 0 !important; }

/* ── Nav links — todos los selectores posibles ── */
[data-testid="stSidebarNav"] { padding: 0.35rem 1rem 1rem !important; }

[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] a:link,
[data-testid="stSidebarNav"] a:visited,
[data-testid="stSidebarNav"] li a,
[data-testid="stSidebarNav"] ul li a {
  display: flex !important;
  align-items: center !important;
  border-radius: var(--r1) !important;
  padding: 0.52rem 0.875rem !important;
  margin-bottom: 2px !important;
  color: #a8d5be !important;
  font-size: 0.83rem !important;
  font-weight: 500 !important;
  text-decoration: none !important;
  transition: all 0.12s ease !important;
}

/* Fuerza el color en los spans internos que Streamlit genera */
[data-testid="stSidebarNav"] a span,
[data-testid="stSidebarNav"] a div,
[data-testid="stSidebarNav"] a p,
[data-testid="stSidebarNav"] li span,
[data-testid="stSidebarNav"] li div {
  color: #a8d5be !important;
}

[data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebarNav"] li a:hover {
  background: rgba(52,211,153,0.08) !important;
  color: #6ee7b7 !important;
}
[data-testid="stSidebarNav"] a:hover span,
[data-testid="stSidebarNav"] a:hover div {
  color: #6ee7b7 !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"],
[data-testid="stSidebarNav"] li a[aria-current="page"] {
  background: rgba(52,211,153,0.12) !important;
  color: #34d399 !important;
  border-left: 2px solid #34d399 !important;
  font-weight: 600 !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] span,
[data-testid="stSidebarNav"] a[aria-current="page"] div {
  color: #34d399 !important;
}

[data-testid="stSidebarNav"] img,
[data-testid="stSidebarNav"] a img { display: none !important; }

.block-container   { padding-left: 3rem !important; padding-right: 2.5rem !important; padding-top: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }
h1,h2,h3,h4,h5,h6 {
  font-family: 'Syne', sans-serif !important;
  letter-spacing: -0.03em !important; color: var(--t1) !important;
}

[data-testid="metric-container"] {
  background: var(--bg2) !important; border: 1px solid var(--br) !important;
  border-radius: var(--r2) !important; padding: 1.25rem 1.5rem !important;
  box-shadow: var(--sh1) !important; transition: border-color .18s, box-shadow .18s !important;
}
[data-testid="metric-container"]:hover {
  border-color: var(--br-em) !important; box-shadow: var(--sh2), var(--glow) !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
  color: var(--t3) !important; font-size: 0.7rem !important;
  font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.1em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"],
[data-testid="metric-container"] [data-testid="stMetricValue"] > div,
[data-testid="metric-container"] [data-testid="stMetricValue"] span,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] > div,
[data-testid="stMetricValue"] span {
  font-family: 'Syne', sans-serif !important;
  font-size: 1.85rem !important;
  font-weight: 800 !important;
  color: #ffffff !important;
  line-height: 1.1 !important;
}

[data-testid="metric-container"] [data-testid="stMetricLabel"],
[data-testid="metric-container"] [data-testid="stMetricLabel"] > div,
[data-testid="metric-container"] [data-testid="stMetricLabel"] span,
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] span {
  color: #6db89a !important;
  font-size: 0.7rem !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] * {
  color: #e8f5f0 !important;
}

.stButton > button {
  background: var(--em) !important; color: #04080c !important;
  border: none !important; border-radius: var(--r1) !important;
  font-family: 'DM Sans', sans-serif !important; font-weight: 700 !important;
  font-size: 0.84rem !important; padding: 0.55rem 1.4rem !important;
  box-shadow: 0 0 22px rgba(52,211,153,0.22) !important; transition: all .15s ease !important;
}
.stButton > button:hover {
  background: var(--em2) !important; box-shadow: 0 0 34px rgba(52,211,153,0.38) !important;
  transform: translateY(-1px) !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div,
[data-testid="stTextInput"] > div > div > input {
  background: var(--bg3) !important; border: 1px solid var(--br2) !important;
  border-radius: var(--r1) !important; color: var(--t1) !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
  border-color: var(--em) !important; box-shadow: 0 0 0 3px rgba(52,211,153,0.1) !important;
}

[data-testid="stDataFrame"] {
  border: 1px solid var(--br) !important; border-radius: var(--r2) !important; overflow: hidden !important;
}
.dvn-scroller { background: var(--bg1) !important; }

[data-testid="stExpander"] {
  background: var(--bg2) !important; border: 1px solid var(--br) !important; border-radius: var(--r2) !important;
}
[data-testid="stExpander"] summary { color: var(--t2) !important; font-size: 0.85rem !important; }

[data-testid="stFileUploader"] {
  background: var(--bg2) !important; border: 1.5px dashed var(--br-em) !important;
  border-radius: var(--r3) !important; transition: all .2s ease !important;
}
[data-testid="stFileUploader"]:hover {
  border-color: var(--em) !important; background: var(--em-dim) !important; box-shadow: var(--glow) !important;
}
[data-testid="stFileUploader"] * { color: var(--t2) !important; }

[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important; border-bottom: 1px solid var(--br) !important;
  border-radius: 0 !important; padding: 0 !important; gap: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  border-radius: 0 !important; color: var(--t2) !important;
  font-size: 0.82rem !important; font-weight: 500 !important;
  padding: 0.62rem 1.25rem !important; border-bottom: 2px solid transparent !important;
  transition: all .12s !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--em2) !important; background: rgba(52,211,153,0.03) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  background: transparent !important; color: var(--em) !important;
  border-bottom: 2px solid var(--em) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-border"],
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none !important; }
[data-testid="stTabs"] [data-baseweb="tab-panel"]     { padding: 1.5rem 0 0 !important; }

[data-testid="stChatMessage"] {
  background: var(--bg2) !important; border: 1px solid var(--br) !important;
  border-radius: var(--r2) !important; margin-bottom: 0.5rem !important;
}
[data-testid="stChatInput"] > div {
  background: var(--bg3) !important; border: 1px solid var(--br2) !important; border-radius: var(--r2) !important;
}
[data-testid="stChatInput"] > div:focus-within {
  border-color: var(--em) !important; box-shadow: 0 0 0 3px rgba(52,211,153,0.1) !important;
}

[data-testid="stSlider"] [role="slider"] { background: var(--em) !important; border-color: var(--em) !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(52,211,153,0.18); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(52,211,153,0.32); }
hr { border-color: var(--br) !important; margin: 0 !important; }

/* ── Topbar ── */
.rc-topbar {
  background: rgba(5,12,10,0.9); border-bottom: 1px solid var(--br);
  padding: 0 2.25rem; height: 54px;
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 999;
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
}
.rc-topbar-left  { display: flex; align-items: center; gap: 14px; }
.rc-topbar-right { display: flex; align-items: center; gap: 8px; }
.rc-logo-mark {
  width: 30px; height: 30px;
  background: linear-gradient(135deg, #34d399 0%, #2dd4bf 100%);
  border-radius: 8px; display: flex; align-items: center; justify-content: center;
  font-size: 14px; box-shadow: 0 0 16px rgba(52,211,153,0.32); flex-shrink: 0;
}
.rc-logo-name { font-family: 'Syne', sans-serif; font-size: 0.92rem; font-weight: 700; color: var(--t1); letter-spacing: -0.02em; }
.rc-sep       { width: 1px; height: 17px; background: rgba(255,255,255,0.15); }
.rc-crumb     { font-size: 0.78rem; color: #6db89a; font-weight: 500; }

/* ── Pills ── */
.rc-pill {
  display: inline-flex; align-items: center; gap: 5px;
  padding: 3px 10px; border-radius: 99px;
  font-size: 0.67rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase;
}
.rc-pill.green  { background: rgba(52,211,153,0.1);  border: 1px solid rgba(52,211,153,0.22);  color: #34d399; }
.rc-pill.amber  { background: rgba(251,191,36,0.1);  border: 1px solid rgba(251,191,36,0.22);  color: #fbbf24; }
.rc-pill.blue   { background: rgba(96,165,250,0.1);  border: 1px solid rgba(96,165,250,0.22);  color: #60a5fa; }
.rc-pill.gray   { background: rgba(255,255,255,0.04);border: 1px solid rgba(255,255,255,0.1);  color: #6db89a; }
.rc-dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; box-shadow: 0 0 5px currentColor; }

/* ── Tags ── */
.rc-tag {
  display: inline-flex; align-items: center;
  padding: 2px 8px; border-radius: 4px;
  font-size: 0.64rem; font-weight: 700; letter-spacing: .07em; text-transform: uppercase;
}
.rc-tag.green { background: rgba(52,211,153,0.1);  border: 1px solid rgba(52,211,153,0.22);  color: #34d399; }
.rc-tag.blue  { background: rgba(96,165,250,0.1);  border: 1px solid rgba(96,165,250,0.22);  color: #60a5fa; }
.rc-tag.gold  { background: rgba(251,191,36,0.1);  border: 1px solid rgba(251,191,36,0.22);  color: #fbbf24; }
.rc-tag.gray  { background: rgba(255,255,255,0.05);border: 1px solid rgba(255,255,255,0.1);  color: #6db89a; }

/* ── Page wrapper ── */
.rc-page { padding: 2.5rem 2.5rem 4rem 3rem; max-width: 1280px; margin: 0 auto; }

/* ── Page header ── */
.rc-page-hd {
  padding-bottom: 1.5rem; margin-bottom: 2rem; border-bottom: 1px solid var(--br);
  display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem;
}
.rc-title { font-family: 'Syne', sans-serif; font-size: 1.55rem; font-weight: 800; color: #e8f5f0; letter-spacing: -0.03em; margin: 0 0 4px; line-height: 1.15; }
.rc-sub   { font-size: 0.8rem; color: #6db89a; line-height: 1.55; }

/* ── Card ── */
.rc-card { background: var(--bg2); border: 1px solid var(--br); border-radius: var(--r3); overflow: hidden; box-shadow: var(--sh1); transition: border-color .15s; }
.rc-card:hover { border-color: var(--br2); }
.rc-card-hd  { padding: 0.9rem 1.25rem; border-bottom: 1px solid var(--br); display: flex; align-items: center; justify-content: space-between; }
.rc-card-ttl { font-family: 'Syne', sans-serif; font-size: 0.86rem; font-weight: 700; color: #e8f5f0; }

/* ── Stat strip ── */
.rc-strip  { display: flex; gap: 1px; background: var(--br); border: 1px solid var(--br); border-radius: var(--r2); overflow: hidden; margin-bottom: 1.75rem; }
.rc-scell  { flex: 1; background: var(--bg2); padding: 0.9rem 1.2rem; }
.rc-slbl   { font-size: 0.63rem; color: #6db89a; font-weight: 600; text-transform: uppercase; letter-spacing: .1em; margin-bottom: 3px; }
.rc-sval   { font-family: 'Syne', sans-serif; font-size: 1.05rem; font-weight: 700; color: #e8f5f0; }

/* ── Control panel ── */
.rc-ctrl    { background: var(--bg2); border: 1px solid var(--br); border-radius: var(--r3); padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; }
.rc-ctrl-ttl{ font-size: 0.63rem; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; color: #6db89a; margin-bottom: 0.9rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--br); }

/* ── Progress bar ── */
.rc-bw { background: var(--bg4); border-radius: 99px; height: 4px; overflow: hidden; }
.rc-b  { height: 100%; border-radius: 99px; transition: width .6s ease; }

/* ── Empty state ── */
.rc-empty     { background: var(--bg2); border: 1px dashed rgba(52,211,153,0.18); border-radius: var(--r4); padding: 4rem 2rem; text-align: center; }
.rc-empty-icon{ font-size: 1.75rem; display: block; margin-bottom: 1rem; }
.rc-empty-ttl { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700; color:#e8f5f0; margin-bottom:.4rem; }
.rc-empty-sub { font-size:.8rem; color:#6db89a; line-height:1.6; }

/* ── Error box ── */
.rc-err     { background:rgba(248,113,113,0.05); border:1px solid rgba(248,113,113,0.2); border-radius:var(--r2); padding:1rem 1.25rem; }
.rc-err-ttl { font-size:.83rem; font-weight:600; color:var(--err); margin-bottom:4px; }
.rc-err-body{ font-size:.75rem; color:#6db89a; font-family:'DM Mono',monospace; }

/* Margen entre sidebar y contenido */
section.main .block-container {
  padding-left: 3rem !important;
  padding-right: 2.5rem !important;
  padding-top: 0 !important;
  max-width: 100% !important;
}

/* ── Footer ── */
.rc-footer { display:flex; align-items:center; justify-content:space-between; padding:1.25rem 0 0; margin-top:2.5rem; border-top:1px solid var(--br); font-size:0.7rem; color:#6db89a; }
</style>
"""

def render_sidebar(filename=None, nrows=None, ncols=None):
    import streamlit as st
    with st.sidebar:
        st.markdown("""
        <div style="padding:1.5rem 1.25rem 1.1rem;border-bottom:1px solid rgba(255,255,255,0.07);">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
            <div style="width:32px;height:32px;background:linear-gradient(135deg,#34d399 0%,#2dd4bf 100%);
                        border-radius:9px;flex-shrink:0;display:flex;align-items:center;
                        justify-content:center;font-size:15px;box-shadow:0 0 14px rgba(52,211,153,0.3);">⚡</div>
            <div>
              <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:0.92rem;
                          color:#e8f5f0;letter-spacing:-0.02em;line-height:1.2;">Revenue Copilot</div>
              <div style="font-size:0.6rem;color:#6db89a;font-weight:500;
                          letter-spacing:0.09em;text-transform:uppercase;">AI Analytics · v3</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="padding:0.9rem 1.25rem 0.4rem;font-size:0.6rem;font-weight:700;
                    letter-spacing:0.13em;text-transform:uppercase;color:#2e6650;">Pages</div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.1rem'></div>", unsafe_allow_html=True)

        if filename:
            st.markdown(f"""
            <div style="margin:0.35rem 0.875rem 0;background:rgba(52,211,153,0.07);
                        border:1px solid rgba(52,211,153,0.2);border-radius:10px;padding:0.9rem 1rem;">
              <div style="display:flex;align-items:center;gap:7px;margin-bottom:6px;">
                <div style="width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 7px #34d399;"></div>
                <span style="font-size:0.6rem;font-weight:700;letter-spacing:0.1em;
                             text-transform:uppercase;color:#34d399;">Dataset active</span>
              </div>
              <div style="font-size:0.82rem;font-weight:600;color:#e8f5f0;
                          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:2px;">{filename}</div>
              <div style="font-size:0.71rem;color:#6db89a;">{nrows:,} rows &nbsp;·&nbsp; {ncols} columns</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="margin:0.35rem 0.875rem 0;background:rgba(251,191,36,0.05);
                        border:1px solid rgba(251,191,36,0.15);border-radius:10px;padding:0.9rem 1rem;">
              <div style="display:flex;align-items:center;gap:7px;margin-bottom:5px;">
                <div style="width:7px;height:7px;border-radius:50%;background:#fbbf24;"></div>
                <span style="font-size:0.6rem;font-weight:700;letter-spacing:0.1em;
                             text-transform:uppercase;color:#fbbf24;">No dataset loaded</span>
              </div>
              <div style="font-size:0.76rem;color:#6db89a;line-height:1.5;">Upload a CSV file to begin</div>
            </div>
            """, unsafe_allow_html=True)
            
            