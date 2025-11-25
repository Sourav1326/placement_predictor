import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import cross_val_score, GridSearchCV
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.data_preprocessing import PlacementDataPreprocessor
import os

class PlacementPredictor:
    """
    Comprehensive placement prediction system with multiple ML models
    """
    
    def __init__(self):
        self.models = {}
        self.preprocessor = PlacementDataPreprocessor()
        self.best_model = None
        self.model_scores = {}
        self.feature_importance = {}
        
    def train_logistic_regression(self, X_train, y_train, X_test, y_test):
        """Train and evaluate Logistic Regression model"""
        print("Training Logistic Regression...")
        
        # Parameter grid with compatible solver-penalty combinations
        param_grid = [
            # liblinear solver with l1 and l2 penalties
            {
                'C': [0.01, 0.1, 1, 10],
                'penalty': ['l1', 'l2'],
                'solver': ['liblinear']
            },
            # lbfgs solver with l2 penalty only
            {
                'C': [0.01, 0.1, 1, 10],
                'penalty': ['l2'],
                'solver': ['lbfgs']
            }
        ]
        
        # Create model
        lr = LogisticRegression(random_state=42, max_iter=1000)
        
        # Grid search for best parameters
        grid_search = GridSearchCV(lr, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        # Best model
        best_lr = grid_search.best_estimator_
        
        # Predictions
        y_pred = best_lr.predict(X_test)
        y_pred_proba = best_lr.predict_proba(X_test)[:, 1]
        
        # Evaluation
        auc_score = roc_auc_score(y_test, y_pred_proba)
        cv_scores = cross_val_score(best_lr, X_train, y_train, cv=5, scoring='roc_auc')
        
        # Store results
        self.models['logistic_regression'] = best_lr
        self.model_scores['logistic_regression'] = {
            'auc': auc_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'best_params': grid_search.best_params_
        }
        
        print(f"Logistic Regression AUC: {auc_score:.4f}")
        print(f"CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        print(f"Best Parameters: {grid_search.best_params_}")
        
        return best_lr, y_pred, y_pred_proba
    
    def train_random_forest(self, X_train, y_train, X_test, y_test):
        """Train and evaluate Random Forest model"""
        print("\nTraining Random Forest...")
        
        # Parameter grid for hyperparameter tuning
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        # Create model
        rf = RandomForestClassifier(random_state=42)
        
        # Grid search for best parameters (reduced for speed)
        grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='roc_auc', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        # Best model
        best_rf = grid_search.best_estimator_
        
        # Predictions
        y_pred = best_rf.predict(X_test)
        y_pred_proba = best_rf.predict_proba(X_test)[:, 1]
        
        # Evaluation
        auc_score = roc_auc_score(y_test, y_pred_proba)
        cv_scores = cross_val_score(best_rf, X_train, y_train, cv=5, scoring='roc_auc')
        
        # Feature importance
        feature_importance = best_rf.feature_importances_
        self.feature_importance['random_forest'] = dict(zip(X_train.columns, feature_importance))
        
        # Store results
        self.models['random_forest'] = best_rf
        self.model_scores['random_forest'] = {
            'auc': auc_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'best_params': grid_search.best_params_
        }
        
        print(f"Random Forest AUC: {auc_score:.4f}")
        print(f"CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        print(f"Best Parameters: {grid_search.best_params_}")
        
        return best_rf, y_pred, y_pred_proba
    
    def train_xgboost(self, X_train, y_train, X_test, y_test):
        """Train and evaluate XGBoost model"""
        print("\nTraining XGBoost...")
        
        # Parameter grid for hyperparameter tuning
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [3, 6, 9],
            'learning_rate': [0.01, 0.1, 0.2],
            'subsample': [0.8, 1.0]
        }
        
        # Create model
        xgb_model = xgb.XGBClassifier(random_state=42, eval_metric='logloss')
        
        # Grid search for best parameters (reduced for speed)
        grid_search = GridSearchCV(xgb_model, param_grid, cv=3, scoring='roc_auc', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        
        # Best model
        best_xgb = grid_search.best_estimator_
        
        # Predictions
        y_pred = best_xgb.predict(X_test)
        y_pred_proba = best_xgb.predict_proba(X_test)[:, 1]
        
        # Evaluation
        auc_score = roc_auc_score(y_test, y_pred_proba)
        cv_scores = cross_val_score(best_xgb, X_train, y_train, cv=5, scoring='roc_auc')
        
        # Feature importance
        feature_importance = best_xgb.feature_importances_
        self.feature_importance['xgboost'] = dict(zip(X_train.columns, feature_importance))
        
        # Store results
        self.models['xgboost'] = best_xgb
        self.model_scores['xgboost'] = {
            'auc': auc_score,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'best_params': grid_search.best_params_
        }
        
        print(f"XGBoost AUC: {auc_score:.4f}")
        print(f"CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        print(f"Best Parameters: {grid_search.best_params_}")
        
        return best_xgb, y_pred, y_pred_proba
    
    def train_all_models(self, file_path='data/placement_data.csv'):
        """Train all models and compare performance"""
        print("Starting comprehensive model training pipeline...")
        
        # Prepare data
        X_train, X_test, y_train, y_test = self.preprocessor.prepare_data_for_training(file_path)
        
        if X_train is None:
            print("Error: Could not load or preprocess data.")
            return False
        
        # Train all models
        models_results = {}
        
        # Logistic Regression
        try:
            lr_model, lr_pred, lr_proba = self.train_logistic_regression(X_train, y_train, X_test, y_test)
            models_results['logistic_regression'] = (lr_model, lr_pred, lr_proba)
        except Exception as e:
            print(f"Error training Logistic Regression: {e}")
        
        # Random Forest
        try:
            rf_model, rf_pred, rf_proba = self.train_random_forest(X_train, y_train, X_test, y_test)
            models_results['random_forest'] = (rf_model, rf_pred, rf_proba)
        except Exception as e:
            print(f"Error training Random Forest: {e}")
        
        # XGBoost
        try:
            xgb_model, xgb_pred, xgb_proba = self.train_xgboost(X_train, y_train, X_test, y_test)
            models_results['xgboost'] = (xgb_model, xgb_pred, xgb_proba)
        except Exception as e:
            print(f"Error training XGBoost: {e}")
        
        # Determine best model
        if self.model_scores:
            best_model_name = max(self.model_scores.keys(), key=lambda x: self.model_scores[x]['auc'])
            self.best_model = self.models[best_model_name]
            print(f"\nBest Model: {best_model_name} (AUC: {self.model_scores[best_model_name]['auc']:.4f})")
        
        # Generate detailed evaluation report
        self.generate_evaluation_report(X_test, y_test, models_results)
        
        # Save models and preprocessor
        self.save_models()
        
        return True
    
    def generate_evaluation_report(self, X_test, y_test, models_results):
        """Generate comprehensive evaluation report"""
        print("\n" + "="*50)
        print("COMPREHENSIVE MODEL EVALUATION REPORT")
        print("="*50)
        
        for model_name in self.model_scores:
            score = self.model_scores[model_name]
            print(f"\n{model_name.upper()}:")
            print(f"  AUC Score: {score['auc']:.4f}")
            print(f"  CV Mean: {score['cv_mean']:.4f}")
            print(f"  CV Std: {score['cv_std']:.4f}")
            print(f"  Best Parameters: {score['best_params']}")
            
            if model_name in models_results:
                model, y_pred, y_pred_proba = models_results[model_name]
                print(f"\n  Classification Report:")
                print(classification_report(y_test, y_pred, target_names=['Not Placed', 'Placed']))
        
        # Feature importance comparison
        print("\n" + "="*50)
        print("FEATURE IMPORTANCE ANALYSIS")
        print("="*50)
        
        if self.feature_importance:
            # Combine feature importance from all models
            all_features = set()
            for model_importance in self.feature_importance.values():
                all_features.update(model_importance.keys())
            
            feature_comparison = {}
            for feature in all_features:
                feature_comparison[feature] = {}
                for model_name, importance_dict in self.feature_importance.items():
                    feature_comparison[feature][model_name] = importance_dict.get(feature, 0)
            
            # Create DataFrame for better visualization
            importance_df = pd.DataFrame(feature_comparison).T
            importance_df = importance_df.fillna(0)
            
            # Show top 10 most important features
            if 'random_forest' in importance_df.columns:
                top_features = importance_df.sort_values('random_forest', ascending=False).head(10)
                print("\nTop 10 Most Important Features (Random Forest):")
                print(top_features.round(4))
    
    def save_models(self):
        """Save all trained models and preprocessor"""
        os.makedirs('data/models', exist_ok=True)
        
        # Save preprocessor
        self.preprocessor.save_preprocessor('data/models/preprocessor.pkl')
        
        # Save individual models
        for model_name, model in self.models.items():
            joblib.dump(model, f'data/models/{model_name}_model.pkl')
            print(f"Saved {model_name} model to data/models/{model_name}_model.pkl")
        
        # Save best model separately for easy access
        if self.best_model:
            joblib.dump(self.best_model, 'data/models/best_model.pkl')
            print("Saved best model to data/models/best_model.pkl")
        
        # Save model scores and feature importance
        joblib.dump(self.model_scores, 'data/models/model_scores.pkl')
        joblib.dump(self.feature_importance, 'data/models/feature_importance.pkl')
        
        print("All models and metadata saved successfully!")
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            # Load preprocessor
            self.preprocessor.load_preprocessor('data/models/preprocessor.pkl')
            
            # Load models
            model_files = ['logistic_regression_model.pkl', 'random_forest_model.pkl', 'xgboost_model.pkl']
            for model_file in model_files:
                model_path = f'data/models/{model_file}'
                if os.path.exists(model_path):
                    model_name = model_file.replace('_model.pkl', '')
                    self.models[model_name] = joblib.load(model_path)
            
            # Load best model
            if os.path.exists('data/models/best_model.pkl'):
                self.best_model = joblib.load('data/models/best_model.pkl')
            
            # Load scores and feature importance
            if os.path.exists('data/models/model_scores.pkl'):
                self.model_scores = joblib.load('data/models/model_scores.pkl')
            
            if os.path.exists('data/models/feature_importance.pkl'):
                self.feature_importance = joblib.load('data/models/feature_importance.pkl')
            
            print("Models loaded successfully!")
            return True
        
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def predict_placement(self, student_data, model_name='best'):
        """Predict placement for a new student"""
        if not self.models and not self.load_models():
            print("No trained models available. Please train models first.")
            return None
        
        # Select model
        if model_name == 'best' and self.best_model:
            model = self.best_model
        elif model_name in self.models:
            model = self.models[model_name]
        else:
            print(f"Model {model_name} not found. Using best model.")
            model = self.best_model
        
        # Preprocess data
        if isinstance(student_data, dict):
            student_df = pd.DataFrame([student_data])
        else:
            student_df = student_data
        
        X_processed = self.preprocessor.transform(student_df)
        
        # Make prediction
        probability = model.predict_proba(X_processed)[:, 1][0]
        prediction = model.predict(X_processed)[0]
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'placement_chance': f"{probability*100:.1f}%"
        }
    
    def get_feature_importance_for_prediction(self, student_data, model_name='random_forest'):
        """Get feature importance for a specific prediction"""
        if model_name not in self.feature_importance:
            return None
        
        # Get feature values for the student
        if isinstance(student_data, dict):
            student_df = pd.DataFrame([student_data])
        else:
            student_df = student_data
        
        X_processed = self.preprocessor.transform(student_df)
        
        # Combine with feature importance
        feature_impact = {}
        importance_dict = self.feature_importance[model_name]
        
        for feature in X_processed.columns:
            if feature in importance_dict:
                feature_impact[feature] = {
                    'value': float(X_processed[feature].iloc[0]),
                    'importance': float(importance_dict[feature]),
                    'impact': float(X_processed[feature].iloc[0] * importance_dict[feature])
                }
        
        # Sort by impact
        sorted_impact = dict(sorted(feature_impact.items(), key=lambda x: abs(x[1]['impact']), reverse=True))
        
        return sorted_impact

def main():
    """Main training pipeline"""
    print("🚀 Starting Placement Prediction Model Training Pipeline")
    print("="*60)
    
    # Initialize predictor
    predictor = PlacementPredictor()
    
    # Train all models
    success = predictor.train_all_models()
    
    if success:
        print("\n✅ Model training completed successfully!")
        print("\nModels trained:")
        for model_name in predictor.models:
            auc_score = predictor.model_scores[model_name]['auc']
            print(f"  - {model_name}: AUC = {auc_score:.4f}")
        
        print(f"\n🏆 Best model saved and ready for deployment!")
    else:
        print("\n❌ Model training failed!")

if __name__ == "__main__":
    main()