"""
Quick installation script for Placement Prediction System
Installs only missing packages and runs system tests
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run command and return success status"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_and_install_package(package_name, install_cmd=None):
    """Check if package exists, install if missing"""
    try:
        __import__(package_name)
        print(f"✅ {package_name} - Already installed")
        return True
    except ImportError:
        print(f"⚠️ {package_name} - Missing, installing...")
        if install_cmd:
            return run_command(install_cmd, f"Installing {package_name}")
        else:
            return run_command(f"pip install {package_name}", f"Installing {package_name}")

def main():
    print("🎯 QUICK SETUP - PLACEMENT PREDICTION SYSTEM")
    print("=" * 50)
    
    # Check Python version
    print(f"🐍 Python Version: {sys.version}")
    
    # Essential packages to check/install
    packages = [
        ("pandas", "pip install pandas"),
        ("numpy", "pip install numpy"),
        ("sklearn", "pip install scikit-learn"),
        ("flask", "pip install flask"),
        ("matplotlib", "pip install matplotlib"),
        ("joblib", "pip install joblib"),
    ]
    
    # Optional packages (won't stop if they fail)
    optional_packages = [
        ("tensorflow", "pip install tensorflow"),
        ("xgboost", "pip install xgboost"),
        ("seaborn", "pip install seaborn"),
        ("plotly", "pip install plotly"),
    ]
    
    print("\n📦 Installing Essential Packages...")
    essential_failed = []
    for package, cmd in packages:
        if not check_and_install_package(package, cmd):
            essential_failed.append(package)
    
    print("\n📦 Installing Optional Packages...")
    for package, cmd in optional_packages:
        check_and_install_package(package, cmd)
    
    if essential_failed:
        print(f"\n❌ Essential packages failed: {essential_failed}")
        print("Try running: pip install pandas numpy scikit-learn flask matplotlib joblib")
        return False
    
    print("\n🧪 Testing System...")
    
    # Test basic imports
    try:
        import pandas as pd
        import numpy as np
        import sklearn
        import flask
        print("✅ All essential packages working!")
        
        # Check if dataset exists
        if os.path.exists('data/placement_data.csv'):
            print("✅ Dataset found")
        else:
            print("⚠️ Dataset missing - will generate on first run")
        
        print("\n🎉 SETUP COMPLETE!")
        print("\n🚀 TO RUN THE PROJECT:")
        print("1. python quick_start.py          # Test system")
        print("2. python app.py                  # Run Streamlit app")
        print("3. python flask_app.py            # Run Flask app")
        print("4. python run_industry_system.py  # Run full system")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🔧 MANUAL INSTALLATION:")
        print("pip install pandas numpy scikit-learn flask matplotlib joblib")
        print("pip install tensorflow xgboost seaborn plotly  # Optional")
    
    input("\nPress Enter to continue...")