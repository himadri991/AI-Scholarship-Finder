from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import os
import subprocess
import threading
import time
import signal
import sys

app = Flask(__name__)

# Global variable to store the Streamlit process
streamlit_process = None

# Function to start Streamlit in a separate thread
def start_streamlit():
    global streamlit_process
    # Set environment variables to prevent torch.classes errors
    env = os.environ.copy()
    env["STREAMLIT_SERVER_WATCH_DIRS"] = "false"
    env["STREAMLIT_SERVER_FILEWATCH"] = "false"
    env["PYTHONPATH"] = os.getcwd()
    
    # Run Streamlit with minimal watcher on port 8502
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py", 
           "--server.fileWatcherType", "none", 
           "--server.port", "8502",
           "--server.baseUrlPath", "scholarship-finder"]
    
    streamlit_process = subprocess.Popen(cmd, env=env)
    print("Streamlit process started")

# Start Streamlit when Flask starts
@app.before_request
def before_first_request():
    global streamlit_process
    if streamlit_process is None:
        thread = threading.Thread(target=start_streamlit)
        thread.daemon = True
        thread.start()
        # Give Streamlit time to start
        time.sleep(5)

# Clean up Streamlit process when Flask exits
def cleanup(signal, frame):
    global streamlit_process
    if streamlit_process:
        print("Terminating Streamlit process")
        streamlit_process.terminate()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Serve static images
@app.route('/static/images/<path:path>')
def serve_images(path):
    return send_from_directory('static/images', path)

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# Redirect to Streamlit app
@app.route('/scholarship-finder')
def scholarship_finder():
    return redirect('http://localhost:8502/scholarship-finder')

# Proxy for Streamlit
@app.route('/scholarship-finder/<path:path>')
def streamlit_proxy(path):
    return redirect(f'http://localhost:8502/scholarship-finder/{path}')

if __name__ == '__main__':
    app.run(debug=True, port=8501)