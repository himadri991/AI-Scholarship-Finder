import os
import subprocess
import sys
import threading
import time
import signal

# Set environment variables to prevent torch.classes errors
os.environ["STREAMLIT_SERVER_WATCH_DIRS"] = "false"
os.environ["STREAMLIT_SERVER_FILEWATCH"] = "false"
os.environ["PYTHONPATH"] = os.getcwd()

# Global variables to store processes
flask_process = None
streamlit_process = None

# Function to start Streamlit in a separate thread
def start_streamlit():
    global streamlit_process
    print("Starting Streamlit server on port 8502...")
    # Run Streamlit with minimal watcher on port 8502
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py", 
           "--server.fileWatcherType", "none", 
           "--server.port", "8502",
           "--server.baseUrlPath", "scholarship-finder"]
    
    streamlit_process = subprocess.Popen(cmd)
    print("Streamlit process started")

# Function to start Flask in a separate thread
def start_flask():
    global flask_process
    print("Starting Flask server on port 8501...")
    # Run Flask app
    cmd = [sys.executable, "flask_app.py"]
    
    flask_process = subprocess.Popen(cmd)
    print("Flask process started")

# Clean up processes when script exits
def cleanup(signal, frame):
    global flask_process, streamlit_process
    print("\nShutting down servers...")
    
    if flask_process:
        print("Terminating Flask process")
        flask_process.terminate()
        flask_process.wait()
    
    if streamlit_process:
        print("Terminating Streamlit process")
        streamlit_process.terminate()
        streamlit_process.wait()
    
    print("All processes terminated. Goodbye!")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def main():
    try:
        # Start Streamlit in a separate thread
        streamlit_thread = threading.Thread(target=start_streamlit)
        streamlit_thread.daemon = True
        streamlit_thread.start()
        
        # Give Streamlit time to start
        time.sleep(3)
        
        # Start Flask in the main thread
        start_flask()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup(None, None)

if __name__ == "__main__":
    print("Starting AI Scholarship Finder...")
    print("Landing page will be available at: http://localhost:8501")
    print("Scholarship Finder will be available at: http://localhost:8501/scholarship-finder")
    main()