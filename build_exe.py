import os
import sys
import subprocess

def build_exe():
    """Build Streamlit app as EXE using PyInstaller"""
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create a launcher script
    launcher_script = """
import subprocess
import sys
import os

# Change to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run Streamlit app
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
"""
    
    with open("launcher.py", "w") as f:
        f.write(launcher_script)
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "launcher.py",
        "--name=SpeakAI",
        "--onefile",
        "--windowed",
        "--add-data=app.py;.",
        "--add-data=.env;.",
        "--hidden-import=streamlit",
        "--hidden-import=openai",
        "--hidden-import=dotenv",
        "--collect-all=streamlit",
    ]
    
    print("Building EXE file...")
    subprocess.run(cmd)
    
    print("\n✅ EXE file created in dist/SpeakAI.exe")
    print("Note: When you run the EXE, it will start the Streamlit server and open in your browser.")

if __name__ == "__main__":
    build_exe()

