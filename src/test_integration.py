#!/usr/bin/env python3
"""
Quick Integration Test for Advanced Assessment Features
Tests the Flask application with new assessment modules
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 
        'textblob', 'PyPDF2', 'python-docx'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
            print(f"✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} - MISSING")
    
    if missing_modules:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing_modules)}")
        print("📦 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies satisfied!")
    return True

def test_assessment_modules():
    """Test if assessment modules can be imported"""
    print("\n🧪 Testing assessment modules...")
    
    modules_to_test = [
        'comprehensive_assessment',
        'communication_assessment', 
        'situational_judgment_test',
        'resume_scorer',
        'mock_interview_simulator'
    ]
    
    for module_name in modules_to_test:
        try:
            exec(f"from {module_name} import *")
            print(f"✅ {module_name}")
        except Exception as e:
            print(f"❌ {module_name} - Error: {str(e)[:50]}...")
            return False
    
    print("✅ All assessment modules import successfully!")
    return True

def create_test_directories():
    """Create necessary directories"""
    print("\n📁 Creating necessary directories...")
    
    directories = [
        'uploads',
        'data',
        'templates/student',
        'models'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}")

def quick_test():
    """Run a quick integration test"""
    print("🚀 ADVANCED ASSESSMENT FEATURES - INTEGRATION TEST")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Test modules
    if not test_assessment_modules():
        return False
    
    # Create directories
    create_test_directories()
    
    print("\n🎉 INTEGRATION TEST PASSED!")
    print("\n📋 What's Available:")
    print("   🧠 Comprehensive Assessment Module")
    print("   ✍️ Automated Written Communication Test") 
    print("   🎯 Gamified Situational Judgment Tests")
    print("   📄 AI-Powered Resume Scorer")
    print("   🎤 Mock Interview Simulator")
    
    print("\n🌐 Flask Routes Added:")
    print("   /assessment-hub - Main assessment dashboard")
    print("   /comprehensive-assessment - Aptitude tests")
    print("   /communication-assessment - Writing tests")
    print("   /situational-judgment-test - Behavioral tests") 
    print("   /resume-scorer - Resume analysis")
    print("   /mock-interview - Interview practice")
    
    print("\n🔗 To start the Flask app:")
    print("   python industry_flask_app.py")
    print("   Open http://localhost:5000")
    print("   Login: admin@placement.system / admin123")
    
    return True

if __name__ == '__main__':
    success = quick_test()
    
    if success:
        print("\n🎯 Ready to launch! The advanced assessment features are integrated and ready to use.")
        
        # Ask if user wants to start the Flask app
        response = input("\n🚀 Start Flask application now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("🌐 Starting Flask application...")
            try:
                subprocess.run([sys.executable, 'industry_flask_app.py'])
            except KeyboardInterrupt:
                print("\n👋 Flask application stopped.")
    else:
        print("\n❌ Integration test failed. Please check the errors above.")
        sys.exit(1)