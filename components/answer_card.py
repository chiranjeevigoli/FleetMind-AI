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