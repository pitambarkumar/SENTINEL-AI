import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
from pathlib import Path
from sklearn.metrics import (
    roc_curve, roc_auc_score,
    precision_recall_curve, average_precision_score,
    confusion_matrix, precision_score, recall_score,
    f1_score
)
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent

@st.cache_resource
def load_model():
    return joblib.load(BASE / "real_fraud_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv(BASE / "creditcard.csv")

def run_upgrade():
    st.divider()
    st.title("🛡️ SENTINEL AI 7.0")
    st.caption("Professional Explainable Fraud Intelligence")

    if not (BASE / "real_fraud_model.pkl").exists():
        st.error("Trained model missing.")
        return
    if not (BASE / "creditcard.csv").exists():
        st.error("Dataset missing.")
        return

    bundle = load_model()
    model = bundle["model"]
    features = list(bundle["features"])
    data = load_data()

    if not hasattr(model, "predict_proba"):
        st.error("Model does not support probabilities.")
        return

    if "Class" not in data or not set(features).issubset(data.columns):
        st.error("Dataset schema does not match model.")
        return

    tab1, tab2, tab3 = st.tabs([
        "🧠 SHAP Explainable AI",
        "📈 ROC Analytics",
        "🎯 Threshold Lab"
    ])

    with tab1:
        st.subheader("Why Did AI Make This Prediction?")
        st.caption(
            "SHAP explains model output contributions, "
            "not the cause of fraud."
        )

        row_id = st.number_input(
            "Transaction Row",
            min_value=0,
            max_value=len(data) - 1,
            value=541,
            key="pro_shap_row"
        )

        if st.button("🧠 Generate SHAP Explanation"):
            try:
                import shap

                X = data.iloc[[int(row_id)]][features]
                probability = float(model.predict_proba(X)[0, 1])

                with st.spinner("Calculating SHAP values..."):
                    explainer = shap.TreeExplainer(model)
                    values = explainer.shap_values(X)

                    if isinstance(values, list):
                        contributions = np.asarray(values[-1])[0]
                    else:
                        arr = np.asarray(values)
                        if arr.ndim == 3:
                            contributions = arr[0, :, 1]
                        elif arr.ndim == 2:
                            contributions = arr[0]
                        else:
                            raise ValueError(
                                "Unsupported SHAP output shape"
                            )

                    if len(contributions) != len(features):
                        raise ValueError(
                            "SHAP feature count mismatch"
                        )

                st.metric(
                    "Estimated Fraud Probability",
                    f"{probability * 100:.2f}%"
                )

                explanation = pd.DataFrame({
                    "Feature": features,
                    "SHAP Contribution": contributions
                })
                explanation["Magnitude"] = (
                    explanation["SHAP Contribution"].abs()
                )
                explanation = explanation.nlargest(
                    12, "Magnitude"
                ).sort_values("SHAP Contribution")

                fig = px.bar(
                    explanation,
                    x="SHAP Contribution",
                    y="Feature",
                    orientation="h",
                    color="SHAP Contribution",
                    color_continuous_scale="RdBu_r",
                    title="Top 12 Feature Contributions"
                )
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

                st.info(
                    "Positive and negative contributions are "
                    "relative to the explainer's model-output "
                    "baseline. They are not necessarily "
                    "percentage-point changes."
                )

            except Exception as exc:
                st.error(f"SHAP analysis failed: {exc}")

    with tab2:
        st.subheader("Advanced Model Evaluation")
        st.warning(
            "Evaluation is valid only if the model was trained "
            "without the selected test rows. Verify the original "
            "training split before presenting these metrics."
        )

        if st.button("📊 Calculate Evaluation Curves"):
            with st.spinner("Evaluating model..."):
                X = data[features]
                y = data["Class"]

                _, X_test, _, y_test = train_test_split(
                    X, y,
                    test_size=0.20,
                    random_state=42,
                    stratify=y
                )

                probs = model.predict_proba(X_test)[:, 1]
                fpr, tpr, _ = roc_curve(y_test, probs)
                auc = roc_auc_score(y_test, probs)
                precision, recall, _ = precision_recall_curve(
                    y_test, probs
                )
                ap = average_precision_score(y_test, probs)

            a, b = st.columns(2)
            a.metric("ROC AUC", f"{auc:.4f}")
            b.metric("Average Precision", f"{ap:.4f}")

            roc_fig = go.Figure()
            roc_fig.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode="lines",
                name="Random Forest"
            ))
            roc_fig.add_trace(go.Scatter(
                x=[0, 1], y=[0, 1],
                mode="lines",
                name="Random Baseline",
                line=dict(dash="dash")
            ))
            roc_fig.update_layout(
                title="ROC Curve",
                xaxis_title="False Positive Rate",
                yaxis_title="True Positive Rate",
                template="plotly_dark"
            )
            st.plotly_chart(roc_fig, use_container_width=True)

            pr_fig = go.Figure()
            pr_fig.add_trace(go.Scatter(
                x=recall, y=precision,
                mode="lines",
                name="Precision-Recall"
            ))
            pr_fig.update_layout(
                title="Precision-Recall Curve",
                xaxis_title="Recall",
                yaxis_title="Precision",
                template="plotly_dark"
            )
            st.plotly_chart(pr_fig, use_container_width=True)

    with tab3:
        st.subheader("Decision Threshold Laboratory")
        st.caption(
            "Explore different decision thresholds without "
            "changing or retraining the saved model."
        )

        threshold = st.slider(
            "Fraud Threshold",
            0.05, 0.95, 0.50, 0.05,
            key="pro_threshold"
        )

        if st.button("⚡ Analyze Threshold"):
            X = data[features]
            y = data["Class"]

            _, X_test, _, y_test = train_test_split(
                X, y,
                test_size=0.20,
                random_state=42,
                stratify=y
            )

            probs = model.predict_proba(X_test)[:, 1]
            predicted = (probs >= threshold).astype(int)

            a, b, c = st.columns(3)
            a.metric(
                "Precision",
                f"{precision_score(y_test, predicted, zero_division=0):.3f}"
            )
            b.metric(
                "Recall",
                f"{recall_score(y_test, predicted, zero_division=0):.3f}"
            )
            c.metric(
                "F1 Score",
                f"{f1_score(y_test, predicted, zero_division=0):.3f}"
            )

            cm = confusion_matrix(
                y_test, predicted, labels=[0, 1]
            )
            fig = px.imshow(
                cm,
                x=["Genuine", "Fraud"],
                y=["Genuine", "Fraud"],
                text_auto=True,
                title="Threshold Confusion Matrix",
                color_continuous_scale="Blues"
            )
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

            st.caption(
                "These results require an independent test set "
                "to be considered reliable."
            )