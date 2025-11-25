import sys
import os
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

def train_deep_learning_model():
    """Train the deep learning model with a small dataset"""
    try:
        print("Training deep learning model...")
        
        # Import the deep learning model
        from src.deep_learning_model import DeepPlacementPredictor
        
        # Create a larger sample dataset for training
        sample_data = pd.DataFrame({
            'student_id': range(1, 101),
            'branch': ['CSE'] * 30 + ['ECE'] * 25 + ['EEE'] * 20 + ['MECH'] * 15 + ['CIVIL'] * 10,
            'cgpa': [round(6.0 + (i % 40) * 0.1, 2) for i in range(100)],
            'tenth_percentage': [round(60 + (i % 40), 1) for i in range(100)],
            'twelfth_percentage': [round(60 + (i % 35), 1) for i in range(100)],
            'num_projects': [i % 5 for i in range(100)],
            'num_internships': [i % 3 for i in range(100)],
            'num_certifications': [i % 4 for i in range(100)],
            'programming_languages': ['Python,Java'] * 25 + ['Python'] * 25 + ['Python,JavaScript,C++'] * 25 + ['Java,C++'] * 25,
            'leetcode_score': [i * 50 for i in range(100)],
            'codechef_rating': [1000 + i * 20 for i in range(100)],
            'communication_score': [round(5.0 + (i % 50) * 0.1, 2) for i in range(100)],
            'leadership_score': [round(5.0 + (i % 50) * 0.1, 2) for i in range(100)],
            'num_hackathons': [i % 4 for i in range(100)],
            'club_participation': [i % 5 for i in range(100)],
            'online_courses': [i % 8 for i in range(100)],
            'placed': [1 if i > 30 else 0 for i in range(100)]  # Simple rule for placement
        })
        
        print(f"Sample data created with {len(sample_data)} records")
        
        # Initialize the model
        model = DeepPlacementPredictor()
        print("Model initialized successfully")
        
        # Train the model with a small number of epochs for testing
        metrics = model.train_model(sample_data, epochs=10, validation_split=0.2)
        print(f"Training completed with metrics: {metrics}")
        
        # Save the model
        model.save_model('data/models/test_deep_learning_model')
        print("Model saved successfully")
        
        print("✅ Deep learning model training test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Deep learning model training test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    train_deep_learning_model()