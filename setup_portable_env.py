import os
import subprocess
import sys
import venv
from pathlib import Path

def create_portable_environment():
    """Create a portable Python environment with all dependencies installed from local cache."""
    
    project_root = Path(__file__).parent.absolute()
    venv_path = project_root / "portable_env"
    requirements_file = project_root / "requirements.txt"
    cache_dir = project_root / "requirements_cache"
    
    print(f"Project root: {project_root}")
    print(f"Creating portable environment at: {venv_path}")
    
    # Create virtual environment
    if not venv_path.exists():
        print("Creating virtual environment...")
        venv.create(venv_path, with_pip=True)
        print("Virtual environment created successfully!")
    else:
        print("Virtual environment already exists.")
    
    # Determine the path to pip in the virtual environment
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip.exe"
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        pip_path = venv_path / "bin" / "pip"
        python_path = venv_path / "bin" / "python"
    
    # Try to upgrade pip first (but don't fail if it doesn't work)
    print("Upgrading pip...")
    try:
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
    except subprocess.CalledProcessError:
        print("Warning: Could not upgrade pip, continuing with existing version...")
    
    # Install all packages from local cache
    print("Installing packages from local cache...")
    if cache_dir.exists() and any(cache_dir.iterdir()):
        # Install from local cache directory
        cmd = [
            str(pip_path), 
            "install", 
            "--find-links", str(cache_dir),
            "--no-index",  # Don't connect to PyPI
            "-r", str(requirements_file)
        ]
        result = subprocess.run(cmd)
        
        if result.returncode != 0:
            print("Failed to install from cache. Trying alternative method...")
            # Alternative method: install each wheel file individually
            wheel_files = list(cache_dir.glob("*.whl"))
            for wheel_file in wheel_files:
                print(f"Installing {wheel_file.name}...")
                subprocess.run([str(pip_path), "install", str(wheel_file)], check=True)
    else:
        print("Cache directory not found or empty. Please run the download script first.")
        return False
    
    print("\nPortable environment setup complete!")
    print(f"Environment location: {venv_path}")
    print("\nTo activate the environment:")
    if sys.platform == "win32":
        print(f"  {venv_path / 'Scripts' / 'activate.bat'}")
        print(f"\nTo run the application:")
        print(f"  {venv_path / 'Scripts' / 'python.exe'} src/main.py")
    else:
        print(f"  source {venv_path / 'bin' / 'activate'}")
        print(f"\nTo run the application:")
        print(f"  {venv_path / 'bin' / 'python'} src/main.py")
    
    return True

def create_activation_scripts():
    """Create convenient activation scripts."""
    project_root = Path(__file__).parent.absolute()
    venv_path = project_root / "portable_env"
    
    if sys.platform == "win32":
        # Create Windows activation script
        activate_bat = venv_path / "Scripts" / "activate.bat"
        custom_activate_bat = project_root / "activate_portable.bat"
        
        if activate_bat.exists():
            with open(custom_activate_bat, "w") as f:
                f.write("@echo off\n")
                f.write(f"cd /d \"{project_root}\"\n")
                f.write(f"call \"{activate_bat}\"\n")
                f.write("@echo Portable environment activated. Run 'python src/main.py' to start the application.\n")
            print(f"Created {custom_activate_bat}")
        
        # Create Windows run script
        run_bat = project_root / "run_app_portable.bat"
        python_exe = venv_path / "Scripts" / "python.exe"
        if activate_bat.exists():
            with open(run_bat, "w") as f:
                f.write("@echo off\n")
                f.write(f"cd /d \"{project_root}\"\n")
                f.write(f"\"{python_exe}\" src/main.py\n")
                f.write("pause\n")
            print(f"Created {run_bat}")

if __name__ == "__main__":
    success = create_portable_environment()
    if success:
        create_activation_scripts()
        print("\nSetup completed successfully!")
    else:
        print("\nSetup failed!")
        sys.exit(1)