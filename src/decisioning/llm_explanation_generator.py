from openai import OpenAI

from src.config.settings import settings
from src.schemas.claim_schema import ClaimDecision, ParsedClaimDescription, InvoiceData


client = OpenAI(api_key=settings.openai_api_key)


def generate_llm_explanation(
    parsed_claim: ParsedClaimDescription,
    invoice_data: InvoiceData,
    decision: ClaimDecision,
) -> str:
    """
    Generate a professional adjuster-style explanation using OpenAI.
    The LLM does not change the decision. It only explains the rule-based decision.
    """

    policy_summaries = []

    for citation in decision.policy_citations[:3]:
        policy_summaries.append(
            {
                "state": citation.state,
                "source_document": citation.source_document,
                "clause_preview": citation.clause_text[:800],
            }
        )

    prompt = f"""
You are an auto insurance claim decisioning assistant.

Your job:
Write a professional, clear, adjuster-style explanation for the claim decision.

Important rules:
- Do NOT change the decision.
- Do NOT invent facts.
- Use only the provided claim, invoice, and policy citation information.
- Mention why the claim was approved, denied, or sent to human review.
- Keep the explanation concise but business-professional.
- Avoid legal advice.
- Avoid saying the claim is guaranteed payable.
- Use evidence-based wording.

Rule-based decision:
Decision: {decision.decision}
Confidence: {decision.confidence}
Rule-based reasoning: {decision.reasoning}

Parsed claim:
Incident type: {parsed_claim.incident_type}
Collision type: {parsed_claim.collision_type}
Severity: {parsed_claim.incident_severity}
Police report available: {parsed_claim.police_report_available}
Property damage: {parsed_claim.property_damage}
Fraud / risk signals: {parsed_claim.possible_fraud_signals}
Claim summary: {parsed_claim.accident_summary}

Invoice data:
Invoice number: {invoice_data.invoice_number}
Repair shop: {invoice_data.repair_shop_name}
Customer name: {invoice_data.customer_name}
Vehicle: {invoice_data.vehicle_year} {invoice_data.vehicle_make} {invoice_data.vehicle_model}
VIN: {invoice_data.vin}
Mileage: {invoice_data.mileage}
Total amount: {invoice_data.total_amount}
Line items: {invoice_data.line_items}

Policy citation summaries:
{policy_summaries}

Write the explanation in this format:

Decision Explanation:
<paragraph>

Key Evidence:
- <bullet>
- <bullet>
- <bullet>

Recommended Next Step:
<one sentence>
"""

    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {
                "role": "system",
                "content": "You are a careful auto insurance claim decisioning assistant.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content