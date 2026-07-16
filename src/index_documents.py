# Import project modules
from pdf_loader import load_documents
from chunker import chunk_documents
from embedding_generator import generate_embeddings
from vector_store import store_embeddings


def main():
    """
    Complete indexing pipeline.

    PDF
      ↓
    Text
      ↓
    Chunks
      ↓
    Embeddings
      ↓
    ChromaDB
    """

    print("Loading PDF manuals...")
    documents = load_documents("data/manuals")

    print(f"Loaded {len(documents)} pages.")

    print("\nCreating chunks...")
    chunks = chunk_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("\nGenerating embeddings...")
    embedded_chunks = generate_embeddings(chunks)

    print("\nSaving embeddings to ChromaDB...")
    store_embeddings(embedded_chunks)

    print("\n Indexing completed successfully!")


if __name__ == "__main__":
    main()