from pathlib import Path

from src.parsing.invoice_parser import parse_invoice_basic
from src.parsing.claim_description_parser import parse_claim_description_basic
from src.retrieval.policy_retriever import retrieve_policy_citations
from src.decisioning.claim_decision_engine import make_basic_claim_decision
from src.decisioning.llm_explanation_generator import generate_llm_explanation


def run_claim_decision_pipeline(
    claim_description_path: str,
    invoice_file_path: str,
    claim_state: str,
) -> dict:
    """
    Full end-to-end claim decisioning pipeline.

    Input:
    - claim description text file
    - repair invoice PDF
    - claim state

    Output:
    - parsed claim
    - parsed invoice
    - policy citations
    - rule-based decision
    - LLM explanation
    """

    # Step 1: Read claim description
    description_text = Path(claim_description_path).read_text(encoding="utf-8")

    # Step 2: Parse claim description
    parsed_claim = parse_claim_description_basic(description_text)
    
    # Use selected claim state as the authoritative state for this run
    parsed_claim.claim_state = claim_state
    
    # Step 3: Parse invoice
    invoice_data = parse_invoice_basic(invoice_file_path)

    # Step 4: Build policy retrieval query
    query = f"""
    Incident type: {parsed_claim.incident_type}
    Collision type: {parsed_claim.collision_type}
    Severity: {parsed_claim.incident_severity}
    Police report available: {parsed_claim.police_report_available}
    Risk signals: {parsed_claim.possible_fraud_signals}
    Invoice total: {invoice_data.total_amount}
    Vehicle damage line items: {invoice_data.line_items}
    """

    # Step 5: Retrieve policy citations for selected state
    policy_citations = retrieve_policy_citations(
        query=query,
        k=3,
        claim_state=claim_state,
    )

    # Step 6: Make rule-based decision
    decision = make_basic_claim_decision(
        parsed_claim=parsed_claim,
        invoice_data=invoice_data,
        policy_citations=policy_citations,
    )

    # Step 7: Generate LLM explanation
    llm_explanation = generate_llm_explanation(
        parsed_claim=parsed_claim,
        invoice_data=invoice_data,
        decision=decision,
    )

    # Step 8: Return final pipeline output
    return {
        "claim_state": claim_state,
        "parsed_claim": parsed_claim.model_dump(),
        "invoice_data": invoice_data.model_dump(),
        "policy_citations": [
            citation.model_dump() for citation in policy_citations
        ],
        "decision": decision.model_dump(),
        "llm_explanation": llm_explanation,
    }