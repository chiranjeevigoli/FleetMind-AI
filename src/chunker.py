# Import RecursiveCharacterTextSplitter for intelligent text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    """
    Splits extracted PDF pages into smaller overlapping chunks.

    Args:
        documents (list): List of dictionaries containing
                          source, page number and extracted text.

    Returns:
        list: List of chunk dictionaries with metadata.
    """

    # Create the text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    # Store all generated chunks
    chunks = []

    # Process every page
    for doc in documents:

        # Split one page into multiple chunks
        split_texts = splitter.split_text(doc["text"])

        # Store each chunk with its metadata
        for text in split_texts:

            chunks.append({
                "source": doc["source"],
                "page": doc["page"],
                "text": text
            })

    return chunks