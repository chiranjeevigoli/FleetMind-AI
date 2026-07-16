import streamlit as st


def show_sources(retrieved_documents):

    st.markdown(" 📄 Sources")

    for index, doc in enumerate(retrieved_documents, start=1):

        metadata = doc["metadata"]

        source = metadata.get("source", "Unknown")

        page = metadata.get("page", "N/A")

        text = doc["text"][:250]

        st.markdown(
            f"""
<div class="source-card">

<b>Source {index}</b><br><br>

📘 <b>{source}</b><br>

📄 Page: <b>{page}</b><br><br>

{text}...

</div>
""",
            unsafe_allow_html=True,
        )