#!/usr/bin/env python3
"""
Simple test script to verify the placement prediction system
Run this to test the models before starting the web interface
"""

import sys
import os
sys.path.append('utils')

from src.model_training import PlacementPredictor
import pandas as pd

def test_system():
    """Test the complete placement prediction system"""
    print("🚀 Testing Placement Prediction System")
    print("=" * 50)
    
    # Initialize predictor
    predictor = PlacementPredictor()
    
    # Load models
    print("📋 Loading pre-trained models...")
    if predictor.load_models():
        print("✅ Models loaded successfully!")
        
        # Display model performance
        if predictor.model_scores:
            print("\n📊 Model Performance:")
            for model_name, scores in predictor.model_scores.items():
                print(f"  {model_name}: AUC = {scores['auc']:.4f}")
        
        # Test prediction with sample data
        print("\n🎯 Testing Prediction with Sample Student...")
        
        sample_student = {
            'student_id': 'TEST001',
            'branch': 'Computer Science',
            'cgpa': 8.5,
            'tenth_percentage': 92.0,
            'twelfth_percentage': 89.0,
            'num_projects': 4,
            'num_internships': 2,
            'num_certifications': 3,
            'programming_languages': 'Python, Java, C++, JavaScript',
            'leetcode_score': 1800,
            'codechef_rating': 1650,
            'communication_score': 8.0,
            'leadership_score': 7.5,
            'num_hackathons': 3,
            'club_participation': 2,
            'online_courses': 5
            # Note: Removed output variables (placed, salary_package, package_category)
        }
        
        result = predictor.predict_placement(sample_student)
        
        if result:
            print(f"✅ Prediction Result:")
            print(f"   Placement Probability: {result['probability']:.2%}")
            print(f"   Prediction: {'LIKELY TO BE PLACED' if result['prediction'] == 1 else 'MAY NOT BE PLACED'}")
            print(f"   Confidence: {result['placement_chance']}")
            
            # Test feature importance
            try:
                feature_impact = predictor.get_feature_importance_for_prediction(sample_student)
                if feature_impact:
                    print(f"\n📈 Top 5 Influencing Factors:")
                    for i, (feature, details) in enumerate(list(feature_impact.items())[:5], 1):
                        print(f"   {i}. {feature.replace('_', ' ').title()}: {details['importance']:.3f} importance")
            except Exception as e:
                print(f"   ⚠️ Feature importance not available: {e}")
        else:
            print("❌ Prediction failed!")
            
    else:
        print("❌ Failed to load models!")
        print("💡 Run 'python model_training.py' first to train the models.")
        return False
    
    # Test dataset loading
    print(f"\n📊 Testing Dataset...")
    if os.path.exists('data/placement_data.csv'):
        df = pd.read_csv('data/placement_data.csv')
        print(f"✅ Dataset loaded: {len(df)} students")
        print(f"   Placement rate: {df['placed'].mean():.1%}")
        print(f"   Average CGPA: {df['cgpa'].mean():.2f}")
        print(f"   Branches: {', '.join(df['branch'].unique())}")
    else:
        print("❌ Dataset not found!")
        return False
    
    print(f"\n🎉 System Test Complete!")
    print(f"✅ All components are working correctly!")
    print(f"\n🚀 Ready to launch the web application!")
    return True

def test_multiple_predictions():
    """Test with multiple student profiles"""
    print(f"\n🧪 Testing Multiple Student Profiles")
    print("=" * 50)
    
    predictor = PlacementPredictor()
    predictor.load_models()
    
    test_profiles = [
        {
            'name': 'High Performer',
            'data': {
                'student_id': 'HIGH001', 'branch': 'Computer Science', 'cgpa': 9.2,
                'tenth_percentage': 95.0, 'twelfth_percentage': 93.0, 'num_projects': 5,
                'num_internships': 3, 'num_certifications': 4, 
                'programming_languages': 'Python, Java, C++, JavaScript, React',
                'leetcode_score': 2200, 'codechef_rating': 1850, 'communication_score': 9.0,
                'leadership_score': 8.5, 'num_hackathons': 5, 'club_participation': 3,
                'online_courses': 8
            }
        },
        {
            'name': 'Average Student',
            'data': {
                'student_id': 'AVG001', 'branch': 'Mechanical', 'cgpa': 7.2,
                'tenth_percentage': 78.0, 'twelfth_percentage': 75.0, 'num_projects': 2,
                'num_internships': 1, 'num_certifications': 1,
                'programming_languages': 'Python, C++',
                'leetcode_score': 800, 'codechef_rating': 1200, 'communication_score': 6.0,
                'leadership_score': 5.5, 'num_hackathons': 1, 'club_participation': 1,
                'online_courses': 2
            }
        },
        {
            'name': 'Needs Improvement',
            'data': {
                'student_id': 'LOW001', 'branch': 'Civil', 'cgpa': 6.5,
                'tenth_percentage': 70.0, 'twelfth_percentage': 68.0, 'num_projects': 0,
                'num_internships': 0, 'num_certifications': 0,
                'programming_languages': 'C',
                'leetcode_score': 200, 'codechef_rating': 1100, 'communication_score': 5.0,
                'leadership_score': 4.0, 'num_hackathons': 0, 'club_participation': 0,
                'online_courses': 0
            }
        }
    ]
    
    for profile in test_profiles:
        result = predictor.predict_placement(profile['data'])
        if result:
            print(f"\n👤 {profile['name']}:")
            print(f"   Probability: {result['probability']:.1%}")
            print(f"   Status: {'✅ Likely Placed' if result['probability'] > 0.5 else '❌ Unlikely Placed'}")
        else:
            print(f"\n👤 {profile['name']}: ❌ Prediction failed")

if __name__ == "__main__":
    print("🎯 Placement Prediction System - Test Suite")
    print("=" * 60)
    
    success = test_system()
    
    if success:
        test_multiple_predictions()
        
        print(f"\n" + "=" * 60)
        print(f"🚀 Next Steps:")
        print(f"1. Install Streamlit: pip install streamlit plotly")
        print(f"2. Run the web app: streamlit run app.py")
        print(f"3. Open browser and test the interface")
        print(f"=" * 60)
    else:
        print(f"\n❌ System test failed. Please check the setup.")