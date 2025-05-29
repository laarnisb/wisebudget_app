import streamlit as st
from transaction import submit_transaction, fetch_transactions
from database import create_users_table, create_transactions_table, get_user_id, add_user
from security import hash_password, verify_password
import os

# Initialize the app
st.set_page_config(page_title="WiseBudget", layout="centered")
st.title("💰 WiseBudget App")

# Create necessary database tables
create_users_table()
create_transactions_table()

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Registration
def register():
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if username and password:
            hashed = hash_password(password)
            add_user(username, hashed)
            st.success("User registered! Please log in.")
        else:
            st.warning("Please provide a username and password.")

# Login
def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        user_id, stored_hash = get_user_id(username)
        if user_id and verify_password(password, stored_hash):
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.success(f"Welcome back, {username}!")
        else:
            st.error("Invalid credentials.")

# Transactions
def transactions_page():
    st.subheader("Add a Transaction")
    amount = st.number_input("Amount", min_value=0.01, format="%.2f")
    category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Entertainment", "Other"])
    description = st.text_input("Description")
    if st.button("Submit Transaction"):
        submit_transaction(st.session_state.user_id, amount, category, description)
        st.success("Transaction added successfully!")

    st.subheader("Your Transactions")
    records = fetch_transactions(st.session_state.user_id)
    if records:
        for amount, category, desc, date in records:
            st.write(f"💵 ${amount:.2f} | 📂 {category} | 📝 {desc} | 📅 {date}")
    else:
        st.info("No transactions yet.")

# App flow
if not st.session_state.logged_in:
    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])
    if menu == "Login":
        login()
    else:
        register()
else:
    transactions_page()
