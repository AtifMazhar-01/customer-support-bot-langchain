import json

import streamlit as st

from src.llm import create_llm
from src.workflow import build_workflow, process_ticket


st.set_page_config(
    page_title="AI Customer Support",
    page_icon="🤖",
    layout="wide"
)


@st.cache_resource
def get_workflow():
    llm = create_llm()
    workflow = build_workflow(llm)
    return workflow


st.title("🤖 AI Customer Support Assistant")

st.write(
    "Enter a customer support ticket and let the AI analyze it."
)


customer_name = st.text_input("Customer Name")

ticket_text = st.text_area(
    "Support Ticket",
    placeholder="Describe the customer's problem here...",
    height=150
)


if st.button("Process Ticket"):

    if not customer_name.strip():
        st.warning("Please enter the customer name.")

    elif not ticket_text.strip():
        st.warning("Please enter the support ticket.")

    else:

        ticket = {
            "ticket_id": "WEB-001",
            "customer_name": customer_name,
            "ticket": ticket_text
        }

        with st.spinner("AI is analyzing the ticket..."):

            try:
                workflow = get_workflow()
                result = process_ticket(ticket, workflow)

            except Exception as error:
                st.error(f"Error while processing ticket: {error}")

            else:

                st.success("Ticket processed successfully!")

                # -----------------------------------
                # Ticket Analysis
                # -----------------------------------

                st.subheader("Ticket Analysis")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Category",
                        result.category
                    )

                with col2:
                    st.metric(
                        "Priority",
                        result.priority
                    )

                with col3:
                    st.metric(
                        "Language",
                        result.language
                    )

                # -----------------------------------
                # Case Summary
                # -----------------------------------

                st.subheader("Case Summary")

                try:
                    case_summary = json.loads(result.case_summary)

                except (json.JSONDecodeError, TypeError):
                    case_summary = None

                if isinstance(case_summary, dict):

                    # Billing
                    if result.category == "billing":

                        st.write(
                            f"**Issue:** "
                            f"{case_summary.get('issue', 'Unknown')}"
                        )

                        st.write(
                            f"**Amount:** "
                            f"{case_summary.get('amount', 'Unknown')}"
                        )

                        st.write(
                            f"**Transaction Count:** "
                            f"{case_summary.get('transaction_count', 'Unknown')}"
                        )

                        refund_required = case_summary.get(
                            "refund_required",
                            False
                        )

                        st.write(
                            f"**Refund Required:** "
                            f"{'Yes' if refund_required else 'No'}"
                        )

                    # Technical
                    elif result.category == "technical":

                        st.write(
                            f"**Issue:** "
                            f"{case_summary.get('issue', 'Unknown')}"
                        )

                        st.write(
                            f"**Affected Feature:** "
                            f"{case_summary.get('affected_feature', 'Unknown')}"
                        )

                        st.write(
                            f"**Error Message:** "
                            f"{case_summary.get('error_message', 'None')}"
                        )

                        troubleshooting_required = case_summary.get(
                            "troubleshooting_required",
                            False
                        )

                        st.write(
                            f"**Troubleshooting Required:** "
                            f"{'Yes' if troubleshooting_required else 'No'}"
                        )

                    # Account
                    elif result.category == "account":

                        st.write(
                            f"**Issue:** "
                            f"{case_summary.get('issue', 'Unknown')}"
                        )

                        st.write(
                            f"**Access Problem:** "
                            f"{case_summary.get('access_problem', 'Unknown')}"
                        )

                        verification_required = case_summary.get(
                            "verification_required",
                            False
                        )

                        st.write(
                            f"**Verification Required:** "
                            f"{'Yes' if verification_required else 'No'}"
                        )

                        st.write(
                            f"**Account Status:** "
                            f"{case_summary.get('account_status', 'Unknown')}"
                        )

                    # Cancellation / Refund
                    elif result.category == "cancellation_refund":

                        st.write(
                            f"**Request Type:** "
                            f"{case_summary.get('request_type', 'Unknown')}"
                        )

                        st.write(
                            f"**Reason:** "
                            f"{case_summary.get('reason', 'Unknown')}"
                        )

                        refund_required = case_summary.get(
                            "refund_required",
                            False
                        )

                        st.write(
                            f"**Refund Required:** "
                            f"{'Yes' if refund_required else 'No'}"
                        )

                        retention_opportunity = case_summary.get(
                            "retention_oppurtunity",
                            False
                        )

                        st.write(
                            f"**Retention Opportunity:** "
                            f"{'Yes' if retention_opportunity else 'No'}"
                        )

                    # Order / Delivery
                    elif result.category == "order_delivery":

                        st.write(
                            f"**Issue:** "
                            f"{case_summary.get('issue', 'Unknown')}"
                        )

                        st.write(
                            f"**Order Status:** "
                            f"{case_summary.get('order_status', 'Unknown')}"
                        )

                        delivery = case_summary.get(
                            "delivery",
                            False
                        )

                        st.write(
                            f"**Delivery Problem:** "
                            f"{'Yes' if delivery else 'No'}"
                        )

                        st.write(
                            f"**Customer Request:** "
                            f"{case_summary.get('customer_request', 'Unknown')}"
                        )

                    # General
                    elif result.category == "general":

                        st.write(
                            f"**Issue:** "
                            f"{case_summary.get('issue', 'Unknown')}"
                        )

                        st.write(
                            f"**Customer Request:** "
                            f"{case_summary.get('customer_request', 'Unknown')}"
                        )

                        st.write(
                            f"**Additional Context:** "
                            f"{case_summary.get('additional_context', 'Unknown')}"
                        )

                    else:
                        st.json(case_summary)

                else:
                    st.write(result.case_summary)

                # -----------------------------------
                # Resolution
                # -----------------------------------

                st.subheader("Resolution")

                col1, col2 = st.columns(2)

                with col1:

                    st.write("Resolution Type")

                    st.info(
                        result.resolution_type
                    )

                with col2:

                    st.write("Human Required")

                    if result.requires_human:
                        st.error("Yes")
                    else:
                        st.success("No")

                # -----------------------------------
                # Recommended Action
                # -----------------------------------

                st.subheader("Recommended Action")

                st.write(
                    result.recommended_action
                )

                # -----------------------------------
                # Resolution Reason
                # -----------------------------------

                st.subheader("Resolution Reason")

                st.write(
                    result.resolution_reason
                )

                # -----------------------------------
                # Customer Response
                # -----------------------------------

                st.subheader("Customer Response")

                st.info(
                    result.response
                )