import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def run_minimal_xgboost():
    csv_path = "backend/sample_employees.csv"
    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # 1. Select core numeric features
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    print(f"Using core numeric features: {numeric_cols}")
    
    # 2. Derive a simple target (9-box grid category 0-8)
    # For this minimal test, we'll just create a dummy target based on Manager_Rating
    # low (<5) = 0, med (5-7) = 1, high (>7) = 2. Same for Potential (using self_rating here as proxy).
    perf = pd.cut(df['Manager_Rating'], bins=[-np.inf, 5, 7, np.inf], labels=[0, 1, 2]).astype(int)
    pot = pd.cut(df['Self_Rating'], bins=[-np.inf, 5, 7, np.inf], labels=[0, 1, 2]).astype(int)
    
    # Target label: 0 to 8
    target = perf * 3 + pot
    
    X = df[numeric_cols].fillna(0)
    y = target.values
    
    # 3. Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Fit XGBClassifier
    print("\nFitting XGBClassifier...")
    model = XGBClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Predict
    print("\nMaking predictions on test set...")
    predictions = model.predict(X_test)
    accuracy = (predictions == y_test).mean()
    
    print(f"\nMinimal Training Successful! Accuracy: {accuracy:.2%}")
    print("Sample Predictions:", predictions[:5])
    print("Actual Labels:     ", y_test[:5])

if __name__ == "__main__":
    run_minimal_xgboost()
