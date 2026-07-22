import streamlit as st


def show_sidebar_logo():
    """Renders the branded logo + title block at the top of the sidebar."""
    col_logo, col_text = st.columns([1, 2.5])
    with col_logo:
        st.image("assets/images/truck_sidebar_logo.png", use_container_width=True)
    with col_text:
        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="sidebar-brand-title">FleetMind AI</span><br>
                <span class="sidebar-brand-sub">Fleet Maintenance Intelligence</span>
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