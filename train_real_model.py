import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    average_precision_score,
    roc_auc_score
)

# ==========================================
# SENTINEL AI 4.0
# REAL CREDIT CARD FRAUD DETECTION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "creditcard.csv"
MODEL_FILE = BASE_DIR / "real_fraud_model.pkl"

# STEP 1 - Load dataset
print("\n[1/6] Loading real fraud dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset shape:", df.shape)
print("\nFraud distribution:")
print(df["Class"].value_counts())

# STEP 2 - Prepare features and labels
print("\n[2/6] Preparing features...")

X = df.drop(columns=["Class"])
y = df["Class"]

# STEP 3 - Split data
print("\n[3/6] Splitting training and testing data...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# STEP 4 - Train model
print("\n[4/6] Training Random Forest...")
print("This may take several minutes.")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=15,
    min_samples_leaf=2,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Training completed!")

# STEP 5 - Evaluate
print("\n[5/6] Evaluating model...")

predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

print("\n===== CLASSIFICATION REPORT =====")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\n===== CONFUSION MATRIX =====")
print(confusion_matrix(y_test, predictions))

print("\n===== PR-AUC / AVERAGE PRECISION =====")
print(round(average_precision_score(y_test, probabilities), 4))

print("\n===== ROC-AUC =====")
print(round(roc_auc_score(y_test, probabilities), 4))

# STEP 6 - Save model and feature names
print("\n[6/6] Saving trained model...")

joblib.dump(
    {
        "model": model,
        "features": list(X.columns),
        "dataset": "Credit Card Fraud Detection",
        "model_type": "Random Forest"
    },
    MODEL_FILE
)

print("\n==================================")
print("SENTINEL AI 4.0 TRAINING COMPLETE")
print("==================================")
print("Saved model:", MODEL_FILE.name)
print("Total features:", len(X.columns))