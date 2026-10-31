from pathlib import Path
import json
import time

import joblib
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)

# SENTINEL AI 9.0 - MODEL COMPARISON
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "creditcard.csv"
RESULT_FILE = BASE_DIR / "model_comparison_results.csv"
MODEL_FILE = BASE_DIR / "xgboost_fraud_model.pkl"

if not DATA_FILE.exists():
    raise FileNotFoundError("creditcard.csv not found!")

print("\nSENTINEL AI 9.0 | ML MODEL COMPARISON")
print("=" * 55)

# 1. Load dataset
df = pd.read_csv(DATA_FILE)
X = df.drop(columns=["Class"])
y = df["Class"]

# 2. Same split for both models
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

fraud_count = int(y_train.sum())
genuine_count = len(y_train) - fraud_count
scale_weight = genuine_count / max(fraud_count, 1)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Fraud training records:", fraud_count)

# 3. Model definitions
models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced_subsample"
    ),
    "XGBoost": XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=scale_weight,
        eval_metric="logloss",
        tree_method="hist",
        random_state=42,
        n_jobs=-1
    )
}

results = []

# 4. Train and evaluate
for name, model in models.items():
    print(f"\nTraining {name}...")
    start = time.time()

    model.fit(X_train, y_train)

    duration = time.time() - start
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.50).astype(int)

    cm = confusion_matrix(
        y_test, predictions, labels=[0, 1]
    )

    result = {
        "Model": name,
        "Precision": precision_score(
            y_test, predictions, zero_division=0
        ),
        "Recall": recall_score(
            y_test, predictions, zero_division=0
        ),
        "F1 Score": f1_score(
            y_test, predictions, zero_division=0
        ),
        "ROC-AUC": roc_auc_score(
            y_test, probabilities
        ),
        "PR-AUC": average_precision_score(
            y_test, probabilities
        ),
        "Training Seconds": round(duration, 2),
        "TN": int(cm[0, 0]),
        "FP": int(cm[0, 1]),
        "FN": int(cm[1, 0]),
        "TP": int(cm[1, 1])
    }

    results.append(result)

    print("Precision:", round(result["Precision"], 4))
    print("Recall:", round(result["Recall"], 4))
    print("F1 Score:", round(result["F1 Score"], 4))
    print("ROC-AUC:", round(result["ROC-AUC"], 4))
    print("PR-AUC:", round(result["PR-AUC"], 4))

    if name == "XGBoost":
        joblib.dump(
            {
                "model": model,
                "features": list(X.columns),
                "model_type": "XGBoost",
                "threshold": 0.50
            },
            MODEL_FILE
        )
        print("XGBoost model saved safely!")

# 5. Save comparison
results_df = pd.DataFrame(results)
results_df.to_csv(RESULT_FILE, index=False)

print("\n" + "=" * 55)
print("FINAL MODEL COMPARISON")
print(results_df.to_string(index=False))

print("\nComparison saved:", RESULT_FILE.name)
print("Existing Random Forest model untouched.")
print("SENTINEL AI 9.0 TRAINING COMPLETE!")