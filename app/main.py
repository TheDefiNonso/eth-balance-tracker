from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import asyncio
import logging

from app.db import (
    init_db,
    upsert_wallet,
    insert_transaction,
    get_wallets,
    get_transactions_for_address,
    address_exists,
)
from app.services.eth import fetch_eth_balance, fetch_latest_block
from app.core.config import WATCHED_ADDRESSES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = 300
LIMIT = 100


async def snapshot_address(address: str):

    latest_block = await fetch_latest_block()
    if latest_block is None:
        logger.warning(f"Could not fetch latest block for {address}, skipping")
        return

    balance_wei = await fetch_eth_balance(address)
    if balance_wei is None:
        logger.warning(f"Could not fetch balance for {address}, skipping")
        return

    upsert_wallet(address, balance_wei)

    inserted = insert_transaction(address, latest_block, balance_wei)
    if inserted:
        logger.info(f"New snapshot: {address} at block {latest_block}")
    else:
        logger.info(f"Block {latest_block} already recorded for {address}")


async def poll_wallets_forever():

    while True:
        logger.info("Polling all tracked wallets...")

        rows = get_wallets(limit=10000, offset=0)
        addresses = [r[0] for r in rows]

        for address in addresses:
            try:
                await snapshot_address(address)
            except Exception as e:
                logger.exception(f"Poller error for {address}: {e}")

        logger.info(f"Poll complete. Sleeping {POLL_INTERVAL_SECONDS}s")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


async def seed_addresses():
    logger.info("Seeding watched addresses from config...")
    for address in WATCHED_ADDRESSES:
        try:
            await snapshot_address(address)
        except Exception as e:
            logger.exception(f"Failed to seed {address}: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("DB initialized")

    seed_task = asyncio.create_task(seed_addresses())
    poll_task = asyncio.create_task(poll_wallets_forever())

    yield

    seed_task.cancel()
    poll_task.cancel()
    logger.info("App shutdown")


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def page_index():
    return FileResponse("frontend/index.html")


@app.get("/balance")
def page_balance():
    return FileResponse("frontend/balance.html")


@app.get("/history/{address}")
def page_history(address: str):
    return FileResponse("frontend/history.html")


@app.get("/api/wallets")
def api_wallets(offset: int = 0):

    if offset < 0 or offset % LIMIT != 0:
        raise HTTPException(
            status_code=400, detail=f"Offset must be 0 or a multiple of {LIMIT}")

    rows = get_wallets(LIMIT, offset)

    return {
        "offset": offset,
        "limit": LIMIT,
        "count": len(rows),
        "results": [
            {
                "address": r[0],
                "balance_wei": r[1],
                "last_updated": r[2],
            }
            for r in rows
        ],
    }


@app.get("/api/balance")
async def api_balance(address: str):

    if not address.startswith("0x") or len(address) != 42:
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")

    is_new = not address_exists(address)

    await snapshot_address(address)

    balance_wei = await fetch_eth_balance(address)
    if balance_wei is None:
        raise HTTPException(
            status_code=502, detail="Failed to fetch balance from Alchemy")

    return {
        "address": address,
        "balance_wei": str(balance_wei),
        "eth_balance": balance_wei / 10 ** 18,
        "new_address": is_new,
    }


@app.get("/api/history/{address}")
async def api_history(address: str, offset: int = 0):

    if not address.startswith("0x") or len(address) != 42:
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")

    if offset < 0 or offset % LIMIT != 0:
        raise HTTPException(
            status_code=400, detail=f"Offset must be 0 or a multiple of {LIMIT}")

    await snapshot_address(address)

    rows = get_transactions_for_address(address, LIMIT, offset)

    return {
        "address": address,
        "offset": offset,
        "limit": LIMIT,
        "count": len(rows),
        "results": [
            {
                "id": r[0],
                "block_number": r[1],
                "balance_wei": r[2],
                "recorded_at": r[3],
            }
            for r in rows
        ],
    }
