import sys
import os
import pandas as pd
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

def test_deep_learning_model():
    """Test the deep learning model training"""
    try:
        print("Testing deep learning model...")
        
        # Import the deep learning model
        from src.deep_learning_model import DeepPlacementPredictor
        
        # Create sample data for testing
        sample_data = pd.DataFrame({
            'student_id': [1, 2, 3, 4, 5],
            'branch': ['CSE', 'ECE', 'CSE', 'ECE', 'CSE'],
            'cgpa': [8.5, 7.2, 9.1, 6.8, 8.9],
            'tenth_percentage': [90, 75, 95, 70, 88],
            'twelfth_percentage': [88, 72, 92, 68, 85],
            'num_projects': [3, 1, 4, 2, 3],
            'num_internships': [1, 0, 2, 1, 1],
            'num_certifications': [2, 1, 3, 1, 2],
            'programming_languages': ['Python,Java', 'Python', 'Python,Java,JavaScript', 'Python,C++', 'Python,Java'],
            'leetcode_score': [1800, 500, 2200, 800, 2000],
            'codechef_rating': [1600, 1200, 1800, 1300, 1700],
            'communication_score': [8.5, 6.2, 9.1, 5.8, 8.9],
            'leadership_score': [7.5, 5.2, 8.1, 4.8, 7.9],
            'num_hackathons': [2, 0, 3, 1, 2],
            'club_participation': [3, 1, 4, 2, 3],
            'online_courses': [5, 2, 7, 3, 6],
            'placed': [1, 0, 1, 0, 1]
        })
        
        print("Sample data created successfully")
        
        # Initialize the model
        model = DeepPlacementPredictor()
        print("Model initialized successfully")
        
        # Test data preparation
        X, y = model.prepare_data(sample_data)
        print(f"Data prepared - X shape: {X.shape}, y shape: {y.shape if y is not None else 'None'}")
        
        # Test model building
        model.build_model(X.shape[1])
        print("Model built successfully")
        
        print("✅ Deep learning model test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Deep learning model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_deep_learning_model()