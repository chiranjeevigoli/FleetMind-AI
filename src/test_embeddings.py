from pdf_loader import load_documents
from chunker import chunk_documents
from embedding_generator import generate_embeddings

# Load PDF pages
documents = load_documents("data/manuals")

# Split into chunks
chunks = chunk_documents(documents)

# Generate embeddings
embedded_chunks = generate_embeddings(chunks)

print("\nEmbedding Dimension:", len(embedded_chunks[0]["embedding"]))

print("\nFirst 10 Values:")

print(embedded_chunks[0]["embedding"][:10])