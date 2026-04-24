"""
ML Engine — Trains Random Forest, XGBoost, and Decision Tree models.
Automatically selects the best model based on accuracy.
Predicts employee 9-Box Grid position (Performance × Potential → 3×3 grid).
"""

import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Global state for the trained model
_trained_model = None
_feature_columns = None
_scaler = None
_model_info = {}

# 9-Box Grid labels (row = Performance Low→High, col = Potential Low→High)
NINE_BOX_LABELS = {
    (0, 0): {"label": "Bad Hire", "performance": "Low", "potential": "Low", "box": 1},
    (0, 1): {"label": "Up or Out - Grinder", "performance": "Low", "potential": "Medium", "box": 2},
    (0, 2): {"label": "Rough Diamond", "performance": "Low", "potential": "High", "box": 3},
    (1, 0): {"label": "Talent Risk", "performance": "Medium", "potential": "Low", "box": 4},
    (1, 1): {"label": "Core Player", "performance": "Medium", "potential": "Medium", "box": 5},
    (1, 2): {"label": "High Potential", "performance": "Medium", "potential": "High", "box": 6},
    (2, 0): {"label": "Solid Performer", "performance": "High", "potential": "Low", "box": 7},
    (2, 1): {"label": "High Performer", "performance": "High", "potential": "Medium", "box": 8},
    (2, 2): {"label": "Star", "performance": "High", "potential": "High", "box": 9},
}

def _derive_performance_potential(df: pd.DataFrame, numeric_cols: list):
    """
    Derive Performance and Potential scores robustly.
    """
    if not numeric_cols:
        return np.ones(len(df)), np.ones(len(df))

    # Split features roughly: first half → performance, second half → potential
    mid = max(1, len(numeric_cols) // 2)
    perf_features = numeric_cols[:mid]
    pot_features = numeric_cols[mid:] if mid < len(numeric_cols) else numeric_cols[:1]

    # Fill NaNs with 0 before scaling to avoid errors
    df_perf = df[perf_features].fillna(0)
    df_pot = df[pot_features].fillna(0)

    # Simple min-max scaling to 0-1 range, then mean
    perf_scaled = (df_perf - df_perf.min()) / (df_perf.max() - df_perf.min() + 1e-8)
    pot_scaled = (df_pot - df_pot.min()) / (df_pot.max() - df_pot.min() + 1e-8)

    perf_vals = perf_scaled.mean(axis=1).values * 9 + 1
    pot_vals = pot_scaled.mean(axis=1).values * 9 + 1

    return perf_vals, pot_vals

def _score_to_level(score, low_thresh=4, high_thresh=7):
    """Convert a numeric score to Low (0), Medium (1), High (2)."""
    if score < low_thresh: return 0
    elif score < high_thresh: return 1
    else: return 2

def train_models(df: pd.DataFrame):
    """Train models and select best."""
    global _trained_model, _feature_columns, _scaler, _model_info

    # Strictly select only numeric columns
    feature_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
    
    # Remove id/employee columns if accidentally numeric
    exclude = ['id', 'employee_id']
    feature_cols = [c for c in feature_cols if c.lower().strip() not in exclude]

    if len(feature_cols) == 0:
        raise ValueError("No usable numeric columns found.")

    perf_vals, pot_vals = _derive_performance_potential(df, feature_cols)
    targets = np.array([_score_to_level(p) * 3 + _score_to_level(pt) for p, pt in zip(perf_vals, pot_vals)])

    X = df[feature_cols].fillna(0).values
    
    _scaler = StandardScaler()
    X_scaled = _scaler.fit_transform(X)
    _feature_columns = feature_cols

    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=100, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=10),
    }

    results = {}
    for name, model in models.items():
        try:
            if len(X_scaled) < 10:
                model.fit(X_scaled, targets)
                score = model.score(X_scaled, targets)
            else:
                scores = cross_val_score(model, X_scaled, targets, cv=min(3, len(X_scaled) // 3), scoring="accuracy")
                score = scores.mean()
                model.fit(X_scaled, targets)
            results[name] = {"model": model, "accuracy": round(score * 100, 2)}
        except Exception as e:
            results[name] = {"model": None, "accuracy": 0, "error": str(e)}

    best_name = max(results, key=lambda k: results[k]["accuracy"])
    _trained_model = results[best_name]["model"]

    _model_info = {
        "best_model": best_name,
        "models": {k: {"accuracy": v["accuracy"]} for k, v in results.items()},
        "feature_columns": feature_cols,
        "total_employees": len(df),
    }

    return _model_info

def predict_employee(employee_data_json: str):
    """Predict 9-box position."""
    if _trained_model is None:
        raise ValueError("Model not trained.")

    data = json.loads(employee_data_json)
    row = pd.DataFrame([data])

    X = pd.DataFrame()
    for col in _feature_columns:
        X[col] = pd.to_numeric(row.get(col, [0]), errors="coerce").fillna(0)

    X_scaled = _scaler.transform(X.values)
    prediction = int(_trained_model.predict(X_scaled)[0])

    perf_level = prediction // 3
    pot_level = prediction % 3
    grid_info = NINE_BOX_LABELS.get((perf_level, pot_level), NINE_BOX_LABELS[(1, 1)])

    return {
        "prediction": prediction,
        "grid_position": {"row": perf_level, "col": pot_level},
        "label": grid_info["label"],
        "performance": grid_info["performance"],
        "potential": grid_info["potential"],
        "box_number": grid_info["box"],
        "model_used": _model_info.get("best_model", "Unknown"),
    }

def get_model_info():
    return _model_info
