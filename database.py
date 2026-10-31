import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "sentinel_ai.db"


def init_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT NOT NULL UNIQUE,
                amount REAL NOT NULL,
                fraud_probability REAL NOT NULL,
                risk_score REAL NOT NULL,
                prediction TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_transaction(transaction_id, amount,
                     fraud_probability, risk_score, prediction):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR IGNORE INTO transactions
            (transaction_id, amount, fraud_probability,
             risk_score, prediction, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            transaction_id,
            amount,
            fraud_probability,
            risk_score,
            prediction,
            datetime.now().isoformat(timespec="seconds")
        ))


def get_transactions():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT * FROM transactions
            ORDER BY id DESC
        """).fetchall()
        return [dict(row) for row in rows]


if __name__ == "__main__":
    init_database()
    print("SENTINEL AI Database initialized successfully!")