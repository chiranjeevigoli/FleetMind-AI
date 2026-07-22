import streamlit as st
import base64
from pathlib import Path


def _img_to_base64(path: str) -> str:
    """Convert an image file to a base64 data URI."""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(path).suffix.lstrip(".")
    return f"data:image/{ext};base64,{data}"


def show_hero():
    hero_b64 = _img_to_base64("assets/images/hero_truck_fleet.png")
    engine_b64 = _img_to_base64("assets/images/truck_engine_mechanic.png")
    dashboard_b64 = _img_to_base64("assets/images/truck_dashboard_ai.png")

    st.markdown(
        f"""
        <div class="hero-wrapper">
            <!-- Hero Banner -->
            <div class="hero-card" style="background-image: url('{hero_b64}');">
                <div class="hero-overlay">
                    <div class="hero-badge">⚡ AI-Powered Fleet Intelligence</div>
                    <h1 class="hero-title">🚛 FleetMind AI</h1>
                    <p class="hero-subtitle">AI-Powered Heavy Equipment Maintenance Assistant</p>
                    <p class="hero-desc">
                        Query technical manuals instantly using
                        <span class="hero-tag">Generative AI</span>
                        <span class="hero-tag">RAG</span>
                        <span class="hero-tag">Sentence Transformers</span>
                        <span class="hero-tag">ChromaDB</span>
                    </p>
                    <div class="hero-stats">
                        <div class="hero-stat-item">
                            <span class="stat-icon">🔧</span>
                            <span class="stat-label">Engine Diagnostics</span>
                        </div>
                        <div class="hero-stat-item">
                            <span class="stat-icon">📋</span>
                            <span class="stat-label">Manual Search</span>
                        </div>
                        <div class="hero-stat-item">
                            <span class="stat-icon">🛡️</span>
                            <span class="stat-label">Safety Compliance</span>
                        </div>
                        <div class="hero-stat-item">
                            <span class="stat-icon">⏱️</span>
                            <span class="stat-label">Real-time Answers</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Feature Cards Row -->
            <div class="feature-row">
                <div class="feature-card">
                    <div class="feature-img-wrap">
                        <img src="{engine_b64}" class="feature-img" alt="Engine Maintenance"/>
                    </div>
                    <div class="feature-card-body">
                        <h4>🔧 Engine & Drivetrain</h4>
                        <p>Instant answers on engine overhauls, oil specifications, torque values, and drivetrain maintenance procedures.</p>
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-img-wrap">
                        <img src="{dashboard_b64}" class="feature-img" alt="Fleet AI Dashboard"/>
                    </div>
                    <div class="feature-card-body">
                        <h4>🤖 AI Fleet Intelligence</h4>
                        <p>Powered by Google Gemini and vector search to surface the most relevant manual sections in seconds.</p>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )