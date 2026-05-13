from src.schemas.claim_schema import ClaimInput, ClaimDecision, PolicyCitation


claim = ClaimInput(
    claim_id="CLM-001",
    customer_description="I was rear-ended at a red light and my rear bumper was damaged.",
    policy_state="IL",
    invoice_file_path="data/invoices/invoice_001.pdf"
)

citation = PolicyCitation(
    state="IL",
    source_document="illinois_auto_policy.pdf",
    page_number=4,
    clause_text="Collision coverage applies when the insured vehicle is damaged due to impact with another vehicle.",
    relevance_score=0.91
)

decision = ClaimDecision(
    decision="Approve",
    confidence=0.92,
    reasoning="The accident appears to be a covered collision event based on the customer description and policy clause.",
    policy_citations=[citation]
)

print(claim)
print(decision.model_dump())