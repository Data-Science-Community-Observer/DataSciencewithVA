import streamlit as st
import json
import os

# File path for storing user credentials
USER_DATA_FILE = "./data/users.json"

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = {"users": []}
    return users

def authenticate(username, password):
    users = load_users()
    for user in users['users']:
        if user['username'] == username and user['password'] == password:
            return True
    return False

def login_page():
    st.title("NSE Stock Data Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success("Login successful! Navigate to the Dashboard.")
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.write("You are already logged in. Please proceed to the Dashboard.")
else:
    login_page()
