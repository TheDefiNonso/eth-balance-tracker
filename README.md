# Ethereum Wallet Balance Tracker

![Pipeline Flow](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWw5ZWpjNmh0YXN2aHY0cWl6aGpqMjRua2gycnYxdGgzNHRtcGJwYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/UjBHr2VXgyIGmeZJlx/giphy.gif)

A blockchain data engineering project that tracks Ethereum wallet balances over time, stores them in a local database, and serves historical data through a web interface with three frontend pages.

The main goal is to demonstrate how to design a simple but complete data pipeline — background polling, deduplication, historical storage, and a live frontend — built around real Ethereum data.

This is not just a balance checker. It is a mini ingestion pipeline that automatically seeds itself with the top 200 Ethereum addresses, polls them on a schedule, builds a historical dataset per wallet, and serves it through paginated API endpoints and a browser-based UI.

## What This Project Does

- Seeds itself on first run with 200 well-known Ethereum addresses (exchanges, whales, DeFi protocols, staking contracts)
- Fetches live ETH balances from Alchemy using JSON-RPC
- Runs a background poller every 5 minutes across all tracked wallets
- Stores a balance snapshot per wallet per block in SQLite, deduplicated by `(address, block_number)`
- Automatically adds any new address queried through `/balance` to the tracked set
- Exposes paginated API endpoints for wallets and transaction history
- Serves three frontend pages — a wallet dashboard, a balance lookup, and a per-address history view

This mirrors a real world data ingestion pipeline where data is fetched, validated, deduplicated, stored, and served to consumers.

## Tech Stack

- Python
- FastAPI
- HTTPX
- SQLite
- Alchemy Ethereum RPC
- Async background worker

## Project Structure

```
wallet-balance-tracker/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, lifespan, poller, all endpoints
│   ├── db.py                # SQLite connection, table setup, all queries
│   ├── services/
│   │   ├── __init__.py
│   │   └── eth.py           # Alchemy RPC logic, top accounts seed list
│   └── core/
│       ├── __init__.py
│       └── config.py        # Environment variables (ALCHEMY_URL)
│
├── frontend/
│   ├── index.html           # Wallet dashboard (/)
│   ├── balance.html         # Balance lookup (/balance)
│   ├── history.html         # Per-address history (/history/{address})
│   └── style.css            # Shared stylesheet
│
├── balances.db              # SQLite database (generated at runtime)
├── Procfile                 # Railway deployment entry point
├── .env                     # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

## Database Schema

Two tables:

**`wallets`** — one row per address, tracks current balance and last poll time.

| Column | Type | Description |
|---|---|---|
| address | TEXT PRIMARY KEY | Ethereum address |
| balance_wei | TEXT | Current balance stored as Wei string |
| last_updated | DATETIME | Timestamp of last successful poll |

**`transactions`** — one row per `(address, block_number)`, the full balance history.

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Auto-increment primary key |
| address | TEXT | Ethereum address |
| block_number | INTEGER | Block at which balance was recorded |
| balance_wei | TEXT | Balance at that block stored as Wei string |
| recorded_at | DATETIME | When the snapshot was taken |

`UNIQUE(address, block_number)` prevents duplicate snapshots for the same block.

## Endpoints

### Frontend Pages

| Route | Page | Description |
|---|---|---|
| `GET /` | Dashboard | Paginated table of all tracked wallets and current balances |
| `GET /balance` | Balance Lookup | Search any Ethereum address for its live balance |
| `GET /history/{address}` | History | Paginated block snapshot history for one address |

### JSON API

| Route | Description |
|---|---|
| `GET /api/wallets?offset=0` | Paginated wallet list with current balance and last updated time |
| `GET /api/balance?address=0x...` | Live balance for any address. New addresses are auto-added to tracking |
| `GET /api/history/{address}?offset=0` | Paginated transaction history for one address |

All paginated endpoints use `offset` in multiples of 100.

## How the Data Pipeline Works

**On first run**, the app fetches no data from Etherscan. Instead it uses a curated static list of 200 well-known Ethereum addresses built into `eth.py`. For each address it calls Alchemy, records the current block and balance, and writes both to the database. This seeding only runs once — on every subsequent restart the database already has wallets and the seed is skipped.

**The background poller** runs every 5 minutes. It reads every address currently in the `wallets` table — not just the original 200 — and calls `snapshot_address()` for each. If the latest block has already been recorded for that address, the insert is a no-op. If it is a new block, a new row is added to `transactions` and the `wallets` row is updated.

**Every API endpoint** that touches an address also calls `snapshot_address()` before returning data. This means the database is always current by the time the response is sent, regardless of when the poller last ran.

**New addresses** are added automatically. If you query an address through `/balance` or `/history/{address}` that is not yet in the database, it gets seeded immediately and picked up by the poller going forward.

This mirrors how production pipelines avoid storing duplicate records while continuously ingesting new data.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/wallet-balance-tracker.git
cd wallet-balance-tracker
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
DB_PATH=balances.db
```

### 5. Run the app

```bash
uvicorn app.main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

## Deployment

The app is configured to deploy on Railway with a persistent volume for SQLite.

Set the following environment variables in Railway:

```
ALCHEMY_URL=your_alchemy_url
DB_PATH=/data/balances.db
```

Attach a persistent volume mounted at `/data` so the database survives restarts and redeploys. The `Procfile` handles the rest:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Future Improvements

- Basic metrics endpoint showing total wallets tracked, total snapshots recorded, and poller health
- Caching layer on `/api/wallets` and `/api/balance` to reduce redundant Alchemy calls for recently fetched addresses
- Multi-chain support — extend the pipeline to track balances on Polygon, Arbitrum, Base, and Optimism using their respective RPC endpoints
- Simple frontend dashboard charts showing balance over time per address using the existing transactions data
- Docker support for local development parity and easier self-hosting

## Why This Project Exists

I built this to practice designing blockchain data pipelines, writing async services, working with background jobs, storing and querying time series style data, and structuring a production style API with a real frontend. The project is intentionally simple but designed like a real system.