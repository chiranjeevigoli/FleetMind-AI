# Import SentenceTransformer to generate embeddings
from sentence_transformers import SentenceTransformer


# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Converts text chunks into embedding vectors.

    Args:
        chunks (list): List of chunk dictionaries.

    Returns:
        list: Chunk dictionaries with embeddings added.
    """

    # Extract only the text from each chunk
    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")

    # Generate embeddings
    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    # Attach each embedding to its chunk
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()

    return chunks