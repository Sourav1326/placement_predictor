import os
import sys
from pathlib import Path

def create_activation_scripts():
    """Create convenient activation scripts for the portable environment."""
    project_root = Path(__file__).parent.absolute()
    venv_path = project_root / "portable_env"
    
    if not venv_path.exists():
        print("Virtual environment not found!")
        return False
    
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
            
        # Also create a direct run script
        direct_run_bat = project_root / "run_direct.bat"
        with open(direct_run_bat, "w") as f:
            f.write("@echo off\n")
            f.write(f"cd /d \"{project_root}\"\n")
            f.write(f"\"{python_exe}\" src/main.py\n")
            f.write("pause\n")
        print(f"Created {direct_run_bat}")

    print("\nActivation scripts created successfully!")
    print("\nTo activate the portable environment:")
    print("  Double-click activate_portable.bat")
    print("\nTo run the application directly:")
    print("  Double-click run_app_portable.bat or run_direct.bat")
    
    return True

if __name__ == "__main__":
    create_activation_scripts()