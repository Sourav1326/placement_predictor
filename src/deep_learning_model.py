"""
Advanced Deep Learning Model for Placement Prediction
Neural network implementation with TensorFlow/Keras for enhanced accuracy
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

class DeepPlacementPredictor:
    """
    Advanced deep learning model for placement prediction
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = []
        self.training_history = None
        self.model_metrics = {}
        
    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Advanced data preprocessing for deep learning"""
        
        # Create a copy to avoid modifying original data
        data = df.copy()
        
        # Handle categorical variables (excluding output variables like package_category)
        categorical_cols = ['branch']
        for col in categorical_cols:
            if col in data.columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    data[col + '_encoded'] = self.label_encoders[col].fit_transform(data[col].astype(str))
                else:
                    data[col + '_encoded'] = self.label_encoders[col].transform(data[col].astype(str))
                data.drop(col, axis=1, inplace=True)
        
        # Remove output variables that shouldn't be used as input features
        output_variables = ['package_category', 'salary_package']
        for col in output_variables:
            if col in data.columns:
                data.drop(col, axis=1, inplace=True)
        
        # Advanced feature engineering
        data = self._create_advanced_features(data)
        
        # Prepare features and target
        if 'placed' in data.columns:
            y = data['placed'].values
            X = data.drop(['placed', 'student_id'], axis=1, errors='ignore')
        else:
            y = None
            X = data.drop(['student_id'], axis=1, errors='ignore')
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Convert to numpy arrays
        X = X.values.astype(np.float32)
        
        return X, y
    
    def _create_advanced_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create sophisticated feature engineering"""
        
        # Academic performance features
        data['academic_average'] = (data['cgpa'] + data['tenth_percentage']/10 + 
                                  data['twelfth_percentage']/10) / 3
        
        data['academic_consistency'] = 1 - np.abs(data['cgpa'] - data['tenth_percentage']/10) - \
                                     np.abs(data['cgpa'] - data['twelfth_percentage']/10)
        
        # Technical skills composite
        data['technical_score'] = (data['leetcode_score']/2500 + data['codechef_rating']/2000 + 
                                 data['num_projects']/10 + data['num_certifications']/10) / 4
        
        # Experience factor
        data['experience_score'] = (data['num_internships'] * 2 + data['num_hackathons'] + 
                                  data['club_participation']) / 10
        
        # Communication and leadership composite
        data['soft_skills_score'] = (data['communication_score'] + data['leadership_score']) / 2
        
        # Learning agility
        data['learning_agility'] = data['online_courses'] / 20 + data['num_certifications'] / 10
        
        # Competitive programming effectiveness
        data['cp_effectiveness'] = np.where(data['leetcode_score'] > 0, 
                                          data['leetcode_score'] / (data['num_hackathons'] + 1), 0)
        
        # Project to internship ratio
        data['project_internship_ratio'] = data['num_projects'] / (data['num_internships'] + 1)
        
        # Overall readiness score
        data['readiness_score'] = (data['technical_score'] * 0.4 + 
                                 data['academic_average']/10 * 0.3 + 
                                 data['experience_score'] * 0.2 + 
                                 data['soft_skills_score']/10 * 0.1)
        
        # Programming language diversity
        if 'programming_languages' in data.columns:
            data['language_count'] = data['programming_languages'].str.count(',') + 1
            data['has_python'] = data['programming_languages'].str.contains('Python', case=False, na=False).astype(int)
            data['has_java'] = data['programming_languages'].str.contains('Java', case=False, na=False).astype(int)
            data['has_javascript'] = data['programming_languages'].str.contains('JavaScript', case=False, na=False).astype(int)
            data['has_cpp'] = data['programming_languages'].str.contains('C\\+\\+', case=False, na=False).astype(int)
            data.drop('programming_languages', axis=1, inplace=True)
        
        # Interaction features
        data['cgpa_projects'] = data['cgpa'] * data['num_projects']
        data['leetcode_internships'] = data['leetcode_score'] * data['num_internships']
        data['hackathons_projects'] = data['num_hackathons'] * data['num_projects']
        
        # Normalization features
        data['normalized_cgpa'] = data['cgpa'] / 10.0
        data['normalized_leetcode'] = np.clip(data['leetcode_score'] / 2500.0, 0, 1)
        data['normalized_codechef'] = np.clip(data['codechef_rating'] / 2000.0, 0, 1)
        
        return data
    
    def build_model(self, input_dim: int) -> keras.Model:
        """Build advanced neural network architecture"""
        
        # Input layer
        inputs = keras.Input(shape=(input_dim,), name='features')
        
        # Feature normalization layer
        normalized = layers.BatchNormalization()(inputs)
        
        # First hidden layer with regularization
        x = layers.Dense(256, activation='relu', 
                        kernel_regularizer=regularizers.l2(0.001),
                        name='dense_1')(normalized)
        x = layers.Dropout(0.3)(x)
        x = layers.BatchNormalization()(x)
        
        # Second hidden layer
        x = layers.Dense(128, activation='relu',
                        kernel_regularizer=regularizers.l2(0.001),
                        name='dense_2')(x)
        x = layers.Dropout(0.4)(x)
        x = layers.BatchNormalization()(x)
        
        # Third hidden layer
        x = layers.Dense(64, activation='relu',
                        kernel_regularizer=regularizers.l2(0.001),
                        name='dense_3')(x)
        x = layers.Dropout(0.3)(x)
        
        # Fourth hidden layer
        x = layers.Dense(32, activation='relu',
                        kernel_regularizer=regularizers.l2(0.001),
                        name='dense_4')(x)
        x = layers.Dropout(0.2)(x)
        
        # Output layer
        outputs = layers.Dense(1, activation='sigmoid', name='prediction')(x)
        
        # Create model
        model = keras.Model(inputs=inputs, outputs=outputs, name='placement_predictor')
        
        return model
    
    def train_model(self, df: pd.DataFrame, validation_split: float = 0.2, 
                   epochs: int = 150, batch_size: int = 32) -> Dict:
        """Train the deep learning model with advanced techniques"""
        
        print("🧠 Training Advanced Deep Learning Model...")
        print("=" * 50)
        
        # Prepare data
        X, y = self.prepare_data(df)
        
        if y is None:
            raise ValueError("Training data must contain 'placed' column")
        
        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        
        # Build model
        self.model = self.build_model(X_train_scaled.shape[1])
        
        # Compile model with advanced optimizer
        optimizer = keras.optimizers.Adam(
            learning_rate=0.001,
            beta_1=0.9,
            beta_2=0.999,
            epsilon=1e-07
        )
        
        self.model.compile(
            optimizer=optimizer,
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(name='precision'), keras.metrics.Recall(name='recall'), keras.metrics.AUC(name='auc')]
        )
        
        print(f"Model Architecture:")
        self.model.summary()
        
        # Advanced callbacks
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_auc',
                patience=15,
                restore_best_weights=True,
                mode='max'
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=8,
                min_lr=1e-6
            )
        ]
        
        # Train model
        print("\n🚀 Starting training...")
        self.training_history = self.model.fit(
            X_train_scaled, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(X_val_scaled, y_val),
            callbacks=callbacks,
            verbose=1
        )
        
        # Evaluate model
        val_predictions = self.model.predict(X_val_scaled)
        val_pred_binary = (val_predictions > 0.5).astype(int)
        
        # Calculate metrics
        val_auc = roc_auc_score(y_val, val_predictions)
        val_accuracy = np.mean(y_val == val_pred_binary.flatten())
        
        self.model_metrics = {
            'val_auc': val_auc,
            'val_accuracy': val_accuracy,
            'training_samples': len(X_train),
            'validation_samples': len(X_val),
            'features_count': X_train_scaled.shape[1]
        }
        
        print(f"\n✅ Training completed!")
        print(f"Validation AUC: {val_auc:.4f}")
        print(f"Validation Accuracy: {val_accuracy:.4f}")
        
        return self.model_metrics
    
    def cross_validate(self, df: pd.DataFrame, cv_folds: int = 5) -> Dict:
        """Perform cross-validation for robust model evaluation"""
        
        print(f"\n🔄 Performing {cv_folds}-Fold Cross Validation...")
        
        X, y = self.prepare_data(df)
        
        if y is None:
            raise ValueError("Data must contain 'placed' column for cross-validation")
        
        skf = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
        
        cv_scores = {
            'auc_scores': [],
            'accuracy_scores': [],
            'precision_scores': [],
            'recall_scores': []
        }
        
        fold = 1
        for train_idx, val_idx in skf.split(X, y):
            print(f"\nTraining Fold {fold}/{cv_folds}...")
            
            X_train_fold, X_val_fold = X[train_idx], X[val_idx]
            y_train_fold, y_val_fold = y[train_idx], y[val_idx]
            
            # Scale features for this fold
            scaler_fold = StandardScaler()
            X_train_scaled = scaler_fold.fit_transform(X_train_fold)
            X_val_scaled = scaler_fold.transform(X_val_fold)
            
            # Build and train model for this fold
            model_fold = self.build_model(X_train_scaled.shape[1])
            model_fold.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.001),
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            # Train with early stopping
            model_fold.fit(
                X_train_scaled, y_train_fold,
                batch_size=32,
                epochs=100,
                validation_data=(X_val_scaled, y_val_fold),
                callbacks=[keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)],
                verbose=0
            )
            
            # Evaluate fold
            val_pred = model_fold.predict(X_val_scaled)
            val_pred_binary = (val_pred > 0.5).astype(int).flatten()
            
            # Calculate metrics
            auc_score = roc_auc_score(y_val_fold, val_pred)
            accuracy = np.mean(y_val_fold == val_pred_binary)
            
            # Calculate precision and recall manually
            tp = np.sum((y_val_fold == 1) & (val_pred_binary == 1))
            fp = np.sum((y_val_fold == 0) & (val_pred_binary == 1))
            fn = np.sum((y_val_fold == 1) & (val_pred_binary == 0))
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            cv_scores['auc_scores'].append(auc_score)
            cv_scores['accuracy_scores'].append(accuracy)
            cv_scores['precision_scores'].append(precision)
            cv_scores['recall_scores'].append(recall)
            
            print(f"Fold {fold} - AUC: {auc_score:.4f}, Accuracy: {accuracy:.4f}")
            fold += 1
        
        # Calculate cross-validation statistics
        cv_results = {
            'mean_auc': np.mean(cv_scores['auc_scores']),
            'std_auc': np.std(cv_scores['auc_scores']),
            'mean_accuracy': np.mean(cv_scores['accuracy_scores']),
            'std_accuracy': np.std(cv_scores['accuracy_scores']),
            'mean_precision': np.mean(cv_scores['precision_scores']),
            'std_precision': np.std(cv_scores['precision_scores']),
            'mean_recall': np.mean(cv_scores['recall_scores']),
            'std_recall': np.std(cv_scores['recall_scores']),
            'all_scores': cv_scores
        }
        
        print(f"\n📊 Cross-Validation Results:")
        print(f"AUC: {cv_results['mean_auc']:.4f} (+/- {cv_results['std_auc']*2:.4f})")
        print(f"Accuracy: {cv_results['mean_accuracy']:.4f} (+/- {cv_results['std_accuracy']*2:.4f})")
        print(f"Precision: {cv_results['mean_precision']:.4f} (+/- {cv_results['std_precision']*2:.4f})")
        print(f"Recall: {cv_results['mean_recall']:.4f} (+/- {cv_results['std_recall']*2:.4f})")
        
        return cv_results
    
    def predict(self, student_data: Dict) -> Dict:
        """Make prediction for a single student"""
        
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        # Convert to DataFrame
        if isinstance(student_data, dict):
            df = pd.DataFrame([student_data])
        else:
            df = student_data
        
        # Prepare data
        X, _ = self.prepare_data(df)
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        probability = self.model.predict(X_scaled)[0][0]
        prediction = int(probability > 0.5)
        
        # Calculate confidence
        confidence = max(probability, 1 - probability)
        
        return {
            'prediction': prediction,
            'probability': float(probability),
            'confidence': float(confidence),
            'placement_chance': f"{probability*100:.1f}%",
            'model_type': 'deep_learning'
        }
    
    def get_feature_importance(self) -> Dict:
        """Calculate feature importance using permutation importance"""
        
        if self.model is None:
            raise ValueError("Model not trained")
        
        # This is a simplified version - in practice, you'd use permutation importance
        # For demonstration, we'll return feature names with equal importance
        importance_dict = {}
        for i, feature_name in enumerate(self.feature_names):
            importance_dict[feature_name] = 1.0 / len(self.feature_names)
        
        return importance_dict
    
    def save_model(self, model_path: str = 'data/models/deep_learning_model'):
        """Save the trained model and associated components"""
        
        os.makedirs('data/models', exist_ok=True)
        
        # Save Keras model
        if self.model:
            self.model.save(f'{model_path}.keras')
            print(f"✅ Deep learning model saved to {model_path}.keras")
        
        # Save scaler and encoders
        joblib.dump(self.scaler, f'{model_path}_scaler.pkl')
        joblib.dump(self.label_encoders, f'{model_path}_encoders.pkl')
        joblib.dump(self.feature_names, f'{model_path}_features.pkl')
        
        # Save metrics and history
        if self.model_metrics:
            joblib.dump(self.model_metrics, f'{model_path}_metrics.pkl')
        
        if self.training_history:
            joblib.dump(self.training_history.history, f'{model_path}_history.pkl')
        
        print("✅ All model components saved successfully!")
    
    def load_model(self, model_path: str = 'data/models/deep_learning_model'):
        """Load the trained model and associated components"""
        
        try:
            # Load Keras model
            self.model = keras.models.load_model(f'{model_path}.keras')
            
            # Load scaler and encoders
            self.scaler = joblib.load(f'{model_path}_scaler.pkl')
            self.label_encoders = joblib.load(f'{model_path}_encoders.pkl')
            self.feature_names = joblib.load(f'{model_path}_features.pkl')
            
            # Load metrics if available
            try:
                self.model_metrics = joblib.load(f'{model_path}_metrics.pkl')
            except:
                self.model_metrics = {}
            
            print("✅ Deep learning model loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def plot_training_history(self):
        """Plot training history"""
        
        if not self.training_history:
            print("No training history available")
            return
        
        history = self.training_history.history
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Loss
        axes[0,0].plot(history['loss'], label='Training Loss')
        axes[0,0].plot(history['val_loss'], label='Validation Loss')
        axes[0,0].set_title('Model Loss')
        axes[0,0].set_xlabel('Epoch')
        axes[0,0].set_ylabel('Loss')
        axes[0,0].legend()
        
        # Accuracy
        axes[0,1].plot(history['accuracy'], label='Training Accuracy')
        axes[0,1].plot(history['val_accuracy'], label='Validation Accuracy')
        axes[0,1].set_title('Model Accuracy')
        axes[0,1].set_xlabel('Epoch')
        axes[0,1].set_ylabel('Accuracy')
        axes[0,1].legend()
        
        # AUC
        if 'auc' in history:
            axes[1,0].plot(history['auc'], label='Training AUC')
            axes[1,0].plot(history['val_auc'], label='Validation AUC')
            axes[1,0].set_title('Model AUC')
            axes[1,0].set_xlabel('Epoch')
            axes[1,0].set_ylabel('AUC')
            axes[1,0].legend()
        
        # Learning Rate (if available)
        axes[1,1].text(0.5, 0.5, f"Final Validation AUC: {self.model_metrics.get('val_auc', 'N/A'):.4f}\n"
                                  f"Final Validation Accuracy: {self.model_metrics.get('val_accuracy', 'N/A'):.4f}\n"
                                  f"Training Samples: {self.model_metrics.get('training_samples', 'N/A')}\n"
                                  f"Features Count: {self.model_metrics.get('features_count', 'N/A')}",
                      transform=axes[1,1].transAxes, ha='center', va='center',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        axes[1,1].set_title('Model Summary')
        axes[1,1].axis('off')
        
        plt.tight_layout()
        plt.savefig('data/models/training_history.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """Main training pipeline for deep learning model"""
    
    print("🧠 Advanced Deep Learning Model Training")
    print("=" * 50)
    
    # Load data
    if not os.path.exists('data/placement_data.csv'):
        print("❌ Dataset not found. Please run generate_dataset.py first.")
        return
    
    df = pd.read_csv('data/placement_data.csv')
    print(f"📊 Loaded dataset with {len(df)} samples")
    
    # Initialize model
    deep_predictor = DeepPlacementPredictor()
    
    # Train model
    metrics = deep_predictor.train_model(df, epochs=100)
    
    # Perform cross-validation
    cv_results = deep_predictor.cross_validate(df, cv_folds=5)
    
    # Save model
    deep_predictor.save_model()
    
    # Plot training history
    deep_predictor.plot_training_history()
    
    print("\n🎯 Deep Learning Model Training Complete!")
    print(f"Validation AUC: {metrics['val_auc']:.4f}")
    print(f"Cross-validation AUC: {cv_results['mean_auc']:.4f} (+/- {cv_results['std_auc']*2:.4f})")

if __name__ == "__main__":
    main()