# Northwind Data Warehouse and OLAP Dashboard

A comprehensive data warehouse solution for the Northwind database with an interactive OLAP dashboard.

## Project Structure

```
DWH_CW_1631/
├── data/
│   ├── raw/                  # Raw data files
│   ├── processed/            # Processed data files
│   ├── worldcities.csv      # Cities data for enrichment
│   └── northwind_dwh.sqlite # Data warehouse
├── dashboard/
│   └── streamlit_app.py     # OLAP Dashboard
├── src/
│   ├── config.py           # Configuration settings
│   ├── extract.py          # Data extraction
│   ├── transform.py        # Data transformation
│   ├── load.py            # Data loading
│   ├── main.py            # Main ETL pipeline
│   ├── scheduler.py       # ETL scheduling
│   └── utils/
│       ├── job_metadata.py # Job tracking
│       └── logger.py       # Logging utilities
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── logs/                   # ETL execution logs
├── requirements.txt        # Project dependencies
└── README.md              # Documentation
```

## Features

The dashboard provides interactive OLAP operations:

1. **Roll-up & Drill-down Analysis**
   - Time hierarchy (Year → Quarter → Month → Day)
   - Geography hierarchy (Country → City)
   - Product hierarchy (Category → Product)

2. **Slice & Dice Analysis**
   - Interactive dimension selection
   - Heatmap visualization
   - Detailed data view

3. **Pivot Analysis**
   - Customizable pivot tables
   - Multiple aggregation functions
   - Interactive visualizations

## Running Locally

1. **Setup Environment**:
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Start the ETL Pipeline**:
   ```bash
   # Start the scheduler (recommended)
   python src/scheduler.py
   ```
   This will:
   - Run the ETL pipeline immediately
   - Schedule daily runs at midnight
   - Keep running in the background
   
   Note: The scheduler needs to be running in a separate terminal window. You can stop it at any time by pressing Ctrl+C.

3. **Run the Dashboard**:
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```
   The dashboard will open in your browser at `http://localhost:8501`

4. **Alternative: One-time ETL Run**
   If you only want to run the ETL pipeline once without scheduling:
   ```bash
   python src/scheduler.py --once
   ```
   Or check the current status of the scheduler:
   ```bash
   python src/scheduler.py --status
   ```

## GitHub Repository

The project is available on GitHub: [northwind-dwh](https://github.com/Sav10La/northwind-dwh)

## Online Dashboard

Access the deployed dashboard at: [Northwind OLAP Dashboard](https://northwind-dwh-kca6z7nfgnsu4ldbvadhj9.streamlit.app/)

## Troubleshooting

If you encounter any issues:

1. **Year Values Not Showing**
   - The dashboard uses the year 2024 for all dates
   - This is a known limitation of the data source

2. **Data Not Updating**
   - Ensure the scheduler is running
   - Check the logs in the `logs` directory
   - Verify the data warehouse file exists

3. **Dashboard Not Loading**
   - Make sure the ETL pipeline has run at least once
   - Check if the data warehouse file exists
   - Verify all dependencies are installed 