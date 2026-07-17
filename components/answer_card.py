import streamlit as st

def show_answer(answer):

    st.markdown(" 🤖 FleetMind Response")

    st.markdown(
        f"""
<div class="answer-card">

{answer}

</div>
""",
        unsafe_allow_html=True,
    )


def show_clarification(message):

    st.markdown(" ⚠️ FleetMind Clarification Request")

    st.markdown(
        f"""
<div class="clarification-card">

{message}

</div>
""",
        unsafe_allow_html=True,
    )