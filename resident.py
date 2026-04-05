import streamlit as st
import pandas as pd
import time
from api import api_get, api_post

def show():
    st.title("Resident Dashboard")
    
    tabs = st.tabs(["My Unit", "Pay Fees", "Book Amenities", "My Complaints"])
    
    with tabs[0]:
        st.header("My Unit Information")
        res = api_get("/resident/unit")
        if res.status_code == 200:
            unit = res.json()
            st.write(f"**Unit Number:** {unit.get('unit_number')}")
            st.write(f"**Block:** {unit.get('block')}")
            st.write(f"**Type:** {unit.get('unit_type')}")
            st.write(f"**Status:** {unit.get('residency_status')} since {unit.get('move_in_date')}")
        else:
            st.error("Failed to load unit details.")
            
    with tabs[1]:
        st.header("Fee Management")
       
        res = api_get("/resident/fees")
        if res.status_code == 200:
            fees = res.json().get("payments", [])
            if fees:
                df = pd.DataFrame(fees)
                st.dataframe(df)
                
                st.subheader("Make a Payment")
                payment_id = st.number_input("Enter Payment ID", min_value=1, step=1)
                
                if st.button("Pay Fee", type="primary"):
                    with st.spinner("Processing transaction..."):
                        pay_res = api_post("/resident/pay", {"payment_id": payment_id})
                        if pay_res.status_code == 200:
                            st.success("Payment successful! Transaction committed.")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(f"Transaction Rolled Back: {pay_res.json().get('message')}")
            else:
                st.info("No fees recorded.")
        else:
            st.error("Failed to fetch fees.")

    with tabs[2]:
        st.header("Book an Amenity")
        
        amenities_res = api_get("/amenities/")
        if amenities_res.status_code == 200:
            amenities = amenities_res.json()
            if amenities:
                df_am = pd.DataFrame(amenities)
                st.dataframe(df_am)
                
                with st.form("book_form", clear_on_submit=True):
                    amenity_id = st.number_input("Amenity ID", min_value=1, step=1)
                    booking_date = st.date_input("Booking Date")
                    start_time = st.time_input("Start Time")
                    end_time = st.time_input("End Time")
                    
                    submitted = st.form_submit_button("Confirm Booking")
                    if submitted:
                        payload = {
                            "amenity_id": amenity_id,
                            "booking_date": str(booking_date),
                            "start_time": str(start_time),
                            "end_time": str(end_time)
                        }
                        book_res = api_post("/amenities/book", payload)
                        if book_res.status_code == 201:
                            st.success("Booking confirmed! Transaction committed.")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(f"Transaction Rolled Back: {book_res.text}")
        else:
            st.error("Failed to load amenities.")

    with tabs[3]:
        st.header("My Complaints")
        res = api_get("/resident/complaints")
        if res.status_code == 200:
            complaints = res.json()
            if complaints:
                st.dataframe(pd.DataFrame(complaints))
            else:
                st.info("No complaints lodged.")
                
        st.subheader("File a Complaint")
        with st.form("complaint_form", clear_on_submit=True):
            title = st.text_input("Title")
            description = st.text_area("Description")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            if st.form_submit_button("Submit Complaint"):
                comp_res = api_post("/resident/complaints", {"title": title, "description": description, "priority": priority})
                if comp_res.status_code == 201:
                    st.success("Complaint lodged successfully.")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Submission failed.")
