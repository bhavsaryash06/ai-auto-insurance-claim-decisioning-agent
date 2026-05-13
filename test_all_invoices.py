from pathlib import Path
from src.parsing.invoice_parser import parse_invoice_basic


invoice_folder = Path("data/invoices")

pdf_files = sorted(invoice_folder.glob("*.pdf"))

print(f"Found {len(pdf_files)} invoice PDF files.\n")

for pdf_file in pdf_files:
    print("=" * 80)
    print(f"FILE: {pdf_file.name}")

    try:
        invoice_data = parse_invoice_basic(str(pdf_file))
        data = invoice_data.model_dump()

        print(f"Invoice Number: {data['invoice_number']}")
        print(f"Invoice Date: {data['invoice_date']}")
        print(f"Repair Shop: {data['repair_shop_name']}")
        print(f"Customer Name: {data['customer_name']}")
        print(f"Vehicle: {data['vehicle_year']} {data['vehicle_make']} {data['vehicle_model']}")
        print(f"VIN: {data['vin']}")
        print(f"Mileage: {data['mileage']}")
        print(f"Total Amount: {data['total_amount']}")
        print(f"Line Items Extracted: {len(data['line_items'])}")

    except Exception as e:
        print(f"ERROR parsing {pdf_file.name}: {e}")

print("\nFinished parsing all invoices.")