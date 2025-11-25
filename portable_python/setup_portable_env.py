#!/usr/bin/env python3
"""
Setup script for creating a portable Python environment with all project dependencies.
This script will download Python and install all dependencies locally.
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil
import platform
from pathlib import Path

def get_python_download_url():
    """Get the appropriate Python download URL for the current system"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        if machine == "amd64" or machine == "x86_64":
            return "https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip"
        else:
            return "https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-win32.zip"
    elif system == "linux":
        # For Linux, we'll need to use a different approach
        return None
    elif system == "darwin":  # macOS
        # For macOS, we'll need to use a different approach
        return None
    return None

def download_file(url, filename):
    """Download a file from URL"""
    print(f"Downloading {url}...")
    urllib.request.urlretrieve(url, filename)
    print(f"Downloaded to {filename}")

def extract_zip(zip_path, extract_to):
    """Extract a zip file"""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted to {extract_to}")

def setup_portable_python():
    """Setup portable Python environment"""
    project_root = Path(__file__).parent.parent.absolute()
    portable_dir = project_root / "portable_python"
    python_dir = portable_dir / "python"
    
    print(f"Setting up portable Python environment in {python_dir}")
    
    # Create directories
    portable_dir.mkdir(exist_ok=True)
    python_dir.mkdir(exist_ok=True)
    
    # Download portable Python
    python_url = get_python_download_url()
    if python_url:
        python_zip = portable_dir / "python.zip"
        download_file(python_url, python_zip)
        extract_zip(python_zip, python_dir)
        # Remove the zip file to save space
        python_zip.unlink()
    else:
        print("Could not determine Python download URL for your system.")
        print("Please install Python 3.10 manually in the portable_python/python directory.")
        return False
    
    # Configure Python (for embedded Python on Windows)
    # Remove 'python310._pth' file restrictions
    pth_file = python_dir / "python310._pth"
    if pth_file.exists():
        # Read the file and modify it to include our paths
        with open(pth_file, 'r') as f:
            content = f.read()
        
        # Add our project paths
        content = "..\n..\src\n..\src\utils\n" + content
        
        with open(pth_file, 'w') as f:
            f.write(content)
    
    # Create a pip installation script
    pip_script = portable_dir / "get-pip.py"
    if not pip_script.exists():
        print("Downloading get-pip.py...")
        urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", pip_script)
    
    # Install pip
    print("Installing pip...")
    python_exe = python_dir / "python.exe"
    subprocess.run([str(python_exe), str(pip_script), "--no-warn-script-location"])
    
    # Install project dependencies
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        print("Installing project dependencies...")
        subprocess.run([str(python_exe), "-m", "pip", "install", "-r", str(requirements_file), "--no-warn-script-location"])
    else:
        print("requirements.txt not found. Please create it with your project dependencies.")
        return False
    
    # Create activation scripts
    create_activation_scripts()
    
    print("Portable Python environment setup complete!")
    print(f"Python executable: {python_exe}")
    return True

def create_activation_scripts():
    """Create scripts to easily activate the portable environment"""
    project_root = Path(__file__).parent.parent.absolute()
    portable_dir = project_root / "portable_python"
    python_dir = portable_dir / "python"
    
    # Windows batch script
    activate_bat = project_root / "activate_portable.bat"
    with open(activate_bat, 'w') as f:
        f.write(f"""@echo off
echo Activating portable Python environment...
set PYTHONPATH={project_root};{project_root}\\src;{project_root}\\src\\utils;%PYTHONPATH%
set PATH={python_dir};{python_dir}\\Scripts;%PATH%
echo Portable Python environment activated.
echo To run the application, use: python src\\main.py
cmd /k
""")
    
    # Deactivation script
    deactivate_bat = project_root / "deactivate_portable.bat"
    with open(deactivate_bat, 'w') as f:
        f.write("""@echo off
echo Deactivating portable Python environment...
set PYTHONPATH=
set PATH=%ORIGINAL_PATH%
echo Portable Python environment deactivated.
cmd /k
""")
    
    print("Activation scripts created:")
    print(f"  - {activate_bat}")
    print(f"  - {deactivate_bat}")

if __name__ == "__main__":
    setup_portable_python()