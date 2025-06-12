import os
import subprocess
import sys

# Set environment variables to prevent torch.classes errors
os.environ["STREAMLIT_SERVER_WATCH_DIRS"] = "false"
os.environ["STREAMLIT_SERVER_FILEWATCH"] = "false"
os.environ["PYTHONPATH"] = os.getcwd()

# Run Streamlit with minimal watcher
cmd = [sys.executable, "-m", "streamlit", "run", "app.py", "--server.fileWatcherType", "none"]
subprocess.run(cmd) 