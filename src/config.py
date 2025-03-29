import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Database paths
DB_DIR = "db"
DB_FILENAME = "northwind.sqlite"
DWH_FILENAME = "northwind_dwh.db"

# Construct full paths
DB_PATH = os.path.join(ROOT_DIR, DB_DIR, DB_FILENAME)
DWH_PATH = os.path.join(ROOT_DIR, DB_DIR, DWH_FILENAME)

# Data source URLs
DB_URL = "https://raw.githubusercontent.com/jpwhite3/northwind-SQLite3/main/dist/northwind.db"

# World cities data
DATA_DIR = "data"
CITIES_FILENAME = "worldcities.csv"
CITIES_PATH = os.path.join(ROOT_DIR, DATA_DIR, CITIES_FILENAME)

# Exchange rate API
EXCHANGE_RATE_API = "https://api.exchangerate-api.com/v4/latest/USD"

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DWH_PATH}')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

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

# Create necessary directories
os.makedirs(DB_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True) 