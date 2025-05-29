from sqlalchemy import insert, select, Table, MetaData
from database import engine
from cryptography.fernet import Fernet
import os

# Load Fernet key from environment or fallback for testing (ensure secure handling in production)
FERNET_KEY = os.environ.get("FERNET_KEY", Fernet.generate_key())
fernet = Fernet(FERNET_KEY)

def encrypt_data(data):
    """Encrypt data using Fernet"""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data):
    """Decrypt data using Fernet"""
    return fernet.decrypt(data.encode()).decode()

# Define metadata and transactions table structure
metadata = MetaData()
transactions = Table('transactions', metadata, autoload_with=engine)

def submit_transaction(user_id, amount, category, description):
    """Insert a new transaction into the database with encrypted description"""
    encrypted_description = encrypt_data(description)
    with engine.connect() as conn:
        stmt = insert(transactions).values(
            user_id=user_id,
            amount=amount,
            category=category,
            description=encrypted_description
        )
        conn.execute(stmt)
        conn.commit()

def fetch_transactions(user_id):
    """Retrieve and decrypt transactions for a user"""
    with engine.connect() as conn:
        stmt = select(transactions).where(transactions.c.user_id == user_id)
        result = conn.execute(stmt).fetchall()
        transactions_list = []
        for row in result:
            decrypted_description = decrypt_data(row.description)
            transactions_list.append({
                "id": row.id,
                "amount": row.amount,
                "category": row.category,
                "description": decrypted_description,
                "timestamp": row.timestamp
            })
        return transactions_list
