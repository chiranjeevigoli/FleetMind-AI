import streamlit as st

def show_hero():
    st.markdown("""
<div class="hero-card">
<h1>🚛 FleetMind AI</h1>
<h3>AI-Powered Heavy Equipment Maintenance Assistant</h3>
<p>
Search technical manuals using
<strong>Generative AI</strong>,
<strong>RAG</strong>,
<strong>Sentence Transformers</strong>,
and
<strong>ChromaDB</strong>.
</p>
</div>
""", unsafe_allow_html=True)