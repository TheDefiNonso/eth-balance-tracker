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
        balance_wei TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(address, timestamp)
    )
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_balances_address
    ON balances(address)
    """)

    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_balances_address_wei
    ON balances(address, balance_wei)
    """)

    conn.commit()
    conn.close()


def insert_balance(address: str, balance_wei: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO balances (address, balance_wei)
        VALUES (?, ?)
        ON CONFLICT(address, balance_wei)
        DO NOTHING
        """,
        (address, str(balance_wei))
    )

    conn.commit()
    conn.close()


def get_all_balances():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, address, balance_wei, timestamp FROM balances")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_balances_for_address(address: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, address, balance_wei, timestamp FROM balances WHERE address = ? ORDER BY timestamp DESC",
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
        SELECT balance_wei
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
