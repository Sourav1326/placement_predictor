#!/usr/bin/env python3
"""
Setup script for creating a local Python virtual environment with all project dependencies.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path

def create_local_environment():
    """Create a local virtual environment with all dependencies"""
    project_root = Path(__file__).parent.absolute()
    venv_dir = project_root / "venv"
    
    print(f"Creating local virtual environment in {venv_dir}")
    
    # Create virtual environment
    if not venv_dir.exists():
        print("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
        print("Virtual environment created successfully!")
    else:
        print("Virtual environment already exists.")
    
    # Determine the Python executable path based on the OS
    if os.name == 'nt':  # Windows
        python_exe = venv_dir / "Scripts" / "python.exe"
        pip_exe = venv_dir / "Scripts" / "pip.exe"
    else:  # Unix/Linux/macOS
        python_exe = venv_dir / "bin" / "python"
        pip_exe = venv_dir / "bin" / "pip"
    
    # Upgrade pip
    print("Upgrading pip...")
    subprocess.run([str(python_exe), "-m", "pip", "install", "--upgrade", "pip"])
    
    # Install project dependencies
    requirements_file = project_root / "requirements.txt"
    if requirements_file.exists():
        print("Installing project dependencies...")
        subprocess.run([str(pip_exe), "install", "-r", str(requirements_file)])
        print("Dependencies installed successfully!")
    else:
        print("Warning: requirements.txt not found.")
    
    # Create activation scripts
    create_activation_scripts()
    
    print("\nLocal environment setup complete!")
    print(f"Virtual environment location: {venv_dir}")
    print("\nTo activate the environment:")
    if os.name == 'nt':  # Windows
        print(f"  Run: {project_root / 'activate.bat'}")
        print(f"  Or manually: {venv_dir / 'Scripts' / 'activate.bat'}")
    else:  # Unix/Linux/macOS
        print(f"  Run: source {project_root / 'activate.sh'}")
        print(f"  Or manually: source {venv_dir / 'bin' / 'activate'}")
    
    print("\nTo run the application after activation:")
    print("  python src/main.py")

def create_activation_scripts():
    """Create convenient activation scripts"""
    project_root = Path(__file__).parent.absolute()
    venv_dir = project_root / "venv"
    
    # Windows batch script
    if os.name == 'nt':
        activate_bat = project_root / "activate.bat"
        with open(activate_bat, 'w') as f:
            f.write(f"""@echo off
echo Activating local Python environment...
call "{venv_dir / 'Scripts' / 'activate.bat'}"
echo Environment activated. You can now run the application.
""")
        
        deactivate_bat = project_root / "deactivate.bat"
        with open(deactivate_bat, 'w') as f:
            f.write("""@echo off
echo Deactivating Python environment...
deactivate
echo Environment deactivated.
""")
        
        run_app_bat = project_root / "run_app.bat"
        with open(run_app_bat, 'w') as f:
            f.write(f"""@echo off
echo Starting Placement Predictor Application...
call "{activate_bat}"
cd "{project_root}"
python src/main.py
""")
    
    # Unix/Linux/macOS shell script
    else:
        activate_sh = project_root / "activate.sh"
        with open(activate_sh, 'w') as f:
            f.write(f"""#!/bin/bash
echo "Activating local Python environment..."
source "{venv_dir / 'bin' / 'activate'}"
echo "Environment activated. You can now run the application."
""")
        # Make it executable
        os.chmod(activate_sh, 0o755)
        
        run_app_sh = project_root / "run_app.sh"
        with open(run_app_sh, 'w') as f:
            f.write(f"""#!/bin/bash
echo "Starting Placement Predictor Application..."
source "{activate_sh}"
cd "{project_root}"
python src/main.py
""")
        # Make it executable
        os.chmod(run_app_sh, 0o755)
    
    print("Activation scripts created.")

if __name__ == "__main__":
    create_local_environment()