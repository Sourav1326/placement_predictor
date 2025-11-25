#!/usr/bin/env python3
"""
Simple One-Command Launcher for Placement Predictor System
Handles dependency checking and automatic installation
"""

import os
import sys
import subprocess
import importlib.util

def check_and_install_package(package_name, import_name=None):
    """Check if package exists, install if not"""
    if import_name is None:
        import_name = package_name
    
    try:
        # Try to import the package
        if import_name == 'sklearn':
            import sklearn
        else:
            __import__(import_name)
        return True
    except ImportError:
        print(f"Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to install {package_name}")
            return False

def quick_setup():
    """Quick setup and run"""
    print("🚀 Placement Predictor - Quick Start")
    print("="*50)
    
    # Essential packages
    essential = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        ("flask", "flask"),
        ("matplotlib", "matplotlib"),
    ]
    
    print("Checking essential packages...")
    for package, import_name in essential:
        if not check_and_install_package(package, import_name):
            print(f"❌ Failed to install {package}")
            return False
    
    # Create basic directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    # Generate data if needed
    if not os.path.exists('data/placement_data.csv'):
        print("Generating sample data...")
        try:
            subprocess.run([sys.executable, 'generate_dataset.py'], check=True)
        except:
            print("Warning: Could not generate dataset")
    
    # Run the system
    print("\n✅ Starting Placement Predictor System...")
    print("Access at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    try:
        # Try industry system first, fallback to basic Flask app
        if os.path.exists('run_industry_system.py'):
            subprocess.run([sys.executable, 'run_industry_system.py'])
        elif os.path.exists('flask_app.py'):
            subprocess.run([sys.executable, 'flask_app.py'])
        else:
            print("❌ No main application file found")
            return False
    except KeyboardInterrupt:
        print("\n👋 System stopped")
    
    return True

if __name__ == "__main__":
    quick_setup()
