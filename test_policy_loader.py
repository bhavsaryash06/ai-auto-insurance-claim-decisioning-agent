from src.ingestion.policy_loader import load_policy_documents, chunk_policy_documents


documents = load_policy_documents()

print("===== POLICY DOCUMENTS LOADED =====")
print(f"Total policy PDFs loaded: {len(documents)}")

for doc in documents:
    print("=" * 80)
    print(f"Source: {doc['source']}")
    print(f"Text length: {len(doc['text'])}")
    print("Preview:")
    print(doc["text"][:1000])


chunks = chunk_policy_documents()

print("\n===== POLICY CHUNKS CREATED =====")
print(f"Total chunks created: {len(chunks)}")

for chunk in chunks[:5]:
    print("=" * 80)
    print(f"Chunk ID: {chunk['chunk_id']}")
    print(f"Source: {chunk['source']}")
    print(chunk["text"][:500])