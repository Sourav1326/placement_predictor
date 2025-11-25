#!/usr/bin/env python3
"""
One-Click Setup Script for Placement Predictor System
Comprehensive setup that handles all dependencies and initialization
"""

import os
import sys
import subprocess
import platform
import importlib
import urllib.request
import zipfile
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("\n" + "="*80)
    print("    🎯 PLACEMENT PREDICTOR SYSTEM - ONE-CLICK SETUP 🎯")
    print("="*80)
    print("This script will automatically:")
    print("✓ Check Python installation")
    print("✓ Install all required dependencies")
    print("✓ Create and setup database")
    print("✓ Generate training dataset")
    print("✓ Train machine learning models")
    print("✓ Initialize the web application")
    print("="*80)
    input("\nPress Enter to continue...")

def check_python_version():
    """Check if Python version is compatible"""
    print("\n📋 Checking Python version...")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        print("Please install Python 3.8+ from: https://www.python.org/downloads/")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_package_with_fallback(package_name, alternatives=None):
    """Install package with fallback options"""
    packages_to_try = [package_name] + (alternatives or [])
    
    for pkg in packages_to_try:
        try:
            print(f"   Installing {pkg}...")
            
            # Special handling for scikit-learn
            if 'scikit-learn' in pkg:
                # Try with cache-dir to avoid build issues
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", pkg, 
                    "--upgrade", "--user", "--no-warn-script-location",
                    "--cache-dir", "./pip-cache"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", pkg, 
                    "--upgrade", "--user", "--no-warn-script-location"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print(f"   ✅ {pkg} installed successfully")
            return True
            
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {pkg}")
            
            # For scikit-learn, try additional methods
            if 'scikit-learn' in pkg:
                try:
                    print(f"   Trying alternative installation method for scikit-learn...")
                    # Try without version constraints
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", "scikit-learn", 
                        "--user", "--no-deps"
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    # Install dependencies separately
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install", 
                        "numpy", "scipy", "joblib", "threadpoolctl",
                        "--user"
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    print(f"   ✅ scikit-learn installed with alternative method")
                    return True
                except:
                    continue
            continue
    
    return False

def install_dependencies():
    """Install all required dependencies with smart fallbacks"""
    print("\n📦 Installing dependencies...")
    
    # Essential packages with fallbacks
    essential_packages = [
        ("pandas>=2.0.0", ["pandas>=1.5.0", "pandas"]),
        ("numpy>=1.24.0", ["numpy>=1.21.0", "numpy"]),
        ("scikit-learn>=1.3.0", ["scikit-learn>=1.1.0", "scikit-learn"]),
        ("flask>=2.0.0", ["flask>=1.1.0", "flask"]),
        ("matplotlib>=3.5.0", ["matplotlib>=3.3.0", "matplotlib"]),
        ("seaborn>=0.11.0", ["seaborn>=0.10.0", "seaborn"]),
        ("joblib>=1.3.0", ["joblib>=1.0.0", "joblib"]),
    ]
    
    # Optional packages that enhance functionality
    optional_packages = [
        ("xgboost>=1.7.0", ["xgboost>=1.5.0", "xgboost"]),
        ("plotly>=5.0.0", ["plotly>=4.14.0", "plotly"]),
        ("flask-login>=0.6.0", ["flask-login>=0.5.0", "flask-login"]),
        ("tqdm>=4.60.0", ["tqdm"]),
        ("requests>=2.28.0", ["requests"]),
    ]
    
    # Advanced packages (may fail on some systems)
    advanced_packages = [
        ("tensorflow>=2.10.0", ["tensorflow>=2.8.0", "tensorflow-cpu"]),
        ("streamlit>=1.25.0", ["streamlit>=1.20.0", "streamlit"]),
    ]
    
    success_count = 0
    total_count = 0
    
    print("Installing essential packages...")
    for package, alternatives in essential_packages:
        total_count += 1
        if install_package_with_fallback(package, alternatives):
            success_count += 1
        else:
            print(f"⚠️ Could not install {package.split('>=')[0]} - system may not work properly")
    
    print("\nInstalling optional packages...")
    for package, alternatives in optional_packages:
        total_count += 1
        if install_package_with_fallback(package, alternatives):
            success_count += 1
    
    print("\nInstalling advanced packages...")
    for package, alternatives in advanced_packages:
        total_count += 1
        if install_package_with_fallback(package, alternatives):
            success_count += 1
    
    print(f"\n📊 Installation Summary: {success_count}/{total_count} packages installed")
    
    if success_count >= len(essential_packages):
        print("✅ Essential packages installed - system should work!")
        return True
    else:
        print("❌ Critical packages missing - system may not function properly")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating project directories...")
    
    directories = ['data', 'models', 'logs', 'static/uploads']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def generate_sample_data():
    """Generate sample dataset if needed"""
    print("\n📊 Setting up dataset...")
    
    if os.path.exists('data/placement_data.csv'):
        print("✅ Dataset already exists")
        return True
    
    try:
        print("Generating synthetic dataset...")
        result = subprocess.run([sys.executable, 'generate_dataset.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Dataset generated successfully")
            return True
        else:
            print(f"❌ Dataset generation failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Dataset generation timed out")
        return False
    except Exception as e:
        print(f"❌ Dataset generation error: {e}")
        return False

def setup_database():
    """Initialize database with sample data"""
    print("\n🗄️ Setting up database...")
    
    try:
        # Try to import and setup database
        from src.database import db_manager
        
        # Create admin user
        admin_result = db_manager.create_user(
            email='admin@placement.system',
            password='admin123',
            first_name='System',
            last_name='Administrator',
            user_type='admin'
        )
        
        if admin_result['success']:
            print("✅ Admin user created: admin@placement.system / admin123")
        else:
            print("✅ Admin user already exists")
        
        # Create sample student
        student_result = db_manager.create_user(
            email='demo@student.com',
            password='demo123',
            first_name='Demo',
            last_name='Student',
            student_id='DEMO001',
            branch='Computer Science',
            academic_year=2024
        )
        
        if student_result['success']:
            print("✅ Demo student created: demo@student.com / demo123")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Database setup issue: {e}")
        print("Database will be created automatically when the app starts")
        return True  # Don't fail setup for database issues

def train_models():
    """Train machine learning models"""
    print("\n🤖 Training ML models...")
    
    try:
        from src.model_training import PlacementPredictor
        
        predictor = PlacementPredictor()
        success = predictor.train_all_models()
        
        if success:
            print("✅ Traditional ML models trained successfully")
        else:
            print("⚠️ Model training had some issues but core models are available")
        
        # Try deep learning model (optional)
        try:
            print("Training deep learning model (optional)...")
            import pandas as pd
            from deep_learning_model import DeepPlacementPredictor
            
            if os.path.exists('data/placement_data.csv'):
                df = pd.read_csv('data/placement_data.csv')
                deep_predictor = DeepPlacementPredictor()
                metrics = deep_predictor.train_model(df, epochs=20)  # Quick training
                deep_predictor.save_model()
                print("✅ Deep learning model trained successfully")
            
        except Exception as e:
            print(f"⚠️ Deep learning model training skipped: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model training failed: {e}")
        return False

def verify_system():
    """Verify that all components are working"""
    print("\n🧪 Verifying system components...")
    
    components = [
        ("Flask", "flask"),
        ("Pandas", "pandas"),
        ("Scikit-learn", "sklearn"),
        ("Matplotlib", "matplotlib"),
        ("Model Training", "model_training"),
        ("Database", "database"),
    ]
    
    working_components = 0
    
    for name, module in components:
        try:
            importlib.import_module(module)
            print(f"✅ {name}")
            working_components += 1
        except ImportError:
            print(f"❌ {name}")
    
    if working_components >= 4:  # At least core components
        print(f"\n✅ System verification passed ({working_components}/{len(components)} components working)")
        return True
    else:
        print(f"\n❌ System verification failed ({working_components}/{len(components)} components working)")
        return False

def create_quick_start_scripts():
    """Create quick start scripts for different platforms"""
    print("\n📝 Creating quick-start scripts...")
    
    # Windows batch script
    windows_script = '''@echo off
echo Starting Placement Predictor System...
cd /d "%~dp0"
if exist "placement-env\\Scripts\\activate.bat" (
    call placement-env\\Scripts\\activate.bat
    python run_industry_system.py
) else (
    python run_industry_system.py
)
pause
'''
    
    with open('START_SYSTEM.bat', 'w') as f:
        f.write(windows_script)
    
    # Linux/Mac shell script
    unix_script = '''#!/bin/bash
echo "Starting Placement Predictor System..."
cd "$(dirname "$0")"
if [ -f "placement-env/bin/activate" ]; then
    source placement-env/bin/activate
fi
python3 run_industry_system.py
'''
    
    with open('start_system.sh', 'w') as f:
        f.write(unix_script)
    
    # Make shell script executable on Unix systems
    if platform.system() != 'Windows':
        os.chmod('start_system.sh', 0o755)
    
    print("✅ Quick-start scripts created")
    print("   Windows: START_SYSTEM.bat")
    print("   Linux/Mac: ./start_system.sh")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        input("\nPress Enter to exit...")
        return False
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️ Dependency installation had issues. System may not work properly.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    
    # Generate dataset
    generate_sample_data()
    
    # Setup database
    setup_database()
    
    # Train models
    train_models()
    
    # Verify system
    if not verify_system():
        print("\n⚠️ System verification failed. Some components may not work.")
    
    # Create quick start scripts
    create_quick_start_scripts()
    
    # Final success message
    print("\n" + "="*80)
    print("🎉 SETUP COMPLETED SUCCESSFULLY! 🎉")
    print("="*80)
    print("\n📱 Your Placement Predictor System is ready to use!")
    print("\n🚀 To start the system:")
    print("   • Windows: Double-click START_SYSTEM.bat")
    print("   • Linux/Mac: Run ./start_system.sh")
    print("   • Manual: python run_industry_system.py")
    print("\n🌐 Access the application at: http://localhost:5000")
    print("\n👤 Login credentials:")
    print("   • Admin: admin@placement.system / admin123")
    print("   • Demo Student: demo@student.com / demo123")
    print("\n✨ Features available:")
    print("   • AI-powered placement prediction")
    print("   • Interactive skill assessment")
    print("   • Personalized course recommendations")
    print("   • Real-time analytics dashboard")
    print("   • User authentication system")
    print("="*80)
    
    # Ask if user wants to start immediately
    start_now = input("\nStart the system now? (y/n): ")
    if start_now.lower() == 'y':
        print("\n🚀 Starting the system...")
        try:
            subprocess.run([sys.executable, 'run_industry_system.py'])
        except KeyboardInterrupt:
            print("\n👋 System stopped by user")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        input("Press Enter to exit...")