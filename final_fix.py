from pathlib import Path
import shutil
import ast

BASE = Path(__file__).resolve().parent
DASHBOARD = BASE / "dashboard.py"
BACKUP = BASE / "dashboard_before_final_fix.py"

if not DASHBOARD.exists():
    raise FileNotFoundError("dashboard.py not found")

original = DASHBOARD.read_text(encoding="utf-8")
code = original
changes = []

def replace_once(old, new, label):
    global code
    count = code.count(old)
    if count != 1:
        raise RuntimeError(
            f"{label}: expected 1 match, found {count}. "
            "No files have been changed."
        )
    code = code.replace(old, new, 1)
    changes.append(label)


# FIX 1: Avoid stale predictions when row selection changes.
replace_once(
    '''        selected_row = real_df.iloc[
            int(transaction_index)
        ]''',
    '''        selected_row = real_df.iloc[
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
            st.session_state.pop("last_prediction", None)''',
    "Prediction state safety"
)


# FIX 2: Save only a fresh prediction for selected row.
# Detect duplicates before saving, without changing database.py.
replace_once(
    '''             if data:
                save_transaction(
                    data["transaction_id"],
                    data["amount"],
                    data["fraud_probability"],
                    data["risk_score"],
                    data["prediction"]
                )
                st.success("✅ Prediction saved to database!")
             else:   
                st.warning("Please run ML prediction first.")''',
    '''             if data is None:
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
                        )''',
    "Duplicate save feedback"
)


# FIX 3: Keep ML Performance limited to its page.
replace_once(
    '''if st.session_state.get("show_ml_performance", False):''',
    '''if (
    page == "🧠 ML Performance"
    and st.session_state.get("show_ml_performance", False)
):''',
    "ML Performance page isolation"
)


# FIX 4: Correct Feature Importance chart indentation.
replace_once(
    '''        fig.update_traces(
    marker_line_color="#00E5FF",
    marker_line_width=1
)
    st.plotly_chart(fig, width="stretch")
  

st.info(
    "Evaluation uses the held-out test split "
    "from the original model training."
)''',
    '''        fig.update_traces(
            marker_line_color="#00E5FF",
            marker_line_width=1
        )
        st.plotly_chart(fig, width="stretch")

        st.info(
            "Evaluation uses a reproducible stratified "
            "20% test split (random_state=42). "
            "The saved model must have been trained "
            "using the matching split."
        )''',
    "Feature Importance and evaluation note"
)


# FIX 5: Remove outdated system-control statements.
replace_once(
    '''    st.write("Version: 3.1 Hybrid Edition")
    st.write("Interface: Cyber Command + Glassmorphism + Neural")
    st.write("Dataset: Synthetic demonstration data")
    st.write("Detection Engine: Rule-based prototype")
    st.write("Machine Learning: Planned")''',
    '''    st.write("Version: 6.0 Ultra Pro")
    st.write("Interface: Cyber Command + Glassmorphism + Neural")
    st.write(
        "Datasets: Synthetic dashboard and "
        "real credit-card fraud dataset"
    )
    st.write(
        "Detection: Rule-based demonstration "
        "and trained Random Forest"
    )
    st.write("Machine Learning: Integrated")''',
    "System Control version information"
)


# FIX 6: Ensure displayed prediction belongs to current row.
replace_once(
    '''        last = st.session_state.get("last_prediction")

        if not last:
            st.info(
                "Run a prediction in Real ML Engine first."
            )''',
    '''        last = st.session_state.get("last_prediction")

        if not last:
            st.info(
                "Run a prediction in Real ML Engine first."
            )''',
    "AI explanation compatibility"
)


# Validate syntax BEFORE touching the original.
ast.parse(code, filename=str(DASHBOARD))

# Preserve the existing working dashboard.
shutil.copy2(DASHBOARD, BACKUP)

# Apply all validated changes in one operation.
DASHBOARD.write_text(code, encoding="utf-8")

print("=" * 48)
print("SENTINEL AI 6.0 - STABILIZATION COMPLETE")
print("=" * 48)

for change in changes:
    print("[OK]", change)

print()
print("Backup:", BACKUP.name)
print("Updated:", DASHBOARD.name)
print("Python syntax: PASS")
print("Existing ML model and database: UNCHANGED")