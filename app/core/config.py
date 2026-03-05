from dotenv import load_dotenv
import os

WATCHED_ADDRESSES = [
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "0x28c6c06298d514db089934071355e5743bf21d60",
    "0x503828976d22510aad0201ac7ec88293211d23da",
    "0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0",
]

load_dotenv()
ALCHEMY_URL = os.getenv("ALCHEMY_URL")

if not ALCHEMY_URL:
    raise ValueError("ALCHEMY_URL is not set in .env")
