#!/usr/bin/env python3
"""
Conda Environment Setup Script for Placement Prediction System
Provides step-by-step instructions for conda setup
"""

import os
import sys
import subprocess

def check_conda():
    """Check if conda is available"""
    try:
        result = subprocess.run(['conda', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Conda detected: {result.stdout.strip()}")
            return True
        else:
            print("❌ Conda not found in PATH")
            return False
    except FileNotFoundError:
        print("❌ Conda not installed or not in PATH")
        return False

def main():
    """Main setup function"""
    print("🐍 Conda Environment Setup for Placement Prediction System")
    print("=" * 60)
    
    if not check_conda():
        print("\n📋 Please install Anaconda/Miniconda first:")
        print("   - Download from: https://www.anaconda.com/products/distribution")
        print("   - Or Miniconda: https://docs.conda.io/en/latest/miniconda.html")
        return False
    
    print(f"\n📋 CONDA SETUP INSTRUCTIONS")
    print("-" * 40)
    print("1. Open Anaconda Prompt (or your terminal)")
    print("2. Navigate to project directory:")
    print(f"   cd \"{os.getcwd()}\"")
    print("\n3. Create environment from file:")
    print("   conda env create -f environment.yml")
    print("\n4. Activate the environment:")
    print("   conda activate placement-predictor")
    print("\n5. Verify installation:")
    print("   python test_system.py")
    print("\n6. Run the application:")
    print("   python flask_app.py")
    
    print(f"\n🔧 ALTERNATIVE MANUAL SETUP")
    print("-" * 40)
    print("If environment.yml doesn't work, create manually:")
    print("conda create -n placement-predictor python=3.10")
    print("conda activate placement-predictor")
    print("conda install pandas numpy scikit-learn matplotlib seaborn flask joblib")
    print("conda install -c conda-forge xgboost plotly")
    print("pip install streamlit shap")
    
    print(f"\n🎯 QUICK START COMMANDS")
    print("-" * 40)
    print("# Create and activate environment")
    print("conda env create -f environment.yml")
    print("conda activate placement-predictor")
    print("")
    print("# Test the system")
    print("python test_system.py")
    print("")
    print("# Run web application")
    print("python flask_app.py")
    print("")
    print("# Access at: http://localhost:5000")
    
    print(f"\n📦 ENVIRONMENT MANAGEMENT")
    print("-" * 40)
    print("# List environments")
    print("conda env list")
    print("")
    print("# Activate environment")
    print("conda activate placement-predictor")
    print("")
    print("# Deactivate environment")
    print("conda deactivate")
    print("")
    print("# Remove environment (if needed)")
    print("conda env remove -n placement-predictor")
    
    print(f"\n✅ READY FOR CONDA SETUP!")
    print("Follow the instructions above in Anaconda Prompt")

if __name__ == "__main__":
    main()