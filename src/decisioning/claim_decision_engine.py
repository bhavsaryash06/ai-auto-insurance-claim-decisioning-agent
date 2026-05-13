from src.schemas.claim_schema import ClaimDecision, InvoiceData, ParsedClaimDescription, PolicyCitation


def make_basic_claim_decision(
    parsed_claim: ParsedClaimDescription,
    invoice_data: InvoiceData,
    policy_citations: list[PolicyCitation],
) -> ClaimDecision:
    """
    Basic rule-based claim decision engine.
    This is the first version.
    Later, we will improve it using LLM reasoning + LangGraph.
    """

    decision = "Human Review"
    confidence = 0.60
    reasoning_parts = []

    incident_type = parsed_claim.incident_type
    collision_type = parsed_claim.collision_type
    severity = parsed_claim.incident_severity
    police_report_available = parsed_claim.police_report_available
    fraud_signals = parsed_claim.possible_fraud_signals
    total_amount = invoice_data.total_amount

    # Rule 1: Mechanical breakdown usually needs review or denial
    if incident_type == "mechanical / other":
        decision = "Human Review"
        confidence = 0.55
        reasoning_parts.append(
            "The claim includes a mechanical breakdown component, which may not be covered unless related physical damage is validated."
        )

    # Rule 2: Clear covered collision with invoice and citations
    elif incident_type == "collision" and total_amount and total_amount > 0 and policy_citations:
        if fraud_signals:
            decision = "Human Review"
            confidence = 0.68
            reasoning_parts.append(
                "The claim appears to involve a collision, but fraud or risk signals were detected."
            )
        else:
            decision = "Approve"
            confidence = 0.88
            reasoning_parts.append(
                "The claim appears to involve a covered collision event with supporting repair invoice data and relevant policy citations."
            )

    # Rule 3: Comprehensive-style events
    elif incident_type in ["weather", "fire", "theft", "vandalism", "animal collision", "falling object", "comprehensive"]:
        if total_amount and total_amount > 0 and policy_citations:
            if incident_type == "theft" and police_report_available is not True:
                decision = "Human Review"
                confidence = 0.65
                reasoning_parts.append(
                    "The claim involves theft, but a confirmed police report is missing."
                )
            elif incident_type == "vandalism" and police_report_available is not True:
                decision = "Human Review"
                confidence = 0.65
                reasoning_parts.append(
                    "The claim involves vandalism, but a confirmed police report is missing."
                )
            else:
                decision = "Approve"
                confidence = 0.84
                reasoning_parts.append(
                    "The claim appears to involve a covered comprehensive-style event with supporting repair invoice data and relevant policy citations."
                )
        else:
            decision = "Human Review"
            confidence = 0.58
            reasoning_parts.append(
                "The claim may involve a comprehensive-style event, but invoice data or policy evidence is incomplete."
            )

    # Rule 4: No invoice amount
    elif not total_amount:
        decision = "Human Review"
        confidence = 0.52
        reasoning_parts.append(
            "The repair invoice total amount could not be validated."
        )

    # Rule 5: High severity claims need extra review
    if severity == "high" and total_amount and total_amount >= 10000:
        decision = "Human Review"
        confidence = min(confidence, 0.72)
        reasoning_parts.append(
            "The claim severity and repair amount are high, so manual adjuster review is recommended."
        )

    # Rule 6: Fraud signals
    if fraud_signals:
        decision = "Human Review"
        confidence = min(confidence, 0.70)
        reasoning_parts.append(
            f"Risk signals detected: {', '.join(fraud_signals)}."
        )

    # Policy evidence summary
    if policy_citations:
        reasoning_parts.append(
            f"{len(policy_citations)} relevant policy citation(s) were retrieved to support the decision."
        )
    else:
        reasoning_parts.append(
            "No policy citations were retrieved, so the claim cannot be fully validated."
        )

    reasoning = " ".join(reasoning_parts)

    return ClaimDecision(
        decision=decision,
        confidence=confidence,
        reasoning=reasoning,
        policy_citations=policy_citations,
        invoice_data=invoice_data,
    )