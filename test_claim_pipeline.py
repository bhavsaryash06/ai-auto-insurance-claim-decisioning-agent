from src.agents.claim_pipeline import run_claim_decision_pipeline


result = run_claim_decision_pipeline(
    claim_description_path="data/claim_descriptions/claim_015.txt",
    invoice_file_path="data/invoices/invoice_013.pdf",
    claim_state="OH",
)

print("===== FINAL PIPELINE RESULT =====")
print(f"Claim State: {result['claim_state']}")

print("\n===== PARSED CLAIM =====")
print(result["parsed_claim"])

print("\n===== INVOICE DATA =====")
print(result["invoice_data"])

print("\n===== DECISION =====")
print(result["decision"])

print("\n===== LLM EXPLANATION =====")
print(result["llm_explanation"])