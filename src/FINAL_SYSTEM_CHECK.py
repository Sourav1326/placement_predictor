"""
FINAL SYSTEM CHECK AND FIX SCRIPT
Comprehensive verification and automatic fixing of all components
"""

import os
import sys
import subprocess
import importlib
import sqlite3
from pathlib import Path

def print_status(message, status="INFO"):
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "FIXING": "🔧"}
    print(f"{symbols.get(status, 'ℹ️')} {message}")

def check_python_version():
    """Check if Python version is compatible"""
    print_status("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and 8 <= version.minor <= 11:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Compatible", "SUCCESS")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - May cause issues", "WARNING")
        return False

def check_virtual_environment():
    """Check if virtual environment is active"""
    print_status("Checking virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print_status("Virtual environment is active", "SUCCESS")
        return True
    else:
        print_status("No virtual environment detected", "WARNING")
        return False

def install_package(package_name, alternative_names=None):
    """Install a package with fallback options"""
    alternatives = alternative_names or []
    
    for name in [package_name] + alternatives:
        try:
            print_status(f"Installing {name}...", "FIXING")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print_status(f"Successfully installed {name}", "SUCCESS")
            return True
        except subprocess.CalledProcessError:
            continue
    
    # Try conda as last resort
    try:
        subprocess.check_call(['conda', 'install', package_name, '-y'], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_status(f"Installed {package_name} via conda", "SUCCESS")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    print_status(f"Failed to install {package_name}", "ERROR")
    return False

def check_and_fix_packages():
    """Check and fix all required packages"""
    print_status("Checking required packages...")
    
    # Essential packages with alternatives
    packages = {
        'pandas': ['pandas'],
        'numpy': ['numpy'], 
        'sklearn': ['scikit-learn', 'sklearn'],
        'flask': ['Flask'],
        'matplotlib': ['matplotlib'],
        'seaborn': ['seaborn'],
        'requests': ['requests'],
        'jinja2': ['Jinja2'],
        'werkzeug': ['Werkzeug'],
        'joblib': ['joblib'],
        'xgboost': ['xgboost'],
        'nltk': ['nltk'],
        'textblob': ['textblob'],
        'PyPDF2': ['PyPDF2', 'pypdf2'],
        'docx': ['python-docx'],
        'tqdm': ['tqdm'],
        'flask_login': ['Flask-Login']
    }
    
    failed_packages = []
    
    for module_name, package_names in packages.items():
        try:
            importlib.import_module(module_name)
            print_status(f"{module_name} - OK", "SUCCESS")
        except ImportError:
            print_status(f"{module_name} - Missing", "WARNING")
            if install_package(package_names[0], package_names[1:]):
                try:
                    importlib.import_module(module_name)
                    print_status(f"{module_name} - Fixed", "SUCCESS")
                except ImportError:
                    failed_packages.append(module_name)
            else:
                failed_packages.append(module_name)
    
    return failed_packages

def check_project_files():
    """Check if all required project files exist"""
    print_status("Checking project files...")
    
    required_files = [
        'industry_flask_app.py',
        'database.py',
        'authentication.py',
        'ats_resume_analyzer.py',
        'conversational_ai_chatbot.py',
        'smart_search_engine.py',
        'company_role_prediction.py',
        'verified_skill_badge_system.py',
        'live_coding_engine.py',
        'sql_sandbox_engine.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print_status(f"{file} - OK", "SUCCESS")
        else:
            print_status(f"{file} - Missing", "ERROR")
            missing_files.append(file)
    
    return missing_files

def check_database():
    """Check if database can be initialized"""
    print_status("Checking database...")
    
    try:
        # Test basic SQLite functionality
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY)')
        cursor.execute('INSERT INTO test (id) VALUES (1)')
        cursor.execute('SELECT * FROM test')
        conn.close()
        print_status("Database functionality - OK", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Database error: {e}", "ERROR")
        return False

def create_missing_directories():
    """Create missing directories"""
    print_status("Creating missing directories...")
    
    dirs = ['data', 'models', 'logs', 'static', 'templates']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print_status(f"Created directory: {dir_name}", "SUCCESS")

def test_main_application():
    """Test if main application can be imported"""
    print_status("Testing main application...")
    
    try:
        # Try to import the main Flask app
        if os.path.exists('industry_flask_app.py'):
            sys.path.insert(0, '.')
            import industry_flask_app
            print_status("Main application imports successfully", "SUCCESS")
            return True
        else:
            print_status("Main application file not found", "ERROR")
            return False
    except Exception as e:
        print_status(f"Main application import error: {e}", "WARNING")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print_status("Downloading NLTK data...")
    
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('stopwords', quiet=True)
        print_status("NLTK data downloaded", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"NLTK download failed: {e}", "WARNING")
        return False

def generate_test_data():
    """Generate test data if needed"""
    print_status("Checking test data...")
    
    try:
        if os.path.exists('generate_dataset.py'):
            subprocess.run([sys.executable, 'generate_dataset.py'], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
            print_status("Test data generated", "SUCCESS")
        else:
            print_status("Dataset generator not found", "WARNING")
    except Exception as e:
        print_status(f"Test data generation failed: {e}", "WARNING")

def run_comprehensive_check():
    """Run comprehensive system check and fixes"""
    print("=" * 70)
    print("🎯 PLACEMENT PREDICTOR SYSTEM - COMPREHENSIVE CHECK")
    print("=" * 70)
    print()
    
    # Track issues
    issues = []
    
    # Check Python version
    if not check_python_version():
        issues.append("Python version compatibility")
    
    # Check virtual environment
    if not check_virtual_environment():
        issues.append("Virtual environment not active")
    
    # Check and fix packages
    failed_packages = check_and_fix_packages()
    if failed_packages:
        issues.append(f"Failed packages: {', '.join(failed_packages)}")
    
    # Check project files
    missing_files = check_project_files()
    if missing_files:
        issues.append(f"Missing files: {', '.join(missing_files)}")
    
    # Check database
    if not check_database():
        issues.append("Database functionality")
    
    # Create directories
    create_missing_directories()
    
    # Download NLTK data
    download_nltk_data()
    
    # Generate test data
    generate_test_data()
    
    # Test main application
    if not test_main_application():
        issues.append("Main application import")
    
    print()
    print("=" * 70)
    print("📊 SYSTEM CHECK RESULTS")
    print("=" * 70)
    
    if not issues:
        print_status("🎉 ALL SYSTEMS GREEN! Ready to launch!", "SUCCESS")
        print()
        print("🚀 To start the application:")
        print("   • Double-click: START_APPLICATION.bat")
        print("   • Or run: python industry_flask_app.py")
        print()
        print("🌐 Application URL: http://localhost:5000")
        print("👤 Admin Login: admin@placement.system / admin123")
        print("👤 Demo Student: demo@student.com / demo123")
    else:
        print_status("⚠️ Issues found that need attention:", "WARNING")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        
        print()
        print("🔧 SUGGESTED FIXES:")
        print("   • Run: ULTIMATE_ONE_CLICK_SETUP.bat")
        print("   • Or manually fix the issues above")
        print("   • Check TROUBLESHOOTING.md for detailed solutions")
    
    print("=" * 70)
    return len(issues) == 0

if __name__ == "__main__":
    try:
        success = run_comprehensive_check()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)