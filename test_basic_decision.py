from pathlib import Path

from src.parsing.invoice_parser import parse_invoice_basic
from src.parsing.claim_description_parser import parse_claim_description_basic
from src.retrieval.policy_retriever import retrieve_policy_citations
from src.decisioning.claim_decision_engine import make_basic_claim_decision


# ------------------------------------------------------------
# Test input files
# ------------------------------------------------------------

description_path = Path("data/claim_descriptions/claim_001.txt")
invoice_path = "data/invoices/invoice_001.pdf"


# ------------------------------------------------------------
# Step 1: Read customer claim description
# ------------------------------------------------------------

description_text = description_path.read_text(encoding="utf-8")


# ------------------------------------------------------------
# Step 2: Parse claim description
# ------------------------------------------------------------

parsed_claim = parse_claim_description_basic(description_text)


# ------------------------------------------------------------
# Step 3: Parse invoice PDF
# ------------------------------------------------------------

invoice_data = parse_invoice_basic(invoice_path)


# ------------------------------------------------------------
# Step 4: Build retrieval query for policy search
# ------------------------------------------------------------

query = f"""
Incident type: {parsed_claim.incident_type}
Collision type: {parsed_claim.collision_type}
Severity: {parsed_claim.incident_severity}
Police report available: {parsed_claim.police_report_available}
Invoice total: {invoice_data.total_amount}
Vehicle damage line items: {invoice_data.line_items}
"""


# ------------------------------------------------------------
# Step 5: Retrieve policy citations
# ------------------------------------------------------------
# Option A: Use parsed claim state if available.
# For claim_001, claim_state is None, so this may return IL/IN/OH together.

policy_citations = retrieve_policy_citations(
    query=query,
    k=3,
    claim_state="IL",
)

# Option B: Force state filtering for testing.
# Uncomment this block if you want to test only Illinois citations.
#
# policy_citations = retrieve_policy_citations(
#     query=query,
#     k=3,
#     claim_state="IL",
# )


# ------------------------------------------------------------
# Step 6: Make basic claim decision
# ------------------------------------------------------------

decision = make_basic_claim_decision(
    parsed_claim=parsed_claim,
    invoice_data=invoice_data,
    policy_citations=policy_citations,
)


# ------------------------------------------------------------
# Step 7: Print results
# ------------------------------------------------------------

print("===== PARSED CLAIM =====")
print(parsed_claim.model_dump())

print("\n===== INVOICE DATA =====")
print(invoice_data.model_dump())

print("\n===== POLICY CITATIONS COUNT =====")
print(len(policy_citations))

print("\n===== POLICY CITATIONS SUMMARY =====")

for i, citation in enumerate(policy_citations, start=1):
    print("=" * 80)
    print(f"CITATION {i}")
    print(f"State: {citation.state}")
    print(f"Source: {citation.source_document}")
    print(f"Relevance Score: {citation.relevance_score}")
    print("Clause Preview:")
    print(citation.clause_text[:500])

print("\n===== FINAL CLAIM DECISION =====")
print(decision.model_dump())