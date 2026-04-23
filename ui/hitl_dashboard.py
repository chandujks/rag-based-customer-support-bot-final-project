import requests
import streamlit as st

API = "http://127.0.0.1:8000"

st.title("HITL Dashboard")

try:
    response = requests.get(f"{API}/hitl/pending", timeout=15)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as exc:
    st.error(f"Could not load pending tickets: {exc}")
    data = {}

if not data:
    st.info("No pending tickets.")

for tid, item in data.items():
    st.subheader(tid)
    st.write(item["query"])

    reply = st.text_area(f"Reply {tid}", key=f"reply-{tid}")

    if st.button(f"Submit {tid}", key=f"submit-{tid}"):
        try:
            response = requests.post(
                f"{API}/hitl/respond",
                json={"ticket_id": tid, "response": reply},
                timeout=15,
            )
            response.raise_for_status()
            st.success("Submitted")
            st.rerun()
        except requests.RequestException as exc:
            st.error(f"Submit failed: {exc}")
