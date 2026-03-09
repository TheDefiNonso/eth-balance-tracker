import httpx
import asyncio
from pythonjsonlogger import jsonlogger
import logging
from app.core.config import ALCHEMY_URL

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.getLogger("httpx").setLevel(logging.WARNING)


async def _post_rpc(payload: dict, retries: int = 3) -> dict | None:

    timeout = httpx.Timeout(10.0)

    for attempt in range(1, retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(ALCHEMY_URL, json=payload)

            response.raise_for_status()
            return response.json()

        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.warning(f"Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(2 ** attempt)
            else:
                logger.error("All retries exhausted")
                return None

        except Exception as e:
            logger.exception(f"Unexpected RPC error: {e}")
            return None


async def fetch_eth_balance(address: str) -> int | None:

    data = await _post_rpc({
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1,
    })

    if data is None or "result" not in data:
        logger.error(f"Invalid balance response for {address}: {data}")
        return None

    return int(data["result"], 16)


async def fetch_balance_at_block(address: str, block: int) -> int | None:
    data = await _post_rpc({
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, hex(block)],
        "id": 1,
    })

    if data is None or "result" not in data:
        logger.error(
            f"Invalid balance response for {address} at block {block}: {data}")
        return None

    return int(data["result"], 16)


async def fetch_latest_block() -> int | None:

    data = await _post_rpc({
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1,
    })

    if data is None or "result" not in data:
        logger.error(f"Invalid blockNumber response: {data}")
        return None

    return int(data["result"], 16)
