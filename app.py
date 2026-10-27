import sqlite3

import requests
import streamlit as st

from tickets import DB_PATH

BASE = "http://127.0.0.1:8000"

st.title("Support assistant")

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.customer = None

# ---------- Login screen ----------
if st.session_state.token is None:
    st.subheader("Log in")
    customer_id = st.text_input("Customer ID")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        try:
            resp = requests.post(
                f"{BASE}/login",
                json={"customer_id": customer_id, "password": password},
                timeout=30,
            )
        except requests.RequestException as e:
            st.error(f"Could not reach the service: {e}")
        else:
            if resp.status_code == 200:
                st.session_state.token = resp.json()["token"]
                st.session_state.customer = customer_id
                st.rerun()
            else:
                st.error("Wrong customer ID or password")
    st.stop()

# ---------- Ticket screen ----------
st.sidebar.write(f"Logged in as **{st.session_state.customer}**")
if st.sidebar.button("Log out"):
    st.session_state.token = None
    st.session_state.customer = None
    st.rerun()

st.sidebar.divider()
st.sidebar.caption("Demo only")
if st.sidebar.button("Reset ticket history"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM tickets")
    conn.commit()
    conn.close()
    st.sidebar.success("History cleared")

text = st.text_area("Describe your issue", placeholder="Hi, where is my order OD123?")

if st.button("Send") and text.strip():
    try:
        resp = requests.post(
            f"{BASE}/tickets",
            json={"text": text},
            headers={"Authorization": f"Bearer {st.session_state.token}"},
            timeout=120,
        )
        if resp.status_code == 401:
            st.session_state.token = None
            st.error("Your session is no longer valid. Please log in again.")
        else:
            resp.raise_for_status()
            data = resp.json()
            st.write(data["reply"])
            st.caption(f"Route: {data['route']}")
    except requests.RequestException as e:
        st.error(f"Could not reach the service: {e}")