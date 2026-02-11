import httpx


async def get_eth_balance(address: str, alchemy_url: str) -> float:
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(alchemy_url, json=payload)
        data = res.json()

    wei_hex = data["result"]
    wei_int = int(wei_hex, 16)
    eth_balance = wei_int / 10**18

    return eth_balance
