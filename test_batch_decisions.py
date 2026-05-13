from pathlib import Path

from src.parsing.invoice_parser import parse_invoice_basic
from src.parsing.claim_description_parser import parse_claim_description_basic
from src.retrieval.policy_retriever import retrieve_policy_citations
from src.decisioning.claim_decision_engine import make_basic_claim_decision


test_cases = [
    {
        "name": "Rear-end collision",
        "claim_file": "claim_001.txt",
        "invoice_file": "invoice_001.pdf",
        "claim_state": "IL",
    },
    {
        "name": "Theft recovery",
        "claim_file": "claim_012.txt",
        "invoice_file": "invoice_005.pdf",
        "claim_state": "IN",
    },
    {
        "name": "Hit-and-run without police report",
        "claim_file": "claim_015.txt",
        "invoice_file": "invoice_013.pdf",
        "claim_state": "OH",
    },
    {
        "name": "Mechanical breakdown with debris damage",
        "claim_file": "claim_018.txt",
        "invoice_file": "invoice_014.pdf",
        "claim_state": "OH",
    },
    {
        "name": "Severe head-on collision",
        "claim_file": "claim_019.txt",
        "invoice_file": "invoice_015.pdf",
        "claim_state": "IL",
    },
]


for test_case in test_cases:
    print("=" * 100)
    print(f"TEST CASE: {test_case['name']}")
    print("=" * 100)

    description_path = Path("data/claim_descriptions") / test_case["claim_file"]
    invoice_path = Path("data/invoices") / test_case["invoice_file"]

    description_text = description_path.read_text(encoding="utf-8")

    parsed_claim = parse_claim_description_basic(description_text)
    invoice_data = parse_invoice_basic(str(invoice_path))

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
        claim_state=test_case["claim_state"],
    )

    decision = make_basic_claim_decision(
        parsed_claim=parsed_claim,
        invoice_data=invoice_data,
        policy_citations=policy_citations,
    )

    print(f"Claim File: {test_case['claim_file']}")
    print(f"Invoice File: {test_case['invoice_file']}")
    print(f"Forced Claim State: {test_case['claim_state']}")
    print("-" * 100)

    print(f"Incident Type: {parsed_claim.incident_type}")
    print(f"Collision Type: {parsed_claim.collision_type}")
    print(f"Severity: {parsed_claim.incident_severity}")
    print(f"Police Report: {parsed_claim.police_report_available}")
    print(f"Fraud Signals: {parsed_claim.possible_fraud_signals}")
    print(f"Invoice Total: {invoice_data.total_amount}")
    print(f"Policy Citations: {len(policy_citations)}")
    print("-" * 100)

    print(f"Decision: {decision.decision}")
    print(f"Confidence: {decision.confidence}")
    print(f"Reasoning: {decision.reasoning}")
    print()