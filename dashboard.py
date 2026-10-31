import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import joblib
from pathlib import Path
# =============================================
# SENTINEL AI 3.1 - ULTIMATE HYBRID COMMAND CENTER
# Cyber Command + Glassmorphism + Neural AI
# =============================================

st.set_page_config(
    page_title="SENTINEL AI | Neural Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# CYBER NEON DESIGN SYSTEM
# =============================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 80% 5%, #1a2758 0%, transparent 40%),
        radial-gradient(ellipse at 10% 90%, #251344 0%, transparent 45%),
        #050816;
    color: #edf5ff;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.18;
    background-image:
        linear-gradient(#42e8ff20 1px, transparent 1px),
        linear-gradient(90deg, #42e8ff20 1px, transparent 1px);
    background-size: 45px 45px;
    animation: gridMove 25s linear infinite;
}

@keyframes gridMove {
    from { background-position: 0 0; }
    to { background-position: 45px 45px; }
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111d3c, #070b1c);
    border-right: 1px solid #3b4c80;
}

[data-testid="stSidebar"] * {
    color: #dceaff;
}

h1 {
    font-weight: 900 !important;
    background: linear-gradient(90deg, #ffffff, #65eaff, #ac88ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2, h3 {
    color: #eaf4ff !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(31, 52, 102, 0.75),
        rgba(18, 25, 53, 0.65)
    );
    backdrop-filter: blur(18px);
    border: 1px solid #50669b;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 8px 35px #00000055;
    transition: transform 0.3s, box-shadow 0.3s;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow:
    0 0 20px rgba(0, 229, 255, 0.35),
    0 0 45px rgba(113, 84, 255, 0.25),
    inset 0 0 15px rgba(0, 229, 255, 0.08);
}

[data-testid="stMetricLabel"] {
    color: #a9c2ea;
}

[data-testid="stMetricValue"] {
    color: #6ceaff;
}

div.stButton > button,
div.stDownloadButton > button {
    background: linear-gradient(90deg, #7154ff, #00bfdc);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 700;
    padding: 12px 22px;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    border: 1px solid #88f4ff;
    color: white;
    box-shadow: 0 0 25px #00d9ff55;
}

[data-testid="stDataFrame"] {
    border: 1px solid #435b90;
    border-radius: 16px;
}

.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(
        110deg,
        rgba(26, 47, 101, 0.9),
        rgba(48, 25, 91, 0.85),
        rgba(9, 52, 77, 0.9)
    );
    border: 1px solid #5b6fac;
    border-radius: 26px;
    padding: 36px;
    margin-bottom: 28px;
    box-shadow: 0 0 55px #785bff25;
}

.hero::after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -60px;
    top: -100px;
    background: #00e5ff;
    filter: blur(110px);
    opacity: 0.25;
    animation: pulseGlow 5s ease-in-out infinite alternate;
}

@keyframes pulseGlow {
    from { opacity: 0.12; transform: scale(0.9); }
    to { opacity: 0.35; transform: scale(1.2); }
}

.hero-title {
    color: white;
    font-size: clamp(32px, 5vw, 56px);
    font-weight: 900;
    letter-spacing: 2px;
}

.hero-sub {
    color: #75eaff;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
}

.glass {
    background: rgba(23, 38, 77, 0.55);
    border: 1px solid rgba(116, 169, 255, 0.3);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
}

.neural {
    color: #6ceaff;
    font-weight: 800;
    text-shadow: 0 0 18px #00dfff80;
}

.status {
    color: #55f5bd;
    font-weight: 700;
}

.neural-orb {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    margin: 15px auto;
    background: radial-gradient(
        circle,
        #ffffff 0%,
        #00e5ff 12%,
        #684aff 45%,
        transparent 70%
    );
    box-shadow: 0 0 45px #00e5ff90;
    animation: orbPulse 3s ease-in-out infinite alternate;
}

@keyframes orbPulse {
    from { transform: scale(0.9); opacity: 0.7; }
    to { transform: scale(1.12); opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# =============================================
# SYNTHETIC DEMO DATA
# =============================================

@st.cache_data
def load_demo_data():
    rng = np.random.default_rng(42)
    n = 160

    amounts = rng.integers(300, 150000, n)
    scores = rng.integers(5, 99, n)
    channels = rng.choice(
        ["UPI", "Card", "Net Banking"], n
    )

    data = pd.DataFrame({
        "Transaction ID": [
            f"TX-{1001+i}" for i in range(n)
        ],
        "Amount": amounts,
        "Risk Score": scores,
        "Channel": channels
    })

    def status(score):
        if score >= 70:
            return "HIGH RISK"
        elif score >= 40:
            return "MEDIUM RISK"
        return "LOW RISK"

    data["Status"] = data["Risk Score"].apply(status)
    return data

df = load_demo_data()

COLORS = {
    "HIGH RISK": "#ff5478",
    "MEDIUM RISK": "#ffbf59",
    "LOW RISK": "#00e5df"
}

def chart_style(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#dceaff",
        margin=dict(l=15, r=15, t=40, b=20),
        font=dict(family="Inter")
    )
    return fig

# =============================================
# SIDEBAR NAVIGATION
# =============================================

st.sidebar.markdown("## 🛡️ SENTINEL AI")
st.sidebar.caption("NEURAL INTELLIGENCE PLATFORM")
st.sidebar.divider()

page = st.sidebar.radio(
    "COMMAND CENTER",
    [
        "🏠 Command Overview",
        "📊 Neural Analytics",
        "💳 Transactions",
        "🧠 AI Risk Analyzer",
        "🚨 Threat Intelligence",
        "⚙️ System Control",
        "🧠 ML Performance",
        "🛡️ Ultra Pro Intelligence",
        "📡 Live Fraud Monitor",
        "📊 Model Comparison",
        "🧬 Explainable AI Lab",
    ]
)

st.sidebar.divider()
st.sidebar.success("● DEMO SYSTEM ONLINE")
st.sidebar.caption("SENTINEL AI 9.0 | NEURAL INTELLIGENCE")

# =============================================
# COMMAND OVERVIEW
# =============================================

if page == "🏠 Command Overview":

    st.markdown("""
    <div class="hero">
        <div class="hero-sub">
            NEXT GENERATION FRAUD INTELLIGENCE
        </div>
        <div class="hero-title">
            🛡️ SENTINEL AI 9.0
        </div>
        <p style="color:#c3d7f6;font-size:17px">
            Cyber Command • Glassmorphism • Neural Intelligence
        </p>
        <div class="status">
            ● DEMONSTRATION SYSTEM ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    a, b, c, d = st.columns(4)

    a.metric("Transactions", len(df))
    b.metric(
        "High Risk Alerts",
        int((df["Risk Score"] >= 70).sum())
    )
    c.metric(
        "Average Risk",
        f"{df['Risk Score'].mean():.1f}/100"
    )
    d.metric(
        "Total Volume",
        f"₹{df['Amount'].sum():,}"
    )

    left, right = st.columns([1.6, 1])

    with left:
        st.subheader("⚡ Neural Risk Intelligence")

        fig = px.area(
            df,
            x="Transaction ID",
            y="Risk Score",
            title="Transaction Risk Signal"
        )

        fig.update_traces(
            line_color="#00e5ff",
            fillcolor="rgba(0,229,255,0.12)"
        )

        st.plotly_chart(
            chart_style(fig),
            width="stretch"
        )

    with right:
        st.subheader("🎯 Threat Distribution")

        counts = df["Status"].value_counts().reset_index()
        counts.columns = ["Status", "Count"]

        fig = px.pie(
            counts,
            names="Status",
            values="Count",
            hole=0.72,
            color="Status",
            color_discrete_map=COLORS
        )

        st.plotly_chart(
            chart_style(fig),
            width="stretch"
        )

    st.subheader("🧠 Neural Intelligence Core")

    st.markdown("""
    <div class="glass" style="text-align:center">
        <div class="neural-orb"></div>
        <h2 class="neural">SENTINEL NEURAL CORE</h2>
        <p style="color:#a9c4eb">
            Visual simulation of the intelligence engine
        </p>
        <p class="status">● VISUAL DEMO ACTIVE</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🚨 Recent Transaction Intelligence")
    st.dataframe(df.tail(12), width="stretch", hide_index=True)

# =============================================
# NEURAL ANALYTICS
# =============================================

elif page == "📊 Neural Analytics":

    st.title("📊 Neural Analytics")
    st.caption("Interactive synthetic transaction analysis")

    fig = px.scatter(
        df,
        x="Amount",
        y="Risk Score",
        color="Status",
        size="Amount",
        hover_data=["Transaction ID", "Channel"],
        color_discrete_map=COLORS,
        title="Transaction Behavior Intelligence"
    )

    st.plotly_chart(chart_style(fig), width="stretch")

    fig2 = px.histogram(
        df,
        x="Channel",
        color="Status",
        barmode="group",
        color_discrete_map=COLORS,
        title="Payment Channel Risk Distribution"
    )

    st.plotly_chart(chart_style(fig2), width="stretch")

    fig3 = px.box(
        df,
        x="Channel",
        y="Amount",
        color="Channel",
        title="Transaction Amount Distribution"
    )

    st.plotly_chart(chart_style(fig3), width="stretch")

# =============================================
# TRANSACTION MONITORING
# =============================================

elif page == "💳 Transactions":

    st.title("💳 Transaction Monitoring")

    choice = st.selectbox(
        "Risk Classification",
        ["All", "HIGH RISK", "MEDIUM RISK", "LOW RISK"]
    )

    channel = st.selectbox(
        "Payment Channel",
        ["All", "UPI", "Card", "Net Banking"]
    )

    filtered = df.copy()

    if choice != "All":
        filtered = filtered[filtered["Status"] == choice]

    if channel != "All":
        filtered = filtered[filtered["Channel"] == channel]

    st.metric("Matching Transactions", len(filtered))
    st.dataframe(filtered, width="stretch", hide_index=True)

    st.download_button(
        "Export CSV Report",
        filtered.to_csv(index=False),
        "sentinel_transactions.csv",
        "text/csv"
    )

# =============================================
# AI RISK ANALYZER - RULE BASED DEMO
# =============================================

elif page == "🧠 AI Risk Analyzer":

    st.title("🧠 AI Risk Analyzer")
    st.info("Rule-based demonstration. ML model not connected yet.")

    amount = st.number_input(
        "Transaction Amount (₹)",
        min_value=0,
        value=5000
    )

    unusual = st.checkbox("Unusual Transaction Pattern")
    foreign = st.checkbox("Unfamiliar Location")
    rapid = st.checkbox("Multiple Rapid Transactions")

    if st.button("⚡ INITIATE NEURAL SCAN"):

        risk = min(
            100,
            round(
                10 + amount / 2000
                + (25 if unusual else 0)
                + (20 if foreign else 0)
                + (20 if rapid else 0)
            )
        )

        st.metric("Illustrative Risk Score", f"{risk}/100")

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk,
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#00e5ff"},
                    "bgcolor": "#111b35",
                    "steps": [
                        {"range": [0, 40], "color": "#104c50"},
                        {"range": [40, 70], "color": "#675020"},
                        {"range": [70, 100], "color": "#69243f"}
                    ]
                }
            )
        )

        fig.update_layout(height=350)
        st.plotly_chart(chart_style(fig), width="stretch")

        if risk >= 70:
            st.error("HIGH RISK — Manual Review Recommended")
        elif risk >= 40:
            st.warning("MEDIUM RISK — Additional Verification")
        else:
            st.success("LOW RISK — No Rule-Based Alert")

        st.caption(
            "The displayed score is illustrative and is "
            "not a trained ML fraud probability."
        )

# =============================================
# THREAT INTELLIGENCE
# =============================================

elif page == "🚨 Threat Intelligence":

    st.title("🚨 Threat Intelligence Center")
    st.caption("Synthetic demonstration alerts")

    threats = df[df["Risk Score"] >= 70]

    a, b, c = st.columns(3)

    a.metric("High Risk Alerts", len(threats))
    b.metric("Maximum Risk", f"{df['Risk Score'].max()}/100")
    c.metric(
        "Flagged Volume",
        f"₹{threats['Amount'].sum():,}"
    )

    st.subheader("Flagged Transactions")
    st.dataframe(threats, width="stretch", hide_index=True)

    st.warning(
        "These are simulated risk alerts, "
        "not confirmed fraud cases."
    )

# =============================================
# SYSTEM CONTROL
# =============================================

elif page == "⚙️ System Control":

    st.title("⚙️ System Control")

    st.markdown("""
    <div class="glass">
        <h2 class="neural">SENTINEL AI 9.0</h2>
        <p>Ultimate Hybrid Intelligence Command Center</p>
        <p class="status">● DEMO SYSTEM OPERATIONAL</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("Platform: SENTINEL AI")
    st.write("Version: 9.0 | Neural Intelligence")
    st.write("Interface: Cyber Command + Glassmorphism + Neural")
    st.write(
        "Datasets: Synthetic dashboard and "
        "real credit-card fraud dataset"
    )
    st.write(
        "Detection: Rule-based demonstration "
        "and trained Random Forest"
    )
    st.write("Machine Learning: Integrated")
    st.write(
        "Last Render:",
        datetime.now().strftime("%d %B %Y %H:%M")
    )
    # ==========================================
# SENTINEL AI - ML MODEL INFORMATION
# ==========================================

import os
import joblib

st.sidebar.divider()
st.sidebar.markdown("### 🧠 Machine Learning Engine")

if os.path.exists("fraud_model.pkl"):
    st.sidebar.success("ML Model Loaded File Available")

    if st.sidebar.button("🔍 Check ML Model"):
        model = joblib.load("fraud_model.pkl")

        st.sidebar.write("Algorithm: Random Forest")
        st.sidebar.write(
            "Features:",
            model.n_features_in_
        )
        st.sidebar.success("Model loaded successfully!")
else:
    st.sidebar.error("ML Model File Not Found")

    # ================================================
# SENTINEL AI 4.1 - REAL ML FRAUD DETECTION ENGINE
# ================================================
from pathlib import Path
from database import init_database, save_transaction, get_transactions

init_database()

st.sidebar.divider()
st.sidebar.markdown("### 🔬 Real Fraud Detection")

real_ml_page = st.sidebar.checkbox(
    "Open Real ML Engine",
    key="real_ml_engine"
)

if real_ml_page:
    st.markdown("---")
    st.title("🔬 SENTINEL AI | Real Fraud Detection")
    st.caption(
        "Random Forest predictions on anonymized "
        "credit-card transaction data"
    )

    project_dir = Path(__file__).resolve().parent
    model_path = project_dir / "real_fraud_model.pkl"
    csv_path = project_dir / "creditcard.csv"

    if not model_path.exists():
        st.error("real_fraud_model.pkl not found.")

    elif not csv_path.exists():
        st.error("creditcard.csv not found.")

    else:
        @st.cache_resource
        def load_real_model(path):
            return joblib.load(path)

        @st.cache_data
        def load_real_data(path):
            return pd.read_csv(path)

        bundle = load_real_model(str(model_path))
        real_model = bundle["model"]
        feature_names = bundle["features"]

        real_df = load_real_data(str(csv_path))

        st.success("Real ML model loaded successfully!")

        c1, c2, c3 = st.columns(3)

        c1.metric("Dataset Transactions", len(real_df))
        c2.metric(
            "Actual Fraud Cases",
            int(real_df["Class"].sum())
        )
        c3.metric("ML Features", len(feature_names))

        st.markdown("### 💳 Select Transaction")

        transaction_index = st.number_input(
            "Transaction Row Number",
            min_value=0,
            max_value=len(real_df) - 1,
            value=0,
            step=1
        )

        selected_row = real_df.iloc[
            int(transaction_index)
        ]

        current_prediction = st.session_state.get(
            "last_prediction"
        )
        if (
            current_prediction is not None
            and int(current_prediction["transaction_id"])
            != int(transaction_index)
        ):
            st.session_state.pop("last_prediction", None)

        transaction_features = (
            real_df.loc[
                [int(transaction_index)],
                feature_names
            ]
        )

        st.write(
            "Transaction Amount:",
            selected_row["Amount"]
        )

        if st.button("⚡ RUN REAL ML PREDICTION"):

            probability = float(
                real_model.predict_proba(
                    transaction_features
                )[0][1]
            )

            prediction = int(
                real_model.predict(
                    transaction_features
                )[0]
            )
           # SENTINEL AI - Transaction Risk Classification
            if probability < 0.20:
                risk_level = "LOW"
            elif probability < 0.50:
                risk_level = "MEDIUM"
            elif probability < 0.80:
                risk_level = "HIGH"
            else:
                risk_level = "CRITICAL"

            st.session_state["last_prediction"] = {
                "transaction_id": int(transaction_index),
                "amount": float(selected_row["Amount"]),
                "fraud_probability": float(probability),
                "risk_score": float(probability * 100),
                "prediction": int(prediction),
                "risk_level": risk_level
            }

            st.markdown("### 🧠 Model Prediction")
            st.metric(          
                    "Estimated Fraud Probability",
                    f"{probability * 100:.2f}%"
                )
# SENTINEL AI - CYBER NEON RISK CARD
            risk_colors = {
                "LOW": "#00E5FF",
                "MEDIUM": "#FFD166",
                "HIGH": "#FF8C42",
                "CRITICAL": "#FF4560"
            }
            if prediction == 1:
                st.error("MODEL PREDICTION: POTENTIAL FRAUD")
            else:
                st.success("MODEL PREDICTION: GENUINE")

            actual = int(selected_row["Class"])

            st.info(
                "Actual Dataset Label: "
                + ("FRAUD" if actual == 1 else "GENUINE")
            )

            st.caption(
                "Educational ML demonstration. "
                "Predictions are not guaranteed and "
                "the selected row may have been used "
                "during model training."
            )

            risk_color = risk_colors[risk_level]

            st.markdown("### 🛡️ AI Fraud Risk Assessment")

            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #101D35, #1A3050);
                    border: 2px solid {risk_color};
                    border-radius: 18px;
                    padding: 25px;
                    text-align: center;
                    box-shadow: 0 0 20px {risk_color}44;
                ">
                    <h3 style="color: #EAF4FF;">
                        TRANSACTION RISK LEVEL
                    </h3>
                    <h1 style="color: {risk_color};">
                        {risk_level}
                    </h1>
                    <p style="color: #B8CDE0;">
                        Estimated Fraud Probability:
                        {probability * 100:.2f}%
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            fig = go.Figure(
                    go.Indicator(
                        mode="gauge+number",
                        value=probability * 100,
                        number={"suffix": "%"},
                        gauge={
                            "axis": {"range": [0, 100]},
                            "bar": {"color": "#00e5ff"},
                            "bgcolor": "#111b35",
                            "steps": [
                                {
                                    "range": [0, 40],
                                    "color": "#104c50"
                                },
                                {
                                    "range": [40, 70],
                                    "color": "#675020"
                                },
                                {
                                    "range": [70, 100],
                                    "color": "#69243f"
                                }
                            ]
                        }
                    )
                )

            fig.update_layout(height=350)

            st.plotly_chart(
                        chart_style(fig),
                        width="stretch"
                    )

            
            # SENTINEL AI - CLEAR NEON INPUT FIELDS
        if st.button("💾 Save Prediction to Database"):
             data = st.session_state.get("last_prediction")  

             if data is None:
                st.warning("Please run ML prediction first.")
             elif int(data["transaction_id"]) != int(transaction_index):
                st.warning(
                    "Selected transaction has changed. "
                    "Run prediction again before saving."
                )
             else:
                existing_rows = get_transactions()
                existing_ids = {
                    int(item["transaction_id"])
                    if isinstance(item, dict)
                    else int(item[1])
                    for item in existing_rows
                }

                if int(data["transaction_id"]) in existing_ids:
                    st.info(
                        "This transaction is already saved. "
                        "No duplicate record was created."
                    )
                else:
                    save_transaction(
                        data["transaction_id"],
                        data["amount"],
                        data["fraud_probability"],
                        data["risk_score"],
                        data["prediction"]
                    )

                    updated_rows = get_transactions()
                    updated_ids = {
                        int(item["transaction_id"])
                        if isinstance(item, dict)
                        else int(item[1])
                        for item in updated_rows
                    }

                    if int(data["transaction_id"]) in updated_ids:
                        st.success(
                            "Prediction saved successfully!"
                        )
                    else:
                        st.error(
                            "Save could not be verified."
                        )

        st.markdown("### 📜 Saved Prediction History")

        saved_rows = get_transactions()

        if saved_rows:
            history_df = pd.DataFrame(saved_rows)
            st.dataframe(
                history_df,
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("No predictions saved yet.")

        
st.markdown("""
<style>
div[data-testid="stNumberInput"] input {
    background-color: #101d35 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 2px solid #00e5ff !important;
    border-radius: 10px !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    padding: 12px !important;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 16px rgba(0,229,255,0.45) !important;
}

div[data-testid="stNumberInput"] button {
    background-color: #192846 !important;
    color: #ffffff !important;
}

div[data-testid="stNumberInput"] label {
    color: #a5f3fc !important;
    font-weight: 700 !important;
    font-size: 16px !important;
}
</style>
""", unsafe_allow_html=True)
# ==========================================
# SENTINEL AI 5.0 - ML PERFORMANCE INTEGRATION
# ==========================================

st.sidebar.divider()
st.sidebar.markdown("### 📊 ML Intelligence")

if page == "🧠 ML Performance":
    import time

    with st.spinner("🧠 Initializing SENTINEL AI Intelligence..."):
        progress = st.progress(0, text="Starting AI visualization sequence...")

        stages = [
            "🔐 Establishing secure analytics session...",
            "🧠 Preparing machine learning dashboard...",
            "📊 Initializing Confusion Matrix...",
            "📈 Preparing Precision-Recall Curve...",
            "⚡ Loading Feature Importance visualization...",
            "✅ ML Intelligence Dashboard Ready!"
        ]

        for i in range(101):
            stage = min(i * len(stages) // 101, len(stages) - 1)
            progress.progress(i, text=stages[stage])
            time.sleep(0.015)

        progress.empty()

    st.session_state["show_ml_performance"] = True

if st.sidebar.button("🏠 Back to Command Center"):
    st.session_state["show_ml_performance"] = False

if (
    page == "🧠 ML Performance"
    and st.session_state.get("show_ml_performance", False)
):
    from pathlib import Path
    import joblib
    model_path = Path(__file__).resolve().parent / "real_fraud_model.pkl"
    csv_path = Path(__file__).resolve().parent / "creditcard.csv"

    st.markdown("---")
    st.title("📈 SENTINEL AI 5.0 | ML Performance")
    st.caption("Real Random Forest Model Evaluation")

    from sklearn.model_selection import train_test_split
    from sklearn.metrics import (
        confusion_matrix,
        classification_report,
        average_precision_score,
        precision_recall_curve
    )

    if not model_path.exists() or not csv_path.exists():
        st.error("Model or dataset missing.")
    else:
        bundle = joblib.load(str(model_path))
       
        ml_model = bundle["model"]
        ml_features = bundle["features"]

        dataset = pd.read_csv(str(csv_path))

        X = dataset[ml_features]
        y = dataset["Class"]

        _, X_test, _, y_test = train_test_split(
            X, y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

        y_pred = ml_model.predict(X_test)
        y_prob = ml_model.predict_proba(X_test)[:, 1]

        report = classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0
        )

        fraud = report["1"]

        a, b, c, d = st.columns(4)

        a.metric("Fraud Precision", f"{fraud['precision']*100:.2f}%")
        b.metric("Fraud Recall", f"{fraud['recall']*100:.2f}%")
        c.metric("Fraud F1", f"{fraud['f1-score']*100:.2f}%")
        d.metric(
            "Average Precision",
            f"{average_precision_score(y_test, y_prob):.4f}"
        )

        left, right = st.columns(2)
        with left:
            st.subheader("🎯 Confusion Matrix")

            cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

            fig_cm = px.imshow(
                cm,
                x=["Genuine", "Fraud"],
                y=["Genuine", "Fraud"],
                text_auto=True,
                color_continuous_scale=[
                    [0, "#10243A"],
                    [0.5, "#087EAE"],
                    [1, "#00E5FF"]
                ]
            )

            fig_cm.update_layout(
                template="plotly_dark",
                paper_bgcolor="#050816",
                plot_bgcolor="#0B1530",
                font=dict(color="#EAF4FF")
            )

            st.plotly_chart(fig_cm, width="stretch")
        with right:


      
            st.subheader("📉 Precision-Recall Curve")

            precision, recall, _ = precision_recall_curve(
                y_test, y_prob
            )

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=recall,
                y=precision,
                mode="lines",
                line=dict(color="#00e5ff", width=3)
            ))

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Recall",
                yaxis_title="Precision"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.subheader("⚡ Feature Importance")

        importance = pd.DataFrame({
            "Feature": ml_features,
            "Importance": ml_model.feature_importances_
        })

        importance = importance.sort_values(
            "Importance", ascending=False
        ).head(15)

        fig = px.bar(
            importance,
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Tealgrn"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#050816",
            plot_bgcolor="#0B1530",
            font=dict(color="#EAF4FF"),
            xaxis=dict(gridcolor="rgba(0,229,255,0.12)"),
            yaxis=dict(gridcolor="rgba(0,229,255,0.12)"),
            margin=dict(l=20, r=20, t=30, b=20)
        )

        fig.update_traces(
            marker_line_color="#00E5FF",
            marker_line_width=1
        )
        st.plotly_chart(fig, width="stretch")

        st.info(
            "Evaluation uses a reproducible stratified "
            "20% test split (random_state=42). "
            "The saved model must have been trained "
            "using the matching split."
        )
# ============================================================
# SENTINEL AI 6.0 - ULTRA PRO INTELLIGENCE EXTENSION
# AI Explanations | Smart Alerts | Threshold Simulator | Export
# ============================================================

import io
from datetime import datetime as sentinel_datetime
if page == "🛡️ Ultra Pro Intelligence":
    st.divider()        
    st.markdown("## 🛡️ SENTINEL AI | ULTRA PRO INTELLIGENCE")
    st.caption("Advanced Fraud Intelligence & Decision Support")

    ultra_tab1, ultra_tab2, ultra_tab3, ultra_tab4 = st.tabs([
        "🧠 AI Explanation",
        "🚨 Smart Alert Center",
        "🎯 Threshold Simulator",
        "📥 Intelligence Reports"
    ])

    # ------------------------------------------------------------
    # LOAD EXISTING MODEL SAFELY
    # ------------------------------------------------------------

    @st.cache_resource
    def ultra_load_model(model_file):
        return joblib.load(model_file)


    @st.cache_data
    def ultra_load_dataset(csv_file):
        return pd.read_csv(csv_file)


    ultra_folder = Path(__file__).resolve().parent
    ultra_model_file = ultra_folder / "real_fraud_model.pkl"
    ultra_csv_file = ultra_folder / "creditcard.csv"

    ultra_ready = (
        ultra_model_file.exists()
        and ultra_csv_file.exists()
    )

    if ultra_ready:
        ultra_bundle = ultra_load_model(str(ultra_model_file))
        ultra_model = ultra_bundle["model"]
        ultra_features = ultra_bundle["features"]
    else:
        st.warning("Real ML model or dataset is unavailable.")

    # ------------------------------------------------------------
    # TAB 1 - AI PREDICTION EXPLANATION
    # ------------------------------------------------------------

    with ultra_tab1:
        st.subheader("🧠 AI Decision Explanation")

        if not ultra_ready:
            st.info("Load the trained model and dataset first.")
        else:
            last = st.session_state.get("last_prediction")

            if not last:
                st.info(
                    "Run a prediction in Real ML Engine first."
                )
            else:
                row_id = int(last["transaction_id"])
                real_data = ultra_load_dataset(str(ultra_csv_file))

                if row_id < 0 or row_id >= len(real_data):
                    st.error("Selected transaction is unavailable.")
                else:
                    row = real_data.iloc[[row_id]][ultra_features]
                    original_probability = float(
                        ultra_model.predict_proba(row)[0, 1]
                    )

                    st.metric(
                        "Estimated Fraud Probability",
                        f"{original_probability * 100:.2f}%"
                    )

                    st.markdown("### 🔍 Feature Sensitivity Analysis")

                    # This is a perturbation-based explanation.
                    # It is not SHAP or a causal explanation.
                    baseline = real_data[ultra_features].median()
                    feature_effects = []

                    for feature in ultra_features:
                        modified = row.copy()
                        modified.loc[:, feature] = baseline[feature]

                        changed_probability = float(
                            ultra_model.predict_proba(modified)[0, 1]
                        )

                        feature_effects.append({
                            "Feature": feature,
                            "Probability Change (pp)": (
                                original_probability
                                - changed_probability
                            ) * 100
                        })

                    effects_df = pd.DataFrame(feature_effects)
                    effects_df["Magnitude"] = (
                        effects_df["Probability Change (pp)"].abs()
                    )

                    effects_df = effects_df.sort_values(
                        "Magnitude", ascending=False
                    ).head(10)

                    fig = px.bar(
                        effects_df,
                        x="Probability Change (pp)",
                        y="Feature",
                        orientation="h",
                        color="Probability Change (pp)",
                        color_continuous_scale="RdBu_r",
                        title="Top 10 Feature Sensitivities"
                    )

                    fig.update_layout(
                        template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        height=450,
                        yaxis={"categoryorder": "total ascending"}
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                    st.caption(
                        "Each feature is individually replaced by "
                        "its dataset median. Positive changes indicate "
                        "higher estimated fraud probability for the "
                        "original value. Results are model sensitivities, "
                        "not proof of fraud or causal effects."
                    )

    # ------------------------------------------------------------
    # TAB 2 - SMART ALERT CENTER
    # ------------------------------------------------------------

    with ultra_tab2:
        st.subheader("🚨 Smart Fraud Alert Center")

        alert_rows = get_transactions()

        if alert_rows:
            alert_df = pd.DataFrame(alert_rows)

            alert_df["Fraud Probability %"] = (
                pd.to_numeric(
                    alert_df["fraud_probability"],
                    errors="coerce"
                ) * 100
            )

            alert_df["Alert Level"] = alert_df[
                "Fraud Probability %"
            ].apply(
                lambda x:
                    "CRITICAL" if x >= 80 else
                    "HIGH" if x >= 50 else
                    "MEDIUM" if x >= 20 else
                    "LOW"
            )

            critical_count = int(
                (alert_df["Alert Level"] == "CRITICAL").sum()
            )
            high_count = int(
                (alert_df["Alert Level"] == "HIGH").sum()
            )
            total_count = len(alert_df)

            a1, a2, a3 = st.columns(3)

            a1.metric("Saved Predictions", total_count)
            a2.metric("High Risk Alerts", high_count)
            a3.metric("Critical Alerts", critical_count)

            st.markdown("### 📡 Alert Monitoring")

            alert_filter = st.selectbox(
                "Filter by Risk",
                ["ALL", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
                key="ultra_alert_filter"
            )

            if alert_filter == "ALL":
                filtered_alerts = alert_df
            else:
                filtered_alerts = alert_df[
                    alert_df["Alert Level"] == alert_filter
                ]

            st.dataframe(
                filtered_alerts,
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                "Alerts are based on saved model predictions, "
                "not independently verified fraud cases."
            )
        else:
            st.info("No saved predictions available.")

    # ------------------------------------------------------------
    # TAB 3 - RISK THRESHOLD SIMULATOR
    # ------------------------------------------------------------

    with ultra_tab3:
        st.subheader("🎯 AI Risk Threshold Simulator")

        threshold = st.slider(
            "Fraud Decision Threshold",
            min_value=0.01,
            max_value=0.99,
            value=0.50,
            step=0.01,
            key="ultra_threshold"
        )

        last = st.session_state.get("last_prediction")

        if last:
            probability = float(last["fraud_probability"])

            c1, c2 = st.columns(2)

            c1.metric(
                "Fraud Probability",
                f"{probability * 100:.2f}%"
            )

            c2.metric(
                "Selected Threshold",
                f"{threshold * 100:.0f}%"
            )

            if probability >= threshold:
                st.error(
                    "🚨 SIMULATED DECISION: FLAG FOR REVIEW"
                )
            else:
                st.success(
                    "✅ SIMULATED DECISION: BELOW THRESHOLD"
                )

            st.progress(
                min(max(probability, 0.0), 1.0)
            )

            st.caption(
                "This simulator does not retrain the model, "
                "change the saved prediction, or modify the database."
            )
        else:
            st.info("Run a prediction first.")

    # ------------------------------------------------------------
    # TAB 4 - INTELLIGENCE REPORTS
    # ------------------------------------------------------------

    with ultra_tab4:
        st.subheader("📥 Intelligence Report Center")

        report_rows = get_transactions()

        if report_rows:
            report_df = pd.DataFrame(report_rows)

            st.metric(
                "Total Saved Records",
                len(report_df)
            )

            st.dataframe(
                report_df,
                use_container_width=True,
                hide_index=True
            )

            csv_bytes = report_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="📥 DOWNLOAD TRANSACTION REPORT",
                data=csv_bytes,
                file_name=(
                    "sentinel_ai_report_"
                    + sentinel_datetime.now().strftime("%Y%m%d")
                    + ".csv"
                ),
                mime="text/csv",
                key="ultra_report_download"
            )

            st.success("Intelligence report ready.")
        else:
            st.info("Save predictions to generate a report.")

    st.divider()

    st.caption(
        "SENTINEL AI 6.0 | Advanced ML Demonstration "
        "| Educational Fraud Intelligence Platform"
    )

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# SENTINEL AI 8.0 - LIVE DEMO MONITOR
# Synthetic transactions only

def run_live_monitor():
    st.divider()
    st.title("🛡️ SENTINEL AI 8.0")
    st.caption("LIVE FRAUD MONITORING | SIMULATION MODE")
    st.info("Educational simulation — not live banking data.")

    if "live_transactions" not in st.session_state:
        st.session_state.live_transactions = []

    if "live_running" not in st.session_state:
        st.session_state.live_running = False

    if "live_counter" not in st.session_state:
        st.session_state.live_counter = 0

    a, b, c = st.columns(3)

    if a.button("▶ START", key="live_start"):
        st.session_state.live_running = True

    if b.button("⏸ PAUSE", key="live_pause"):
        st.session_state.live_running = False

    if c.button("🔄 RESET", key="live_reset"):
        st.session_state.live_running = False
        st.session_state.live_transactions = []
        st.session_state.live_counter = 0

    @st.fragment(run_every="2s")
    def monitoring_panel():
        if st.session_state.live_running:
            rng = np.random.default_rng()
            st.session_state.live_counter += 1

            amount = int(rng.integers(100, 100000))
            risk = int(rng.integers(1, 100))
            channel = str(rng.choice(
                ["UPI", "CARD", "NET BANKING"]
            ))

            if risk >= 70:
                status = "HIGH RISK"
            elif risk >= 40:
                status = "MEDIUM RISK"
            else:
                status = "LOW RISK"

            transaction = {
                "ID": f"LIVE-{st.session_state.live_counter:05d}",
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Amount": amount,
                "Channel": channel,
                "Risk Score": risk,
                "Status": status
            }

            st.session_state.live_transactions.append(
                transaction
            )

            # Keep the latest 200 demo records
            st.session_state.live_transactions = (
                st.session_state.live_transactions[-200:]
            )

        records = st.session_state.live_transactions

        if st.session_state.live_running:
            st.success("● SIMULATION RUNNING")
        else:
            st.warning("● SIMULATION PAUSED")

        if not records:
            st.info("Press START to generate demo transactions.")
            return

        df = pd.DataFrame(records)

        high = int((df["Risk Score"] >= 70).sum())
        medium = int(
            df["Risk Score"].between(40, 69).sum()
        )

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Transactions", len(df))
        m2.metric("High Risk", high)
        m3.metric("Medium Risk", medium)
        m4.metric(
            "Average Risk",
            f"{df['Risk Score'].mean():.1f}%"
        )

        st.subheader("📈 Live Risk Intelligence")

        fig = px.line(
            df,
            x="ID",
            y="Risk Score",
            markers=True,
            title="Simulated Transaction Risk"
        )

        fig.update_traces(line_color="#00E5FF")

        fig.add_hline(
            y=70,
            line_dash="dash",
            line_color="#FF4560"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#050816",
            plot_bgcolor="#101D35",
            yaxis_range=[0, 100],
            height=360
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("🚨 Smart Alert Center")

        alerts = df[df["Risk Score"] >= 70]

        if not alerts.empty:
            st.error(
                f"{len(alerts)} simulated high-risk alerts"
            )
            st.dataframe(
                alerts.iloc[::-1].head(15),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No high-risk demo alerts yet.")

        st.subheader("💳 Recent Transactions")

        st.dataframe(
            df.iloc[::-1].head(20),
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "📥 EXPORT LIVE REPORT",
            data=df.to_csv(index=False),
            file_name="sentinel_live_demo.csv",
            mime="text/csv",
            key="live_export"
        )

        st.caption(
            "Risk scores are randomly simulated. "
            "No trained ML prediction is performed here."
        )

    monitoring_panel()
if page == "📡 Live Fraud Monitor":
    run_live_monitor()
    
# SENTINEL AI 9.0 - Model Comparison
from model_comparison_dashboard import run_model_comparison

if page == "📊 Model Comparison":
    run_model_comparison()
    # SENTINEL AI 7.0 - Explainable AI Lab
from sentinel_pro_upgrade import run_upgrade

if page == "🧬 Explainable AI Lab":
    run_upgrade()

    # ============================================================
# SENTINEL AI 9.0 — FINAL PREMIUM UI POLISH
# Visual styling only | Existing functionality preserved
# ============================================================

st.markdown("""
<style>
/* Premium navigation */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101b3b 0%, #080d20 100%);
    border-right: 1px solid rgba(0, 229, 255, 0.24);
    box-shadow: 8px 0 40px rgba(0, 0, 0, 0.25);
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    border: 1px solid transparent;
    border-radius: 12px;
    padding: 9px 12px;
    margin-bottom: 5px;
    transition: background 0.2s ease, border-color 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(0, 229, 255, 0.09);
    border-color: rgba(0, 229, 255, 0.25);
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(
        90deg,
        rgba(0, 229, 255, 0.17),
        rgba(113, 84, 255, 0.14)
    );
    border-color: rgba(0, 229, 255, 0.45);
}

/* Main workspace */
.block-container {
    max-width: 1500px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

/* Premium headings */
h1 {
    letter-spacing: -0.6px;
    font-weight: 900 !important;
}

h2, h3 {
    letter-spacing: 0.2px;
}

/* Glassmorphism metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(28, 48, 95, 0.85),
        rgba(13, 22, 49, 0.9)
    );
    border: 1px solid rgba(94, 167, 255, 0.35);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.2);
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(0, 229, 255, 0.7);
    box-shadow: 0 10px 35px rgba(0, 229, 255, 0.14);
}

/* Premium tabs */
button[data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    font-weight: 700;
    padding: 12px 18px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #68efff !important;
    background: rgba(0, 229, 255, 0.09);
}

/* Input fields */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div {
    border-radius: 11px;
    border-color: rgba(0, 229, 255, 0.35);
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 14px;
    overflow: hidden;
}

/* Chart containers */
[data-testid="stPlotlyChart"] {
    border: 1px solid rgba(90, 145, 225, 0.15);
    border-radius: 16px;
    padding: 8px;
    background: rgba(12, 22, 48, 0.22);
}

/* Buttons */
div.stButton > button,
div.stDownloadButton > button {
    border-radius: 12px;
    font-weight: 700;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 22px rgba(0, 229, 255, 0.3);
}

/* Mobile / narrow screens */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 22px;
        border-radius: 18px;
    }

    .hero-title {
        font-size: 30px;
        letter-spacing: 0;
    }

    [data-testid="stMetric"] {
        padding: 14px;
    }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SENTINEL AI 9.0 — FINAL PREMIUM UI POLISH
# Visual styling only | Existing functionality preserved
# ============================================================

st.markdown("""
<style>
/* Premium navigation */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101b3b 0%, #080d20 100%);
    border-right: 1px solid rgba(0, 229, 255, 0.24);
    box-shadow: 8px 0 40px rgba(0, 0, 0, 0.25);
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    border: 1px solid transparent;
    border-radius: 12px;
    padding: 9px 12px;
    margin-bottom: 5px;
    transition: background 0.2s ease, border-color 0.2s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(0, 229, 255, 0.09);
    border-color: rgba(0, 229, 255, 0.25);
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(
        90deg,
        rgba(0, 229, 255, 0.17),
        rgba(113, 84, 255, 0.14)
    );
    border-color: rgba(0, 229, 255, 0.45);
}

/* Main workspace */
.block-container {
    max-width: 1500px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

/* Premium headings */
h1 {
    letter-spacing: -0.6px;
    font-weight: 900 !important;
}

h2, h3 {
    letter-spacing: 0.2px;
}

/* Glassmorphism metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        rgba(28, 48, 95, 0.85),
        rgba(13, 22, 49, 0.9)
    );
    border: 1px solid rgba(94, 167, 255, 0.35);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.2);
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(0, 229, 255, 0.7);
    box-shadow: 0 10px 35px rgba(0, 229, 255, 0.14);
}

/* Premium tabs */
button[data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    font-weight: 700;
    padding: 12px 18px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #68efff !important;
    background: rgba(0, 229, 255, 0.09);
}

/* Input fields */
[data-baseweb="input"] > div,
[data-baseweb="select"] > div {
    border-radius: 11px;
    border-color: rgba(0, 229, 255, 0.35);
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 229, 255, 0.25);
    border-radius: 14px;
    overflow: hidden;
}

/* Chart containers */
[data-testid="stPlotlyChart"] {
    border: 1px solid rgba(90, 145, 225, 0.15);
    border-radius: 16px;
    padding: 8px;
    background: rgba(12, 22, 48, 0.22);
}

/* Buttons */
div.stButton > button,
div.stDownloadButton > button {
    border-radius: 12px;
    font-weight: 700;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 22px rgba(0, 229, 255, 0.3);
}

/* Mobile / narrow screens */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {
        padding: 22px;
        border-radius: 18px;
    }

    .hero-title {
        font-size: 30px;
        letter-spacing: 0;
    }

    [data-testid="stMetric"] {
        padding: 14px;
    }
}

/* Accessibility */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)