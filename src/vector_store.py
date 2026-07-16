# Import ChromaDB
import chromadb


def store_embeddings(chunks):
    """
    Stores chunk embeddings and metadata in ChromaDB.
    REPLACES the entire collection (used during initial indexing).

    Args:
        chunks (list): List of chunks with embeddings.

    Returns:
        Collection: ChromaDB collection.
    """

    # Create a persistent database
    client = chromadb.PersistentClient(path="chroma_db")

    # Delete the collection if it already exists
    try:
        client.delete_collection("fleetmind_manuals")
    except Exception:
        pass

    # Create a fresh collection
    collection = client.get_or_create_collection(
        name="fleetmind_manuals"
    )

    # Add every chunk into ChromaDB
    for index, chunk in enumerate(chunks):

        collection.add(
            ids=[str(index)],
            embeddings=[chunk["embedding"]],
            documents=[chunk["text"]],
            metadatas=[{
                "source": chunk["source"],
                "page": chunk["page"]
            }]
        )

    return collection


def append_embeddings(chunks, start_id: int = None):
    """
    Appends new chunk embeddings to the EXISTING ChromaDB collection.
    Existing data is preserved — only new chunks are added.

    Args:
        chunks (list): List of chunks with embeddings.
        start_id (int): Starting ID offset. If None, auto-detected from
                        current collection size.

    Returns:
        Collection: ChromaDB collection.
    """

    client = chromadb.PersistentClient(path="chroma_db")
    collection = client.get_or_create_collection(name="fleetmind_manuals")

    if start_id is None:
        start_id = collection.count()

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

    return collection


def get_collection_stats() -> dict:
    """
    Returns live stats from ChromaDB.

    Returns:
        dict with keys: "total_chunks", "unique_sources"
    """
    try:
        client = chromadb.PersistentClient(path="chroma_db")
        collection = client.get_or_create_collection("fleetmind_manuals")
        total_chunks = collection.count()
        all_meta = collection.get(include=["metadatas"])
        sources = set()
        for meta in all_meta.get("metadatas", []):
            if meta and "source" in meta:
                sources.add(meta["source"])
        return {"total_chunks": total_chunks, "unique_sources": len(sources)}
    except Exception:
        return {"total_chunks": 0, "unique_sources": 0}