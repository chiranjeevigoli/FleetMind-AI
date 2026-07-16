# Import our own modules
from pdf_loader import load_documents
from chunker import chunk_documents


# Load all PDF pages
documents = load_documents("data/manuals")

print(f"Pages Loaded : {len(documents)}")

# Create chunks
chunks = chunk_documents(documents)

print(f"Chunks Created : {len(chunks)}")

print("\nFirst Chunk\n")
print("-" * 60)

print(chunks[0]["text"])

print("\n")

print("Source :", chunks[0]["source"])
print("Page :", chunks[0]["page"])