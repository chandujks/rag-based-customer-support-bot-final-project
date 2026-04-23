import requests
import streamlit as st

API = "http://127.0.0.1:8000/query"

st.title("RAG Bot (Ollama)")

query = st.text_input("Ask question:")
ticket = st.text_input("Ticket ID (optional)")

if st.button("Submit"):
    if not query.strip() and not ticket.strip():
        st.warning("Enter a question or a ticket ID.")
    else:
        try:
            res = requests.post(
                API,
                json={"query": query, "ticket_id": ticket or None},
                timeout=30,
            )
            res.raise_for_status()
            data = res.json()

            st.write("### Answer:")
            st.write(data["answer"])
            st.write("Confidence:", data["confidence"])

            if data["escalated"]:
                st.warning(f"Escalated -> Ticket ID: {data['ticket_id']}")
        except requests.RequestException as exc:
            st.error(f"API request failed: {exc}")
