from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class ClaimInput(BaseModel):
    claim_id: Optional[str] = Field(default=None, description="Unique claim identifier")
    customer_description: str = Field(description="Natural language accident description from customer")
    policy_state: Optional[str] = Field(default=None, description="Policy state such as IL, IN, or OH")
    invoice_file_path: Optional[str] = Field(default=None, description="Path to uploaded repair invoice PDF")


class InvoiceData(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    repair_shop_name: Optional[str] = None
    customer_name: Optional[str] = None
    vehicle_make: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_year: Optional[int] = None
    vin: Optional[str] = None
    mileage: Optional[int] = None
    total_amount: Optional[float] = None
    line_items: List[str] = Field(default_factory=list)

class ParsedClaimDescription(BaseModel):
    incident_type: Optional[str] = None
    collision_type: Optional[str] = None
    incident_severity: Optional[str] = None
    property_damage: Optional[bool] = None
    police_report_available: Optional[bool] = None
    claim_state: Optional[str] = None
    accident_summary: Optional[str] = None
    possible_fraud_signals: List[str] = Field(default_factory=list)

class PolicyCitation(BaseModel):
    state: Optional[str] = None
    source_document: Optional[str] = None
    page_number: Optional[int] = None
    clause_text: str
    relevance_score: Optional[float] = None


class ClaimDecision(BaseModel):
    decision: Literal["Approve", "Deny", "Human Review"]
    confidence: float = Field(ge=0, le=1)
    reasoning: str
    policy_citations: List[PolicyCitation] = Field(default_factory=list)
    invoice_data: Optional[InvoiceData] = None