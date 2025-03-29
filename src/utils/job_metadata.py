import sqlite3
from datetime import datetime
from pathlib import Path
import sys

# Add src directory to Python path
src_path = Path(__file__).parent.parent
sys.path.append(str(src_path))

from config import SQLITE_DB

def init_job_metadata():
    """Initialize the job metadata table."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    # Create job metadata table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_metadata (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_name TEXT NOT NULL,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP,
        status TEXT,
        error_message TEXT,
        duration_seconds REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def log_job_start(job_name):
    """Log the start of a job."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO job_metadata (job_name, start_time, status)
    VALUES (?, ?, ?)
    ''', (job_name, datetime.now(), 'running'))
    
    job_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return job_id

def log_job_end(job_id, status, error_message=None):
    """Log the end of a job."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    # Get start time
    cursor.execute('SELECT start_time FROM job_metadata WHERE job_id = ?', (job_id,))
    start_time = datetime.fromisoformat(cursor.fetchone()[0])
    
    # Calculate duration
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Update job record
    cursor.execute('''
    UPDATE job_metadata 
    SET end_time = ?, status = ?, error_message = ?, duration_seconds = ?
    WHERE job_id = ?
    ''', (end_time, status, error_message, duration, job_id))
    
    conn.commit()
    conn.close()
    
    return duration

def get_job_history(job_name=None, limit=10):
    """Get the execution history of jobs."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    query = '''
    SELECT job_id, job_name, start_time, end_time, status, error_message, duration_seconds
    FROM job_metadata
    '''
    
    if job_name:
        query += ' WHERE job_name = ?'
        cursor.execute(query + ' ORDER BY start_time DESC LIMIT ?', (job_name, limit))
    else:
        cursor.execute(query + ' ORDER BY start_time DESC LIMIT ?', (limit,))
    
    # Convert tuples to dictionaries
    columns = ['job_id', 'job_name', 'start_time', 'end_time', 'status', 'error_message', 'duration']
    results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    
    conn.close()
    return results 