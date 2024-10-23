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

def save_user(username, password):
    users = load_users()
    users['users'].append({"username": username, "password": password})
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

def user_exists(username):
    users = load_users()
    return any(user['username'] == username for user in users['users'])

def authenticate(username, password):
    users = load_users()
    for user in users['users']:
        if user['username'] == username and user['password'] == password:
            return True
    return False

def login():
    st.title("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success("Login successful! Navigate to the Dashboard.")
        else:
            st.error("Invalid credentials")

def signup():
    st.title("Sign Up")
    username = st.text_input("New Username", key="signup_username")
    password = st.text_input("New Password", type="password", key="signup_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif user_exists(username):
            st.error("Username already exists!")
        else:
            save_user(username, password)
            st.success("Sign up successful! Please log in.")
            st.session_state.signup = False

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if 'signup' not in st.session_state:
        st.session_state.signup = False

    if st.session_state.signup:
        signup()
        if st.button("Already have an account? Login here"):
            st.session_state.signup = False
    else:
        login()
        if st.button("New user? Sign up here"):
            st.session_state.signup = True

if __name__ == "__main__":
    main()
