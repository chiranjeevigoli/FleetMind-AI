import streamlit as st


def show_hero():
    # ── Hero Banner (pure CSS gradient — no inline base64) ────────
    st.markdown(
        """
        <div class="hero-card">
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
        """,
        unsafe_allow_html=True,
    )

    # ── Feature Cards (use st.image — no base64 in HTML) ─────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.image("assets/images/truck_engine_mechanic.png", use_container_width=True)
        st.markdown(
            """
            <div class="feature-card-body">
                <h4>🔧 Engine &amp; Drivetrain</h4>
                <p>Instant answers on engine overhauls, oil specifications, torque values,
                and drivetrain maintenance procedures.</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.image("assets/images/truck_dashboard_ai.png", use_container_width=True)
        st.markdown(
            """
            <div class="feature-card-body">
                <h4>🤖 AI Fleet Intelligence</h4>
                <p>Powered by Google Gemini and vector search to surface the most relevant
                manual sections in seconds.</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )