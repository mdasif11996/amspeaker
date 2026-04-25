
import subprocess
import sys
import os

# Change to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run Streamlit app
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
