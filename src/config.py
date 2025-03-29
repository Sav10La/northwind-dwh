import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Data directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DATA_DIR.mkdir(exist_ok=True)

# Database configuration
SQLITE_DB = DATA_DIR / "northwind_dwh.sqlite"
DATABASE_URL = f"sqlite:///{SQLITE_DB}"

# Logging configuration
LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "etl.log"

# ETL configuration
BATCH_SIZE = 1000
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Data source URLs
DB_URL = "https://raw.githubusercontent.com/jpwhite3/northwind-SQLite3/main/dist/northwind.db"

# World cities data
CITIES_FILENAME = "worldcities.csv"
CITIES_PATH = DATA_DIR / CITIES_FILENAME

# Exchange rate API
EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/USD"

# City name fixes for standardization
CITY_FIXES = {
    "bruxelles": "brussels",
    "sao paulo": "são paulo",
    "tsawassen": "vancouver",
    "kobenhavn": "copenhagen",
    "århus": "aarhus",
    "cunewalde": "dresden",
    "frankfurt a.m.": "frankfurt",
    "köln": "cologne",
    "münchen": "munich",
    "torino": "turin",
    "méxico d.f.": "mexico city",
    "stavern": "oslo",
    "warszawa": "warsaw",
    "lisboa": "lisbon",
    "bräcke": "östersund",
    "genève": "geneva",
    "cowes": "southampton",
    "i. de margarita": "porlamar",  # Main city in Margarita Island, Venezuela
    "lander": "casper",  # Map to Casper, the largest city in Wyoming
    "unknown": "unknown"  # Handle unknown cities
}

# Country name fixes for standardization
COUNTRY_FIXES = {
    "uk": "united kingdom",
    "usa": "united states"
} 