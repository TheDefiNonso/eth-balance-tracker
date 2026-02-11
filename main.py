from fastapi import FastAPI, HTTPException
import httpx
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from app.db import init_db
import asyncio
from app.db import insert_balance, get_all_balances, get_balances_for_address, get_latest_balance_for_address


load_dotenv()

ALCHEMY_URL = os.getenv("ALCHEMY_URL")

WATCHED_ADDRESSES = [
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "0x28c6c06298d514db089934071355e5743bf21d60",
    "0x503828976d22510aad0201ac7ec88293211d23da",
    "0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0",
]


async def poll_wallets_forever():
    while True:
        print("🔁 Polling wallets...")

        async with httpx.AsyncClient() as client:
            for address in WATCHED_ADDRESSES:
                payload = {
                    "jsonrpc": "2.0",
                    "method": "eth_getBalance",
                    "params": [address, "latest"],
                    "id": 1
                }

                res = await client.post(ALCHEMY_URL, json=payload)
                data = res.json()

                wei_hex = data["result"]
                wei_int = int(wei_hex, 16)
                eth_balance = wei_int / 10**18

                latest = get_latest_balance_for_address(address)

                if latest is None or abs(latest - eth_balance) > 1e-9:
                    insert_balance(address, eth_balance)
                    print(f"✅ Stored new balance for {address}: {eth_balance}")
                else:
                    print(f"⏭ No change for {address}")

        await asyncio.sleep(300)  # every 5 minutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not ALCHEMY_URL:
        raise RuntimeError("ALCHEMY_URL is not set in .env")
    print("✅ App startup: ALCHEMY_URL loaded")

    init_db()
    print("✅ DB initialized")

    task = asyncio.create_task(poll_wallets_forever())

    yield

    task.cancel()
    print("🛑 App shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/balance")
async def balance(address: str):
    if not address.startswith("0x") or len(address) != 42:
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")

    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(ALCHEMY_URL, json=payload)
        data = res.json()

    wei_hex = data["result"]
    wei_int = int(wei_hex, 16)
    eth_balance = wei_int / 10**18

    insert_balance(address, eth_balance)

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
            "eth_balance": r[2],
            "timestamp": r[3],
        }
        for r in rows
    ]


@app.get("/history/{address}")
def read_wallet_history(address: str):
    rows = get_balances_for_address(address)
    return [
        {
            "id": r[0],
            "address": r[1],
            "eth_balance": r[2],
            "timestamp": r[3],
        }
        for r in rows
    ]
