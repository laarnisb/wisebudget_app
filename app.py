import streamlit as st
from transaction import submit_transaction, fetch_transactions
from budget import get_spending_by_category, compare_budget_vs_spending
from user import authenticate_user
import datetime

st.set_page_config(page_title="WiseBudget", layout="wide")
st.title("💰 WiseBudget - Personal Finance Recommendation System")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None

menu = st.sidebar.radio("Navigate", ["Login", "Transactions", "Dashboard", "Forecast", "Tips"])

if menu == "Login":
    st.subheader("🔐 User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
            st.session_state.authenticated = True
            st.session_state.user_id = 1
        else:
            st.error("Invalid credentials. Please try again.")

elif not st.session_state.authenticated:
    st.warning("Please log in to access the application.")
else:
    user_id = st.session_state.user_id

    if menu == "Transactions":
        st.subheader("➕ Add a Transaction")
        amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Food", "Bills", "Transportation", "Shopping", "Other"])
        description = st.text_input("Description")
        if st.button("Submit"):
            submit_transaction(user_id, amount, category, description)
            st.success(f"Transaction saved: ${amount:.2f} - {category}")

        st.markdown("---")
        st.subheader("📄 Recent Transactions")
        records = fetch_transactions(user_id)
        if records:
            for record in records:
                date = record[3].strftime('%Y-%m-%d')
                st.write(f"{date} — ${record[0]:.2f} — {record[1]} — {record[2]}")
        else:
            st.info("No transactions found.")

    elif menu == "Dashboard":
        st.subheader("📊 Budget Dashboard")
        user_budget = {}
        categories = ["Food", "Bills", "Transportation", "Shopping", "Other"]
        for cat in categories:
            user_budget[cat] = st.number_input(f"{cat} Budget ($)", min_value=0.0, format="%.2f", key=cat)

        if st.button("Compare Budget vs Spending"):
            actuals = get_spending_by_category(user_id)
            comparison = compare_budget_vs_spending(user_budget, actuals)
            for cat, values in comparison.items():
                diff = values['difference']
                status = "under" if diff >= 0 else "over"
                st.markdown(f"- **{cat}**: Spent ${values['spent']:.2f} of ${values['planned']:.2f} — {abs(diff):.2f} {status} budget")

    elif menu == "Forecast":
        st.subheader("🔮 Expense Forecast")
        st.info("This section uses LSTM to forecast future expenses. (Functionality placeholder)")

    elif menu == "Tips":
        st.subheader("💡 Financial Tips")
        st.success("Example: Cut spending on subscriptions and increase emergency savings.")