from sqlalchemy import text
from database import engine

def submit_transaction(user_id, amount, category, description):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO transactions (user_id, amount, category, description)
            VALUES (:user_id, :amount, :category, :description)
        """), {
            "user_id": user_id,
            "amount": amount,
            "category": category,
            "description": description
        })
        conn.commit()

def fetch_transactions(user_id):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT amount, category, description, created_at
            FROM transactions
            WHERE user_id = :user_id
            ORDER BY created_at DESC
        """), {"user_id": user_id})
        return result.fetchall()