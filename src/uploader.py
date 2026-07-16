"""
uploader.py
-----------
Handles the full indexing pipeline for user-uploaded PDF files.
Unlike index_documents.py (which resets the DB), this module
APPENDS new documents to the existing ChromaDB collection so
previously indexed manuals are preserved.
"""

import io
import fitz  # PyMuPDF
import chromadb

from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ----------------------------------------------------------------
# Shared model (loaded once per process)
# ----------------------------------------------------------------

_embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------

def _extract_pages_from_bytes(file_bytes: bytes, filename: str) -> list[dict]:
    """
    Open a PDF from raw bytes and extract text page by page.

    Returns:
        list of {"source": str, "page": int, "text": str}
    """
    pages = []
    pdf = fitz.open(stream=file_bytes, filetype="pdf")

    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        text = page.get_text()

        if text.strip():          # skip blank pages
            pages.append({
                "source": filename,
                "page": page_num + 1,
                "text": text
            })

    pdf.close()
    return pages


def _chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Split pages into overlapping chunks using LangChain splitter.

    Returns:
        list of {"source": str, "page": int, "text": str}
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []
    for doc in pages:
        split_texts = splitter.split_text(doc["text"])
        for text in split_texts:
            chunks.append({
                "source": doc["source"],
                "page": doc["page"],
                "text": text
            })

    return chunks


def _embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Generate embeddings for each chunk and attach them in-place.
    """
    texts = [c["text"] for c in chunks]
    embeddings = _embed_model.encode(texts, show_progress_bar=False)

    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb.tolist()

    return chunks


def _get_next_id(collection) -> int:
    """
    Return the next available integer ID for ChromaDB entries.
    """
    existing = collection.count()
    return existing   # 0-based → next id == current count


def _already_indexed(collection, filename: str) -> bool:
    """
    Check whether this filename already has chunks in the collection.
    """
    results = collection.get(
        where={"source": filename},
        limit=1
    )
    return len(results["ids"]) > 0


# ----------------------------------------------------------------
# Public API
# ----------------------------------------------------------------

def index_uploaded_file(
    uploaded_file,          # st.UploadedFile object
    progress_callback=None  # optional callable(float 0-1, str message)
) -> dict:
    """
    Full pipeline: PDF bytes → ChromaDB (append).

    Args:
        uploaded_file : Streamlit UploadedFile (has .name and .read())
        progress_callback : optional fn(progress: float, message: str)

    Returns:
        dict with keys:
            "filename"  : str
            "pages"     : int   (non-blank pages extracted)
            "chunks"    : int   (chunks added)
            "skipped"   : bool  (True if already indexed)
            "error"     : str | None
    """
    filename = uploaded_file.name
    result = {
        "filename": filename,
        "pages": 0,
        "chunks": 0,
        "skipped": False,
        "error": None
    }

    def _report(p, msg):
        if progress_callback:
            progress_callback(p, msg)

    try:
        # 1. Connect to ChromaDB
        _report(0.0, "Connecting to vector database…")
        client = chromadb.PersistentClient(path="chroma_db")
        collection = client.get_or_create_collection("fleetmind_manuals")

        # 2. Skip if already indexed
        if _already_indexed(collection, filename):
            result["skipped"] = True
            _report(1.0, f"⚠️ '{filename}' is already indexed — skipped.")
            return result

        # 3. Extract text from PDF bytes
        _report(0.15, f"Extracting text from '{filename}'…")
        file_bytes = uploaded_file.read()
        pages = _extract_pages_from_bytes(file_bytes, filename)
        result["pages"] = len(pages)

        if not pages:
            result["error"] = "No readable text found in the PDF."
            return result

        # 4. Chunk
        _report(0.35, f"Creating chunks from {len(pages)} pages…")
        chunks = _chunk_pages(pages)

        # 5. Embed
        _report(0.55, f"Generating embeddings for {len(chunks)} chunks…")
        chunks = _embed_chunks(chunks)

        # 6. Store (append only)
        _report(0.80, "Saving to ChromaDB…")
        start_id = _get_next_id(collection)

        for i, chunk in enumerate(chunks):
            collection.add(
                ids=[str(start_id + i)],
                embeddings=[chunk["embedding"]],
                documents=[chunk["text"]],
                metadatas=[{
                    "source": chunk["source"],
                    "page": chunk["page"]
                }]
            )

        result["chunks"] = len(chunks)
        _report(1.0, f"✅ '{filename}' indexed — {len(chunks)} chunks added.")

    except Exception as exc:
        result["error"] = str(exc)
        _report(1.0, f"❌ Error indexing '{filename}': {exc}")

    return result


def get_kb_stats() -> dict:
    """
    Return live knowledge-base statistics from ChromaDB.

    Returns:
        dict with keys: "total_chunks", "unique_sources"
    """
    try:
        client = chromadb.PersistentClient(path="chroma_db")
        collection = client.get_or_create_collection("fleetmind_manuals")

        total_chunks = collection.count()

        # Fetch all metadata to count unique source filenames
        all_meta = collection.get(include=["metadatas"])
        sources = set()
        for meta in all_meta.get("metadatas", []):
            if meta and "source" in meta:
                sources.add(meta["source"])

        return {
            "total_chunks": total_chunks,
            "unique_sources": len(sources)
        }
    except Exception:
        return {"total_chunks": 0, "unique_sources": 0}
