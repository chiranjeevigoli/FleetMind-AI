import streamlit as st
import base64
from pathlib import Path


def _img_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(path).suffix.lstrip(".")
    return f"data:image/{ext};base64,{data}"


def show_sidebar_logo():
    logo_b64 = _img_to_base64("assets/images/truck_sidebar_logo.png")
    st.markdown(
        f"""
        <div class="sidebar-logo-wrap">
            <img src="{logo_b64}" class="sidebar-logo" alt="FleetMind Logo"/>
            <div class="sidebar-brand">
                <span class="sidebar-brand-title">FleetMind AI</span>
                <span class="sidebar-brand-sub">Fleet Maintenance Intelligence</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_answer(answer):
    st.markdown(
        """
        <div class="response-label">
            <span class="response-dot"></span> 🤖 FleetMind Response
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="answer-card">
            <div class="answer-icon">🚛</div>
            {answer}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_clarification(message):
    st.markdown(
        """
        <div class="response-label warn">
            <span class="response-dot warn-dot"></span> ⚠️ FleetMind Clarification Request
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="clarification-card">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )