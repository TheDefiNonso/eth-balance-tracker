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


async def fetch_eth_balance(address: str, retries: int = 3) -> float | None:
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1,
    }

    timeout = httpx.Timeout(10.0)

    for attempt in range(1, retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(ALCHEMY_URL, json=payload)

            response.raise_for_status()
            data = response.json()

            if "result" not in data:
                logger.error(f"Invalid RPC response for {address}: {data}")
                return None

            wei_int = int(data["result"], 16)
            return wei_int

        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            logger.warning(
                f"Attempt {attempt}/{retries} failed for {address}: {e}"
            )

            if attempt < retries:
                await asyncio.sleep(2 ** attempt)  # exponential backoff
            else:
                logger.error(f"All retries failed for {address}")
                return None

        except Exception as e:
            logger.exception(
                f"Unexpected error fetching balance for {address}: {e}")
            return None
