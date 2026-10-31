import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# STEP 1: Generate synthetic labeled training data
X, y = make_classification(
    n_samples=5000,
    n_features=8,
    n_informative=5,
    n_redundant=1,
    weights=[0.95, 0.05],
    random_state=42
)

columns = [
    "amount_pattern",
    "transaction_frequency",
    "location_risk",
    "device_risk",
    "time_risk",
    "merchant_risk",
    "velocity_risk",
    "account_risk"
]

df = pd.DataFrame(X, columns=columns)
df["is_fraud"] = y

print("Dataset Created:", df.shape)
print(df["is_fraud"].value_counts())

# STEP 2: Separate inputs and target
X = df.drop("is_fraud", axis=1)
y = df["is_fraud"]

# STEP 3: Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# STEP 4: Train Random Forest model
model = RandomForestClassifier(
    n_estimators=150,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# STEP 5: Evaluate model
predictions = model.predict(X_test)

print("\nMODEL EVALUATION")
print(classification_report(y_test, predictions, zero_division=0))

# STEP 6: Save trained model
joblib.dump(model, "fraud_model.pkl")

print("\nModel saved successfully: fraud_model.pkl")