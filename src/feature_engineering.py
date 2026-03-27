# src/feature_engineering.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    
    # Separate features and target
    X = df.drop('default', axis=1)
    y = df['default']
    
    # Convert categorical → numeric
    X = pd.get_dummies(X, drop_first=True)
    
    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, y