import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000/api/v1")

def get_headers():
    headers = {"Content-Type": "application/json"}
    if "token" in st.session_state and st.session_state.token:
        headers["Authorization"] = f"Bearer {st.session_state.token}"
    return headers

def login_user(username, password):
    url = f"{API_BASE_URL}/auth/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    return response

def register_user(payload):
    url = f"{API_BASE_URL}/auth/register"
    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    return response

# Generic requests
def api_get(endpoint):
    url = f"{API_BASE_URL}{endpoint}"
    return requests.get(url, headers=get_headers())

def api_post(endpoint, payload):
    url = f"{API_BASE_URL}{endpoint}"
    return requests.post(url, json=payload, headers=get_headers())

def api_put(endpoint, payload=None):
    url = f"{API_BASE_URL}{endpoint}"
    return requests.put(url, json=payload, headers=get_headers())

def api_delete(endpoint):
    url = f"{API_BASE_URL}{endpoint}"
    return requests.delete(url, headers=get_headers())
