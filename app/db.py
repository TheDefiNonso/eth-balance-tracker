import sqlite3
from pathlib import Path

DB_PATH = Path("balances.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS balances (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL,
        eth_balance REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def insert_balance(address: str, eth_balance: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO balances (address, eth_balance) VALUES (?, ?)",
        (address, eth_balance)
    )

    conn.commit()
    conn.close()


def get_all_balances():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, address, eth_balance, timestamp FROM balances")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_balances_for_address(address: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, address, eth_balance, timestamp FROM balances WHERE address = ? ORDER BY timestamp DESC",
        (address,)
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_latest_balance_for_address(address: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT eth_balance
        FROM balances
        WHERE address = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (address,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None
