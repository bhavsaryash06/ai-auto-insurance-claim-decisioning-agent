from pathlib import Path
from src.parsing.claim_description_parser import parse_claim_description_basic


description_path = Path("data/claim_descriptions/claim_001.txt")

description_text = description_path.read_text(encoding="utf-8")

parsed_claim = parse_claim_description_basic(description_text)

print("===== RAW CLAIM DESCRIPTION =====")
print(description_text)

print("\n===== STRUCTURED CLAIM DESCRIPTION =====")
print(parsed_claim.model_dump())