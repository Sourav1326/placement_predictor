"""
System Status Checker - Diagnose what's working and what's not
"""

import sys
import os
from datetime import datetime

def print_status(message, status="INFO"):
    symbols = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}
    print(f"{symbols.get(status, 'ℹ️')} {message}")

def check_python_environment():
    """Check Python version and environment"""
    print("=" * 60)
    print("🐍 PYTHON ENVIRONMENT")
    print("=" * 60)
    
    print_status(f"Python Version: {sys.version}", "SUCCESS")
    print_status(f"Python Executable: {sys.executable}", "INFO")
    print_status(f"Virtual Environment: {'Yes' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'No'}", "INFO")
    print()

def check_core_packages():
    """Check essential packages"""
    print("📦 CORE PACKAGES")
    print("=" * 60)
    
    packages = {
        'pandas': 'Data processing',
        'numpy': 'Numerical computing', 
        'sklearn': 'Machine learning',
        'flask': 'Web framework',
        'sqlite3': 'Database (built-in)',
        'matplotlib': 'Visualization',
        'seaborn': 'Statistical visualization',
        'requests': 'HTTP requests'
    }
    
    for package, description in packages.items():
        try:
            __import__(package)
            if package == 'sklearn':
                import sklearn
                print_status(f"{package} ({sklearn.__version__}) - {description}", "SUCCESS")
            elif package == 'pandas':
                import pandas
                print_status(f"{package} ({pandas.__version__}) - {description}", "SUCCESS")
            elif package == 'numpy':
                import numpy
                print_status(f"{package} ({numpy.__version__}) - {description}", "SUCCESS")
            else:
                print_status(f"{package} - {description}", "SUCCESS")
        except ImportError as e:
            print_status(f"{package} - {description} - MISSING", "ERROR")
    print()

def check_ml_packages():
    """Check ML-specific packages"""
    print("🤖 MACHINE LEARNING PACKAGES")
    print("=" * 60)
    
    ml_packages = {
        'xgboost': 'Gradient boosting',
        'joblib': 'Model persistence',
        'tensorflow': 'Deep learning (optional)',
        'keras': 'Deep learning API (optional)'
    }
    
    for package, description in ml_packages.items():
        try:
            module = __import__(package)
            if hasattr(module, '__version__'):
                print_status(f"{package} ({module.__version__}) - {description}", "SUCCESS")
            else:
                print_status(f"{package} - {description}", "SUCCESS")
        except ImportError:
            if package in ['tensorflow', 'keras']:
                print_status(f"{package} - {description} - NOT INSTALLED (optional)", "WARNING")
            else:
                print_status(f"{package} - {description} - MISSING", "ERROR")
    print()

def check_nlp_packages():
    """Check NLP packages"""
    print("💬 NLP PACKAGES")
    print("=" * 60)
    
    nlp_packages = {
        'nltk': 'Natural language toolkit',
        'textblob': 'Text processing',
        'spacy': 'Advanced NLP (optional)'
    }
    
    for package, description in nlp_packages.items():
        try:
            __import__(package)
            print_status(f"{package} - {description}", "SUCCESS")
        except ImportError:
            if package == 'spacy':
                print_status(f"{package} - {description} - NOT INSTALLED (optional)", "WARNING") 
            else:
                print_status(f"{package} - {description} - MISSING", "ERROR")
    print()

def check_document_packages():
    """Check document processing packages"""
    print("📄 DOCUMENT PROCESSING")
    print("=" * 60)
    
    doc_packages = {
        'PyPDF2': 'PDF processing',
        'docx': 'Word document processing'
    }
    
    for package, description in doc_packages.items():
        try:
            if package == 'docx':
                import docx
            else:
                __import__(package)
            print_status(f"{package} - {description}", "SUCCESS")
        except ImportError:
            print_status(f"{package} - {description} - MISSING", "ERROR")
    print()

def check_project_files():
    """Check if project files exist"""
    print("📁 PROJECT FILES")
    print("=" * 60)
    
    critical_files = [
        ('industry_flask_app.py', 'Main Flask application'),
        ('database.py', 'Database management'),
        ('authentication.py', 'User authentication'),
        ('model_training.py', 'Traditional ML models'),
        ('requirements.txt', 'Package requirements')
    ]
    
    optional_files = [
        ('deep_learning_model.py', 'Deep learning models'),
        ('ats_resume_analyzer.py', 'ATS resume analysis'),
        ('conversational_ai_chatbot.py', 'AI chatbot'),
        ('smart_search_engine.py', 'Smart search'),
        ('company_role_prediction.py', 'Company predictions'),
        ('verified_skill_badge_system.py', 'Skill verification')
    ]
    
    for filename, description in critical_files:
        if os.path.exists(filename):
            print_status(f"{filename} - {description}", "SUCCESS")
        else:
            print_status(f"{filename} - {description} - MISSING", "ERROR")
    
    print_status("Optional advanced features:", "INFO")
    for filename, description in optional_files:
        if os.path.exists(filename):
            print_status(f"  {filename} - {description}", "SUCCESS")
        else:
            print_status(f"  {filename} - {description} - MISSING", "WARNING")
    print()

def check_database():
    """Check database connectivity"""
    print("🗄️ DATABASE")
    print("=" * 60)
    
    try:
        import sqlite3
        # Test database creation
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY)')
        cursor.execute('INSERT INTO test (id) VALUES (1)')
        cursor.execute('SELECT * FROM test')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print_status("SQLite functionality", "SUCCESS")
        
        # Check if project database exists
        if os.path.exists('data/placement_system.db'):
            print_status("Project database exists", "SUCCESS")
        else:
            print_status("Project database will be created on first run", "INFO")
            
    except Exception as e:
        print_status(f"Database error: {e}", "ERROR")
    print()

def check_application_startup():
    """Test if main application can be imported"""
    print("🚀 APPLICATION STARTUP TEST")
    print("=" * 60)
    
    try:
        # Add current directory to path
        sys.path.insert(0, '.')
        
        # Test database module
        try:
            from src.database import db_manager
            print_status("Database module", "SUCCESS")
        except Exception as e:
            print_status(f"Database module: {e}", "ERROR")
        
        # Test authentication
        try:
            from src.authentication import init_auth
            print_status("Authentication module", "SUCCESS")
        except Exception as e:
            print_status(f"Authentication module: {e}", "ERROR")
        
        # Test ML models
        try:
            from src.model_training import PlacementPredictor
            print_status("Traditional ML models", "SUCCESS")
        except Exception as e:
            print_status(f"Traditional ML models: {e}", "ERROR")
        
        # Test deep learning (optional)
        try:
            from deep_learning_model import DeepPlacementPredictor
            print_status("Deep learning models", "SUCCESS")
        except Exception as e:
            print_status("Deep learning models: Not available (using traditional ML)", "WARNING")
        
        # Test Flask app import
        try:
            import industry_flask_app
            print_status("Flask application", "SUCCESS")
        except Exception as e:
            print_status(f"Flask application: {e}", "ERROR")
            
    except Exception as e:
        print_status(f"Application startup test failed: {e}", "ERROR")
    print()

def generate_summary():
    """Generate system status summary"""
    print("📊 SYSTEM STATUS SUMMARY")
    print("=" * 60)
    
    # Quick compatibility check
    critical_working = True
    
    try:
        import pandas, numpy, sklearn, flask, sqlite3
        print_status("Core functionality: READY", "SUCCESS")
    except ImportError:
        print_status("Core functionality: ISSUES DETECTED", "ERROR")
        critical_working = False
    
    try:
        import xgboost, joblib
        print_status("Traditional ML: READY", "SUCCESS")
    except ImportError:
        print_status("Traditional ML: PARTIAL", "WARNING")
    
    try:
        import tensorflow
        print_status("Deep Learning: AVAILABLE", "SUCCESS")
    except ImportError:
        print_status("Deep Learning: NOT AVAILABLE (using traditional ML)", "WARNING")
    
    try:
        import nltk, textblob
        print_status("NLP Features: READY", "SUCCESS")
    except ImportError:
        print_status("NLP Features: ISSUES DETECTED", "WARNING")
    
    print()
    if critical_working:
        print_status("🎉 SYSTEM IS READY TO RUN!", "SUCCESS")
        print_status("Run: python industry_flask_app.py", "INFO")
        print_status("URL: http://localhost:5000", "INFO")
    else:
        print_status("⚠️ SYSTEM NEEDS ATTENTION", "WARNING") 
        print_status("Run: FIX_DEPENDENCIES_COMPREHENSIVE.bat", "INFO")

def main():
    """Main diagnostic function"""
    print(f"🔍 PLACEMENT PREDICTOR SYSTEM - STATUS CHECK")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    check_python_environment()
    check_core_packages()
    check_ml_packages()
    check_nlp_packages()
    check_document_packages()
    check_project_files()
    check_database()
    check_application_startup()
    generate_summary()
    
    print("\n" + "=" * 60)
    print("✅ Diagnostic complete!")

if __name__ == "__main__":
    main()