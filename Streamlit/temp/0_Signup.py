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

def signup_page():
    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        elif user_exists(username):
            st.error("Username already exists!")
        else:
            save_user(username, password)
            st.success("Sign up successful! You can now log in.")

if __name__ == "__main__":
    signup_page()
