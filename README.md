# Northwind Data Warehouse ETL Pipeline

## Project Structure
```
coursework/
├── data/               # Data files (worldcities.csv)
├── db/                 # Database files
├── logs/              # Log files
├── src/               # Source code
│   ├── utils/         # Utility modules
│   ├── config.py      # Configuration
│   ├── extract.py     # Data extraction
│   ├── load.py        # Data loading
│   ├── main.py        # Main entry point
│   ├── scheduler.py   # Scheduling
│   └── transform.py   # Data transformation
├── app.py             # Web dashboard
├── Procfile           # Heroku process configuration
├── README.md          # Documentation
└── requirements.txt   # Dependencies
```

## Setup

1. Ensure you have Python 3.8 or higher installed
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Place the worldcities.csv file in the data directory

## Running Locally

1. Run the ETL pipeline:
   ```bash
   python src/main.py
   ```

2. Start the dashboard:
   ```bash
   python app.py
   ```

3. Access the dashboard at http://localhost:8050

## Deployment to Heroku

1. Install the Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create northwind-dwh
   ```

3. Add PostgreSQL addon:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. Set environment variables:
   ```bash
   heroku config:set DATABASE_URL=$(heroku config:get DATABASE_URL)
   ```

5. Deploy the application:
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. Scale the dynos:
   ```bash
   heroku ps:scale web=1 worker=1
   ```

7. Access your dashboard at https://northwind-dwh.herokuapp.com

## Features

### ETL Pipeline
- Automated data extraction from Northwind database
- Data transformation and cleaning
- Geographic data enrichment
- Daily scheduled updates
- Comprehensive logging

### Dashboard
- Sales trends visualization
- Top products analysis
- Top customers analysis
- Geographic distribution of sales
- Real-time data updates

## Monitoring and Maintenance

### Logs
- Application logs are available in the logs directory
- View Heroku logs:
  ```bash
  heroku logs --tail
  ```

### Database
- Regular backups are automatically created
- Monitor database size:
  ```bash
  heroku pg:info
  ```

### Scaling
- Scale dynos as needed:
  ```bash
  heroku ps:scale web=2 worker=2
  ```

## Troubleshooting

### Common Issues
1. Database connection errors
   - Check DATABASE_URL environment variable
   - Verify PostgreSQL addon status

2. ETL failures
   - Check logs for specific error messages
   - Verify data file permissions

3. Dashboard not updating
   - Check worker dyno status
   - Verify scheduler is running

### Support
For issues or questions, please create an issue in the repository. 