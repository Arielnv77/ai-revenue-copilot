"""
RevenueOS — Design System
Aesthetic: Astra-inspired · Deep black + Emerald gradients
"""

import base64
from pathlib import Path

_ASSETS = Path(__file__).parent / "assets"

# Load CSS from static file (keeps source clean and editable)
_css = (_ASSETS / "style.css").read_text(encoding="utf-8")
SHARED = f"<style>{_css}</style>"


def render_sidebar(filename=None, nrows=None, ncols=None):
    import streamlit as st
    from _i18n import t

    # Default language
    st.session_state.setdefault("lang", "en")

    # Read dataset state from session if not passed explicitly
    if filename is None and "dataset_clean" in st.session_state:
        df = st.session_state.dataset_clean
        filename = st.session_state.get("filename", "dataset.csv")
        nrows = nrows or (df.shape[0] if df is not None else 0)
        ncols = ncols or (df.shape[1] if df is not None else 0)

    # Load logo at runtime — avoids hardcoding 73KB of base64 in source
    _logo_b64 = base64.b64encode((_ASSETS / "logo.png").read_bytes()).decode()

    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="padding:1.5rem 1.25rem 1.1rem;border-bottom:1px solid rgba(255,255,255,0.07);">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
            <img src="data:image/png;base64,{_logo_b64}" style="width:32px;height:32px;border-radius:9px;box-shadow:0 0 14px rgba(52,211,153,0.3);">
            <div>
              <div style="font-family:'DM Sans',sans-serif;font-weight:700;font-stretch:condensed;font-size:1rem;
                          color:#ffffff;letter-spacing:-0.03em;line-height:1.2;">RevenueOS</div>
              <div style="font-size:0.6rem;color:#6db89a;font-weight:500;
                          letter-spacing:0.09em;text-transform:uppercase;">AI Analytics · v3</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Language toggle ────────────────────────────────────────────────────
        st.markdown("<div style='padding:0.7rem 0.875rem 0.3rem;'>", unsafe_allow_html=True)
        _lc1, _lc2 = st.columns(2)
        _lang = st.session_state.lang
        with _lc1:
            _en_css = "font-weight:700;background:#34d399;color:#050c0a;border:none;" if _lang == "en" else "font-weight:500;background:rgba(255,255,255,0.05);color:#6db89a;border:none;"
            if st.button("EN", key="_lang_en", use_container_width=True, help="Switch to English"):
                st.session_state.lang = "en"
                st.rerun()
        with _lc2:
            _es_css = "font-weight:700;background:#34d399;color:#050c0a;border:none;" if _lang == "es" else "font-weight:500;background:rgba(255,255,255,0.05);color:#6db89a;border:none;"
            if st.button("ES", key="_lang_es", use_container_width=True, help="Cambiar a español"):
                st.session_state.lang = "es"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Pages label ────────────────────────────────────────────────────────
        st.markdown(f"""
        <div style="padding:0.6rem 1.25rem 0.4rem;font-size:0.6rem;font-weight:700;
                    letter-spacing:0.13em;text-transform:uppercase;color:#2e6650;">{t("pages")}</div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.1rem'></div>", unsafe_allow_html=True)

        # ── Dataset status ─────────────────────────────────────────────────────
        if filename:
            st.markdown(f"""
            <div style="margin:0.35rem 0.875rem 0;background:rgba(52,211,153,0.07);
                        border:1px solid rgba(52,211,153,0.2);border-radius:10px;padding:0.9rem 1rem;">
              <div style="display:flex;align-items:center;gap:7px;margin-bottom:6px;">
                <div style="width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 7px #34d399;"></div>
                <span style="font-size:0.6rem;font-weight:700;letter-spacing:0.1em;
                             text-transform:uppercase;color:#34d399;">{t("dataset_active")}</span>
              </div>
              <div style="font-size:0.82rem;font-weight:600;color:#e8f5f0;
                          white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:2px;">{filename}</div>
              <div style="font-size:0.71rem;color:#6db89a;">{nrows:,} {t("rows").lower()} &nbsp;·&nbsp; {ncols} {t("columns").lower()}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="margin:0.35rem 0.875rem 0;background:rgba(251,191,36,0.05);
                        border:1px solid rgba(251,191,36,0.15);border-radius:10px;padding:0.9rem 1rem;">
              <div style="display:flex;align-items:center;gap:7px;margin-bottom:5px;">
                <div style="width:7px;height:7px;border-radius:50%;background:#fbbf24;"></div>
                <span style="font-size:0.6rem;font-weight:700;letter-spacing:0.1em;
                             text-transform:uppercase;color:#fbbf24;">{t("no_dataset")}</span>
              </div>
              <div style="font-size:0.76rem;color:#6db89a;line-height:1.5;">{t("upload_hint")}</div>
            </div>
            """, unsafe_allow_html=True)
