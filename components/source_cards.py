import streamlit as st


def show_sources(retrieved_documents):

    st.markdown(
        """
        <div class="sources-header">
            <span>📄</span> Retrieved Manual Sources
        </div>
        """,
        unsafe_allow_html=True,
    )

    for index, doc in enumerate(retrieved_documents, start=1):

        metadata = doc["metadata"]
        source   = metadata.get("source", "Unknown")
        page     = metadata.get("page", "N/A")
        distance = doc.get("distance", None)
        text     = doc["text"][:280]

        # Confidence badge colour
        if distance is not None:
            if distance < 0.70:
                badge_cls, badge_label = "badge-high",   "High Match"
            elif distance < 1.00:
                badge_cls, badge_label = "badge-medium", "Good Match"
            else:
                badge_cls, badge_label = "badge-low",    "Partial Match"
            confidence_html = f'<span class="conf-badge {badge_cls}">{badge_label}</span>'
        else:
            confidence_html = ""

        st.markdown(
            f"""
            <div class="source-card">
                <div class="source-header">
                    <span class="source-index">#{index}</span>
                    <span class="source-filename">📘 {source}</span>
                    {confidence_html}
                </div>
                <div class="source-meta">
                    <span>📄 Page <strong>{page}</strong></span>
                    {"<span>📏 Distance: <strong>" + f"{distance:.3f}" + "</strong></span>" if distance is not None else ""}
                </div>
                <div class="source-excerpt">
                    {text}…
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )