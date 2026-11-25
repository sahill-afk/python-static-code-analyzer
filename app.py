"""Streamlit entry point for Python Static Code Analyzer."""

from __future__ import annotations

import streamlit as st

from src.analyzer import analyze_code
from src.reports import create_csv_report, create_pdf_report
from src.ui import render_analyzer, render_header, render_home, render_results
from src.utils import AnalysisResult

st.set_page_config(
    page_title="Python Static Code Analyzer",
    page_icon="⌘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
.stApp { font-family: 'Segoe UI', system-ui, sans-serif; }
.block-container { max-width: 1180px; padding-top: 1.5rem; padding-bottom: 4rem; }
.topline { display:flex; align-items:center; gap:12px; border-bottom:1px solid rgba(120,135,160,.2); padding:4px 0 18px; margin-bottom:22px; }
.brand-mark { width:30px; height:30px; display:grid; place-items:center; border-radius:8px; color:#fff; background:#5678e8; font-size:18px; }
.brand-name { font-family:'Cascadia Code',Consolas,monospace; font-weight:500; letter-spacing:.06em; font-size:14px; }
.brand-name span { color:#5678e8; }
.brand-caption { color:color-mix(in srgb,var(--text-color) 58%,transparent); font:10px 'Cascadia Code',Consolas,monospace; letter-spacing:.1em; margin-left:4px; }
.hero { padding:50px 0 24px; max-width:760px; }
.eyebrow,.section-label { color:color-mix(in srgb,var(--text-color) 68%,transparent); font:11px 'Cascadia Code',Consolas,monospace; letter-spacing:.13em; }
.hero h1 { font-size:clamp(2.5rem,6vw,4.6rem); line-height:1.08; letter-spacing:-.055em; margin:16px 0; }
.hero h1 span { color:color-mix(in srgb,var(--text-color) 68%,transparent); }
.hero p { color:color-mix(in srgb,var(--text-color) 72%,transparent); font-size:1.08rem; line-height:1.7; max-width:610px; margin-bottom:22px; }
.section-label { margin:64px 0 16px; }
.feature-card { border:1px solid color-mix(in srgb,var(--text-color) 18%,transparent); border-radius:12px; background:var(--secondary-background-color); padding:18px; min-height:156px; }
.feature-number { color:#5678e8; font:11px 'DM Mono',monospace; }
.feature-card h3 { font-size:17px; margin:16px 0 7px; }
.feature-card p { color:color-mix(in srgb,var(--text-color) 70%,transparent); font-size:13px; line-height:1.5; margin:0; }
.severity-card { display:flex; justify-content:space-between; align-items:center; border:1px solid color-mix(in srgb,var(--text-color) 18%,transparent); border-left:4px solid #94a3b8; border-radius:10px; padding:13px; background:var(--secondary-background-color); }
.severity-card span { color:var(--text-color); font-size:13px; }.severity-card strong { font:500 19px 'Cascadia Code',Consolas,monospace; }
.severity-critical { --severity-color:#b91c1c; border-left-color:#b91c1c; }.severity-high { --severity-color:#dc2626; border-left-color:#dc2626; }.severity-medium { --severity-color:#d97706; border-left-color:#d97706; }.severity-low { --severity-color:#2563eb; border-left-color:#2563eb; }.severity-info { --severity-color:#64748b; border-left-color:#64748b; }
.severity-pill { display:inline-block; border:1px solid var(--severity-color,#64748b); border-radius:999px; padding:2px 8px; color:var(--text-color); background:color-mix(in srgb,var(--severity-color,#64748b) 15%,var(--secondary-background-color)); font-size:12px; font-weight:600; }
.finding-heading { display:flex; flex-wrap:wrap; align-items:center; gap:9px; margin-bottom:8px; }
.complexity-row { padding:5px 0; }
div[data-testid="stTextArea"] textarea { font-family:'Cascadia Code',Consolas,monospace; font-size:13px; line-height:1.65; }
@media (max-width:640px) { .brand-caption { display:none; }.hero { padding-top:30px; }.feature-card { min-height:130px; } }
</style>
""", unsafe_allow_html=True)


def main() -> None:
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None

    render_header()
    page = st.radio(
        "Navigation",
        ["Home", "Code Analyzer"],
        horizontal=True,
        label_visibility="collapsed",
        key="main_navigation",
    )

    if page == "Home":
        render_home()
    else:
        code, uploaded_name, analyze_requested, clear_requested = render_analyzer()
        if clear_requested:
            st.session_state.analysis_result = None
            st.session_state.editor_epoch = st.session_state.get("editor_epoch", 0) + 1
            st.rerun()
        if analyze_requested:
            st.session_state.analysis_result = None
            if not code.strip():
                st.warning("Add or upload Python code before starting an analysis.")
            else:
                try:
                    st.session_state.analysis_result = analyze_code(code, uploaded_name)
                except ValueError as error:
                    st.warning(str(error))
                except Exception:
                    st.error("Analysis could not be completed. Please review the input and try again.")

        result: AnalysisResult | None = st.session_state.analysis_result
        reports_ready = False
        if result is not None:
            try:
                render_results(result)
                csv_data = create_csv_report(result)
                pdf_data = create_pdf_report(result)
                reports_ready = True
            except Exception:
                csv_data = b""
                pdf_data = b""
                st.error("The report could not be prepared. Please rerun the analysis and try again.")
        else:
            csv_data = b""
            pdf_data = b""

        st.markdown('<div class="section-label results-label">REPORTS</div>', unsafe_allow_html=True)
        st.caption("Exports become available after a completed analysis.")
        col_csv, col_pdf = st.columns(2)
        col_csv.download_button(
            "Download CSV report", csv_data, "python-analysis-report.csv",
            "text/csv", disabled=not reports_ready or result is None or not result.analyzed,
            use_container_width=True,
        )
        col_pdf.download_button(
            "Download PDF report", pdf_data, "python-analysis-report.pdf",
            "application/pdf", disabled=not reports_ready or result is None or not result.analyzed,
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
