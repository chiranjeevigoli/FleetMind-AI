"""
upload_panel.py
---------------
Sidebar widget for uploading, indexing, and tracking PDF documents.
"""

import streamlit as st
from src.uploader import index_uploaded_file, get_kb_stats


def show_upload_panel():
    """
    Renders the 'Upload Documents' section inside the Streamlit sidebar.
    Handles file upload, indexing progress, success/error feedback,
    and live KB stats refresh.
    """

    st.markdown("---")
    st.subheader("📂 Upload Documents")

    st.markdown(
        "<p style='font-size:13px; color:#a0b4cc; margin-top:-8px;'>"
        "Add new PDF manuals to the knowledge base.</p>",
        unsafe_allow_html=True
    )

    # ── Display Upload Results from Previous Run ────────────────
    if "upload_results" in st.session_state:
        st.markdown("#### 📊 Indexing Summary")
        for r in st.session_state["upload_results"]:
            if r["skipped"]:
                st.warning(f"⚠️ **{r['filename']}** — already indexed, skipped.")
            elif r["error"]:
                st.error(f"❌ **{r['filename']}** — {r['error']}")
            else:
                st.success(
                    f"✅ **{r['filename']}** — "
                    f"{r['pages']} pages · {r['chunks']} chunks added"
                )
        del st.session_state["upload_results"]

    # ── File uploader ───────────────────────────────────────────
    uploaded_files = st.file_uploader(
        label="Select PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key="doc_uploader",
        help="Drag & drop one or more PDF manuals. They will be chunked, "
             "embedded, and added to ChromaDB immediately.",
        label_visibility="collapsed"
    )

    # ── Index button ────────────────────────────────────────────
    if uploaded_files:
        st.markdown(
            f"<p style='color:#60a5fa; font-size:13px;'>"
            f"📎 {len(uploaded_files)} file(s) selected</p>",
            unsafe_allow_html=True
        )

        if st.button("⚡ Index Documents", key="btn_index"):
            _run_indexing(uploaded_files)

    else:
        st.markdown(
            "<div class='upload-hint'>"
            "🗂️ Drop PDFs here to expand the knowledge base"
            "</div>",
            unsafe_allow_html=True
        )


def _run_indexing(uploaded_files):
    """
    Iterate over uploaded files, index each one, and show progress.
    """
    total = len(uploaded_files)

    st.markdown("---")
    overall_bar = st.progress(0, text="Starting indexing…")
    status_area = st.empty()
    results_log = []

    for file_idx, uf in enumerate(uploaded_files):

        # Per-file progress bar
        file_bar = st.progress(0, text=f"Processing **{uf.name}**…")

        def _progress(frac: float, msg: str, _bar=file_bar):
            _bar.progress(frac, text=msg)
            status_area.markdown(
                f"<span style='color:#93c5fd; font-size:13px;'>{msg}</span>",
                unsafe_allow_html=True
            )

        result = index_uploaded_file(uf, progress_callback=_progress)
        results_log.append(result)

        # Update overall bar
        overall_bar.progress(
            (file_idx + 1) / total,
            text=f"Processed {file_idx + 1}/{total} file(s)…"
        )

    # ── Refresh live KB stats ────────────────────────────────────
    stats = get_kb_stats()
    st.session_state["kb_stats"] = stats
    
    # Store results to show them after rerun
    st.session_state["upload_results"] = results_log
    st.rerun()
