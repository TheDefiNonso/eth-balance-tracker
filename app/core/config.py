from dotenv import load_dotenv
import os

load_dotenv()
ALCHEMY_URL = os.getenv("ALCHEMY_URL")

if not ALCHEMY_URL:
    raise ValueError("ALCHEMY_URL is not set in .env")
