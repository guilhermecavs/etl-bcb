# Brazilian Economic Indicators — ETL Pipeline

A pipeline that pulls economic data directly from Brazil's Central Bank (BCB) public API and stores it in a PostgreSQL database. It runs automatically every day at 08:00 so the data is always fresh.

## What it tracks

Three key indicators from the BCB's SGS system:

| Indicator | Description | Series Code |
|-----------|-------------|-------------|
| SELIC | Brazil's base interest rate | 11 |
| USD Exchange Rate | BRL/USD daily rate | 1 |
| IPCA | Official inflation index | 13522 |

## How it works

The pipeline follows a straightforward ETL flow:

1. **Extract** — Fetches the last 60 days of data from the BCB API for each indicator
2. **Transform** — Parses dates, normalizes decimal separators, and drops any incomplete rows
3. **Load** — Inserts the cleaned records into PostgreSQL, skipping duplicates automatically

After the first run, it schedules itself to repeat daily at 08:00.

## Tech stack

- **Python** — pipeline logic
- **PostgreSQL 15** — data storage
- **pgAdmin 4** — database UI
- **Docker & Docker Compose** — containerized infrastructure
- **SQLAlchemy** — database connection and query execution
- **pandas** — data transformation
- **schedule** — daily job scheduling

## Getting started

### Prerequisites

- Docker and Docker Compose installed
- Python 3.9+

### 1. Clone the repo and install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```env
DB_USER=etl_user
DB_PASSWORD=etl_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bcb_data
```

### 3. Start the database

```bash
docker-compose up -d
```

This spins up PostgreSQL on port `5432` and pgAdmin on port `8080`.

The tables are created automatically via `init.sql` on the first run.

### 4. Run the pipeline

```bash
python pipeline.py
```

The pipeline will run immediately and then schedule itself to run every day at 08:00.

## Accessing pgAdmin

Open your browser at `http://localhost:8080` and log in with:

- **Email:** admin@admin.com
- **Password:** admin

Then add a new server with the credentials from your `.env` file to browse the data.

## Project structure

```
.
├── src/
│   ├── database.py   # SQLAlchemy engine setup
│   ├── extract.py    # BCB API requests
│   ├── transform.py  # Data cleaning and normalization
│   └── load.py       # Database insertion logic
├── pipeline.py       # Entry point and scheduler
├── init.sql          # Table definitions
├── docker-compose.yml
└── requirements.txt
```

## Notes

- The pipeline uses `ON CONFLICT DO NOTHING` on inserts, so re-running it won't create duplicate records
- If the BCB API returns an error for a given series (e.g., during maintenance), that series is skipped and logged — the rest of the pipeline continues normally
- Logs are written to the `logs/` directory
