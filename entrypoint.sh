#!/bin/sh

if [ "$1" = "dashboard" ]; then
    echo "Starting Streamlit dashboard..."
    exec streamlit run dashboard/streamlit_app.py
elif [ "$1" = "scheduler" ]; then
    echo "Running ETL scheduler..."
    exec python src/scheduler.py
else
    echo "Usage: docker run your-image-name [dashboard|scheduler]"
    exit 1
fi
