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
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── entrypoint.sh          # Container entrypoint script
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

## Prerequisites

1. **Docker Installation**:
   - Download and install Docker Desktop from [Docker Downloads](https://www.docker.com/products/docker-desktop)
   - Make sure Docker Desktop is running
   - Verify installation by running `docker --version` in terminal

## Running with Docker

1. **Build and Start Containers**:
   ```bash
   # Build and start all services
   docker-compose up --build
   ```
   This will:
   - Build the Docker image
   - Start the ETL scheduler
   - Start the Streamlit dashboard
   - Mount necessary volumes for data persistence

2. **Access the Dashboard**:
   - Open your browser and navigate to `http://localhost:8501`
   - The dashboard will be available and automatically update with new data

3. **View Logs**:
   ```bash
   # View logs for all services
   docker-compose logs -f
   
   # View logs for specific service
   docker-compose logs -f scheduler
   docker-compose logs -f dashboard
   ```

4. **Stop the Services**:
   ```bash
   # Stop all services
   docker-compose down
   ```

## Running Locally (Alternative)

If you prefer to run the application without Docker:

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

## Troubleshooting

If you encounter any issues:

1. **Docker Issues**
   - Make sure Docker Desktop is running
   - Check if ports 8501 are available
   - Try rebuilding the containers:
     ```bash
     docker-compose down
     docker-compose up --build
     ```

2. **Data Not Updating**
   - Check the scheduler logs:
     ```bash
     docker-compose logs -f scheduler
     ```
   - Verify the data volumes are properly mounted
   - Check the logs in the `logs` directory

3. **Dashboard Not Loading**
   - Check the dashboard logs:
     ```bash
     docker-compose logs -f dashboard
     ```
   - Verify the dashboard container is running:
     ```bash
     docker-compose ps
     ```
   - Make sure port 8501 is not in use by another application

4. **Dependencies Installation**
   - If you encounter any package installation errors in the container, check the build logs:
     ```bash
     docker-compose build --no-cache
     ```
   - Make sure all required packages are listed in requirements.txt 