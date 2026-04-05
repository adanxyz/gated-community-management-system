import streamlit as st
import pandas as pd
import time
from api import api_get, api_post, api_put
import datetime

def show():
    st.title("Security Dashboard")
    
    tabs = st.tabs(["Today's Visitors", "Log Entry", "Log Exit"])
    
    with tabs[0]:
        st.header("Currently Logged Visitors")
        res = api_get("/security/visitors")
        if res.status_code == 200:
            visitors = res.json()
            if visitors:
                st.dataframe(pd.DataFrame(visitors), use_container_width=True)
            else:
                st.info("No visitors logged for today.")
        else:
            st.error("Failed to load visitors.")
            
    with tabs[1]:
        st.header("Log Visitor Entry")
        
        with st.form("visitor_entry", clear_on_submit=True):
            name = st.text_input("Visitor Name")
            id_type = st.selectbox("ID Type", ["Passport", "National ID", "Driver License"])
            id_number = st.text_input("ID Number")
            contact_number = st.text_input("Contact Number (Optional)")
            unit_id = st.number_input("Target Unit ID", min_value=1, step=1)
            
            if st.form_submit_button("Log Entry"):
                payload = {
                    "name": name,
                    "id_type": id_type,
                    "id_number": id_number,
                    "contact_number": contact_number,
                    "unit_id": unit_id
                }
                res = api_post("/security/visitors/log", payload)
                if res.status_code == 201:
                    st.success(f"Visitor logged successfully! Gate Pass: {res.json().get('gate_pass_code')}")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"Failed to log entry (Transaction Rolled Back): {res.text}")
                    
    with tabs[2]:
        st.header("Log Visitor Exit")
        log_id = st.number_input("Access Log ID", min_value=1, step=1)
        if st.button("Log Exit", type="primary"):
            res = api_put(f"/security/visitors/exit/{log_id}")
            if res.status_code == 200:
                st.success("Exit time logged successfully.")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error(f"Failed to log exit: {res.text}")
