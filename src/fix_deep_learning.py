"""
Quick fix for Deep Learning Model to address Keras file format issue
"""

import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score
import joblib

print(f"TensorFlow version: {tf.__version__}")
print(f"Keras version: {keras.__version__}")

# Check if dataset exists
if not os.path.exists('data/placement_data.csv'):
    print("❌ Dataset not found. Please run generate_dataset.py first.")
    exit()

df = pd.read_csv('data/placement_data.csv')
print(f"📊 Loaded dataset with {len(df)} samples")

# Simple data preparation
feature_columns = [
    'cgpa', 'tenth_percentage', 'twelfth_percentage', 'num_projects', 
    'num_internships', 'num_certifications', 'leetcode_score', 
    'codechef_rating', 'communication_score', 'leadership_score',
    'num_hackathons', 'club_participation', 'online_courses'
]

X = df[feature_columns].fillna(0)
y = df['placed']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(f"Training samples: {len(X_train)}")
print(f"Test samples: {len(X_test)}")

# Build simple model
model = keras.Sequential([
    keras.Input(shape=(len(feature_columns),)),
    keras.layers.BatchNormalization(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

# Compile model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy', 'AUC']
)

print("\nModel Architecture:")
model.summary()

# Create models directory
os.makedirs('data/models', exist_ok=True)

# Test callbacks with correct extensions
callbacks = [
    keras.callbacks.EarlyStopping(
        monitor='val_auc',
        patience=10,
        restore_best_weights=True
    ),
    keras.callbacks.ModelCheckpoint(
        'data/models/test_deep_model.keras',  # Use .keras extension
        monitor='val_auc',
        save_best_only=True,
        mode='max'
    )
]

print("\n🚀 Starting training...")

# Train model
try:
    history = model.fit(
        X_train_scaled, y_train,
        batch_size=32,
        epochs=50,  # Reduced epochs for testing
        validation_data=(X_test_scaled, y_test),
        callbacks=callbacks,
        verbose=1
    )
    
    print("✅ Training completed successfully!")
    
    # Evaluate model
    test_predictions = model.predict(X_test_scaled)
    test_auc = roc_auc_score(y_test, test_predictions)
    
    print(f"Test AUC: {test_auc:.4f}")
    
    # Save model manually
    model.save('data/models/fixed_deep_model.keras')
    joblib.dump(scaler, 'data/models/fixed_deep_model_scaler.pkl')
    
    print("✅ Model saved successfully!")
    
    # Test loading the model
    loaded_model = keras.models.load_model('data/models/fixed_deep_model.keras')
    print("✅ Model loaded successfully!")
    
except Exception as e:
    print(f"❌ Error during training: {e}")
    import traceback
    traceback.print_exc()