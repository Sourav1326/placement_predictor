#!/usr/bin/env python3
"""
Quick Setup Script for Placement Prediction System
Handles dependency installation with fallback options
"""

import subprocess
import sys
import importlib

def install_package(package):
    """Install a package using pip with error handling"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is already installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} is already installed")
        return True
    except ImportError:
        print(f"📦 {package_name} needs to be installed")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Placement Prediction System...")
    print("=" * 50)
    
    # Essential packages in order of dependency
    essential_packages = [
        ("numpy", "numpy"),
        ("pandas", "pandas"), 
        ("scikit-learn", "sklearn"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("flask", "flask"),
        ("joblib", "joblib")
    ]
    
    # Optional packages
    optional_packages = [
        ("xgboost", "xgboost"),
        ("plotly", "plotly"),
        ("tqdm", "tqdm")
    ]
    
    print("📋 Checking essential packages...")
    missing_essential = []
    
    for package, import_name in essential_packages:
        if not check_package(package, import_name):
            missing_essential.append(package)
    
    print("\n📋 Checking optional packages...")
    missing_optional = []
    
    for package, import_name in optional_packages:
        if not check_package(package, import_name):
            missing_optional.append(package)
    
    # Install missing packages
    if missing_essential:
        print(f"\n🔧 Installing essential packages: {', '.join(missing_essential)}")
        for package in missing_essential:
            print(f"Installing {package}...")
            if not install_package(package):
                print(f"⚠️ Could not install {package}. You may need to install it manually.")
    
    if missing_optional:
        print(f"\n🔧 Installing optional packages: {', '.join(missing_optional)}")
        for package in missing_optional:
            print(f"Installing {package}...")
            install_package(package)  # Don't fail on optional packages
    
    # Test the system
    print(f"\n🧪 Testing system components...")
    
    try:
        import pandas as pd
        import numpy as np
        from sklearn.ensemble import RandomForestClassifier
        import flask
        import matplotlib.pyplot as plt
        print("✅ Core components working!")
        
        # Test if our system files work
        import sys
        sys.path.append('utils')
        
        try:
            from src.model_training import PlacementPredictor
            print("✅ Model training module works!")
        except Exception as e:
            print(f"⚠️ Model training module issue: {e}")
        
        try:
            from src.utils.data_preprocessing import PlacementDataPreprocessor
            print("✅ Data preprocessing module works!")
        except Exception as e:
            print(f"⚠️ Data preprocessing module issue: {e}")
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        return False
    
    print(f"\n🎉 Setup complete!")
    print(f"📁 System ready to run!")
    print(f"\n🚀 Next steps:")
    print(f"1. Run the web app: python flask_app.py")
    print(f"2. Or test the system: python test_system.py")
    print(f"3. Access web interface at: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    main()