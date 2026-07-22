from src.retriever import retrieve
from src.llm import generate_answer
from src.vector_store import get_collection_stats

from components.hero import show_hero
from components.answer_card import show_answer, show_clarification, show_sidebar_logo
from components.source_cards import show_sources
from components.upload_panel import show_upload_panel

import streamlit as st


# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="FleetMind AI",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Load CSS
# --------------------------------------------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retrieved" not in st.session_state:
    st.session_state.retrieved = []

# Live KB stats — refreshed after each upload
if "kb_stats" not in st.session_state:
    st.session_state.kb_stats = get_collection_stats()

kb = st.session_state.kb_stats


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    # Branded logo + title
    show_sidebar_logo()

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    # ── Knowledge Base Stats ──────────────────────────────────────
    st.markdown(
        "<div class='sidebar-section-title'>📊 Knowledge Base</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="sidebar-stat-grid">
            <div class="sidebar-stat-card">
                <div class="sidebar-stat-value">{kb['unique_sources']}</div>
                <div class="sidebar-stat-label">📚 Manuals</div>
            </div>
            <div class="sidebar-stat-card">
                <div class="sidebar-stat-value">{kb['total_chunks']}</div>
                <div class="sidebar-stat-label">🧩 Chunks</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-info-list">
            <div class="sidebar-info-item">🗄 <span>Vector DB</span><strong>ChromaDB</strong></div>
            <div class="sidebar-info-item">🧠 <span>Embedding</span><strong>MiniLM-L6-v2</strong></div>
            <div class="sidebar-info-item">🤖 <span>LLM</span><strong>Gemini</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Upload Documents Panel ──────────────────────────────────────
    show_upload_panel()

    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center; font-size:11px; color:#4a6fa5; padding-top:4px;'>FleetMind AI · Version 1.1</div>",
        unsafe_allow_html=True
    )


# --------------------------------------------------
# Hero Section
# --------------------------------------------------

show_hero()

st.markdown("<br>", unsafe_allow_html=True)


# --------------------------------------------------
# Previous Chat History
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "assistant":

            if message.get("is_clarification", False):
                show_clarification(message["content"])
            else:
                show_answer(message["content"])

        else:

            st.markdown(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input("🔧 Ask a maintenance question about your fleet...")

if question:

    # User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Retrieve + Generate

    with st.spinner("🔍 Searching manuals..."):

        retrieved = retrieve(question)

        # Confidence Evaluation & Routing Decision
        # L2 Distance Threshold: 1.20
        CONFIDENCE_THRESHOLD = 1.20
        is_clarification = False

        if not retrieved:
            is_clarification = True
            answer = (
                "#### 🔍 No reference manuals are currently indexed/loaded.\n\n"
                "Please upload the relevant vehicle maintenance PDF manuals in the sidebar and index them before asking questions."
            )
        else:
            # Check the closest match distance (lower L2 distance = closer match)
            best_distance = retrieved[0]["distance"]
            if best_distance > CONFIDENCE_THRESHOLD:
                is_clarification = True
                answer = (
                    f"#### ⚠️Sorry! I couldn't answer this question.\n\n"
                    "I could not locate highly relevant information in the manuals to answer your question safely. "
                    "To prevent generating unreliable or potentially dangerous vehicle maintenance instructions, "
                    "please specify your query with additional context, such as:\n"
                    "- **Truck Model / Engine Type** (e.g., Komatsu HD325, Freightliner)\n"
                    "- **Specific Subsystem** (e.g., front disc brakes, hydraulic cylinder, oil filter)\n"
                    "- **Operational Symptom or specific manual section**"
                )
            else:
                answer = generate_answer(question, retrieved)

    # Store

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "is_clarification": is_clarification
        }
    )

    st.session_state.retrieved = retrieved

    # Display Answer

    with st.chat_message("assistant"):
        if is_clarification:
            show_clarification(answer)
        else:
            show_answer(answer)

    # Display Sources
    with st.expander("📄 View Retrieved Sources"):
        show_sources(retrieved)

# --------------------------------------------------
# Metrics  (live, from ChromaDB)
# --------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div class="metrics-label">📈 Live Knowledge Base Metrics</div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📚 Manuals", kb["unique_sources"])

with col2:
    st.metric("🧩 Chunks", kb["total_chunks"])

with col3:
    st.metric("🗄 Vector DB", "ChromaDB")

with col4:
    st.metric("🧠 Model", "MiniLM-L6")