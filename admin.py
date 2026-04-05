import streamlit as st
import pandas as pd
import time
from api import api_get, api_post, api_delete

def show():
    st.title("Admin / Manager Dashboard")
    
    tabs = st.tabs(["Overview Analytics", "Manage Users", "Manage Units", "All Complaints", "All Payments"])
    
    with tabs[0]:
        st.header("System Overview")
       
        
        with st.spinner("Loading overview..."):
            res = api_get("/admin/overview")
            if res.status_code == 200:
                data = res.json()
                active_bookings = data.get("active_bookings", [])
                resident_dues = data.get("resident_dues", [])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Pending Resident Dues")
                    if resident_dues:
                        df_dues = pd.DataFrame(resident_dues)
                        st.bar_chart(data=df_dues, x="username", y="total_pending", use_container_width=True)
                        st.dataframe(df_dues, use_container_width=True)
                    else:
                        st.info("No residents have pending dues.")
                
                with col2:
                    st.subheader("Active Bookings")
                    if active_bookings:
                        df_bookings = pd.DataFrame(active_bookings)
                        st.dataframe(df_bookings, use_container_width=True)
                    else:
                        st.info("No active bookings.")
            else:
                st.error(f"Failed to load overview data: {res.text}")

    with tabs[1]:
        st.header("Manage Users")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            res = api_get("/admin/users")
            if res.status_code == 200:
                users = res.json()
                if users:
                    df_users = pd.DataFrame(users)
                    st.dataframe(df_users, use_container_width=True)
                else:
                    st.write("No users found.")
            else:
                st.error("Failed to load users.")
                
        with col2:
            st.subheader("Delete User")
            user_id_to_delete = st.number_input("User ID to Delete", min_value=1, step=1)
            if st.button("Delete User", type="primary"):
                with st.spinner("Deleting..."):
                    del_res = api_delete(f"/admin/users/{user_id_to_delete}")
                    if del_res.status_code == 200:
                        st.success("User deleted successfully.")
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(f"Failed to delete: {del_res.text}")

    with tabs[2]:
        st.header("Manage Units")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            res = api_get("/admin/units")
            if res.status_code == 200:
                units = res.json()
                if units:
                    st.dataframe(pd.DataFrame(units), use_container_width=True)
                else:
                    st.write("No units found.")
                    
        with col2:
            st.subheader("Create New Unit")
            with st.form("create_unit_form", clear_on_submit=True):
                unit_num = st.text_input("Unit Number (e.g., 101)")
                block = st.text_input("Block (e.g., A)")
                unit_type = st.selectbox("Type", ["1BHK", "2BHK", "3BHK", "Villa"])
                sq_ft = st.number_input("Square Feet", min_value=100, step=50, value=1000)
                submitted = st.form_submit_button("Create Unit")
                
                if submitted:
                    payload = {"unit_number": unit_num, "block": block, "unit_type": unit_type, "square_feet": sq_ft}
                    create_res = api_post("/admin/units", payload)
                    if create_res.status_code == 201:
                        st.success("Unit created successfully.")
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(f"Creation failed: {create_res.text}")

    with tabs[3]:
        st.header("Complaints")
        res = api_get("/admin/complaints")
        if res.status_code == 200:
            complaints = res.json()
            if complaints:
                df_complaints = pd.DataFrame(complaints)
                
                
                status_filter = st.multiselect("Filter by Status", options=df_complaints['status'].unique(), default=df_complaints['status'].unique())
                priority_filter = st.multiselect("Filter by Priority", options=df_complaints['priority'].unique(), default=df_complaints['priority'].unique())
                
                filtered_df = df_complaints[(df_complaints['status'].isin(status_filter)) & (df_complaints['priority'].isin(priority_filter))]
                
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.write("No complaints filed.")
                
    with tabs[4]:
        st.header("All Payments Tracker")
        res = api_get("/admin/payments")
        if res.status_code == 200:
            payments = res.json()
            if payments:
                df_payments = pd.DataFrame(payments)
                search_user = st.text_input("Search by Username")
                if search_user:
                    df_payments = df_payments[df_payments['username'].str.contains(search_user, case=False, na=False)]
                
                st.dataframe(df_payments, use_container_width=True)
            else:
                st.write("No payments recorded.")
