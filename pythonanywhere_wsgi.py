import sys
import os

# Add your project directory to the Python path
project_home = '/home/asharakhmedov/northwind_dwh'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set environment variables
os.environ['PYTHONPATH'] = project_home
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'

# Import and run the Streamlit app
from dashboard.streamlit_app import main

def application(environ, start_response):
    # Run Streamlit in a separate thread
    import threading
    thread = threading.Thread(target=main)
    thread.daemon = True
    thread.start()
    
    # Return a simple response
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Streamlit app is running...'] 