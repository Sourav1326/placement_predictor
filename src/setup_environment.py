"""
Complete Environment Setup for Placement Prediction System
Handles conda environment creation and package installation with error recovery
"""

import os
import sys
import subprocess
import time

def run_command(command, description, critical=True):
    """Run a command with proper error handling"""
    print(f"\n🔄 {description}...")
    print(f"Command: {command}")
    
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        else:  # Unix/Linux/Mac
            result = subprocess.run(command.split(), capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print("Output:", result.stdout[-500:])  # Last 500 chars
            return True
        else:
            print(f"❌ {description} failed")
            print("Error:", result.stderr)
            if not critical:
                print("⚠️ Continuing despite error (non-critical)")
                return False
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out (5 minutes)")
        return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_conda():
    """Check if conda is available"""
    print("🔍 Checking conda installation...")
    result = run_command("conda --version", "Conda version check", critical=False)
    if not result:
        print("❌ Conda not found. Please install Anaconda or Miniconda first.")
        print("Download from: https://www.anaconda.com/products/distribution")
        return False
    return True

def create_environment():
    """Create conda environment from environment.yml"""
    print("\n📦 Creating conda environment...")
    
    # Remove existing environment if it exists
    print("🗑️ Removing existing environment (if any)...")
    run_command("conda env remove -n placement-predictor -y", "Remove existing environment", critical=False)
    
    # Create new environment
    if run_command("conda env create -f environment.yml", "Create conda environment"):
        print("✅ Environment created successfully!")
        return True
    else:
        print("❌ Environment creation failed")
        return False

def install_additional_packages():
    """Install additional packages that might have failed"""
    print("\n🔧 Installing additional packages...")
    
    # Activate environment and install packages
    commands = [
        "conda activate placement-predictor && pip install --upgrade pip",
        "conda activate placement-predictor && pip install xgboost==1.7.6",
        "conda activate placement-predictor && pip install tensorflow==2.13.0",
        "conda activate placement-predictor && pip install flask-login==0.6.3",
        "conda activate placement-predictor && pip install streamlit==1.28.1",
        "conda activate placement-predictor && pip install shap==0.42.1"
    ]
    
    for cmd in commands:
        run_command(cmd, f"Installing package: {cmd.split()[-1]}", critical=False)

def verify_installation():
    """Verify that all packages are installed correctly"""
    print("\n🧪 Verifying installation...")
    
    test_script = '''
import sys
print(f"Python version: {sys.version}")

packages_to_test = [
    "pandas", "numpy", "sklearn", "flask", "matplotlib", 
    "seaborn", "plotly", "joblib", "tensorflow", "xgboost"
]

failed_imports = []
for package in packages_to_test:
    try:
        if package == "sklearn":
            import sklearn
            print(f"✅ scikit-learn: {sklearn.__version__}")
        else:
            module = __import__(package)
            version = getattr(module, "__version__", "unknown")
            print(f"✅ {package}: {version}")
    except ImportError as e:
        print(f"❌ {package}: {e}")
        failed_imports.append(package)

if failed_imports:
    print(f"\\n❌ Failed imports: {failed_imports}")
    sys.exit(1)
else:
    print("\\n🎉 All packages imported successfully!")
'''
    
    # Write test script
    with open("test_imports.py", "w") as f:
        f.write(test_script)
    
    # Run test
    result = run_command("conda activate placement-predictor && python test_imports.py", "Package verification")
    
    # Clean up
    if os.path.exists("test_imports.py"):
        os.remove("test_imports.py")
    
    return result

def create_activation_script():
    """Create scripts to easily activate the environment"""
    
    # Windows batch file
    batch_content = '''@echo off
echo 🚀 Activating Placement Prediction Environment...
call conda activate placement-predictor
echo ✅ Environment activated!
echo 💡 Available commands:
echo   - python app.py          (Run Streamlit app)
echo   - python flask_app.py    (Run Flask app)
echo   - python quick_start.py  (Quick system test)
echo.
cmd /k
'''
    
    with open("activate_env.bat", "w") as f:
        f.write(batch_content)
    
    # PowerShell script
    ps_content = '''Write-Host "🚀 Activating Placement Prediction Environment..." -ForegroundColor Green
conda activate placement-predictor
Write-Host "✅ Environment activated!" -ForegroundColor Green
Write-Host "💡 Available commands:" -ForegroundColor Yellow
Write-Host "  - python app.py          (Run Streamlit app)" -ForegroundColor Cyan
Write-Host "  - python flask_app.py    (Run Flask app)" -ForegroundColor Cyan
Write-Host "  - python quick_start.py  (Quick system test)" -ForegroundColor Cyan
'''
    
    with open("activate_env.ps1", "w") as f:
        f.write(ps_content)
    
    print("✅ Activation scripts created:")
    print("   - activate_env.bat (Windows Command Prompt)")
    print("   - activate_env.ps1 (PowerShell)")

def main():
    """Main setup function"""
    print("🎯" + "="*60)
    print("   PLACEMENT PREDICTION SYSTEM - ENVIRONMENT SETUP")
    print("="*63)
    
    # Check conda
    if not check_conda():
        return False
    
    # Create environment
    if not create_environment():
        print("❌ Environment creation failed. Trying alternative method...")
        
        # Try manual installation
        print("🔄 Attempting manual package installation...")
        commands = [
            "conda create -n placement-predictor python=3.10 -y",
            "conda activate placement-predictor && conda install pandas=2.0.3 numpy=1.24.4 scikit-learn=1.3.0 -y",
            "conda activate placement-predictor && conda install flask=2.3.3 matplotlib=3.7.2 seaborn=0.12.2 -y",
            "conda activate placement-predictor && pip install tensorflow==2.13.0 xgboost==1.7.6"
        ]
        
        for cmd in commands:
            if not run_command(cmd, f"Manual install: {cmd}", critical=False):
                print("⚠️ Some packages may not be installed correctly")
    
    # Install additional packages
    install_additional_packages()
    
    # Verify installation
    if verify_installation():
        print("\n🎉 SETUP COMPLETED SUCCESSFULLY!")
        
        # Create activation scripts
        create_activation_script()
        
        print("\n📋 NEXT STEPS:")
        print("1. 🔄 Activate environment:")
        print("   Windows: activate_env.bat")
        print("   PowerShell: ./activate_env.ps1")
        print("   Manual: conda activate placement-predictor")
        print("")
        print("2. 🚀 Test the system:")
        print("   python quick_start.py")
        print("")
        print("3. 🌐 Run the application:")
        print("   python run_industry_system.py")
        
        return True
    else:
        print("\n❌ SETUP FAILED!")
        print("Some packages could not be installed or verified.")
        print("Please check the error messages above and try manual installation.")
        
        print("\n🔧 MANUAL TROUBLESHOOTING:")
        print("1. Try updating conda: conda update conda")
        print("2. Clear conda cache: conda clean --all")
        print("3. Install packages individually:")
        print("   conda install pandas numpy scikit-learn")
        print("   pip install tensorflow xgboost")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)