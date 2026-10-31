import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    average_precision_score,
    precision_recall_curve
)

st.set_page_config(
    page_title="SENTINEL AI | ML Performance",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #070b17, #101a35);
    color: white;
}

h1, h2, h3 {
    color: #7cecff !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #142748, #201a45);
    border: 1px solid #36dfff;
    border-radius: 16px;
    padding: 18px;
}

[data-testid="stMetricValue"] {
    color: #61f5df;
}

[data-testid="stSidebar"] {
    background: #10182e;
}
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "real_fraud_model.pkl"
DATA_PATH = BASE_DIR / "creditcard.csv"

st.title("🧠 SENTINEL AI 4.2")
st.subheader("Advanced Machine Learning Performance")
st.caption("Random Forest | Credit Card Fraud Detection")

if not MODEL_PATH.exists() or not DATA_PATH.exists():
    st.error("Model or dataset file not found.")
    st.stop()


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


bundle = load_model()

model = bundle["model"]
features = bundle["features"]

df = load_data()

X = df[features]
y = df["Class"]

# Reproduce the original train/test split
_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Evaluate only on held-out test records
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]

report = classification_report(
    y_test,
    predictions,
    output_dict=True,
    zero_division=0
)

fraud_metrics = report["1"]

precision = fraud_metrics["precision"]
recall = fraud_metrics["recall"]
f1 = fraud_metrics["f1-score"]

pr_auc = average_precision_score(
    y_test,
    probabilities
)

st.success("Real ML Model Loaded Successfully!")

a, b, c, d = st.columns(4)

a.metric("Fraud Precision", f"{precision * 100:.2f}%")
b.metric("Fraud Recall", f"{recall * 100:.2f}%")
c.metric("Fraud F1-Score", f"{f1 * 100:.2f}%")
d.metric("Average Precision", f"{pr_auc:.4f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("🎯 Confusion Matrix")

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    )

    fig = px.imshow(
        cm,
        x=["Genuine", "Fraud"],
        y=["Genuine", "Fraud"],
        text_auto=True,
        color_continuous_scale="Blues",
        labels={
            "x": "Predicted Label",
            "y": "Actual Label",
            "color": "Count"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("📈 Precision-Recall Curve")

    p, r, _ = precision_recall_curve(
        y_test,
        probabilities
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=r,
            y=p,
            mode="lines",
            line=dict(
                color="#00e5ff",
                width=3
            ),
            name="Random Forest"
        )
    )

    fig.update_layout(
        xaxis_title="Recall",
        yaxis_title="Precision",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("⚡ Feature Importance")

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    "Importance",
    ascending=False
).head(15)

fig = px.bar(
    importance_df,
    x="Importance",
    y="Feature",
    orientation="h",
    color="Importance",
    color_continuous_scale="Tealgrn"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(autorange="reversed"),
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📋 Full Classification Report")

report_df = pd.DataFrame(report).transpose()

st.dataframe(
    report_df,
    use_container_width=True
)

st.info(
    "Metrics use the held-out test split from training. "
    "Feature importance shows model-level importance, "
    "not an explanation of an individual prediction."
)

st.caption("SENTINEL AI 4.2 | ML Performance Intelligence")