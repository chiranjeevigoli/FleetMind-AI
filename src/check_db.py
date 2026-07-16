import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("fleetmind_manuals")

print("Total documents:", collection.count())