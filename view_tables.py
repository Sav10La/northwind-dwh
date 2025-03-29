import pandas as pd
import sqlite3
from pathlib import Path
import sys

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from config import SQLITE_DB

def view_table(table_name, limit=5):
    """View the first few rows of a table."""
    conn = sqlite3.connect(SQLITE_DB)
    query = f"SELECT * FROM {table_name} LIMIT {limit}"
    df = pd.read_sql(query, conn)
    print(f"\n=== {table_name} ===")
    print(df)
    print("\nColumns:", ", ".join(df.columns))
    print(f"Total rows: {pd.read_sql(f'SELECT COUNT(*) as count FROM {table_name}', conn).iloc[0]['count']}")
    conn.close()

def main():
    # List of tables to view
    tables = [
        'fact_sales',
        'dim_customer',
        'dim_product',
        'dim_date'
    ]
    
    print("Data Warehouse Tables Overview")
    print("=" * 50)
    
    for table in tables:
        view_table(table)

if __name__ == "__main__":
    main() 