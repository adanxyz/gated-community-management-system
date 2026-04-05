import streamlit as st
import jwt
from api import login_user, register_user


st.set_page_config(page_title="Gated Community System", page_icon="🏢", layout="wide")


if "token" not in st.session_state:
    st.session_state.token = None
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.username = None
    st.success("Logged out successfully.")

def decode_role(token):
    try:
        
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get("role_id"), payload.get("username")
    except Exception as e:
        st.error("Failed to parse token")
        return None, None

def show_login():
    st.title("Gated Community Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            if not username or not password:
                st.warning("Please fill out both fields.")
            else:
                with st.spinner("Authenticating..."):
                    res = login_user(username, password)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.token = data.get("token")
                        role_id, uname = decode_role(st.session_state.token)
                        st.session_state.role = role_id
                        st.session_state.username = uname
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(res.json().get("message", "Login failed"))

def show_register():
    st.title("Resident Registration")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        phone = st.text_input("Phone (Optional)")
        unit_id = st.number_input("Unit ID", min_value=1, step=1)
        status = st.selectbox("Residency Status", ["Owner", "Tenant"])
        submit = st.form_submit_button("Register")

        if submit:
            payload = {
                "username": username,
                "password": password,
                "email": email,
                "phone": phone,
                "unit_id": unit_id,
                "residency_status": status
            }
            with st.spinner("Registering..."):
                res = register_user(payload)
                if res.status_code == 201:
                    st.success("Registration successful! Please login.")
                else:
                    st.error(f"Registration failed: {res.json().get('message', res.text)}")


if not st.session_state.token:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        show_login()
    with tab2:
        show_register()
else:
   
    with st.sidebar:
        st.header(f"Welcome, {st.session_state.username}")
        role_map = {1: "Admin", 2: "Resident", 3: "Security", 4: "Maintenance", 5: "Manager"}
        st.write(f"**Role:** {role_map.get(st.session_state.role, 'Unknown')}")
        if st.button("Logout"):
            logout()
            st.rerun()

    
    if st.session_state.role in [1, 5]:
        import admin
        admin.show()
    elif st.session_state.role == 2:
        import resident
        resident.show()
    elif st.session_state.role == 3:
        import security
        security.show()
    else:
        st.warning("Dashboard for your role is not yet implemented.")
