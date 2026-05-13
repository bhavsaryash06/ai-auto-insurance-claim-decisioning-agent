from src.retrieval.policy_retriever import retrieve_policy_citations


query = """
The customer was rear-ended at a red light.
The rear bumper and trunk were damaged.
Is this covered under collision coverage?
"""

citations = retrieve_policy_citations(query=query, k=3)

print(f"Retrieved {len(citations)} policy citations.\n")

for i, citation in enumerate(citations, start=1):
    print("=" * 80)
    print(f"CITATION {i}")
    print(f"State: {citation.state}")
    print(f"Source: {citation.source_document}")
    print(f"Relevance Score: {citation.relevance_score}")
    print("Clause Preview:")
    print(citation.clause_text[:1000])