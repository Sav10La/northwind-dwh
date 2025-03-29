import sqlite3
import pandas as pd
from config import DWH_PATH
import logging

logger = logging.getLogger(__name__)

def load_table(df, table_name, conn):
    """Load a DataFrame into the data warehouse."""
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {table_name} into data warehouse.")

def create_data_warehouse():
    """Create the data warehouse database."""
    # Connect to (or create) the DW SQLite database
    dwh_conn = sqlite3.connect(DWH_PATH)
    return dwh_conn

def load_data_warehouse(fact_sales, dimensions):
    """Load all tables into the data warehouse."""
    dwh_conn = create_data_warehouse()
    
    # Load fact table
    load_table(fact_sales, "fact_sales", dwh_conn)
    
    # Load dimension tables
    for name, df in dimensions.items():
        load_table(df, name, dwh_conn)
    
    # Confirm tables are created
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", dwh_conn)
    print("\n✅ Data warehouse schema stored successfully in SQLite:")
    print(tables)
    
    return dwh_conn

def add_revenue_eur(conn, exchange_rate):
    """Add EUR revenue to fact_sales table."""
    cursor = conn.cursor()
    
    # Add EUR revenue column if it doesn't exist
    cursor.execute("""
    ALTER TABLE fact_sales ADD COLUMN RevenueEUR REAL
    """)
    
    # Update EUR revenue
    cursor.execute("""
    UPDATE fact_sales 
    SET RevenueEUR = RevenueUSD * ?
    """, (exchange_rate,))
    
    conn.commit()
    logger.info(f"Added EUR revenue (rate: {exchange_rate})") 