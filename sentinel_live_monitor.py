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