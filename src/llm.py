import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables (works locally)
load_dotenv(override=True)

# Read API key — Streamlit Cloud secrets take priority, .env used locally
def _get_api_key():
    # 1. Try reading directly from local .env to bypass Streamlit's environment injection
    try:
        import dotenv
        env_vals = dotenv.dotenv_values(".env")
        key = env_vals.get("GOOGLE_API_KEY")
        if key and not key.startswith("your-"):
            return key
    except Exception:
        pass

    # 2. Fall back to Streamlit secrets (e.g., in Streamlit Cloud)
    try:
        key = st.secrets["GOOGLE_API_KEY"]
        if key and not key.startswith("your-"):
            return key
    except Exception:
        pass

    # 3. Fall back to standard environment variable
    return os.getenv("GOOGLE_API_KEY")

# Initialize Gemini Client
client = genai.Client(
    api_key=_get_api_key()
)


def generate_answer(question, retrieved_chunks):
    """
    Generates an answer using Gemini based only on the retrieved
    context from the vector database.
    """

    # --------------------------------------------------------
    # Remove duplicate chunks
    # --------------------------------------------------------

    unique_chunks = []
    seen = set()

    for chunk in retrieved_chunks:
        if chunk["text"] not in seen:
            seen.add(chunk["text"])
            unique_chunks.append(chunk)

    # --------------------------------------------------------
    # Build Context
    # --------------------------------------------------------

    context = ""
    sources = []

    for i, chunk in enumerate(unique_chunks, start=1):

        source = chunk["metadata"].get("source", "Unknown Source")
        page = chunk["metadata"].get("page", "Unknown Page")
        text = chunk["text"]

        context += f"""
==========================
Document {i}

Source : {source}
Page   : {page}

Content:
{text}

==========================

"""

        sources.append(f"{source} (Page {page})")

    # Remove duplicate sources
    unique_sources = list(dict.fromkeys(sources))

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
You are FleetMind AI, an AI assistant specialized in heavy-duty truck maintenance manuals.

Your job is to answer ONLY using the retrieved context.

Rules:

1. Answer ONLY from the provided context.
2. Never use your own knowledge.
3. Never guess or invent maintenance procedures.
4. If the answer is not available in the context, reply exactly:
"I couldn't find this information in the provided manuals."
5. Combine information from multiple documents whenever appropriate.
6. Keep the answer clear, professional and concise.
7. Do NOT mention "Document 1", "Document 2", etc.
8. Do NOT mention that you were given context.
9. Focus on helping maintenance engineers.

Retrieved Context:

{context}

User Question:

{question}

Answer:
"""

    # --------------------------------------------------------
    # Gemini Generation
    # --------------------------------------------------------

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        answer = response.text.strip()

    except Exception as e:
        return f" AI model unavailable.\n\n{e}"

    # --------------------------------------------------------
    # Append Sources
    # --------------------------------------------------------

    answer += "\n\nSources:\n"

    for source in unique_sources:
        answer += f"• {source}\n"

    return answer