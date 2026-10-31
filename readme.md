# 🛡️ SENTINEL AI 9.0
## Intelligent Credit Card Fraud Detection & Analytics Platform

### Project Overview

SENTINEL AI 9.0 is a machine learning-based fraud detection and analytics platform developed using Python and Streamlit.

The system analyzes anonymized credit card transactions, estimates fraud probabilities, visualizes model performance, and provides explainable AI insights through an interactive dashboard.

### Objectives

- Detect potentially fraudulent credit card transactions.
- Estimate fraud probabilities using machine learning.
- Visualize transaction patterns and risk levels.
- Explain model predictions using SHAP.
- Compare machine learning models.
- Simulate transaction monitoring.
- Store prediction history in SQLite.

### Technologies Used

- Python
- Streamlit
- Pandas and NumPy
- Scikit-learn
- Random Forest Classifier
- Plotly
- SHAP
- SQLite
- Joblib

### Dataset

Credit Card Fraud Detection Dataset

- Total Transactions: 284,807
- Fraud Transactions: 492
- Genuine Transactions: 284,315
- Input Features: 30

The dataset is highly imbalanced, making precision, recall and F1-score important evaluation metrics.

### Major Modules

1. Command Overview
2. Neural Analytics
3. Transaction Monitoring
4. Rule-Based AI Risk Analyzer
5. Threat Intelligence
6. System Control
7. ML Performance Dashboard
8. Ultra Pro Intelligence
9. Live Fraud Monitor
10. Model Comparison
11. Explainable AI Lab
12. Real ML Fraud Detection Engine

### Machine Learning Model

The primary fraud detection model uses Random Forest classification.

The system displays:

- Estimated fraud probability
- Predicted transaction class
- Risk classification
- Confusion matrix
- Precision, recall and F1-score
- Precision-Recall and ROC curves
- Feature importance
- SHAP feature contributions

### Observed Evaluation Metrics

- Precision: 89.53%
- Recall: 78.57%
- F1-Score: 83.70%

These are previously observed dashboard metrics. Independent test-set validity must be verified against the original model training process before treating them as final held-out evaluation results.

### Live Fraud Monitor

The Live Fraud Monitor generates synthetic transactions and simulated risk scores.

Features include:

- Start, Pause and Reset controls
- Automatically updating charts
- Simulated risk alerts
- Transaction history
- CSV export

Note: This module is a demonstration simulation, not a real-time banking connection or ML-powered transaction feed.

### Database

SQLite stores saved prediction history.

Database file: `sentinel_ai.db`

### How to Run

Open a terminal inside the project folder.

Install the required Python dependencies:

```bash
pip install streamlit pandas numpy plotly scikit-learn joblib shap
```

Run the dashboard:

```bash
streamlit run dashboard.py
```

The project requires its supporting Python modules, saved model file and dataset to be available in the project directory.

### Limitations

- The system is an educational prototype.
- It does not connect to real banking infrastructure.
- Synthetic risk scores are not trained ML predictions.
- Predictions do not establish confirmed fraud.
- Real-world deployment would require additional validation, security controls and monitoring.

### Future Scope

- Secure API integration
- Production-grade fraud monitoring
- Model drift detection
- Authentication and role-based access
- Automated model retraining
- Cloud deployment

### Conclusion

SENTINEL AI 9.0 demonstrates the integration of machine learning, explainable AI, interactive analytics, simulated monitoring and database storage in a unified fraud intelligence platform.

**Project Category:** Machine Learning / Data Science / Financial Fraud Detection