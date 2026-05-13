from fastapi import FastAPI
from pydantic import BaseModel

from src.agents.claim_pipeline import run_claim_decision_pipeline


app = FastAPI(
    title="AI Auto Insurance Claim Decisioning API",
    description="API for parsing claims, retrieving policy evidence, and generating claim decisions.",
    version="1.0.0",
)


class ClaimDecisionRequest(BaseModel):
    claim_description_path: str
    invoice_file_path: str
    claim_state: str


@app.get("/")
def root():
    return {
        "message": "AI Auto Insurance Claim Decisioning API is running",
        "status": "healthy",
    }


@app.post("/decide-claim")
def decide_claim(request: ClaimDecisionRequest):
    result = run_claim_decision_pipeline(
        claim_description_path=request.claim_description_path,
        invoice_file_path=request.invoice_file_path,
        claim_state=request.claim_state,
    )

    return result