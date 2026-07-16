from retriever import retrieve

query = "When should I replace engine oil?"

results = retrieve(query)

print("\nRetrieved Results")
print("=" * 80)

documents = results["documents"][0]
metadatas = results["metadatas"][0]
distances = results["distances"][0]

for i in range(len(documents)):
    print(f"\nResult {i+1}")
    print("-" * 80)

    print("Document:")
    print(documents[i][:500])

    print("\nMetadata:")
    print(metadatas[i])

    print("\nDistance:")
    print(distances[i])