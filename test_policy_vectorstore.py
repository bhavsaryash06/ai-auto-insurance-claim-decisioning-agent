from src.retrieval.policy_vectorstore import build_policy_vectorstore, search_policy


print("Building policy vector store...")
vectorstore = build_policy_vectorstore()
print("Policy vector store built successfully.")

print("\nSearching policy vector store...")

query = "collision coverage for damage to insured auto"
results = search_policy(query, k=5)

for i, (doc, score) in enumerate(results, start=1):
    print("=" * 80)
    print(f"RESULT {i}")
    print(f"Similarity Score: {score}")
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Chunk ID: {doc.metadata.get('chunk_id')}")
    print("Text Preview:")
    print(doc.page_content[:1000])