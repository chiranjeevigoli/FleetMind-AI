import chromadb
from sentence_transformers import SentenceTransformer

# Load the same embedding model used during indexing
model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB client (persistent connection)
_client = chromadb.PersistentClient(path="chroma_db")


def _get_collection():
    """
    Always return a fresh handle to the collection so that newly
    uploaded documents are immediately visible without restarting.
    """
    return _client.get_or_create_collection("fleetmind_manuals")


def retrieve(query, top_k=5):
    """
    Retrieve the most relevant chunks for a query.
    """

    query_embedding = model.encode(query).tolist()

    collection = _get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_docs = []

    for i in range(len(results["documents"][0])):

        retrieved_docs.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return retrieved_docs