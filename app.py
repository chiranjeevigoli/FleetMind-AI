from src.retriever import retrieve
from src.llm import generate_answer
from src.vector_store import get_collection_stats

from components.hero import show_hero
from components.answer_card import show_answer
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

    st.title("🚛 FleetMind AI")

    st.markdown("---")

    st.subheader("Knowledge Base")

    st.success(f"📚 Manuals Loaded : {kb['unique_sources']}")

    st.info(f"🧩 Indexed Chunks : {kb['total_chunks']}")

    st.info("🗄 Vector Database : ChromaDB")

    st.info("🧠 Embedding : all-MiniLM-L6-v2")

    st.info("🤖 LLM : Gemini")

    # ── Upload Documents Panel ──────────────────────────────────
    show_upload_panel()

    st.markdown("---")

    st.caption("Version 1.1")


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

            show_answer(message["content"])

        else:

            st.markdown(message["content"])


# --------------------------------------------------
# Chat Input
# --------------------------------------------------

question = st.chat_input("Ask a maintenance question...")

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

    with st.spinner("Searching manuals..."):

        retrieved = retrieve(question)

        answer = generate_answer(question, retrieved)

    # Store

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.session_state.retrieved = retrieved

    # Display Answer

    with st.chat_message("assistant"):
        show_answer(answer)

    # Display Sources
    with st.expander("📄 View Retrieved Sources"):
        show_sources(retrieved)

# --------------------------------------------------
# Metrics  (live, from ChromaDB)
# --------------------------------------------------

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Manuals", kb["unique_sources"])

with col2:
    st.metric("Chunks", kb["total_chunks"])

with col3:
    st.metric("Vector DB", "ChromaDB")

with col4:
    st.metric("Model", "MiniLM-L6")