from extract import (
    download_database,
    get_database_connection,
    load_tables,
    load_cities_data,
    get_exchange_rate
)
from transform import (
    clean_dataframes,
    create_dimensions,
    create_fact_table,
    enrich_customer_dimension
)
from load import load_data_warehouse, add_revenue_eur

def main():
    """Main function to orchestrate the ETL process."""
    print("Starting ETL process...")
    
    # Extract
    print("\n=== Extraction Phase ===")
    download_database()
    conn = get_database_connection()
    tables = load_tables(conn)
    world_cities = load_cities_data()
    exchange_rate = get_exchange_rate()
    
    # Transform
    print("\n=== Transformation Phase ===")
    cleaned_tables = clean_dataframes(tables)
    dimensions = create_dimensions(cleaned_tables)
    fact_sales = create_fact_table(cleaned_tables)
    
    # Enrich customer dimension with geographic data
    dimensions['dim_customer'] = enrich_customer_dimension(
        dimensions['dim_customer'],
        world_cities
    )
    
    # Load
    print("\n=== Loading Phase ===")
    dwh_conn = load_data_warehouse(fact_sales, dimensions)
    add_revenue_eur(dwh_conn, exchange_rate)
    
    print("\nETL process completed successfully!")

if __name__ == "__main__":
    main() 