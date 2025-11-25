"""
Fix for Placement Prediction Error: 'Unknown' package_category issue
This script retrains the deep learning model with corrected feature handling
"""

import os
import pandas as pd
from deep_learning_model import DeepPlacementPredictor

def main():
    print("🔧 Fixing Placement Prediction Error")
    print("=" * 50)
    
    # Check if dataset exists
    if not os.path.exists('data/placement_data.csv'):
        print("❌ Dataset not found. Please run generate_dataset.py first.")
        return False
    
    # Load dataset
    df = pd.read_csv('data/placement_data.csv')
    print(f"📊 Loaded dataset with {len(df)} samples")
    
    # Print package categories in the dataset
    print(f"\n📋 Package categories in training data:")
    print(df['package_category'].value_counts())
    
    # Initialize corrected deep learning predictor
    print(f"\n🧠 Initializing corrected deep learning model...")
    deep_predictor = DeepPlacementPredictor()
    
    try:
        # Train model with corrected feature handling
        print(f"\n🚀 Training deep learning model (this may take a few minutes)...")
        metrics = deep_predictor.train_model(df, epochs=50)  # Reduced epochs for faster training
        
        # Save the corrected model
        deep_predictor.save_model()
        
        print(f"\n✅ Model training completed successfully!")
        print(f"📈 Validation AUC: {metrics['val_auc']:.4f}")
        print(f"📈 Validation Accuracy: {metrics['val_accuracy']:.4f}")
        
        # Test prediction with sample data (without output variables)
        print(f"\n🧪 Testing corrected prediction...")
        test_student = {
            'student_id': 'TEST_FIX',
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
        
        result = deep_predictor.predict(test_student)
        
        if result:
            print(f"✅ Prediction test successful!")
            print(f"   Probability: {result['probability']:.1%}")
            print(f"   Prediction: {'Likely Placed' if result['prediction'] == 1 else 'May Not Be Placed'}")
            print(f"   Confidence: {result['confidence']:.1%}")
        else:
            print(f"❌ Prediction test failed!")
            return False
        
        print(f"\n🎉 Fix completed successfully!")
        print(f"💡 The placement prediction system should now work without errors.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during model training: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🔄 You can now restart the web application and try the prediction again.")
    else:
        print(f"\n💔 Fix failed. Please check the error messages above.")