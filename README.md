# Ethereum Wallet Balance Tracker API

![Pipeline Flow](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2cwM2pkZ3l5ZHF1Y3U1ZzNqdmEyNjdzZWtqNGhtZWJtaW5lN3RqdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vGq1m34VZKvOlwS6I0/giphy.gif)

This is a small blockchain data engineering project where I built an API that tracks Ethereum wallet balances over time, stores them in a database, and exposes historical data through HTTP endpoints.

The main goal of this project is to demonstrate how I design simple data pipelines, background workers, APIs, and storage layers for blockchain data.

This is not just a balance checker. It is a mini ingestion pipeline that polls wallets periodically and builds a historical dataset you can query.

## What This Project Does

This API:

- Fetches Ethereum wallet balances from Alchemy using JSON-RPC
- Exposes an endpoint to query live balances
- Periodically polls selected wallets in the background
- Stores balance history in SQLite
- Avoids duplicate rows if the balance has not changed
- Exposes historical balance data through API endpoints

This mimics a real world data ingestion pipeline where data is fetched, validated, deduplicated, stored, and served to consumers.

## Tech Stack

- Python
- FastAPI
- HTTPX
- SQLite
- Alchemy Ethereum RPC
- Async background worker

## Project Structure
```
wallet-balance-api/
│
├── app/
│   ├── main.py            # FastAPI app and lifespan setup
│   ├── db.py              # SQLite connection and queries
│   ├── services/
│   │   └── eth.py         # Ethereum RPC logic
│   └── core/
│       └── config.py      # Environment variables and settings (ALCHEMY_URL, WATCHED_ADDRESSES)
│
├── balances.db            # SQLite database (generated at runtime)
├── .env                   # API keys (not committed)
├── .gitignore
├── pyproject.toml
└── README.md
```

## Endpoints

### Get Live Balance
```
GET /wallet/balance?address=0x...
```

Returns the current ETH balance for a wallet and stores it in the database if it changed.

### Get Full Balance History
```
GET /history
```

Returns all recorded wallet balances.

### Get Balance History for One Wallet
```
GET /history/{address}
```

Returns historical balances for a specific wallet.

## How the Data Pipeline Works

1. The API fetches live wallet balances using Ethereum JSON-RPC
2. A background task runs every 5 minutes
3. Each wallet is polled
4. If the balance changed, it is stored
5. If not, it is skipped
6. Data is persisted in SQLite
7. The API exposes historical data

This mirrors how production data pipelines avoid storing duplicate records while continuously ingesting new data.

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/thedefinonso/wallet-balance-api.git
cd wallet-balance-api
```

### 2. Create virtual environment
```bash
uv venv
source .venv/bin/activate
```

Windows:
```bash
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file:
```
ALCHEMY_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
```

### 5. Run the API
```bash
uv run uvicorn app.main:app --reload
```

Open in browser:
```
http://127.0.0.1:8000/docs
```

## Why This Project Exists

I built this to practice:

- Designing simple blockchain data pipelines
- Writing async services
- Working with background jobs
- Storing and querying time series style data
- Structuring a production style API
- Thinking about data engineering patterns even in small projects

This project is intentionally simple but designed like a real system.

## Future Improvements

- Add PostgreSQL support
- Add Docker and deployment
- Add wallet registry table
- Add basic metrics and logging
- Add simple frontend dashboard
- Add caching layer
- Add more chains

## Notes

This project is part of my personal portfolio. The code is intentionally simple and readable. Security, rate limiting, and auth would be added in production.