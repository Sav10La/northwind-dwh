import os
import urllib.request
import sqlite3
import pandas as pd
import requests
from pathlib import Path
from config import (
    RAW_DATA_DIR, DB_URL, CITIES_PATH, EXCHANGE_RATE_API
)

def download_database():
    """Download the Northwind database if it doesn't exist locally."""
    db_path = RAW_DATA_DIR / "northwind.db"
    if not db_path.exists():
        print("Downloading Northwind database...")
        urllib.request.urlretrieve(DB_URL, db_path)
        print("Download complete.")
    else:
        print("Database already exists locally.")
    return db_path

def get_database_connection(db_path):
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    print("Connected to the Northwind database.")
    return conn

def load_tables(conn):
    """Load all required tables from the database into pandas DataFrames."""
    tables = {
        'customers': pd.read_sql("SELECT * FROM Customers", conn),
        'orders': pd.read_sql("SELECT * FROM Orders", conn),
        'order_details': pd.read_sql("SELECT * FROM 'Order Details'", conn),
        'products': pd.read_sql("SELECT * FROM Products", conn),
        'categories': pd.read_sql("SELECT * FROM Categories", conn),
        'suppliers': pd.read_sql("SELECT * FROM Suppliers", conn)
    }
    return tables

def load_cities_data():
    """Load world cities data from local CSV file."""
    if not CITIES_PATH.exists():
        raise FileNotFoundError(
            f"World cities dataset not found at {CITIES_PATH}. "
            "Please ensure the worldcities.csv file is in the data directory."
        )
    return pd.read_csv(CITIES_PATH)

def get_exchange_rate():
    """Get current USD to EUR exchange rate."""
    try:
        response = requests.get(EXCHANGE_RATE_API)
        response.raise_for_status()
        data = response.json()
        return data['rates']['EUR']
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return 0.92  # Fallback rate if API fails 