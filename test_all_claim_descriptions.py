from pathlib import Path
from src.parsing.claim_description_parser import parse_claim_description_basic


description_folder = Path("data/claim_descriptions")

text_files = sorted(description_folder.glob("*.txt"))

print(f"Found {len(text_files)} claim description files.\n")

for text_file in text_files:
    print("=" * 80)
    print(f"FILE: {text_file.name}")

    try:
        description_text = text_file.read_text(encoding="utf-8")
        parsed_claim = parse_claim_description_basic(description_text)
        data = parsed_claim.model_dump()

        print(f"Incident Type: {data['incident_type']}")
        print(f"Collision Type: {data['collision_type']}")
        print(f"Severity: {data['incident_severity']}")
        print(f"Property Damage: {data['property_damage']}")
        print(f"Police Report Available: {data['police_report_available']}")
        print(f"Claim State: {data['claim_state']}")
        print(f"Fraud Signals: {data['possible_fraud_signals']}")

    except Exception as e:
        print(f"ERROR parsing {text_file.name}: {e}")

print("\nFinished parsing all claim descriptions.")