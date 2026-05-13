from src.parsing.invoice_parser import extract_invoice_text, parse_invoice_basic


invoice_path = "data/invoices/invoice_001.pdf"

text = extract_invoice_text(invoice_path)
print("===== RAW INVOICE TEXT =====")
print(text[:2000])

invoice_data = parse_invoice_basic(invoice_path)
print("\n===== STRUCTURED INVOICE DATA =====")
print(invoice_data.model_dump())