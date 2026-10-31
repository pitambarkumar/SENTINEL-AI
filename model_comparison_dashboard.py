from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent
RESULT_FILE = BASE_DIR / "model_comparison_results.csv"

METRICS = [
    "Precision", "Recall", "F1 Score",
    "ROC-AUC", "PR-AUC"
]

@st.cache_data
def load_comparison():
    if not RESULT_FILE.exists():
        return None
    return pd.read_csv(RESULT_FILE)


def run_model_comparison():
    st.markdown("## 🛡️ SENTINEL AI 9.0")
    st.caption(
        "Advanced Machine Learning Model Comparison"
    )

    df = load_comparison()

    if df is None:
        st.error("model_comparison_results.csv not found!")
        return

    required = [
        "Model", "Training Seconds",
        "TN", "FP", "FN", "TP"
    ] + METRICS

    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        return

    st.success("Model comparison results loaded!")

    # Model ranking
    st.subheader("🏆 Model Leaderboard")

    ranked = df.sort_values(
        "F1 Score", ascending=False
    ).reset_index(drop=True)

    st.dataframe(
        ranked.style.format({
            m: "{:.2%}" for m in METRICS
        }),
        width="stretch",
        hide_index=True
    )

    winner = ranked.iloc[0]["Model"]

    st.metric(
        "Highest F1 Score Model",
        winner
    )

    st.caption(
        "Ranking uses F1 Score. The best model "
        "depends on false-positive and "
        "false-negative costs."
    )

    # Interactive metrics
    st.subheader("📊 Performance Comparison")

    selected_metrics = st.multiselect(
        "Select metrics",
        METRICS,
        default=METRICS,
        key="v9_metrics"
    )

    if selected_metrics:
        chart_df = df.melt(
            id_vars="Model",
            value_vars=selected_metrics,
            var_name="Metric",
            value_name="Score"
        )

        fig = px.bar(
            chart_df,
            x="Metric",
            y="Score",
            color="Model",
            barmode="group",
            text_auto=".3f",
            template="plotly_dark",
            color_discrete_sequence=[
                "#00E5FF", "#FF4FD8", "#A78BFA"
            ]
        )
        fig.update_layout(
            yaxis_range=[0, 1],
            height=450
        )
        st.plotly_chart(fig, width="stretch")

    # Radar comparison
    st.subheader("🧠 Model Intelligence Radar")

    radar = go.Figure()

    for _, row in df.iterrows():
        values = [float(row[m]) for m in METRICS]
        radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=METRICS + [METRICS[0]],
            fill="toself",
            name=row["Model"]
        ))

    radar.update_layout(
        template="plotly_dark",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        height=500
    )

    st.plotly_chart(radar, width="stretch")

    # Training speed
    st.subheader("⚡ Training Speed")

    speed_fig = px.bar(
        df,
        x="Model",
        y="Training Seconds",
        color="Model",
        text_auto=".2f",
        template="plotly_dark"
    )

    st.plotly_chart(speed_fig, width="stretch")

    # Confusion matrix
    st.subheader("🔍 Confusion Matrix Comparison")

    for _, row in df.iterrows():
        st.markdown(f"#### {row['Model']}")

        matrix = [
            [int(row["TN"]), int(row["FP"])],
            [int(row["FN"]), int(row["TP"])]
        ]

        heatmap = go.Figure(data=go.Heatmap(
            z=matrix,
            x=["Predicted Genuine", "Predicted Fraud"],
            y=["Actual Genuine", "Actual Fraud"],
            text=matrix,
            texttemplate="%{text}",
            colorscale="Blues"
        ))

        heatmap.update_layout(
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(heatmap, width="stretch")

    # Export
    st.subheader("📥 Export Results")

    st.download_button(
        "Download Model Comparison CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="sentinel_ai_model_comparison.csv",
        mime="text/csv",
        key="v9_comparison_export"
    )

    st.info(
        "Educational evaluation only. "
        "Results should be verified on an "
        "independent test set before deployment."
    )


if __name__ == "__main__":
    st.set_page_config(
        page_title="SENTINEL AI 9.0",
        page_icon="🛡️",
        layout="wide"
    )
    run_model_comparison()