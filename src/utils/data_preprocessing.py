import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

class PlacementDataPreprocessor:
    """
    Comprehensive data preprocessing pipeline for placement prediction
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.is_fitted = False
    
    def load_data(self, file_path='data/placement_data.csv'):
        """Load the placement dataset"""
        try:
            df = pd.read_csv(file_path)
            print(f"Data loaded successfully. Shape: {df.shape}")
            return df
        except FileNotFoundError:
            print(f"File {file_path} not found. Please run generate_dataset.py first.")
            return None
    
    def create_features(self, df):
        """Create additional features from existing ones"""
        df_processed = df.copy()
        
        # Create academic performance score
        df_processed['academic_score'] = (
            df_processed['cgpa'] * 0.5 + 
            df_processed['tenth_percentage'] * 0.025 + 
            df_processed['twelfth_percentage'] * 0.025
        )
        
        # Create technical skills score
        df_processed['technical_score'] = (
            df_processed['num_projects'] * 2 + 
            df_processed['num_internships'] * 3 + 
            df_processed['num_certifications'] * 1.5 +
            df_processed['leetcode_score'] / 1000 +
            df_processed['codechef_rating'] / 1000
        )
        
        # Create overall coding score
        df_processed['coding_score'] = (
            df_processed['leetcode_score'] * 0.0002 + 
            df_processed['codechef_rating'] * 0.0003
        )
        
        # Create soft skills score
        df_processed['soft_skills_score'] = (
            df_processed['communication_score'] * 0.6 + 
            df_processed['leadership_score'] * 0.4
        )
        
        # Create extracurricular score
        df_processed['extracurricular_score'] = (
            df_processed['num_hackathons'] * 2 + 
            df_processed['club_participation'] * 1.5 + 
            df_processed['online_courses'] * 1
        )
        
        # Create overall experience score
        df_processed['experience_score'] = (
            df_processed['num_internships'] * 3 + 
            df_processed['num_projects'] * 2 + 
            df_processed['num_hackathons'] * 1.5
        )
        
        # Create binary features
        df_processed['has_internship'] = (df_processed['num_internships'] > 0).astype(int)
        df_processed['has_projects'] = (df_processed['num_projects'] > 0).astype(int)
        df_processed['has_certifications'] = (df_processed['num_certifications'] > 0).astype(int)
        df_processed['high_cgpa'] = (df_processed['cgpa'] >= 8.0).astype(int)
        df_processed['active_coder'] = (df_processed['leetcode_score'] > 1000).astype(int)
        
        # Programming language diversity (count unique languages)
        df_processed['prog_lang_count'] = df_processed['programming_languages'].apply(
            lambda x: len(str(x).split(',')) if pd.notna(x) else 0
        )
        
        return df_processed
    
    def encode_categorical_features(self, df):
        """Encode categorical variables"""
        df_encoded = df.copy()
        
        # List of categorical columns to encode
        categorical_columns = ['branch']
        
        for column in categorical_columns:
            if column in df_encoded.columns:
                if column not in self.label_encoders:
                    self.label_encoders[column] = LabelEncoder()
                    df_encoded[f'{column}_encoded'] = self.label_encoders[column].fit_transform(df_encoded[column])
                else:
                    df_encoded[f'{column}_encoded'] = self.label_encoders[column].transform(df_encoded[column])
        
        return df_encoded
    
    def select_features(self, df):
        """Select relevant features for model training"""
        # Define feature columns for training
        feature_columns = [
            'cgpa', 'tenth_percentage', 'twelfth_percentage',
            'num_projects', 'num_internships', 'num_certifications',
            'leetcode_score', 'codechef_rating',
            'communication_score', 'leadership_score',
            'num_hackathons', 'club_participation', 'online_courses',
            'branch_encoded', 'prog_lang_count',
            'academic_score', 'technical_score', 'coding_score',
            'soft_skills_score', 'extracurricular_score', 'experience_score',
            'has_internship', 'has_projects', 'has_certifications',
            'high_cgpa', 'active_coder'
        ]
        
        # Filter only existing columns
        available_columns = [col for col in feature_columns if col in df.columns]
        self.feature_columns = available_columns
        
        return df[available_columns]
    
    def fit_transform(self, df):
        """Fit preprocessor and transform data"""
        # Create additional features
        df_features = self.create_features(df)
        
        # Encode categorical variables
        df_encoded = self.encode_categorical_features(df_features)
        
        # Select features for training
        X = self.select_features(df_encoded)
        
        # Scale numerical features
        X_scaled = self.scaler.fit_transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        
        self.is_fitted = True
        
        return X_scaled_df
    
    def transform(self, df):
        """Transform new data using fitted preprocessor"""
        if not self.is_fitted:
            raise ValueError("Preprocessor not fitted. Call fit_transform first.")
        
        # Create additional features
        df_features = self.create_features(df)
        
        # Encode categorical variables
        df_encoded = self.encode_categorical_features(df_features)
        
        # Select features
        X = df_encoded[self.feature_columns]
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
        
        return X_scaled_df
    
    def prepare_data_for_training(self, file_path='data/placement_data.csv', test_size=0.2, random_state=42):
        """Complete data preparation pipeline for model training"""
        # Load data
        df = self.load_data(file_path)
        if df is None:
            return None, None, None, None
        
        # Prepare features
        X = self.fit_transform(df)
        y = df['placed']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"Training set: {X_train.shape}")
        print(f"Test set: {X_test.shape}")
        print(f"Training set placement rate: {y_train.mean():.3f}")
        print(f"Test set placement rate: {y_test.mean():.3f}")
        
        return X_train, X_test, y_train, y_test
    
    def save_preprocessor(self, file_path='data/models/preprocessor.pkl'):
        """Save the fitted preprocessor"""
        if not self.is_fitted:
            raise ValueError("Preprocessor not fitted. Cannot save.")
        
        preprocessor_data = {
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_columns': self.feature_columns,
            'is_fitted': self.is_fitted
        }
        
        joblib.dump(preprocessor_data, file_path)
        print(f"Preprocessor saved to {file_path}")
    
    def load_preprocessor(self, file_path='data/models/preprocessor.pkl'):
        """Load a fitted preprocessor"""
        try:
            preprocessor_data = joblib.load(file_path)
            self.scaler = preprocessor_data['scaler']
            self.label_encoders = preprocessor_data['label_encoders']
            self.feature_columns = preprocessor_data['feature_columns']
            self.is_fitted = preprocessor_data['is_fitted']
            print(f"Preprocessor loaded from {file_path}")
            return True
        except FileNotFoundError:
            print(f"Preprocessor file {file_path} not found.")
            return False
    
    def get_feature_names(self):
        """Get list of feature names used in the model"""
        return self.feature_columns if self.feature_columns else []
    
    def describe_features(self):
        """Provide description of all features"""
        feature_descriptions = {
            'cgpa': 'Current Cumulative Grade Point Average (0-10)',
            'tenth_percentage': '10th grade percentage (0-100)',
            'twelfth_percentage': '12th grade percentage (0-100)',
            'num_projects': 'Number of completed projects',
            'num_internships': 'Number of internships completed',
            'num_certifications': 'Number of certifications earned',
            'leetcode_score': 'LeetCode rating/score',
            'codechef_rating': 'CodeChef rating',
            'communication_score': 'Communication skills score (1-10)',
            'leadership_score': 'Leadership skills score (1-10)',
            'num_hackathons': 'Number of hackathons participated',
            'club_participation': 'Number of clubs participated',
            'online_courses': 'Number of online courses completed',
            'branch_encoded': 'Engineering branch (encoded)',
            'prog_lang_count': 'Number of programming languages known',
            'academic_score': 'Combined academic performance score',
            'technical_score': 'Combined technical skills score',
            'coding_score': 'Combined coding platform score',
            'soft_skills_score': 'Combined soft skills score',
            'extracurricular_score': 'Combined extracurricular activities score',
            'experience_score': 'Combined experience score',
            'has_internship': 'Has at least one internship (binary)',
            'has_projects': 'Has at least one project (binary)',
            'has_certifications': 'Has at least one certification (binary)',
            'high_cgpa': 'CGPA >= 8.0 (binary)',
            'active_coder': 'LeetCode score > 1000 (binary)'
        }
        
        return feature_descriptions

def main():
    """Test the preprocessing pipeline"""
    preprocessor = PlacementDataPreprocessor()
    
    # Prepare data for training
    X_train, X_test, y_train, y_test = preprocessor.prepare_data_for_training()
    
    if X_train is not None:
        print(f"\nFeatures used ({len(preprocessor.get_feature_names())}):")
        for feature in preprocessor.get_feature_names():
            print(f"  - {feature}")
        
        # Save preprocessor
        preprocessor.save_preprocessor()
        
        print(f"\nData preprocessing completed successfully!")
        print(f"Training data shape: {X_train.shape}")
        print(f"Ready for model training!")

if __name__ == "__main__":
    main()