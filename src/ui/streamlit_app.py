import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

from src.agents.claim_pipeline import run_claim_decision_pipeline


st.set_page_config(
    page_title="AI Auto Insurance Claim Decisioning Agent",
    page_icon="🚗",
    layout="wide",
)


def format_currency(value):
    if value is None:
        return "N/A"
    return f"${value:,.2f}"


def show_decision_box(decision_label: str, confidence: float):
    if decision_label == "Approve":
        st.success(f"✅ Decision: {decision_label} | Confidence: {confidence}")
    elif decision_label == "Human Review":
        st.warning(f"⚠️ Decision: {decision_label} | Confidence: {confidence}")
    elif decision_label == "Deny":
        st.error(f"❌ Decision: {decision_label} | Confidence: {confidence}")
    else:
        st.info(f"Decision: {decision_label} | Confidence: {confidence}")


st.title("🚗 AI Auto Insurance Claim Decisioning Agent")

st.markdown(
    """
This portfolio app demonstrates an end-to-end AI insurance claim workflow:

1. Parse customer accident descriptions  
2. Extract structured data from repair invoice PDFs  
3. Retrieve policy evidence using RAG  
4. Apply business decision rules  
5. Generate an adjuster-style LLM explanation  
"""
)


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------

st.sidebar.title("Claim Input Controls")

claim_description_folder = Path("data/claim_descriptions")
invoice_folder = Path("data/invoices")

claim_files = sorted([file.name for file in claim_description_folder.glob("*.txt")])
invoice_files = sorted([file.name for file in invoice_folder.glob("*.pdf")])

selected_claim_file = st.sidebar.selectbox(
    "Select Claim Description",
    claim_files,
)

selected_invoice_file = st.sidebar.selectbox(
    "Select Invoice PDF",
    invoice_files,
)

selected_state = st.sidebar.selectbox(
    "Select Claim State",
    ["IL", "IN", "OH"],
)

run_button = st.sidebar.button("Run Claim Decision", type="primary")


claim_description_path = str(claim_description_folder / selected_claim_file)
invoice_file_path = str(invoice_folder / selected_invoice_file)


# ------------------------------------------------------------
# Input summary
# ------------------------------------------------------------

st.subheader("Selected Input")

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    st.info(f"Claim Description\n\n`{selected_claim_file}`")

with input_col2:
    st.info(f"Invoice PDF\n\n`{selected_invoice_file}`")

with input_col3:
    st.info(f"Claim State\n\n`{selected_state}`")


# ------------------------------------------------------------
# Run pipeline
# ------------------------------------------------------------

if run_button:
    with st.spinner("Running claim decision pipeline..."):
        result = run_claim_decision_pipeline(
            claim_description_path=claim_description_path,
            invoice_file_path=invoice_file_path,
            claim_state=selected_state,
        )

    st.success("Claim decision completed.")

    decision = result["decision"]
    parsed_claim = result["parsed_claim"]
    invoice_data = result["invoice_data"]
    policy_citations = result["policy_citations"]

    st.divider()

    # ------------------------------------------------------------
    # Final decision
    # ------------------------------------------------------------

    st.header("Final Claim Decision")

    decision_label = decision["decision"]
    confidence = decision["confidence"]

    show_decision_box(decision_label, confidence)

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        st.metric("Decision", decision_label)

    with metric_col2:
        st.metric("Confidence", confidence)

    with metric_col3:
        st.metric("Invoice Total", format_currency(invoice_data["total_amount"]))

    st.subheader("Rule-Based Reasoning")
    st.write(decision["reasoning"])

    st.subheader("LLM Explanation")
    st.markdown(result["llm_explanation"])

    # ------------------------------------------------------------
    # Parsed claim
    # ------------------------------------------------------------

    st.divider()
    st.header("Parsed Claim Description")

    claim_col1, claim_col2, claim_col3 = st.columns(3)

    with claim_col1:
        st.write(f"**Incident Type:** {parsed_claim['incident_type']}")
        st.write(f"**Collision Type:** {parsed_claim['collision_type']}")

    with claim_col2:
        st.write(f"**Severity:** {parsed_claim['incident_severity']}")
        st.write(f"**Police Report:** {parsed_claim['police_report_available']}")

    with claim_col3:
        st.write(f"**Claim State:** {parsed_claim['claim_state']}")
        st.write(f"**Property Damage:** {parsed_claim['property_damage']}")

    st.subheader("Accident Summary")
    st.write(parsed_claim["accident_summary"])

    st.subheader("Risk Signals")

    if parsed_claim["possible_fraud_signals"]:
        for signal in parsed_claim["possible_fraud_signals"]:
            st.warning(signal)
    else:
        st.success("No major risk signals detected.")

    # ------------------------------------------------------------
    # Invoice data
    # ------------------------------------------------------------

    st.divider()
    st.header("Parsed Invoice Data")

    invoice_col1, invoice_col2, invoice_col3 = st.columns(3)

    with invoice_col1:
        st.write(f"**Invoice Number:** {invoice_data['invoice_number']}")
        st.write(f"**Invoice Date:** {invoice_data['invoice_date']}")
        st.write(f"**Repair Shop:** {invoice_data['repair_shop_name']}")

    with invoice_col2:
        st.write(f"**Customer Name:** {invoice_data['customer_name']}")
        st.write(
            f"**Vehicle:** {invoice_data['vehicle_year']} "
            f"{invoice_data['vehicle_make']} {invoice_data['vehicle_model']}"
        )
        st.write(f"**VIN:** {invoice_data['vin']}")

    with invoice_col3:
        st.write(f"**Mileage:** {invoice_data['mileage']}")
        st.write(f"**Total Amount:** {format_currency(invoice_data['total_amount'])}")

    st.subheader("Invoice Line Items")

    line_items = invoice_data["line_items"]

    if line_items:
        line_item_df = pd.DataFrame(
            {
                "Line Item": line_items
            }
        )
        st.dataframe(line_item_df, use_container_width=True)
    else:
        st.info("No invoice line items extracted.")

    # ------------------------------------------------------------
    # Policy citations
    # ------------------------------------------------------------

    st.divider()
    st.header("Policy Evidence Citations")

    if policy_citations:
        for index, citation in enumerate(policy_citations, start=1):
            with st.expander(
                f"Citation {index} | State: {citation['state']} | Source: {citation['source_document']}"
            ):
                distance_score = citation["relevance_score"]

                if distance_score <= 1.05:
                    relevance_label = "High match"
                elif distance_score <= 1.20:
                    relevance_label = "Medium match"
                else:
                    relevance_label = "Low match"

                st.write(f"**Retrieval Distance Score:** {distance_score}")
                st.write(f"**Relevance Label:** {relevance_label}")
                st.caption("Lower distance score means stronger semantic similarity.")
                st.write("**Policy Clause:**")
                st.write(citation["clause_text"])
    else:
        st.warning("No policy citations retrieved.")

else:
    st.info("Select claim inputs from the sidebar and click **Run Claim Decision**.")