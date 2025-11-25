#!/usr/bin/env python3
"""
Dependency Fix Script for Placement Predictor System
Handles common installation issues, especially with scikit-learn
"""

import os
import sys
import subprocess
import importlib
import platform

def print_header():
    """Print fix script header"""
    print("🔧" + "="*70)
    print("   PLACEMENT PREDICTOR - DEPENDENCY FIX SCRIPT")
    print("="*73)
    print("This script will diagnose and fix common installation issues")
    print("="*73)

def check_package_detailed(package_name, import_name=None):
    """Check package with detailed diagnostics"""
    if import_name is None:
        import_name = package_name.replace('-', '_')
    
    print(f"\n🔍 Checking {package_name}...")
    
    try:
        # Try to import
        if import_name == 'sklearn':
            import sklearn
            print(f"  ✅ Import successful")
        elif import_name == 'flask':
            import flask
            print(f"  ✅ Import successful")
        elif import_name == 'pandas':
            import pandas
            print(f"  ✅ Import successful")
        elif import_name == 'numpy':
            import numpy
            print(f"  ✅ Import successful")
        else:
            module = importlib.import_module(import_name)
            print(f"  ✅ Import successful")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"  ⚠️ Import issue: {e}")
        return False

def fix_scikit_learn():
    """Special fix for scikit-learn installation issues"""
    print("\n🔧 Fixing scikit-learn installation...")
    
    methods = [
        {
            "name": "Standard pip install",
            "commands": [[sys.executable, "-m", "pip", "install", "scikit-learn", "--upgrade"]]
        },
        {
            "name": "Force reinstall",
            "commands": [
                [sys.executable, "-m", "pip", "uninstall", "scikit-learn", "-y"],
                [sys.executable, "-m", "pip", "install", "scikit-learn", "--no-cache-dir"]
            ]
        },
        {
            "name": "Install with dependencies",
            "commands": [
                [sys.executable, "-m", "pip", "install", "numpy", "scipy"],
                [sys.executable, "-m", "pip", "install", "scikit-learn", "--no-deps"],
                [sys.executable, "-m", "pip", "install", "joblib", "threadpoolctl"]
            ]
        },
        {
            "name": "User install",
            "commands": [[sys.executable, "-m", "pip", "install", "scikit-learn", "--user", "--upgrade"]]
        }
    ]
    
    for method in methods:
        print(f"\n  Trying: {method['name']}")
        try:
            for cmd in method['commands']:
                print(f"    Running: {' '.join(cmd)}")
                subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Test if it works now
            try:
                import sklearn
                print(f"  ✅ {method['name']} successful!")
                return True
            except ImportError:
                continue
                
        except subprocess.CalledProcessError:
            print(f"  ❌ {method['name']} failed")
            continue
    
    print("  ❌ All scikit-learn installation methods failed")
    return False

def install_missing_package(package_name, import_name=None):
    """Install a missing package with multiple methods"""
    print(f"\n🔧 Installing {package_name}...")
    
    # Special handling for problematic packages
    if package_name == 'scikit-learn':
        return fix_scikit_learn()
    
    methods = [
        [sys.executable, "-m", "pip", "install", package_name],
        [sys.executable, "-m", "pip", "install", package_name, "--user"],
        [sys.executable, "-m", "pip", "install", package_name, "--no-cache-dir"],
        [sys.executable, "-m", "pip", "install", package_name, "--upgrade", "--force-reinstall"]
    ]
    
    for i, method in enumerate(methods, 1):
        try:
            print(f"  Method {i}: {' '.join(method)}")
            subprocess.check_call(method, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Verify installation
            if check_package_detailed(package_name, import_name):
                print(f"  ✅ {package_name} installed successfully!")
                return True
                
        except subprocess.CalledProcessError:
            print(f"  ❌ Method {i} failed")
            continue
    
    print(f"  ❌ All installation methods failed for {package_name}")
    return False

def suggest_conda_installation():
    """Suggest using conda for installation"""
    print("\n💡 CONDA INSTALLATION SUGGESTED")
    print("="*50)
    print("For better compatibility, consider using Conda:")
    print()
    print("1. Install Anaconda/Miniconda if not already installed")
    print("2. Create environment:")
    print("   conda create -n placement-predictor python=3.10")
    print("3. Activate environment:")
    print("   conda activate placement-predictor")
    print("4. Install packages:")
    print("   conda install pandas numpy scikit-learn flask matplotlib seaborn")
    print("   conda install -c conda-forge xgboost plotly")
    print("   pip install flask-login tensorflow streamlit")
    print("5. Run the application:")
    print("   python run_industry_system.py")
    print()
    print("Or use our conda setup script: CONDA_SETUP.bat")

def create_minimal_requirements():
    """Create a minimal requirements file with only essential packages"""
    minimal_requirements = """# Minimal requirements for Placement Predictor
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.0.0
flask>=1.1.0
matplotlib>=3.3.0
joblib>=1.0.0
"""
    
    with open('requirements_emergency.txt', 'w') as f:
        f.write(minimal_requirements)
    
    print("\n📝 Created requirements_emergency.txt with minimal packages")
    print("Try: pip install -r requirements_emergency.txt")

def main():
    """Main fix function"""
    print_header()
    
    # Essential packages to check
    essential_packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("scikit-learn", "sklearn"),
        ("flask", "flask"),
        ("matplotlib", "matplotlib"),
        ("joblib", "joblib")
    ]
    
    print("\n🔍 DIAGNOSING CURRENT INSTALLATION")
    print("="*50)
    
    missing_packages = []
    working_packages = []
    
    for package, import_name in essential_packages:
        if check_package_detailed(package, import_name):
            working_packages.append(package)
        else:
            missing_packages.append((package, import_name))
    
    print(f"\n📊 DIAGNOSIS SUMMARY")
    print("="*30)
    print(f"✅ Working packages: {len(working_packages)}")
    print(f"❌ Missing packages: {len(missing_packages)}")
    
    if not missing_packages:
        print("\n🎉 All essential packages are working!")
        print("Your system should be ready to run.")
        print("\nTry running: python run_industry_system.py")
        return True
    
    print(f"\n🔧 FIXING MISSING PACKAGES")
    print("="*40)
    
    fixed_count = 0
    for package, import_name in missing_packages:
        if install_missing_package(package, import_name):
            fixed_count += 1
    
    print(f"\n📈 FIX SUMMARY")
    print("="*20)
    print(f"✅ Fixed packages: {fixed_count}")
    print(f"❌ Still missing: {len(missing_packages) - fixed_count}")
    
    if fixed_count == len(missing_packages):
        print("\n🎉 ALL PACKAGES FIXED!")
        print("Your system should now be ready.")
        print("\nTry running: python run_industry_system.py")
        return True
    
    elif fixed_count > 0:
        print("\n⚠️ PARTIAL SUCCESS")
        print("Some packages were fixed, but others still have issues.")
        suggest_conda_installation()
        create_minimal_requirements()
        return False
    
    else:
        print("\n❌ UNABLE TO FIX PACKAGES")
        print("Standard pip installation methods failed.")
        suggest_conda_installation()
        create_minimal_requirements()
        
        print("\n🆘 ALTERNATIVE SOLUTIONS:")
        print("1. Try the conda setup: CONDA_SETUP.bat")
        print("2. Use virtual environment:")
        print("   python -m venv venv")
        print("   venv\\Scripts\\activate  # Windows")
        print("   pip install -r requirements_emergency.txt")
        print("3. Try different Python version (3.8, 3.9, 3.10)")
        print("4. Check if you have admin/write permissions")
        
        return False

if __name__ == "__main__":
    try:
        success = main()
        
        if success:
            # Try to run a quick test
            print("\n🧪 Running quick system test...")
            try:
                subprocess.run([sys.executable, 'QUICK_START.py'], check=True)
            except:
                print("System test had issues, but packages are installed")
        
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\n👋 Fix script cancelled")
    except Exception as e:
        print(f"\n❌ Fix script error: {e}")
        input("Press Enter to exit...")