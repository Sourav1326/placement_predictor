#!/usr/bin/env python3
"""
Verification and Launch Script for Placement Predictor System
Checks installation and provides clear instructions
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print verification header"""
    print("\n" + "="*70)
    print("🔍 PLACEMENT PREDICTOR - INSTALLATION VERIFICATION")
    print("="*70)
    print("Checking your installation and providing next steps...")
    print("="*70)

def check_python_environments():
    """Check available Python environments"""
    print("\n🐍 Python Environment Check:")
    
    environments = []
    
    # Current Python
    print(f"📍 Current Python: {sys.executable}")
    print(f"   Version: {sys.version}")
    environments.append(("current", sys.executable))
    
    # Virtual environment
    venv_python = os.path.join("placement_env", "Scripts", "python.exe")
    if platform.system() != 'Windows':
        venv_python = os.path.join("placement_env", "bin", "python")
    
    if os.path.exists(venv_python):
        print(f"📍 Virtual Environment: {venv_python}")
        try:
            result = subprocess.run([venv_python, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   Version: {result.stdout.strip()}")
                environments.append(("venv", venv_python))
        except:
            print("   ❌ Cannot execute")
    else:
        print("📍 Virtual Environment: ❌ Not found")
    
    # Portable Python
    portable_python = os.path.join("portable_python", "python.exe")
    if os.path.exists(portable_python):
        print(f"📍 Portable Python: {portable_python}")
        try:
            result = subprocess.run([portable_python, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   Version: {result.stdout.strip()}")
                environments.append(("portable", portable_python))
        except:
            print("   ❌ Cannot execute")
    else:
        print("📍 Portable Python: ❌ Not found")
    
    return environments

def check_packages_in_environment(python_exe, env_name):
    """Check if required packages are installed in an environment"""
    print(f"\n📦 Checking packages in {env_name} environment:")
    
    required_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('scikit-learn', 'sklearn'),
        ('flask', 'flask'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('xgboost', 'xgboost'),
        ('plotly', 'plotly')
    ]
    
    working_packages = []
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            result = subprocess.run([
                python_exe, "-c", f"import {import_name}; print('OK')"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"  ✅ {package_name}")
                working_packages.append(package_name)
            else:
                print(f"  ❌ {package_name}")
                missing_packages.append(package_name)
        except:
            print(f"  ❌ {package_name} (error)")
            missing_packages.append(package_name)
    
    print(f"\n📊 {env_name} Summary: {len(working_packages)}/{len(required_packages)} packages working")
    
    return len(working_packages), len(required_packages), missing_packages

def provide_solutions(environments):
    """Provide specific solutions based on environment analysis"""
    print("\n🔧 RECOMMENDED SOLUTIONS:")
    print("="*50)
    
    # Find best environment
    best_env = None
    best_score = 0
    
    for env_name, python_exe in environments:
        working, total, missing = check_packages_in_environment(python_exe, env_name)
        score = working / total
        
        if score > best_score:
            best_score = score
            best_env = (env_name, python_exe, missing)
    
    if best_env and best_score >= 0.8:  # 80% of packages working
        env_name, python_exe, missing = best_env
        print(f"✅ BEST OPTION: Use {env_name} environment")
        print(f"   Python: {python_exe}")
        
        if missing:
            print(f"   Missing packages: {', '.join(missing)}")
            print(f"\n🔧 Quick fix:")
            print(f'   "{python_exe}" -m pip install {" ".join(missing)}')
        
        print(f"\n🚀 Start application:")
        print(f'   "{python_exe}" run_industry_system.py')
        
        return python_exe, missing
    
    else:
        print("❌ No environment has sufficient packages installed")
        print("\n🔧 SOLUTIONS:")
        
        print("\n1. 🎯 Run Quick Fix Script:")
        print("   QUICK_FIX.bat")
        
        print("\n2. 🔄 Reinstall Everything:")
        print("   SETUP_AND_RUN.bat")
        
        print("\n3. 🐍 Use Conda (Recommended):")
        print("   CONDA_SETUP.bat")
        
        print("\n4. 🛠️ Manual Fix:")
        print("   FIX_DEPENDENCIES.py")
        
        return None, []

def test_application(python_exe):
    """Test if the application can start"""
    print(f"\n🧪 Testing application with {python_exe}...")
    
    try:
        # Quick import test
        result = subprocess.run([
            python_exe, "-c", 
"import sys; sys.path.append('src/utils'); from src.model_training import PlacementPredictor; print('✅ Application modules working')"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Application modules are working!")
            return True
        else:
            print(f"❌ Application test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Application test error: {e}")
        return False

def main():
    """Main verification function"""
    print_header()
    
    # Check Python environments
    environments = check_python_environments()
    
    if not environments:
        print("\n❌ No Python installations found!")
        print("Please run: SETUP_AND_RUN.bat")
        input("\nPress Enter to exit...")
        return
    
    # Find best solution
    best_python, missing_packages = provide_solutions(environments)
    
    if best_python:
        # Test application
        if test_application(best_python):
            print("\n🎉 SYSTEM READY!")
            print("="*30)
            
            # Offer to start now
            start_now = input("\nStart the application now? (y/n): ").lower().strip()
            if start_now == 'y':
                print("\n🚀 Starting Placement Predictor System...")
                print("Press Ctrl+C to stop the server\n")
                
                try:
                    subprocess.run([best_python, "run_industry_system.py"])
                except KeyboardInterrupt:
                    print("\n👋 Application stopped by user")
                except Exception as e:
                    print(f"\n❌ Application error: {e}")
            else:
                print(f"\n📝 To start later, run:")
                print(f'   "{best_python}" run_industry_system.py')
                print("   Or double-click: START_APPLICATION.bat")
        else:
            print("\n⚠️ Application test failed")
            print("Please run one of the fix scripts mentioned above")
    
    else:
        print("\n📖 For detailed troubleshooting, check:")
        print("   • INSTALL_SOLUTIONS.md")
        print("   • COMPLETE_SETUP_GUIDE.md")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Verification cancelled")
    except Exception as e:
        print(f"\n❌ Verification error: {e}")
        input("Press Enter to exit...")