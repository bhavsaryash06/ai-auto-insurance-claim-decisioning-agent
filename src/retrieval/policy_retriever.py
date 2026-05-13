from src.schemas.claim_schema import PolicyCitation
from src.retrieval.policy_vectorstore import search_policy


def get_state_from_source(source_document: str | None) -> str | None:
    """
    Detect state code from policy PDF filename.
    """
    if not source_document:
        return None

    if source_document.startswith("IL"):
        return "IL"
    elif source_document.startswith("IN"):
        return "IN"
    elif source_document.startswith("OH"):
        return "OH"

    return None


def retrieve_policy_citations(
    query: str,
    k: int = 5,
    claim_state: str | None = None,
) -> list[PolicyCitation]:
    """
    Retrieve relevant policy chunks and convert them into PolicyCitation objects.

    If claim_state is provided, only return citations from that state.
    """
    results = search_policy(query=query, k=k * 3)

    citations = []

    for doc, score in results:
        source_document = doc.metadata.get("source")
        state = get_state_from_source(source_document)

        if claim_state and state != claim_state:
            continue

        citation = PolicyCitation(
            state=state,
            source_document=source_document,
            page_number=None,
            clause_text=doc.page_content,
            relevance_score=float(score),
        )

        citations.append(citation)

        if len(citations) >= k:
            break

    return citations