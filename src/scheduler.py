import schedule
import time
from datetime import datetime
from pathlib import Path
import sys
import argparse

# Add src directory to Python path
src_path = Path(__file__).parent
sys.path.append(str(src_path))

from utils.logger import get_logger
from utils.job_metadata import log_job_start, log_job_end, init_job_metadata, get_job_history
from extract import download_database, get_database_connection, load_tables, load_cities_data, get_exchange_rate
from transform import clean_dataframes, create_dimensions, create_fact_table, enrich_customer_dimension
from load import load_data_warehouse, add_revenue_eur

# Configure logging
logger = get_logger()

def run_etl():
    """Run the complete ETL process."""
    logger.info("Starting ETL process...")
    
    try:
        # Extract
        job_id = log_job_start('extract_data')
        logger.info("Starting data extraction...")
        
        # Download and connect to database
        db_path = download_database()
        conn = get_database_connection(db_path)
        
        # Load tables
        tables = load_tables(conn)
        logger.info("Loaded all tables from database")
        
        # Load cities data
        world_cities = load_cities_data()
        logger.info("Loaded world cities data")
        
        # Get exchange rate
        exchange_rate = get_exchange_rate()
        logger.info(f"Got exchange rate: {exchange_rate}")
        
        log_job_end(job_id, 'success')
        logger.info("Data extraction completed successfully")
        
        # Transform
        job_id = log_job_start('transform_data')
        logger.info("Starting data transformation...")
        
        # Clean data
        cleaned_tables = clean_dataframes(tables)
        logger.info("Cleaned all tables")
        
        # Create dimensions
        dimensions = create_dimensions(cleaned_tables)
        logger.info("Created dimension tables")
        
        # Create fact table
        fact_sales = create_fact_table(cleaned_tables)
        logger.info("Created fact table")
        
        # Enrich customer dimension
        dimensions['dim_customer'] = enrich_customer_dimension(
            dimensions['dim_customer'],
            world_cities
        )
        logger.info("Enriched customer dimension")
        
        log_job_end(job_id, 'success')
        logger.info("Data transformation completed successfully")
        
        # Load
        job_id = log_job_start('load_data')
        logger.info("Starting data loading...")
        
        # Load data into warehouse
        dwh_conn = load_data_warehouse(fact_sales, dimensions)
        logger.info("Loaded data into warehouse")
        
        # Add EUR revenue
        add_revenue_eur(dwh_conn, exchange_rate)
        logger.info("Added EUR revenue")
        
        log_job_end(job_id, 'success')
        logger.info("Data loading completed successfully")
        
        logger.info("ETL process completed successfully!")
        
    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        raise

def run_etl_with_error_handling():
    """Run ETL with error handling and retries."""
    max_retries = 3
    retry_delay = 300  # 5 minutes
    
    for attempt in range(max_retries):
        try:
            run_etl()
            return
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"All {max_retries} attempts failed. Last error: {str(e)}")
                raise

def show_status():
    """Show current scheduler status and next run time."""
    next_run = schedule.next_run()
    if next_run:
        logger.info(f"Next scheduled run: {next_run}")
    else:
        logger.info("No scheduled runs")
    
    # Show recent job history
    logger.info("\nRecent job history:")
    history = get_job_history(limit=5)
    if not history:
        logger.info("No job history available")
        return
        
    for job in history:
        status = "✓" if job['status'] == 'success' else "✗"
        start_time = datetime.fromisoformat(job['start_time'])
        duration = job['duration'] if job['duration'] is not None else 0
        logger.info(f"{status} {job['job_name']} - {start_time} ({duration:.1f}s)")

def main():
    """Main function to set up and run the scheduler."""
    parser = argparse.ArgumentParser(description='Northwind ETL Scheduler')
    parser.add_argument('--once', action='store_true', help='Run ETL once without scheduling')
    parser.add_argument('--status', action='store_true', help='Show scheduler status and recent history')
    args = parser.parse_args()

    logger.info("Starting ETL scheduler...")
    
    # Initialize job metadata table
    try:
        init_job_metadata()
        logger.info("Initialized job metadata table")
    except Exception as e:
        logger.error(f"Failed to initialize job metadata table: {str(e)}")
        raise

    if args.status:
        show_status()
        return

    if args.once:
        logger.info("Running ETL once (no scheduling)...")
        run_etl_with_error_handling()
        return
    
    # Schedule the ETL job to run daily at midnight
    schedule.every().day.at("00:00").do(run_etl_with_error_handling)
    
    # Run the job immediately on startup
    logger.info("Running initial ETL job...")
    run_etl_with_error_handling()
    
    # Show status after initial run
    show_status()
    
    logger.info("\nScheduler is running. Press Ctrl+C to stop.")
    logger.info("Use --status flag to check current status")
    
    # Keep the script running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("\nScheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in scheduler: {str(e)}")
            time.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    main() 