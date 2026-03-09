import sqlite3
import logging
from pathlib import Path
from app.core.config import DB_PATH


logger = logging.getLogger(__name__)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wallets(
                           address TEXT PRIMARY KEY,
                           balance_wei TEXT NOT NULL,
                           last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    block_number INTEGER NOT NULL,
                    balance_wei TEXT NOT NULL,
                    recorded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(address, block_number)                           
                )
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_transactions_address
                ON transactions(address)
            """)

            conn.commit()
            logger.info("Database initialized successfully")

    except Exception as e:
        logger.exception(f"Failed to initialize database: {e}")
        raise


def upsert_wallet(address: str, balance_wei: int):
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO wallets (address, balance_wei)
                VALUES (?, ?)
                ON CONFLICT(address)
                DO UPDATE SET
                    balance_wei = excluded.balance_wei,
                    last_updated = CURRENT_TIMESTAMP
                """,
                (address, str(balance_wei))
            )
            conn.commit()
    except Exception as e:
        logger.exception(f"Failed to upsert wallet {address}: {e}")
        raise


def insert_transaction(address: str, block_number: int, balance_wei: int) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO transactions (address, block_number, balance_wei)
                VALUES (?, ?, ?)
                ON CONFLICT(address, block_number) DO NOTHING
                """,
                (address, block_number, str(balance_wei))
            )
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        logger.exception(
            f"Failed to insert transaction for {address} at block {block_number}: {e}")
        raise


def get_wallets(limit: int, offset: int):
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT address, balance_wei, last_updated
                FROM wallets
                ORDER BY last_updated DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset)
            )
            return cursor.fetchall()
    except Exception as e:
        logger.exception(f"Failed to get wallets: {e}")
        raise


def get_transactions_for_address(address: str, limit: int, offset: int):
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, block_number, balance_wei, recorded_at
                FROM transactions
                WHERE address = ?
                ORDER BY block_number DESC
                LIMIT ? OFFSET ?
                """,
                (address, limit, offset)
            )
            return cursor.fetchall()
    except Exception as e:
        logger.exception(f"Failed to get transactions for {address}: {e}")
        raise


def address_exists(address: str) -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM wallets WHERE address = ?",
                (address,)
            )
            return cursor.fetchone() is not None
    except Exception as e:
        logger.exception(
            f"Failed to check address existence for {address}: {e}")
        raise
