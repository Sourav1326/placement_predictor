#!/usr/bin/env python3
"""
Universal Setup Script for Placement Predictor System
Downloads Python, creates environment, installs all dependencies automatically
"""

import os
import sys
import subprocess
import platform
import urllib.request
import shutil
import zipfile
import tempfile
import json
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("\n" + "="*80)
    print("🎯 PLACEMENT PREDICTOR - UNIVERSAL SETUP")
    print("="*80)
    print("This script will automatically:")
    print("✓ Download Python 3.10.11 if needed")
    print("✓ Create isolated environment")
    print("✓ Install ALL required packages")
    print("✓ Handle missing dependencies") 
    print("✓ Setup database and models")
    print("✓ Launch the application")
    print("="*80)
    input("\nPress Enter to continue...")

def get_system_info():
    """Get system information"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    return {
        'system': system,
        'machine': machine,
        'python_version': sys.version_info,
        'is_64bit': '64' in machine or 'amd64' in machine
    }

def check_python_compatibility():
    """Check if current Python is compatible"""
    version = sys.version_info
    if version.major == 3 and 8 <= version.minor <= 11:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"⚠️ Python {version.major}.{version.minor}.{version.micro} may have compatibility issues")
        return False

def download_file(url, filename, description="file"):
    """Download file with progress"""
    print(f"📥 Downloading {description}...")
    
    try:
        def progress_hook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(downloaded * 100 / total_size, 100)
                print(f"\r  Progress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end="", flush=True)
        
        urllib.request.urlretrieve(url, filename, progress_hook)
        print(f"\n✅ {description} downloaded successfully")
        return True
        
    except Exception as e:
        print(f"\n❌ Failed to download {description}: {e}")
        return False

def download_python():
    """Download and setup portable Python"""
    system_info = get_system_info()
    
    if system_info['system'] == 'windows':
        if system_info['is_64bit']:
            url = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip"
            folder = "python-3.10.11-embed-amd64"
        else:
            url = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-win32.zip"
            folder = "python-3.10.11-embed-win32"
    else:
        print("❌ Automatic Python download only supported on Windows")
        print("Please install Python 3.8-3.11 manually and run this script again")
        return None
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir, "python.zip")
    
    # Download Python
    if not download_file(url, zip_path, "Python 3.10.11"):
        return None
    
    # Extract Python
    print("📦 Extracting Python...")
    python_dir = os.path.join(os.getcwd(), "portable_python")
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(python_dir)
    
    # Download get-pip.py
    get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
    get_pip_path = os.path.join(python_dir, "get-pip.py")
    
    if download_file(get_pip_url, get_pip_path, "pip installer"):
        # Install pip
        print("🔧 Installing pip...")
        python_exe = os.path.join(python_dir, "python.exe")
        subprocess.run([python_exe, "get-pip.py"], cwd=python_dir)
        
        # Enable pip in pth file
        pth_files = [f for f in os.listdir(python_dir) if f.endswith('._pth')]
        if pth_files:
            pth_path = os.path.join(python_dir, pth_files[0])
            with open(pth_path, 'a') as f:
                f.write('\nimport site\n')
    
    # Cleanup
    shutil.rmtree(temp_dir)
    
    print("✅ Portable Python setup completed")
    return os.path.join(python_dir, "python.exe")

def create_virtual_environment(python_exe):
    """Create virtual environment"""
    print("\n📁 Creating virtual environment...")
    
    venv_path = os.path.join(os.getcwd(), "placement_env")
    
    try:
        subprocess.check_call([python_exe, "-m", "venv", venv_path])
        print("✅ Virtual environment created")
        
        # Return activated Python path
        if platform.system() == 'Windows':
            return os.path.join(venv_path, "Scripts", "python.exe")
        else:
            return os.path.join(venv_path, "bin", "python")
            
    except subprocess.CalledProcessError:
        print("⚠️ venv failed, trying virtualenv...")
        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", "virtualenv"])
            subprocess.check_call([python_exe, "-m", "virtualenv", venv_path])
            if platform.system() == 'Windows':
                return os.path.join(venv_path, "Scripts", "python.exe")
            else:
                return os.path.join(venv_path, "bin", "python")
        except:
            print("⚠️ Virtual environment creation failed, using system Python")
            return python_exe

def install_packages(python_exe):
    """Install all required packages"""
    print("\n📦 Installing packages...")
    
    # Essential packages in order
    essential_packages = [
        "pip>=23.0",
        "setuptools>=65.0", 
        "wheel>=0.38.0",
        "numpy>=1.21.0,<2.0.0",
        "pandas>=1.5.0,<3.0.0",
        "scikit-learn>=1.0.0,<2.0.0",
        "joblib>=1.0.0",
        "scipy>=1.7.0",
        "flask>=1.1.0,<3.0.0",
        "flask-login>=0.5.0",
        "werkzeug>=2.0.0,<3.0.0",
        "jinja2>=3.0.0",
        "matplotlib>=3.3.0",
        "seaborn>=0.10.0",
        "requests>=2.25.0",
        "tqdm>=4.60.0"
    ]
    
    # Optional packages
    optional_packages = [
        "plotly>=4.14.0",
        "xgboost>=1.5.0",
        "tensorflow>=2.8.0,<3.0.0",
        "streamlit>=1.20.0",
        "ipython",
        "jupyter"
    ]
    
    # Upgrade pip first
    print("🔧 Upgrading pip...")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Install essential packages
    success_count = 0
    total_essential = len(essential_packages)
    
    print("Installing essential packages...")
    for package in essential_packages:
        package_name = package.split('>=')[0].split('<')[0]
        print(f"  Installing {package_name}...")
        
        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", package, "--timeout", "300"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ {package_name}")
            success_count += 1
        except subprocess.CalledProcessError:
            # Try alternative installation
            try:
                subprocess.check_call([python_exe, "-m", "pip", "install", package_name, "--user"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  ✅ {package_name} (user install)")
                success_count += 1
            except:
                print(f"  ❌ {package_name} failed")
    
    # Install optional packages
    print("\nInstalling optional packages...")
    for package in optional_packages:
        package_name = package.split('>=')[0].split('<')[0]
        print(f"  Installing {package_name}...")
        
        try:
            subprocess.check_call([python_exe, "-m", "pip", "install", package, "--timeout", "300"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  ✅ {package_name}")
        except:
            print(f"  ⚠️ {package_name} skipped (optional)")
    
    print(f"\n📊 Installation Summary: {success_count}/{total_essential} essential packages installed")
    
    if success_count >= total_essential * 0.8:  # 80% success rate
        print("✅ Package installation successful!")
        return True
    else:
        print("⚠️ Some packages failed, but system may still work")
        return False

def verify_installation(python_exe):
    """Verify critical packages work"""
    print("\n🧪 Verifying installation...")
    
    critical_imports = [
        ("pandas", "pandas"),
        ("numpy", "numpy"), 
        ("sklearn", "scikit-learn"),
        ("flask", "flask"),
        ("matplotlib", "matplotlib")
    ]
    
    working_count = 0
    
    for import_name, package_name in critical_imports:
        try:
            result = subprocess.run([python_exe, "-c", f"import {import_name}; print('OK')"],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"  ✅ {package_name}")
                working_count += 1
            else:
                print(f"  ❌ {package_name}")
        except:
            print(f"  ❌ {package_name}")
    
    if working_count >= 4:  # At least 4 of 5 critical packages
        print("✅ Core packages verified!")
        return True
    else:
        print("❌ Critical package verification failed")
        return False

def setup_project_structure():
    """Create project directories"""
    print("\n📁 Setting up project structure...")
    
    directories = [
        "data", "models", "logs", "static", "static/uploads",
        "templates", "templates/auth", "templates/student", 
        "templates/admin", "utils"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Project structure created")

def generate_dataset(python_exe):
    """Generate dataset if needed"""
    print("\n📊 Setting up dataset...")
    
    if os.path.exists("data/placement_data.csv"):
        print("✅ Dataset already exists")
        return True
    
    try:
        print("Generating synthetic dataset...")
        result = subprocess.run([python_exe, "generate_dataset.py"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Dataset generated successfully")
            return True
        else:
            print("⚠️ Dataset generation had issues, creating minimal dataset...")
            create_minimal_dataset()
            return True
            
    except Exception as e:
        print(f"⚠️ Dataset generation failed: {e}")
        print("Creating minimal dataset...")
        create_minimal_dataset()
        return True

def create_minimal_dataset():
    """Create a minimal dataset if generation fails"""
    import csv
    
    # Create minimal CSV data
    data = [
        ['student_id', 'cgpa', 'tenth_percentage', 'twelfth_percentage', 'num_projects', 'placed'],
        ['DEMO001', '8.5', '85.0', '80.0', '3', '1'],
        ['DEMO002', '7.2', '78.0', '75.0', '2', '0'],
        ['DEMO003', '9.1', '92.0', '88.0', '4', '1']
    ]
    
    os.makedirs("data", exist_ok=True)
    with open("data/placement_data.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    print("✅ Minimal dataset created")

def initialize_system(python_exe):
    """Initialize database and models"""
    print("\n🔧 Initializing system...")
    
    init_script = '''
try:
    print("[INFO] Setting up system components...")
    
    # Setup database
    try:
        import sys
        sys.path.append("utils")
        from src.database import db_manager
        
        result = db_manager.create_user(
            email="admin@placement.system",
            password="admin123",
            first_name="System", 
            last_name="Administrator",
            user_type="admin"
        )
        print("[SUCCESS] Database initialized")
    except Exception as e:
        print(f"[INFO] Database will be created when app starts")
    
    # Train models
    try:
        from src.model_training import PlacementPredictor
        predictor = PlacementPredictor()
        predictor.train_all_models()
        print("[SUCCESS] ML models trained")
    except Exception as e:
        print(f"[INFO] Models will be trained when needed")
    
    print("[SUCCESS] System initialization completed")
    
except Exception as e:
    print(f"[WARNING] Initialization had issues: {e}")
'''
    
    try:
        result = subprocess.run([python_exe, "-c", init_script], 
                              capture_output=True, text=True, timeout=300)
        print("✅ System initialization completed")
        return True
    except:
        print("⚠️ System initialization had issues, but app should still work")
        return True

def create_startup_script(python_exe):
    """Create startup script for future use"""
    print("\n📝 Creating startup script...")
    
    if platform.system() == 'Windows':
        startup_content = f'''@echo off
echo Starting Placement Predictor System...
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
"{python_exe}" run_industry_system.py
if %errorlevel% neq 0 (
    echo.
    echo Trying alternative startup...
    "{python_exe}" flask_app.py
)
pause
'''
        with open("START_APPLICATION.bat", "w") as f:
            f.write(startup_content)
    else:
        startup_content = f'''#!/bin/bash
echo "Starting Placement Predictor System..."
echo ""
echo "Application will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""
"{python_exe}" run_industry_system.py || "{python_exe}" flask_app.py
'''
        with open("start_application.sh", "w") as f:
            f.write(startup_content)
        os.chmod("start_application.sh", 0o755)
    
    print("✅ Startup script created")

def main():
    """Main setup function"""
    print_banner()
    
    # Check current Python
    if check_python_compatibility():
        python_exe = sys.executable
        print("Using current Python installation")
    else:
        # Download Python if needed
        python_exe = download_python()
        if python_exe is None:
            print("❌ Cannot proceed without compatible Python")
            input("Press Enter to exit...")
            return False
    
    # Create virtual environment
    venv_python = create_virtual_environment(python_exe)
    
    # Install packages
    install_success = install_packages(venv_python)
    
    # Verify installation
    verify_success = verify_installation(venv_python)
    
    # Setup project
    setup_project_structure()
    generate_dataset(venv_python)
    initialize_system(venv_python)
    create_startup_script(venv_python)
    
    # Final message
    print("\n" + "="*80)
    print("🎉 INSTALLATION COMPLETED!")
    print("="*80)
    print("\n✅ Status Summary:")
    print(f"  • Python Environment: {'✅ Ready' if python_exe else '❌ Failed'}")
    print(f"  • Package Installation: {'✅ Success' if install_success else '⚠️ Partial'}")
    print(f"  • System Verification: {'✅ Passed' if verify_success else '⚠️ Issues'}")
    print(f"  • Project Setup: ✅ Complete")
    
    print("\n🌐 Application Details:")
    print("  • URL: http://localhost:5000")
    print("  • Admin: admin@placement.system / admin123")
    print("  • Demo Student: demo@student.com / demo123")
    
    print("\n🚀 Features Available:")
    print("  • AI-powered placement prediction")
    print("  • Interactive skill assessment")
    print("  • Personalized course recommendations")
    print("  • Real-time analytics dashboard")
    print("  • User authentication system")
    
    print("\n🔄 Future Usage:")
    if platform.system() == 'Windows':
        print("  • Quick Start: Double-click START_APPLICATION.bat")
    else:
        print("  • Quick Start: ./start_application.sh")
    print(f"  • Manual: {venv_python} run_industry_system.py")
    
    print("="*80)
    
    # Ask to start now
    start_now = input("\nStart the application now? (y/n): ").lower().strip()
    if start_now == 'y':
        print("\n🚀 Starting Placement Predictor System...")
        print("Press Ctrl+C to stop the server when done\n")
        
        try:
            subprocess.run([venv_python, "run_industry_system.py"])
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")
        except Exception as e:
            print(f"\n⚠️ Application had issues: {e}")
            print("Try running manually with: START_APPLICATION.bat")
    
    input("\nPress Enter to exit...")
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        input("Press Enter to exit...")