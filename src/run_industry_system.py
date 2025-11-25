"""
Industry-Ready Placement Prediction System Setup and Runner
Complete setup script with database initialization and model training
"""

import os
import sys
import subprocess
import pandas as pd
from datetime import datetime

# Change to script directory to ensure correct working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Working directory set to: {os.getcwd()}")

def print_banner():
    """Print system banner"""
    print("🎯" + "="*70)
    print("        INDUSTRY-READY PLACEMENT PREDICTION SYSTEM")
    print("="*73)
    print("🚀 Complete ML-powered placement prediction platform")
    print("🔐 User authentication and session management")
    print("📊 Real-time analytics dashboard")
    print("🧠 Deep learning models for enhanced accuracy")
    print("📱 Mobile-responsive web interface")
    print("🎓 Skill assessment and course recommendations")
    print("="*73)

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'scikit-learn', 'xgboost', 
        'flask', 'flask_login', 'matplotlib', 'seaborn', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'flask_login':
                __import__('flask_login')
            elif package == 'scikit-learn':
                __import__('sklearn')  # scikit-learn imports as sklearn
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Please install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def setup_database():
    """Initialize database and create sample data"""
    print("\n🗄️ Setting up database...")
    
    try:
        from src.database import db_manager
        
        # Database is automatically initialized in db_manager
        print("✅ Database schema created successfully")
        
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
            print("⚠️ Admin user already exists")
        
        # Create sample student users
        sample_students = [
            {
                'email': 'student1@example.com',
                'password': 'student123',
                'first_name': 'John',
                'last_name': 'Doe',
                'student_id': 'CS2021001',
                'branch': 'Computer Science',
                'academic_year': 2021
            },
            {
                'email': 'student2@example.com', 
                'password': 'student123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'student_id': 'IT2021002',
                'branch': 'Information Technology',
                'academic_year': 2021
            }
        ]
        
        for student_data in sample_students:
            result = db_manager.create_user(**student_data)
            if result['success']:
                # Update student profile with sample data
                profile_data = {
                    'cgpa': 8.5,
                    'tenth_percentage': 90.0,
                    'twelfth_percentage': 85.0,
                    'num_projects': 3,
                    'num_internships': 1,
                    'num_certifications': 2,
                    'programming_languages': 'Python, Java, JavaScript',
                    'leetcode_score': 1500,
                    'codechef_rating': 1600,
                    'communication_score': 8.0,
                    'leadership_score': 7.5,
                    'num_hackathons': 2,
                    'club_participation': 1,
                    'online_courses': 4
                }
                db_manager.update_student_profile(result['user_id'], profile_data)
                print(f"✅ Sample student created: {student_data['email']} / student123")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def setup_data_and_models():
    """Generate dataset and train models"""
    print("\n🤖 Setting up ML models...")
    
    try:
        # Generate dataset if it doesn't exist
        if not os.path.exists('data/placement_data.csv'):
            print("📊 Generating synthetic dataset...")
            subprocess.run([sys.executable, 'generate_dataset.py'], check=True)
            print("✅ Dataset generated successfully")
        else:
            print("✅ Dataset already exists")
        
        # Train traditional ML models
        print("🧠 Training traditional ML models...")
        from src.model_training import PlacementPredictor
        
        predictor = PlacementPredictor()
        success = predictor.train_all_models()
        
        if success:
            print("✅ Traditional ML models trained successfully")
        else:
            print("⚠️ Traditional ML model training had issues")
        
        # Try training deep learning model
        try:
            print("🧠 Training deep learning model...")
            from deep_learning_model import DeepPlacementPredictor
            
            df = pd.read_csv('data/placement_data.csv')
            deep_predictor = DeepPlacementPredictor()
            metrics = deep_predictor.train_model(df, epochs=50)  # Reduced epochs for faster training
            deep_predictor.save_model()
            print("✅ Deep learning model trained successfully")
            print(f"   Validation AUC: {metrics['val_auc']:.4f}")
            
        except Exception as e:
            print(f"⚠️ Deep learning model training failed: {e}")
            print("   Traditional models will be used instead")
        
        return True
        
    except Exception as e:
        print(f"❌ Model setup failed: {e}")
        return False

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting Industry-Ready Flask Application...")
    print("="*50)
    print("🌐 Application will be available at: http://localhost:5000")
    print("👤 Admin Login: admin@placement.system / admin123")
    print("👤 Student Login: student1@example.com / student123")
    print("📱 Features:")
    print("   • User Authentication & Session Management")
    print("   • AI-Powered Placement Prediction")
    print("   • Interactive Skill Assessment")
    print("   • Personalized Course Recommendations")
    print("   • Real-time Analytics Dashboard")
    print("   • Deep Learning Model Integration")
    print("="*50)
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        # Import and run the Flask app
        from industry_flask_app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Application failed to start: {e}")

def main():
    """Main setup and run function"""
    print_banner()
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed due to missing dependencies")
        print("Please run: pip install -r requirements.txt")
        return
    
    # Step 2: Setup database
    if not setup_database():
        print("\n❌ Setup failed due to database issues")
        return
    
    # Step 3: Setup data and models
    if not setup_data_and_models():
        print("\n❌ Setup failed due to model training issues")
        return
    
    print("\n✅ SETUP COMPLETE!")
    print("🎉 Industry-Ready Placement Prediction System is ready!")
    
    # Step 4: Start application
    input("\nPress Enter to start the web application...")
    start_application()

if __name__ == "__main__":
    main()