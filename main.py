from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import asyncio
from app.db import init_db, insert_balance, get_all_balances, get_balances_for_address, get_latest_balance_for_address
from app.services.eth import fetch_eth_balance
from app.core.config import WATCHED_ADDRESSES
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 300


async def poll_wallets_forever():
    while True:
        logger.info("Polling wallets...")

        for address in WATCHED_ADDRESSES:
            try:
                balance_wei = await fetch_eth_balance(address)

                if balance_wei is None:
                    logger.warning(f"Skipping {address}, fetch failed")
                    continue

                insert_balance(address, balance_wei)

                logger.info(f"Recorded balance snapshot for {address}")

            except Exception as e:
                # absolutely never let the poller die
                logger.exception(f"Unexpected poller error for {address}: {e}")

        await asyncio.sleep(POLL_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):

    init_db()
    logger.info("DB initialized")

    task = asyncio.create_task(poll_wallets_forever())

    yield

    task.cancel()
    logger.info("App shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/balance")
async def balance(address: str):
    if not address.startswith("0x") or len(address) != 42:
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")

    balance_wei = await fetch_eth_balance(address)

    if balance_wei is None:
        raise HTTPException(status_code=502, detail="Failed to fetch balance")

    insert_balance(address, balance_wei)

    eth_balance = balance_wei / 10**18

    return {
        "address": address,
        "eth_balance": eth_balance
    }


@app.get("/history")
def read_all_history():
    rows = get_all_balances()
    return [
        {
            "id": r[0],
            "address": r[1],
            "wei_balance": r[2],
            "timestamp": r[3],
        }
        for r in rows
    ]


@app.get("/history/{address}")
def read_wallet_history(address: str):
    if not address.startswith("0x") or len(address) != 42:
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")

    rows = get_balances_for_address(address)

    return [
        {
            "id": r[0],
            "address": r[1],
            "wei_balance": r[2],
            "timestamp": r[3],
        }
        for r in rows
    ]
