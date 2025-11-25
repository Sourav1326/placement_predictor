"""
Quick verification that traditional ML models work correctly after the fix
"""

import os
import sys
sys.path.append('utils')

from src.model_training import PlacementPredictor

def test_traditional_models():
    print("🔍 Testing Traditional ML Models")
    print("=" * 40)
    
    # Initialize predictor
    predictor = PlacementPredictor()
    
    # Load models
    print("📦 Loading pre-trained models...")
    if predictor.load_models():
        print("✅ Models loaded successfully!")
        
        # Test prediction with sample data (without output variables)
        print("\n🧪 Testing prediction...")
        sample_student = {
            'student_id': 'VERIFY001',
            'branch': 'Computer Science',
            'cgpa': 8.5,
            'tenth_percentage': 92.0,
            'twelfth_percentage': 89.0,
            'num_projects': 4,
            'num_internships': 2,
            'num_certifications': 3,
            'programming_languages': 'Python, Java, C++',
            'leetcode_score': 1800,
            'codechef_rating': 1650,
            'communication_score': 8.0,
            'leadership_score': 7.5,
            'num_hackathons': 3,
            'club_participation': 2,
            'online_courses': 5
        }
        
        result = predictor.predict_placement(sample_student)
        
        if result:
            print(f"✅ Traditional ML models working correctly!")
            print(f"   Probability: {result['probability']:.1%}")
            print(f"   Prediction: {'Likely Placed' if result['prediction'] == 1 else 'May Not Be Placed'}")
            return True
        else:
            print(f"❌ Traditional ML prediction failed!")
            return False
    else:
        print("❌ Failed to load models. Please train models first:")
        print("   Run: python model_training.py")
        return False

if __name__ == "__main__":
    success = test_traditional_models()
    if success:
        print(f"\n🎉 Traditional ML models are working correctly!")
    else:
        print(f"\n💔 Traditional ML models need attention.")