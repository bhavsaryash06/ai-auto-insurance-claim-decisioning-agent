from pathlib import Path

from src.parsing.invoice_parser import parse_invoice_basic
from src.parsing.claim_description_parser import parse_claim_description_basic
from src.retrieval.policy_retriever import retrieve_policy_citations
from src.decisioning.claim_decision_engine import make_basic_claim_decision
from src.decisioning.llm_explanation_generator import generate_llm_explanation


description_path = Path("data/claim_descriptions/claim_015.txt")
invoice_path = "data/invoices/invoice_013.pdf"
claim_state = "OH"

description_text = description_path.read_text(encoding="utf-8")

parsed_claim = parse_claim_description_basic(description_text)
invoice_data = parse_invoice_basic(invoice_path)

query = f"""
Incident type: {parsed_claim.incident_type}
Collision type: {parsed_claim.collision_type}
Severity: {parsed_claim.incident_severity}
Police report available: {parsed_claim.police_report_available}
Invoice total: {invoice_data.total_amount}
Vehicle damage line items: {invoice_data.line_items}
"""

policy_citations = retrieve_policy_citations(
    query=query,
    k=3,
    claim_state=claim_state,
)

decision = make_basic_claim_decision(
    parsed_claim=parsed_claim,
    invoice_data=invoice_data,
    policy_citations=policy_citations,
)

llm_explanation = generate_llm_explanation(
    parsed_claim=parsed_claim,
    invoice_data=invoice_data,
    decision=decision,
)

print("===== RULE-BASED DECISION =====")
print(decision.model_dump())

print("\n===== LLM EXPLANATION =====")
print(llm_explanation)